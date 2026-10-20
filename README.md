# Sphere Brawl: Rolling Rampage - AI Agent Task Pack

This pack is designed to be placed at the root of the Git repository used by Claude Code, Google Antigravity, or another repository-aware AI agent.

## Source of truth
- `MASTER_IMPLEMENTATION_PLAN.md` is the authoritative full specification.
- `AI_AGENT_GLOBAL_SYSTEM_PROMPT.md` contains the non-negotiable agent rules.
- `tasks/` contains atomic sequential task cards. Do not skip gates.
- `ALPHA_ACCEPTANCE_CHECKLIST.md` is the release acceptance checklist.
- `DECISION_LOG.md` records approved changes and blockers.
- `specs/` contains contracts, project scaffolding, and asset pipeline specifications. `specs/DESIGN_CONSTANTS.md` is the compact numeric mirror.
- DOCX/PDF are reading copies; never extract code constants from their rendered tables.
- `ORCHESTRATOR_KICKOFF_PROMPT.md` contains the ready-to-paste orchestration prompt.
- `assets/` contains the approved concept visual used for broad art direction only.

## Start sequence
1. Put the pack contents in the project repository root. Keep `MASTER_IMPLEMENTATION_PLAN.md` at the repository root.
2. Ask the orchestrator agent to read `AI_AGENT_GLOBAL_SYSTEM_PROMPT.md` and Task 00.
3. Execute Gate 0. Path A (Roblox Server Authority) is preferred; use pre-approved Path B only if Path A settings/APIs are genuinely unavailable. Do not begin feature implementation until the selected path passes.
4. Execute one task card at a time; the orchestrator signs off the gate before the next task begins.
5. Keep the owner informed of blockers and untested runtime behavior. Do not claim full completion based only on static analysis.

## Suggested repo-root shape
```text
README.md
MASTER_IMPLEMENTATION_PLAN.md
AI_AGENT_GLOBAL_SYSTEM_PROMPT.md
ALPHA_ACCEPTANCE_CHECKLIST.md
DECISION_LOG.md
default.project.json
src/
assets/
  asset-manifest.json
  concept/Sphere_Brawl_Rolling_Rampage_Final_Concept.png
tasks/
specs/
```

## Repository and Studio place
- GitHub: `https://github.com/HitanshG07/Sphere_Ball` (default branch `alpha`). Branch map and push rules: `docs/AI_DEVELOPMENT_PROTOCOL.md` section 7.
- `place/Gate0.rbxl` is the canonical Studio place. It holds the saved Path A settings (`Workspace.AuthorityMode = Server`) and no game scripts. Open it in Studio, then connect the Rojo plugin to `rojo serve default.project.json` (repo root) to load the code from `src/`.

## Setup and checks
- Tools are pinned in `rokit.toml` (Rojo 7.4.4, luau-lsp 1.70.1, StyLua 2.6.0, Selene 0.32.0); install them with `rokit install` from the repo root.
- Static checks, run from the repo root:
  ```
  rojo build default.project.json -o build/Gate0.rbxlx
  rojo sourcemap default.project.json --include-non-scripts -o sourcemap.json
  luau-lsp analyze --definitions=globalTypes.d.luau --sourcemap=sourcemap.json src
  stylua --check src
  selene src
  ```
- Unit tests run in Studio: open `place/Gate0.rbxl`, run `rojo serve default.project.json` and connect the Rojo plugin, start Play (Test ▸ Play), then in the Server context run `require(game:GetService("ServerScriptService").Server.Tests.TestRunner).run()` (Command Bar or the Studio MCP `execute_luau`). Specs are ModuleScripts named `*.spec` under `src/server/Tests`.
- Source layout: shared contracts in `src/shared/Types.luau` and `src/shared/Config/`, shared modules in `src/shared/Modules/`, tests in `src/server/Tests/`.

## What this pack does not do
It is a specification and execution protocol, not a prebuilt Roblox game. The assigned agents must create the Luau source, procedural environment, UI, visualizers, tests, and assets. A plan cannot guarantee zero defects; the gate-and-evidence process is how defects are caught before moving forward.
