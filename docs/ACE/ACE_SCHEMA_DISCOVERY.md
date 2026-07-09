# ACE Schema Discovery

Package: 3.0.1 - ACE Schema Discovery

## Purpose

ACEMD 3.0.1 establishes safe read-only access patterns for ACE databases before any administrative write features are considered.

## Known ACE Databases

The ACE initialization dump identifies three databases:

| Database | Role | Core Tables |
| --- | --- | --- |
| `ace_auth` | Identity and game access levels | `account`, `accesslevel` |
| `ace_shard` | Runtime shard objects, characters, and dynamic properties | `character`, `biota`, `biota_properties_*`, `character_properties_*` |
| `ace_world` | Static game data and world content | `weenie`, `landblock_instance`, `quest`, `encounter`, `recipe`, `spell` |

## Important Relationship Notes

- ACE accounts live in `ace_auth.account`.
- Game access levels live in `ace_auth.accesslevel`.
- ACE characters live in `ace_shard.character`.
- `ace_shard.character.id` is the character's biota id.
- `ace_shard.character.account_Id` links a character to an ACE account id.
- Dynamic shard objects live in `ace_shard.biota` and related property tables.
- Static world definitions live primarily in `ace_world.weenie` and related property tables.

## Access Level Baseline

The initialization dump identifies these ACE game access levels:

| Level | Name |
| --- | --- |
| 0 | Player |
| 1 | Advocate |
| 2 | Sentinel |
| 3 | Envoy |
| 4 | Developer |
| 5 | Admin |

These are ACE game authority levels. They are not ACEMD administration permissions.

## ACEMD Boundary

ACE game accounts and access levels must not be used as the primary ACEMD authentication or authorization source. ACEMD access should be managed by a future ACEMD-native identity and RBAC subsystem.
