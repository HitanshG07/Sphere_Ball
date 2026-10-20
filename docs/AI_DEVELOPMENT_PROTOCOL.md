# AI Development Protocol — Sphere Brawl: Rolling Rampage

**Status:** permanent project rule (owner instruction, 2026-10-20). Applies to every AI tool, model, agent and subagent.
**Scope:** process only. Product design, constants and engineering rules stay in `MASTER_IMPLEMENTATION_PLAN.md`, `specs/DESIGN_CONSTANTS.md`, `DECISION_LOG.md`, `AI_AGENT_GLOBAL_SYSTEM_PROMPT.md` and the task cards. This protocol never overrides them; if it appears to, stop and ask the owner.

## 1. Sources of truth and precedence
1. Owner decisions in `DECISION_LOG.md`; locked design in `MASTER_IMPLEMENTATION_PLAN.md` and its numeric mirror `specs/DESIGN_CONSTANTS.md`.
2. `AI_AGENT_GLOBAL_SYSTEM_PROMPT.md`, `specs/AGENT_ASSIGNMENT_MATRIX.md`, `specs/STUDIO_GATE_00.md`, `ALPHA_ACCEPTANCE_CHECKLIST.md`, `tasks/*.md`.
3. This protocol.
4. `AGENTS.md` and tool adapters (`CLAUDE.md`, `GEMINI.md`).

Chat history and provider-specific memory are never a source of truth. Anything that matters is written to the repository records (section 6).

## 2. Session start protocol (every AI, every session)
1. Read `AGENTS.md`, this protocol, `docs/PROJECT_STATUS.md`, the active task card, `DECISION_LOG.md` and the most recent `docs/WORK_LOG.md` entries.
2. Verify the actual state: current branch, `git status`, `git log -5`, stashes, open failures in `docs/FAILURES_AND_FIXES.md`. If the records and the repository disagree, the repository wins; append a correction to the work log.
   - Run `git fetch origin`, then compare each local branch with its remote (`git status -sb`, or `git rev-parse <branch> origin/<branch>`).
   - If they diverged or the remote moved ahead, do not pull or merge over uncommitted or unpushed work. Record the divergence in the work log, then fast-forward only when the local branch has no unique commits; otherwise ask the owner.
3. Confirm the authorized milestone and its restrictions (section 10). Do not start unauthorized work.
4. Identify the available models and agents (section 4) and decide whether delegation is justified.
5. Append a work-log entry with a new session ID, the lead tool and model, the objective, dependencies and acceptance criteria before substantial work.

## 3. Roles and the lead agent
- **Lead agent** (exactly one per session): owns architecture decisions, shared interfaces and contracts, task sequencing, integration, Git operations, validation, acceptance and the records. Any capable AI may be lead (Claude, Gemini, Codex, ...); the role, not the vendor, carries the authority.
- **Specialists** (used only when justified):

| Role | Responsibilities | Model tier | Write scope |
|---|---|---|---|
| Architect | Roblox APIs, Server Authority, prediction/rollback, physics, network contracts, risky design questions | strongest reasoning | none by default (research, design notes) |
| Gameplay / server | server services, shared simulation and math, server tests | implementation | `src/server/**`, assigned `src/shared/Modules/**`, their tests |
| Client / presentation | input, camera, UI, VFX, audio, client visualizers | implementation | `src/client/**`, client tests |
| Reviewer / QA / security | independent review, test execution, exploit cases, acceptance evidence | strongest reasoning | none (read-only; reports defects) |
| Docs / tooling | documentation, records, configs, routine mechanical checks | fast/economical | `docs/**` (except locked decisions), tool configs |

  These map onto the workstreams in `specs/AGENT_ASSIGNMENT_MATRIX.md`. Shared contracts (`src/shared/Types.luau`, `src/shared/Config/**`, remote declarations in `default.project.json`, physics ownership) belong to the lead unless explicitly assigned in writing.
- Claude Code project agents for these roles live in `.claude/agents/`. Other tools should express the same roles with their own mechanisms and must not change the role boundaries.

## 4. Model selection
- Pick the cheapest model that can do the task reliably; escalate for risk, not habit.
  - **Strongest reasoning tier:** architecture, physics, Server Authority/prediction, complex or intermittent bugs, security review, acceptance decisions.
  - **Implementation tier:** ordinary Luau implementation, gameplay systems, UI, integration work, coordination.
  - **Fast/economical tier:** documentation, repetitive edits, routine configuration, mechanical checks (link checks, formatting runs, inventory).
- **Verify availability** before assigning: run a trivial probe or check the tool's model list. Record the model actually used (name and ID if the tool exposes it). Never assume an alias exists or record a guessed identity.
- Claude Code mapping verified on 2026-10-20 (session S-20261020-03, read-only probes): `opus` resolves to Opus 5.5 (`claude-opus-5-5`), `sonnet` to Sonnet 5.5 (`claude-sonnet-5-5`), `haiku` to Haiku 4.5 (`claude-haiku-4-5-20251001`). Re-verify if a probe or tool update suggests a change.
- Gemini, Antigravity or other tools: map their models to the same three tiers and record the mapping and its verification in the work log.

