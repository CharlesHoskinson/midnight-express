# Formal specification research

The Astra assignments separate typed model definitions, validation and fixture agreement, and the reader guide. Their notes preserve assumptions and design choices without private model reasoning.

- [Model definitions](astra-model.md)
- [Validation properties](astra-validation.md)
- [Reader guide](astra-reader-guide.md)

The [canonical Lean project](../../formal/lean/README.md) contains the build and proof boundary. The [public specification page](../../website/dist/specification.html) explains the rules and provides source downloads. Kernel checking applies to the Lean definitions; external data provenance and implementation refinement require separate evidence.

The [Opus review](opus-review/README.md) compares the specification with the runtime, probes its proof assumptions and proposes stronger replay, conformance and build checks. The review proposals are separate from the canonical model.
