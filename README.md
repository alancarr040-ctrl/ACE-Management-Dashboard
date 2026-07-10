# ACE Management Dashboard

**ACE Management Dashboard (ACEMD)** is a Linux-first web administration and management platform for servers running the **Asheron's Call Emulator (ACE)**.

ACEMD brings routine server operations, Docker visibility, administration tools, automation, notifications, backups, documentation, and ACE-focused research into one maintainable interface. The project is designed to reduce direct command-line and database work while preserving clear safety boundaries around production systems.

## Project goals

- Provide a single operational view of an ACE deployment.
- Prefer service-based, reusable application components over page-specific logic.
- Keep management actions explicit, auditable, and appropriately constrained.
- Preserve application-generated data outside disposable containers.
- Support repeatable Linux and Docker Compose deployment.
- Document architecture, packages, releases, testing, and engineering decisions as part of the product.

## Current capabilities

ACEMD currently includes:

- dashboard health and deployment visibility;
- ACE and Docker operations views;
- management and administration foundations;
- backup, recovery, and runtime-state tooling;
- automation and notification services;
- metrics and operational event infrastructure;
- ACE discovery and knowledge-base foundations;
- Research Lab snapshots, observations, and persistent evidence storage;
- a read-only in-application documentation browser.

Some administration areas are intentionally read-only while discovery and safety contracts are being established. See the roadmap and package documents for current phase boundaries.

## Architecture

The project follows these core engineering principles:

- **Linux-first deployment** using Docker Compose;
- **service-first architecture** with centralized configuration;
- **read-only by default** for discovery and inspection workflows;
- **host-persistent storage** for durable ACEMD-generated data;
- **no duplicate business logic** across routes and user interfaces;
- **responsive, reusable UI components**;
- **documented and testable releases**.

The default deployment root is `/opt/acserver`. ACEMD's permanent data root is `/opt/acserver/data`, mounted into the dashboard container at `/app/data`.

## Repository layout

```text
ace/                    ACE server configuration and deployment content
dashboard/              ACEMD web application
data/                   Persistent ACEMD data structure and placeholders
database/               Database deployment support
docs/                   Architecture, operations, packages, and releases
scripts/                Backup, restore, preparation, and maintenance scripts
tools/                  Supporting development and deployment tools
docker-compose.yml      Primary Compose deployment
manage.sh               Management wrapper
```

Runtime secrets, generated evidence, database dumps, caches, and server backups are not source-controlled.

## Deployment

Deployment requirements and procedures are maintained under `docs/Operations/` and the applicable release directory.

For release **3.1.2.1**, prepare ownership and recreate the dashboard with:

```bash
cd /opt/acserver
sudo bash ./scripts/prepare-dashboard-owner.sh /opt/acserver
docker compose up -d --build --force-recreate ace-dashboard
```

Using `bash` explicitly is recommended because Windows extraction and FTP/SCP workflows may not preserve Unix executable permissions.

## Documentation

Start with [`docs/README.md`](docs/README.md).

Important document groups include:

- [`docs/Packages/`](docs/Packages/) — package specifications describing what is being built;
- [`docs/Releases/`](docs/Releases/) — delivered release notes, test plans, known issues, and certification records;
- [`docs/Architecture/`](docs/Architecture/) — architecture and engineering decisions;
- [`docs/Operations/`](docs/Operations/) — deployment, Docker, backups, recovery, database, and server operations;
- [`docs/AI/`](docs/AI/) — project governance and AI-assisted engineering standards.

## Development status

The current version is recorded in [`VERSION`](VERSION). Development direction is tracked in [`ROADMAP.md`](ROADMAP.md), and cumulative changes are recorded in [`CHANGELOG.md`](CHANGELOG.md).

The active corrective release is **3.1.2.1 — Research Lab Persistence Correction**. Its certification record remains in progress until all release tests have passed.

## Contributing and engineering standards

Before changing the project, review:

- `docs/AI/AI_PROJECT_SPEC.md`;
- `docs/AI/AI_ENGINEERING_STANDARDS.md`;
- `docs/AI/AI_DEVELOPMENT_WORKFLOW.md`;
- `docs/Development/`;
- the package specification for the active phase.

Changes should preserve certified subsystems, avoid unrelated refactoring, and include appropriate documentation and regression testing.

## License

ACE Management Dashboard is distributed under the terms in [`LICENSE`](LICENSE).
