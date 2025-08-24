# Astronomical Watch

Dual-licensed astronomical timekeeping reference: immutable core + open interfaces.

## Overview
Represent UTC instants as `DDD.mmm` where:
- `DDD` = day index since first reference noon ≥ vernal equinox of the current tropical year.
- `mmm` = thousandths of the current day.

## Install
```bash
pip install .
```
CLI:
```bash
awatch
```
Outputs e.g.:
```
174.532
```

## Licensing Model (Plan C)
- Core (algorithmic invariants): Astronomical Watch Core License v1.0 (no redistribution of modified versions) with a narrowly scoped Security Exception (see LICENSE.CORE §11).
- Everything else (CLI, wrappers, docs excluding spec) under MIT.

## Security Exception Summary
Urgent security patches may be temporarily distributed under strict conditions (see LICENSE.CORE §11) to remediate exploitable vulnerabilities; long-term divergence is not allowed.

See: LICENSE.CORE, LICENSE.MIT, SPEC.md, TRADEMARK_POLICY.md, CONTRIBUTING.md

## Rationale
Ensures a stable canonical definition while allowing broad ecosystem tooling.

## Roadmap
- [ ] ΔT refinement & higher precision solar terms
- [ ] Error bound verification tests
- [ ] JavaScript banner widget (MIT)
- [ ] Web assembly build of core logic (read-only)

## Disclaimer
Not for navigation; educational / experimental.

## Contributing
Read CONTRIBUTING.md first.