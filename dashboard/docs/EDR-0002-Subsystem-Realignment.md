# EDR-0002 - Subsystem Realignment

## Status

Accepted

## Decision

The dashboard is organized into routes, services, ACE-specific integration modules, reusable templates, and shared static assets.

## Phase 2 Extension

ACE-specific runtime checks begin in `ace/status.py`, which is consumed by the Dashboard through the shared route context.

## Status

Accepted.
