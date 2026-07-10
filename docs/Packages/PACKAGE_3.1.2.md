# Package 3.1.2 - ACE Research Lab / Observation Tracker

This package introduces ACEMD-side observation tracking.

## Purpose

Replace manual memory-based testing with stored evidence:

1. Take a character snapshot.
2. Perform a known action in ACE.
3. Take another snapshot.
4. Create an observation.
5. Review the raw diff and use it to improve the Knowledge Base.

## Safety

ACE databases are read-only. Snapshot and observation files are local ACEMD JSON artifacts.
