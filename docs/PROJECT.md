# ACE Server Infrastructure Project

**Project Name:** ACE Server Infrastructure

**Repository Purpose:**

This repository contains the complete infrastructure configuration used to deploy and maintain an Asheron's Call Emulator (ACE) server using Docker on Debian Linux.

This repository is **not** the ACE source code.

Instead, it contains the configuration, documentation, scripts, and operational standards required to deploy, maintain, backup, recover, and upgrade the production server.

---

# Objectives

This project has several primary goals:

- Maintain a repeatable server deployment.
- Keep infrastructure under version control.
- Preserve official upstream configuration separately from local modifications.
- Provide documented recovery procedures.
- Minimize downtime.
- Simplify future upgrades.

---

# Server Information

| Item | Value |
|------|-------|
| Hostname | acedebian |
| Operating System | Debian 12 (Bookworm) |
| Virtualization | Microsoft Hyper-V |
| Host Platform | Windows Server 2022 |
| Memory | 8 GB |
| Storage | 256 GB |
| Network | DHCP Reservation (10.0.0.x) |
| Docker | Official Docker CE Repository |

---

# Repository Layout

```
/opt/acserver

├── ace/                # Emulator configuration and runtime data
│   ├── Config/
│   ├── Content/
│   ├── Dats/
│   ├── Logs/
│   └── Mods/
│
├── database/
│   └── mysql/
│
├── backups/
│
├── docs/
│
├── official/
│
├── scripts/
│
├── docker-compose.yml
├── .env
└── PROJECT.md
```

---

# Repository Principles

This repository stores infrastructure.

It does not store:

- MySQL databases
- World data
- Character data
- Backup archives
- Runtime logs
- Secrets

Those are operational assets and are backed up separately.

---

# Infrastructure Standards

## Official Files

Files downloaded from ACEmulator are stored under:

```
official/
```

These files are never modified.

Local production files are maintained separately.

---

## Docker

Docker is installed from Docker's official repository.

The Debian docker.io package is not used.

Docker daemon configuration enables:

- overlay2 storage
- JSON log rotation
- live restore

---

## Security

- Application files are owned by the `acarr` user.
- Administrative actions use `sudo`.
- Daily work is performed as the normal user.
- Root login is avoided except for operating system administration.

---

## Git Standards

Every significant infrastructure change is committed.

Examples include:

- Docker configuration changes
- Backup improvements
- Recovery procedures
- Compose updates
- Documentation updates

---

# Documentation

The documentation directory contains operational documentation for the server.

| File | Purpose |
|------|---------|
| SERVER.md | General server information |
| DOCKER.md | Docker configuration |
| DATABASE.md | Database information |
| BACKUPS.md | Backup procedures |
| RECOVERY.md | Disaster recovery |
| NETWORK.md | Networking documentation |
| CHANGELOG.md | Infrastructure change history |

---

# Design Philosophy

This project follows the same engineering principles used throughout the Guild CMS project:

- Documentation first.
- Infrastructure as code.
- Version-controlled configuration.
- Small incremental improvements.
- Recovery should always be documented before it is needed.

The objective is to ensure that rebuilding this server should be a straightforward, documented process rather than an exercise in reverse engineering.

---

# Project Status

Current Phase:

Infrastructure Foundation

Current Milestones:

- Debian installation
- Docker installation
- Docker configuration
- Infrastructure repository
- Documentation framework

Upcoming Work:

- Production Docker Compose
- Database initialization
- ACE deployment
- Backup automation
- Recovery automation
- Infrastructure utilities
