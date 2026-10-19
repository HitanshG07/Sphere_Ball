# Agent Assignment Matrix

An orchestrator owns integration and decision-making. Agents may work in parallel only where file ownership is disjoint and contracts are already frozen.

| Workstream | Primary owner | Depends on | Protected files / integration notes |
|---|---|---|---|
| Gate 0 / Studio authority | Orchestrator + gameplay lead | none | no feature implementation until pass |
| Shared types/config/project | Gameplay/code agent A | Gate 0 | types/remotes/config are shared contracts; merge first |
| Grid and ring collapse | Gameplay/code agent B | types/config | owns GridService and its tests |
| Lobby geometry | Environment agent | geometry spec | owns LobbyService/procedural scene/assets; do not edit queue state code |
| Sphere movement/simulation | Gameplay/code agent A | Gate 0, type contracts | sole owner of shared simulation and movement controller |
| Board Pulse | Gameplay/code agent B | grid + simulation interfaces | owns PatternDefinitions/PulseService/Visualizer interfaces |
| Combat/cores/elimination | Gameplay/code agent A or designated combat agent | simulation + pulse interfaces | server-authority outcome only; do not edit PulseService privately |
| Queue/loadout/round | Gameplay/code agent B | lobby, sphere lifecycle, types | state services only; RoundManager owns phase |
| UI/input | UI agent | typed payloads and service contracts | UI does not own authoritative state or edit server services |
| 3D/VFX/audio | Environment/VFX agent | geometry/FX interfaces | assets/visualizer files only; no physics stat changes |
| QA | QA agent | all merged tasks | read-only unless assigned defect fixes |

## Parallelism rule
The orchestrator assigns tasks and file ownership in writing. If two tasks need the same file, sequence them or introduce a narrow interface first. Never merge conflicting edits by simply accepting the last file version.
