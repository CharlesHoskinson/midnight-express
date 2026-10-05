"""Negative tests in a temporary project; canonical sources and archives stay intact.

Run: python -m unittest discover -s formal/lean -p test_proof_gate.py -v
"""
from pathlib import Path
import shutil
import tempfile
import unittest

from proof_gate import (GateFailure, ROOT, canonical_sources, code_only,
                        lint_sources, pinned_lake, run_axiom_audit,
                        run_command, run_proof_gate)


class ProofGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="midnight-proof-gate-")
        cls.root = Path(cls.temporary.name) / "lean"
        shutil.copytree(ROOT, cls.root, ignore=shutil.ignore_patterns(".lake", "__pycache__"))
        cls.baseline = run_proof_gate(cls.root)
        cls.lake = pinned_lake(cls.root)
        cls.umbrella = cls.root / "MidnightExpress.lean"
        cls.original = cls.umbrella.read_text()

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def tearDown(self):
        self.umbrella.write_text(self.original)
        (self.root / "OutsideProject.lean").unlink(missing_ok=True)

    def modules(self):
        return [str(p.relative_to(self.root).with_suffix("")).replace("/", ".")
                for p in canonical_sources(self.root)]

    def test_named_placeholder_fails_lint_and_fatal_warning_build(self):
        self.umbrella.write_text(self.original + "\ntheorem placeholderCanary : False := by sorry\n")
        with self.assertRaisesRegex(GateFailure, "forbidden proof construct sorry"):
            run_proof_gate(self.root)
        # Independently prove warnings are fatal when source lint is bypassed.
        with self.assertRaisesRegex(GateFailure, r"declaration uses [`']sorry[`']"):
            run_command([self.lake, "--wfail", "build"], self.root)

    def test_anonymous_placeholder_fails_lint_and_direct_compilation(self):
        self.umbrella.write_text(self.original + "\nexample : False := by sorry\n")
        with self.assertRaisesRegex(GateFailure, "forbidden proof construct sorry"):
            run_proof_gate(self.root)
        with self.assertRaisesRegex(GateFailure, r"declaration uses [`']sorry[`']"):
            run_command([self.lake, "env", "lean", "-DwarningAsError=true", str(self.umbrella)], self.root)

    def test_axiom_in_orphan_module_outside_namespace_fails_audit(self):
        source = self.root / "OutsideProject.lean"
        source.write_text("import Std\naxiom externalCanary : False\ntheorem canaryLeak : False := externalCanary\n")
        with self.assertRaisesRegex(GateFailure, "forbidden proof construct axiom"):
            run_proof_gate(self.root)
        artifact = self.root / ".lake/build/lib/lean/OutsideProject.olean"
        run_command([self.lake, "env", "lean", "-DwarningAsError=true", str(source),
                     "-o", str(artifact)], self.root)
        with self.assertRaisesRegex(GateFailure, "explicit axiom|forbidden proof dependencies"):
            run_axiom_audit(self.root, self.lake, self.modules())

    def test_unwanted_standard_axiom_dependency_fails_audit(self):
        self.umbrella.write_text(self.original +
            "\nnoncomputable def unwantedDependency : Bool := Classical.choice (show Nonempty Bool from ⟨true⟩)\n")
        # This has no forbidden construct; the kernel-dependency audit must catch it.
        lint_sources(self.root)
        with self.assertRaisesRegex(GateFailure, "Classical.choice"):
            run_proof_gate(self.root)

    def test_unsafe_and_native_oracle_constructs_fail_lint(self):
        for source in ("unsafe def canary : Bool := true", "example : True := by native_decide",
                       "example : True := by admit"):
            with self.subTest(source=source):
                self.umbrella.write_text(self.original + "\n" + source + "\n")
                with self.assertRaisesRegex(GateFailure, "forbidden proof construct"):
                    run_proof_gate(self.root)

    def test_version_pin_cannot_drift(self):
        pin = self.root / "lean-toolchain"
        original = pin.read_text()
        try:
            pin.write_text("leanprover/lean4:v4.34.0\n")
            with self.assertRaisesRegex(GateFailure, "lean-toolchain must be exactly"):
                run_proof_gate(self.root)
        finally:
            pin.write_text(original)

    def test_source_mask_preserves_real_code_after_nested_comments(self):
        text = '"sorry" /- outer /- axiom -/ native_decide -/\n-- unsafe\nexample : True := by trivial'
        masked = code_only(text)
        self.assertNotIn("sorry", masked)
        self.assertNotIn("axiom", masked)
        self.assertIn("example : True", masked)
        self.assertEqual(masked.count("\n"), text.count("\n"))


if __name__ == "__main__":
    unittest.main()
