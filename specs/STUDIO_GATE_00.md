# Studio Gate 0 - Required Environment Verification

This check sheet selects exactly one approved architecture. Verify against current official Roblox Creator Hub documentation and the actual target Studio build. Do not assume the same settings exist in every installed version.

## Path A - Preferred: Roblox Server Authority
- [ ] `Workspace.AuthorityMode` exists and is set to `Server` in Studio.
- [ ] Dependent settings are enabled: `NextGenerationReplication`, `PlayerScriptsUseInputActionSystem`, `SignalBehavior=Deferred`, `UseFixedSimulation`, and `StreamingEnabled`.
- [ ] Shared simulation module binds successfully with `RunService:BindToSimulation()`.
- [ ] Simulation-affecting input uses Input Action System, and rollback-sensitive timing uses `time()` inside the bound simulation.
- [ ] Two-client movement/prediction/correction test passes.
- [ ] Server-authoritative collision/knockback/KO beats a deliberately invalid client claim.

## Path B - Pre-approved fallback only if Path A is genuinely unavailable
- [ ] Gate report records which Path A setting/API is absent and evidence. Do not use Path B solely to avoid debugging an available Path A.
- [ ] Each live sphere root is set server-owned via `SetNetworkOwner(nil)`.
- [ ] Clients send normalized input intent only, with sequence numbers and a maximum of 20 updates/second per player; no client-supplied transform, velocity, collision, impulse or KO is accepted.
- [ ] Server computes motion, hit outcomes, knockback, eliminations, queue state and results.
- [ ] Client extrapolation affects visual shell/camera presentation only.
- [ ] Two-client and four-client movement/collision tests pass; Studio Network Simulation representative-latency test passes or its unavailability is documented as a release risk.
- [ ] If responsiveness or integrity fails, mark `BLOCKED`; do not invent a third architecture.

## Shared requirements
- [ ] No remote path makes a client-confirmed impulse/KO authoritative.
- [ ] Server validates input shape, range, rate and lifecycle state.
- [ ] Produce `docs/GATE_0_REPORT.md` containing selected path, target versions, settings, exact tests/logs, screenshots, results and known limits.
