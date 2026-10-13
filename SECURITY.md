# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.4.x   | ✅        |
| 1.3.x   | ⚠️ security fixes only |
| < 1.3   | ❌        |

## Reporting a vulnerability

This tool generates dungeon maps and tile art. It does not execute
untrusted code, but it *does* load user-supplied tile packs, WFC rule
files, and ONNX checkpoints. A malicious tile pack or ONNX model can
attempt path traversal or, in the ONNX case, exploit a runtime bug in
`onnxruntime`.

If you find an issue:

- Email: `security@pixel-dungeon-generator.dev` (PGP in `docs/keys/`).
- Include a minimal reproducer: the pack file or ONNX model, the command
  used, and the traceback.
- Do not open a public issue for path traversal, deserialization, or
  ONNX-runtime exploits. Give us 90 days.

## Out of scope

- Content of generated dungeons (we don't moderate tiles).
- Third-party tile packs you downloaded elsewhere.
- Anything requiring the attacker to already run code on the host.

## Known hardening

- All pack paths are resolved and checked against the pack root
  (`utils/sandbox.py`).
- ONNX models load with `providers=["CPUExecutionProvider"]` only; no
  custom operators are allowed by default (`config/onnx_policy.yaml`).