## 5. Multi-agent workflow
- **When to parallelize:** tasks with disjoint files and already-frozen interfaces (for example, independent services after the shared contracts exist), independent read-only investigations, or a separate review of finished work.
- **When not to:** simple tasks; anything touching shared contracts; work whose test sequence depends on a previous step; anything blocked by an open gate. Agent count never overrides dependencies, safety or quality.
- **Isolation:** one writer per file at a time. Concurrent writers use separate Git worktrees (`git worktree add`) or branches; the lead merges after review. Never merge conflicting edits by taking the last version.
- **Avoid waste:** no duplicate investigations (check the work log first), no speculative spawning, short and specific briefs that include the files, constraints, acceptance criteria and the required report format.
- **Review:** important implementations, security-sensitive code, physics/authority changes and fixes for hard bugs get an independent reviewer that did not write the code.
- **Delegation briefs must state:** session/task ID, objective, allowed files, forbidden files, milestone restrictions, checks to run, and the report format below.

### Required agent report (returned to the lead)
1. Agent role and model (as reported by the tool, or "unknown").
2. Task assigned and session/task ID.
3. Files inspected; files changed (or "none").
4. Actions and commands actually executed.
5. Checks and tests actually performed, with results.
6. Successes, failures, warnings and blockers.
7. Evidence: error excerpts, log paths, Git changes.
8. Remaining uncertainties.
9. Recommended next action.

Research and review agents label their output as research or review, not implemented work. The lead persists reports to the records; a report that only exists in chat is not persisted.

## 6. Audit trail (single shared history)
| File | Purpose | Rules |
|---|---|---|
| `docs/WORK_LOG.md` | chronological history of sessions, actions, commands, outcomes, decisions, branches, commits | append-only; one section per session `S-YYYYMMDD-NN`; corrections are new entries referencing the original |
| `docs/TEST_RESULTS.md` | every validation attempt | IDs `T-<milestone>-NNN`; statuses `PASS`, `FAIL`, `BLOCKED`, `NOT RUN`, `INCONCLUSIVE`, `SKIPPED`; retests get new IDs that link to the original |
| `docs/FAILURES_AND_FIXES.md` | significant failures | IDs `FAIL-NNN`; statuses `OPEN`, `INVESTIGATING`, `FIXED-VERIFIED`, `FIXED-UNVERIFIED`, `WONT-FIX` (with reason); never delete an entry |
| `docs/PROJECT_STATUS.md` | current snapshot | milestone, branch, status, completed, failed/blocked, outstanding tests, risks, prerequisites, last verified commit, evidence links, next three actions |
| `docs/GATE_0_REPORT.md` (and later milestone reports) | milestone evidence | criteria table with evidence links |
| `DECISION_LOG.md` | decisions | template fields; locked entries are never edited without owner approval |

**Status meanings.** `PASS` means it ran in the required environment and passed. A trivial pass (for example, a formatter with no source files) is recorded as `PASS` with that limitation stated. A mock or disposable stand-in never substitutes for the required environment. A failure stays `FAIL` until a successful retest is recorded under a new test ID. A fix without an environment to verify it is `FIXED-UNVERIFIED`.

**For every meaningful change, record:** affected files; why; what changed in plain English; related task/decision/requirement; validation run and its actual outcome; side effects or unverified behavior; commit hash once committed. Inspect the real `git diff` and compare it with the intent before recording a change as made.

**Evidence.** Store under `docs/evidence/<milestone>/` with names `YYYYMMDD-HHMMSS_<test-id>_<description>.<ext>`. Keep useful excerpts in the reports and link full logs. Redact credentials, tokens and private keys. Do not commit secrets, caches or enormous raw logs.

**Owner identity redaction (the repository is public).** When capturing new evidence (console output, screenshots, decoded files), replace the owner's Roblox username with `<owner-roblox-user>` and the owner's Roblox UserId with `<owner-uid>` before the file is written to the repository. Studio test players (negative UserIds such as `-1`, `Player1`) need no redaction. Evidence committed before 2026-10-20 S-20261020-09 and the existing commit metadata stay unchanged: removing them would need a history rewrite, which requires explicit owner approval.

**Checkpoints.** Before a substantial task: record the objective, dependencies and acceptance criteria. After each significant task or failed attempt: append to the work log and update the test, failure and status records. After each milestone: list passed, failed, blocked, inconclusive and unrun criteria separately and state whether the gate passed.

## 7. Git, branching and GitHub
**Remote.** `origin` = `https://github.com/HitanshG07/Sphere_Ball.git` is the shared hub for every AI tool (owner instruction, 2026-10-20). Authentication stays in the tool's credential store (for example the OS keyring used by `gh`), never in the repository.

