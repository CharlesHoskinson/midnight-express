#!/usr/bin/env python3
"""Fail-closed kernel build and module-owned axiom audit for the canonical sources.

The archived review evidence is deliberately outside this source set. The Lean
metaprogram imports Lean solely for inspection; model modules use bundled Std.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
TOOLCHAIN = "leanprover/lean4:v4.34.1"
VERSION = "4.34.1"


class GateFailure(RuntimeError):
    """A build, source-policy or proof-dependency gate failed."""


def code_only(source: str) -> str:
    """Mask strings and nested Lean comments without hiding line boundaries."""
    result = list(source)
    i, depth = 0, 0
    while i < len(source):
        start = i
        if depth:
            if source.startswith("/-", i):
                depth += 1
                i += 2
            elif source.startswith("-/", i):
                depth -= 1
                i += 2
            else:
                i += 1
        elif source.startswith("/-", i):
            depth = 1
            i += 2
        elif source.startswith("--", i):
            i = source.find("\n", i)
            if i < 0:
                i = len(source)
        elif source[i] == '"':
            i += 1
            while i < len(source):
                if source[i] == "\\":
                    i += 2
                elif source[i] == '"':
                    i += 1
                    break
                else:
                    i += 1
        else:
            i += 1
            continue
        for j in range(start, min(i, len(source))):
            if result[j] != "\n":
                result[j] = " "
    return "".join(result)


def canonical_sources(root: Path) -> list[Path]:
    """All source modules, including new names outside the public namespace."""
    return sorted(p for p in root.rglob("*.lean")
                  if ".lake" not in p.relative_to(root).parts
                  and p.name not in {"lakefile.lean", "Audit.lean"})


def lint_sources(root: Path) -> list[Path]:
    sources = canonical_sources(root)
    if not sources:
        raise GateFailure("No canonical Lean sources found")
    forbidden = re.compile(r"\b(?:sorry|admit|axiom|unsafe|native_decide|ofReduceBool|oracle|run_elab|extern|implemented_by)\b")
    for path in sources:
        code = code_only(path.read_text())
        match = forbidden.search(code)
        if match:
            line = code[:match.start()].count("\n") + 1
            raise GateFailure(f"{path.relative_to(root)}:{line}: forbidden proof construct {match.group()}")
        if re.search(r"\bwarningAsError\b", code):
            raise GateFailure(f"{path.relative_to(root)}: warning policy may not be overridden")
        for imported in re.findall(r"^\s*import\s+([^\n]+)", code, re.M):
            for module in imported.split():
                if module != "Std" and not module.startswith("Std."):
                    candidate = root / (module.replace(".", "/") + ".lean")
                    if not candidate.is_file():
                        raise GateFailure(f"{path.relative_to(root)}: import {module} is not bundled Std or a project module")
    return sources


def pinned_lake(root: Path) -> str:
    if (root / "lean-toolchain").read_text().strip() != TOOLCHAIN:
        raise GateFailure(f"lean-toolchain must be exactly {TOOLCHAIN}")
    direct = Path.home() / ".elan/toolchains/leanprover--lean4---v4.34.1/bin/lake"
    lake = str(direct) if direct.is_file() else shutil.which("lake")
    if not lake:
        raise GateFailure(f"Install pinned toolchain {TOOLCHAIN}")
    result = subprocess.run([lake, "env", "lean", "--version"], cwd=root,
                            text=True, capture_output=True, timeout=30)
    if result.returncode or not re.search(r"\bversion 4\.34\.1\b", result.stdout):
        raise GateFailure(f"Expected Lean {VERSION}; got {result.stdout.strip()} {result.stderr.strip()}")
    return lake


def run_command(command: list[str], root: Path) -> str:
    result = subprocess.run(command, cwd=root, text=True, capture_output=True,
                            timeout=300, env={**os.environ, "NO_COLOR": "1"})
    if result.returncode:
        raise GateFailure(f"Proof command failed: {' '.join(command)}\n{result.stdout}{result.stderr}")
    return result.stdout + result.stderr


def run_axiom_audit(root: Path, lake: str, modules: list[str]) -> dict:
    """Use module ownership, not declaration namespace, and assert dependencies.

    The generated audit imports every source module (including orphan additions),
    so a declaration outside MidnightExpress is covered. No namespace filter is
    trusted. Anonymous examples are enforced by source lint and fatal warnings.
    """
    audit = (root / "Audit.lean").read_text()
    imports = "\n".join("import " + module for module in modules)
    audit = audit.replace("import MidnightExpress\n", imports + "\n")
    audit = audit.replace("(`MidnightExpress).isPrefixOf env.header.moduleNames[idx.toNat]!",
                          "decide (" + " ∨ ".join("env.header.moduleNames[idx.toNat]! = `" + module
                                            for module in modules) + ")")
    # Work inside the project so Lake selects the intended package. Always clean up.
    with tempfile.NamedTemporaryFile(mode="w", prefix=".proof-audit-", suffix=".lean",
                                     dir=root, delete=False) as temporary:
        temporary.write(audit)
        audit_path = Path(temporary.name)
    try:
        output = run_command([lake, "env", "lean", "-DwarningAsError=true", str(audit_path)], root)
    finally:
        audit_path.unlink(missing_ok=True)
    match = re.search(r"PROOF_AUDIT_OK: (\d+) project declarations", output)
    if not match:
        raise GateFailure(f"Audit did not assert successful project coverage:\n{output}")
    return {"declarations": int(match.group(1)), "modules": modules,
            "allowed_axioms": ["propext", "Quot.sound"]}


def run_proof_gate(root: Path = ROOT) -> dict:
    root = Path(root).resolve()
    sources = lint_sources(root)
    lake = pinned_lake(root)
    run_command([lake, "--wfail", "build"], root)
    modules = [str(p.relative_to(root).with_suffix("")).replace(os.sep, ".") for p in sources]
    # Build any new module the umbrella import does not reach. Its imports must
    # already be in the built project; missing/unordered imports fail closed.
    for source, module in zip(sources, modules):
        artifact = root / ".lake/build/lib/lean" / (module.replace(".", "/") + ".olean")
        if not artifact.exists() or artifact.stat().st_mtime_ns < source.stat().st_mtime_ns:
            artifact.parent.mkdir(parents=True, exist_ok=True)
            run_command([lake, "env", "lean", "-DwarningAsError=true", str(source),
                         "-o", str(artifact)], root)
    audit = run_axiom_audit(root, lake, modules)
    return {"toolchain": TOOLCHAIN, "warnings_fatal": True, **audit}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        print(json.dumps(run_proof_gate(args.root), sort_keys=True))
    except (GateFailure, subprocess.TimeoutExpired) as error:
        parser.exit(1, str(error) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
