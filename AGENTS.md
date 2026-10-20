# AGENTS.md — Sphere Brawl: Rolling Rampage

Shared, tool-agnostic instructions for **every** AI coding tool, model, agent and subagent working in this repository (Claude Code, Gemini CLI, Antigravity, and any other or future tool). The tool-specific files `CLAUDE.md` and `GEMINI.md` only import this file and add tool-specific notes; tools that read `AGENTS.md` natively use it directly. No tool may create a separate, conflicting policy or development history.

The detailed process is in [docs/AI_DEVELOPMENT_PROTOCOL.md](docs/AI_DEVELOPMENT_PROTOCOL.md). Read it before any substantial work.

## Authority (highest first)
1. Owner instructions recorded in [DECISION_LOG.md](DECISION_LOG.md) and the locked design in [MASTER_IMPLEMENTATION_PLAN.md](MASTER_IMPLEMENTATION_PLAN.md) + [specs/DESIGN_CONSTANTS.md](specs/DESIGN_CONSTANTS.md).
2. [AI_AGENT_GLOBAL_SYSTEM_PROMPT.md](AI_AGENT_GLOBAL_SYSTEM_PROMPT.md) (engineering rules) and the task cards in [tasks/](tasks/).
3. [docs/AI_DEVELOPMENT_PROTOCOL.md](docs/AI_DEVELOPMENT_PROTOCOL.md) (process: agents, models, reporting, Git).
4. This file and tool adapters.

If anything conflicts, stop, record the conflict in the work log, and ask the owner. Never resolve a conflict silently. DOCX/PDF copies are reading references only.

## Current milestone gate (check docs/PROJECT_STATUS.md for the live state)
- Gate 0 **passed** on 2026-10-20 with Path A (D-024). TASK-01 is authorized (owner approval, 2026-10-20). Every later task needs its own owner approval before it starts.
- Do **not** merge the Gate 0 prototype (`gate-0` on GitHub, local alias `gate0-spike`) into `alpha`. `main` holds the untouched spec baseline and is never modified.
- Supporting agents write only the files their brief assigns, in their own worktree or branch; the lead integrates.
- Switching tools, starting a new session or delegating to another agent never bypasses a gate.

## GitHub: the shared hub
- `origin` = `https://github.com/HitanshG07/Sphere_Ball` (public by owner decision; default branch `alpha`) is the shared version-control hub for every AI tool. Branch map, push procedure and pre-push audit: protocol §7.
- At session start, `git fetch origin` and compare local and remote branches. Never auto-pull or merge remote changes over uncommitted or unpushed local work; record the divergence and ask.
- Concurrent writers use task branches or worktrees. Push only validated branches that the owner or lead has authorized.
- No force-push or history rewrite without explicit owner approval. Never commit credentials, tokens, cookies or keys.
- Record every push (commit hash and remote ref from `git ls-remote`) in the work log. Never claim a backup or publication until the push has succeeded.
- New evidence redacts the owner's Roblox identity as `<owner-roblox-user>` and `<owner-uid>` (protocol §6).

## Start of every session
1. Read this file, [docs/AI_DEVELOPMENT_PROTOCOL.md](docs/AI_DEVELOPMENT_PROTOCOL.md), [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md), the active task card, [DECISION_LOG.md](DECISION_LOG.md) and the latest entries of [docs/WORK_LOG.md](docs/WORK_LOG.md).
2. Verify the real repository state yourself (`git branch --show-current`, `git status`, `git log -5`, `git fetch origin` and a local-versus-remote comparison). Do not trust a previous chat's claims.
3. Confirm the authorized milestone, open acceptance criteria and blockers.
4. Identify which models and agents are actually available; choose only what the task justifies.
5. Append a work-log entry with a new session ID, the objective and the validation plan before substantial work.

## Multi-agent and model rules
- One **lead agent** owns architecture decisions, shared contracts, integration, Git, validation and acceptance.
- Delegate to narrowly scoped specialists only when work is genuinely independent; keep dependent work sequential. Simple tasks use one agent.
- Choose models by risk: strongest reasoning tier for architecture, physics, Server Authority/prediction, difficult debugging and high-risk review; capable implementation tier for normal code, UI and integration; fast/economical tier for documentation, repetitive edits and mechanical checks. Verify a model is available before assigning it; never assume a name or alias.
- One writer per file at a time. Concurrent writers use separate Git worktrees or branches; the lead integrates. Shared contracts (types, config, remotes, physics ownership) have one owner.
- Important, security-sensitive or physics/authority changes get an independent review before acceptance.
- Every agent returns the structured report defined in the protocol; the lead persists it to the records.

## Engineering non-negotiables (summary; full list in AI_AGENT_GLOBAL_SYSTEM_PROMPT.md)
- Luau with `--!strict`; server owns all game outcomes; clients send intent only; no client-applied authoritative impulses.
- No invented asset IDs; no per-tile scripts; every connection, tween and loop has a cleanup owner.
- Build and check from the repo root: `rojo build default.project.json -o build/Gate0.rbxlx`, `rojo sourcemap default.project.json --include-non-scripts -o sourcemap.json`, `luau-lsp analyze --definitions=globalTypes.d.luau --sourcemap=sourcemap.json src`, `stylua --check src`, `selene src` (tools pinned in `rokit.toml`).

## Records every AI must keep (append, never rewrite history)
- [docs/WORK_LOG.md](docs/WORK_LOG.md): chronological actions, commands, outcomes, decisions, commits (session IDs `S-YYYYMMDD-NN`).
- [docs/TEST_RESULTS.md](docs/TEST_RESULTS.md): every validation attempt (`PASS`, `FAIL`, `BLOCKED`, `NOT RUN`, `INCONCLUSIVE`, `SKIPPED`).
- [docs/FAILURES_AND_FIXES.md](docs/FAILURES_AND_FIXES.md): failure IDs `FAIL-NNN`, causes, attempts, retests (`OPEN`, `INVESTIGATING`, `FIXED-VERIFIED`, `FIXED-UNVERIFIED`, `WONT-FIX`).
- [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md): current snapshot and next three actions.
- [docs/GATE_0_REPORT.md](docs/GATE_0_REPORT.md) and [DECISION_LOG.md](DECISION_LOG.md): milestone evidence and decisions.

## Honesty rules
- Never report a test as passed unless it ran in the required environment and produced evidence. A proposed fix is not a verified fix.
- Never fabricate model identities, commands, outputs, timestamps, evidence or agent activity. Mark reconstructed history as such.
- Record failures and failed approaches; corrections are appended and reference the original entry.
- Redact secrets. Do not delete user work, rewrite Git history, force-push, publish, or upload assets without explicit owner approval.

## Before ending a substantial session
Update the work log, test and failure registers and project status; inspect the real `git diff`; record the commit and working-tree state; state what passed, failed, was blocked, inconclusive or unrun; leave the exact next action so another AI can resume without the chat history.
