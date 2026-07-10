# Package 3.1.2.1 - Research Lab Persistence Correction

## Objective

Prevent Research Lab snapshots and observations from being lost when the
`ace-dashboard` container is rebuilt or recreated.

## Storage Contract

- Host: `/opt/acserver/data/research_lab`
- Container: `/app/data/research_lab`
- Environment: `ACEMD_RESEARCH_ROOT=/app/data/research_lab`

The application refuses to initialize Research Lab storage without an absolute,
configured path.
