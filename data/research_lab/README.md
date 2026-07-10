# Persistent Research Lab Evidence

This host directory is mounted into the dashboard container at
`/app/data/research_lab`.

It contains irreplaceable ACEMD-generated evidence:

- `observations.json`
- `snapshots/*.json`
- future Research Lab evidence attachments

Do not replace or delete this directory during application deployments. Runtime
backups include it inside `ace_infrastructure.tar.gz`.
