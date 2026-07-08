# EDR-0003 - Live Server Status

## Status

Accepted

## Context

Phase 2 shifts the product from infrastructure management to ACE Server Management.

## Decision

The Dashboard will include a live ACE Server Status section. The initial implementation checks:

- ACE container state
- Docker health
- Database TCP reachability
- ACE process running state
- recent ACE log errors

Player counts, world counters, ACE server version, and authenticated database status remain future integration points.

## Rationale

The Dashboard should answer the operational question: can the server be played right now?
