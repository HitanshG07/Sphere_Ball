@AGENTS.md

## Claude Code specifics

The shared rules above (imported from `AGENTS.md`) and `docs/AI_DEVELOPMENT_PROTOCOL.md` are authoritative. This section only adds Claude Code mechanics.

### Mandatory Multi-Agent Development Workflow
- Start Claude Code with this repository root as the working directory (`C:\Sphere_ball_rblox\Sphere_Brawl_AI_Agent_Task_Pack`). A session started in a parent folder loads this file only on demand.
- Project specialists live in `.claude/agents/` (see `docs/AI_DEVELOPMENT_PROTOCOL.md` section 3):

| Agent | Model alias | Use for |
|---|---|---|
| `sphere-architect` | `opus` | Roblox APIs, Server Authority, prediction/rollback, physics, high-risk design |
| `sphere-gameplay` | `sonnet` | server services, shared simulation and math, server tests |
| `sphere-client` | `sonnet` | input, camera, UI, presentation, client visualizers |
| `sphere-reviewer` | `opus` | independent review, tests, exploit and security checks (read-only) |
| `sphere-docs` | `haiku` | records, documentation, tool configs, mechanical checks |

- Aliases verified 2026-10-20 by read-only probes: `opus` = Opus 5.5 (`claude-opus-5-5`), `sonnet` = Sonnet 5.5 (`claude-sonnet-5-5`), `haiku` = Haiku 4.5 (`claude-haiku-4-5-20251001`). Re-verify if they stop resolving; never assume.
- Spawn only the agents a task justifies; a simple task uses the main session alone. Agents are configured not to spawn further agents; the main session is the lead.
- Concurrent writers use `isolation: "worktree"` (or separate branches); the lead integrates, runs the checks and updates the records.
- Persist every agent report to `docs/WORK_LOG.md` (and the test/failure registers when relevant) before relying on it.

### Roblox Studio access
- The Studio MCP server is registered as `Roblox_Studio` (local scope for this repo, plus user scope). Its tools load only at session start; if they are missing, record it as a blocker and check `claude mcp list` (see `docs/FAILURES_AND_FIXES.md` FAIL-004).
- MCP play mode is solo only. Multi-client tests need the owner to start Studio Test ▸ Clients and Servers.

### Verifying these instructions loaded
Run `/context` and confirm `CLAUDE.md` (with `AGENTS.md` through the import) appears under Memory files. `/memory` lists the memory file locations.
