# EDR-0008 - Operations Console Refinement

## Status

Accepted for Phase 2.4.1.

## Context

Phase 2.4.0 introduced interactive wrapper execution on the Management page. The first implementation exposed wrapper actions as individual cards. That was functional, but future growth could cause the Management page to become difficult to scan and overly long.

## Decision

The Management page will use subsystem-level cards with compact action rows instead of one visible card per action. Additional actions should be added to the appropriate existing subsystem group whenever practical. Shell commands are hidden behind per-action expanders, and command output is displayed in one shared console panel.

## Consequences

- The page remains compact as wrapper capability grows.
- Operators can find actions using section collapse and filtering.
- The interface presents operations first and shell details second.
- Future subsystems may receive new cards, but individual commands should not create top-level card sprawl.

## Implementation Notes

The 2.4.1 implementation keeps the existing whitelisted execution model and backend service. Changes are primarily template and style refinements, with client-side confirmation, filtering, and busy-state behavior.