**Branch map.**
| Branch | Role | Rules |
|---|---|---|
| `main` | untouched specification baseline (`f726ddd`) | never commit or push to it without owner approval |
| `alpha` | GitHub default branch; integration branch for approved work and records | receives only validated work, by fast-forward or a lead merge |
| `gate-0` | Gate 0 prototype (`bc4cfa7`) | never merged into `alpha`; only verified documentation moved to `alpha`, in a separate docs-only commit. Local alias `gate0-spike` tracks `origin/gate-0`. A duplicate local branch `gate-0` (same commit) also exists and is kept until the owner authorizes deleting it |
| `task<NN>` (for example `task01`) | one task's work, branched from `alpha` | pushed after validation; merged into `alpha` by the lead once the task gate passes |
| agent worktree branches | parallel writers | local only unless the lead decides otherwise; merged by the lead after review |

**Push procedure.**
1. `git fetch origin` and confirm the push is a fast-forward of the remote branch.
2. Run the pre-push audit below.
3. `git push origin <branch>` (never `--force` or `--force-with-lease` without explicit owner approval).
4. Verify with `git ls-remote origin <branch>` and record the pushed hash and remote ref in the work log and `PROJECT_STATUS.md`. A backup or publication is claimed only after this check succeeds.

**Pre-push audit.**
- Secret scan of the new commits (`git log -p origin/<branch>..<branch>`): tokens (`gh[pousr]_`, `github_pat_`), API keys, private keys, `.ROBLOSECURITY` cookies, `.env` files, passwords.
- Ignore review: no build output (`build/`), generated `sourcemap.json`, lock files or caches staged.
- Large files: anything above about 50 MB goes through Git LFS (needs owner approval to enable). The largest tracked file today is the 2.7 MB concept PNG.
- Scope: `git diff --stat origin/<branch>..<branch>` matches what the work log says was changed; no prototype `src`/`tests` files from `gate-0` reach `alpha`.

**Visibility.** The repository is **public** by owner decision (2026-10-20). Owner identifiers in new evidence are redacted (section 6). Changing visibility is an owner decision.

**Canonical Studio place.** `place/Gate0.rbxl` is version-controlled: Path A Workspace settings (`AuthorityMode = Server`, saved) and no game scripts. Code comes from Rojo (`rojo serve default.project.json`), never from scripts saved in the place. Before committing a re-saved place, check that the decoded file contains no scripts or owner identifiers and still decodes to `AuthorityMode` 0. `*.rbxl.lock` stays ignored; `*.rbxl` is binary in `.gitattributes`.

**General.**
- Commit coherent, scoped units with descriptive messages. Do not rewrite published history, force-push, skip hooks or amend another agent's commit.
- Never discard uncommitted user work; use a stash or branch and record it.

## 8. Session end protocol
1. Append the work-log entry: actions, commands, results, failures, decisions, commits.
2. Update `docs/TEST_RESULTS.md`, `docs/FAILURES_AND_FIXES.md` and `docs/PROJECT_STATUS.md`, including the next three actions.
3. Inspect `git status` and `git diff`; report every changed file; record the last commit and any uncommitted or stashed work.
4. State which checks passed, failed, were blocked, inconclusive or unrun.
5. Give the owner a short human-readable summary including failures and risks.

If a record cannot be updated (permissions, tool limits, environment unavailable), say so explicitly; the handoff is then incomplete.

## 9. Cross-AI continuation and registering a new tool
- An incoming AI resumes from the last **verified** state in the records and the repository, not from another tool's chat.
- To add a tool: if it reads `AGENTS.md` natively, nothing else is required. Otherwise create a minimal adapter that imports `AGENTS.md` with the tool's documented mechanism (or tells the tool to read `AGENTS.md` and this protocol first), plus only genuinely tool-specific notes. Record the adapter, the loading mechanism and how it was verified in the work log and in the table below. Never copy and fork the rules.

| Tool | Entry point | Loading mechanism | Verification status |
|---|---|---|---|
| Claude Code (v2.1.303) | `CLAUDE.md` with `@AGENTS.md` import; `.claude/agents/*.md` | official docs: imports at launch; check with `/context` or `/memory` | documented; actual load confirmed only after a new session in the repo root runs `/context` |
| Gemini CLI | `GEMINI.md` with `@./AGENTS.md` import | official memport docs | documented; not run on this machine |
| Antigravity | `GEMINI.md` (precedence) and `AGENTS.md` | third-party guides only (AGENTS.md from IDE v1.20.x; workspace rules in `.agents/rules/`) | **unverified**; owner to confirm in Antigravity |
| GitHub Copilot, Cursor | none (owner instruction 2026-10-20: not needed) | both read `AGENTS.md` natively per their docs | not configured |

## 10. Milestone restrictions (current)
- Gate 0 (TASK-00) passed on 2026-10-20 with Path A (D-024).
- TASK-01 is authorized (owner approval of `docs/TASK-01_PLAN.md`, 2026-10-20). TASK-02 and later tasks each need owner approval before they start.
- The Gate 0 prototype (`gate-0` / `gate0-spike`) is never merged into `alpha`.
- Supporting agents write only the files their brief assigns, in an isolated worktree or branch; the lead integrates.
- Locked decisions (D-001 to D-018) and owner decisions (D-019 onward) change only through a recorded, owner-approved decision.
- Apply section 5 to TASK-01 onward using the task dependencies in `MASTER_IMPLEMENTATION_PLAN.md` section 15 and the frozen interfaces.
