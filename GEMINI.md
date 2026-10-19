@./AGENTS.md

## Gemini CLI and Antigravity specifics

The shared rules above (imported from `AGENTS.md`) and `docs/AI_DEVELOPMENT_PROTOCOL.md` are authoritative. Read both before acting. This file adds no separate policy.

- If your tool did not expand the import above, read `AGENTS.md` and `docs/AI_DEVELOPMENT_PROTOCOL.md` manually before any work.
- Map your available models to the protocol's three tiers (strongest reasoning, implementation, fast/economical), verify they are available, and record the mapping and the model actually used in `docs/WORK_LOG.md`.
- Use the same records as every other tool: `docs/WORK_LOG.md`, `docs/TEST_RESULTS.md`, `docs/FAILURES_AND_FIXES.md`, `docs/PROJECT_STATUS.md`. Do not keep project history only in Antigravity artifacts or chat.
- The Roblox Studio MCP is at `%LOCALAPPDATA%\Roblox\mcp.bat`. Record any Studio test you run, with evidence, in `docs/TEST_RESULTS.md`.
- Antigravity's loading of `AGENTS.md` and `GEMINI.md` is documented only by third-party guides and has not been verified on this machine. Confirm it in Antigravity and record the result in `docs/WORK_LOG.md`.
