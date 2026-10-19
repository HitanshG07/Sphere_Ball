# Studio Gate 0 - Required Environment Verification

This check sheet selects exactly one approved architecture. Verify against current official Roblox Creator Hub documentation and the actual target Studio build. Do not assume the same settings exist in every installed version.

## Path A - Preferred: Roblox Server Authority
- [ ] `Workspace.AuthorityMode` exists and is set to `Server` in Studio.
- [ ] Dependent settings are enabled: `NextGenerationReplication`, `PlayerScriptsUseInputActionSystem`, `SignalBehavior=Deferred`, `UseFixedSimulation`, and `StreamingEnabled`.
- [ ] Shared simulation module binds successfully with `RunService:BindToSimulation()`.
- [ ] Simulation-affecting input uses Input Action System, and rollback-sensitive timing uses `time()` inside the bound simulation.
- [ ] Two-client movement/prediction/correction test passes.
- [ ] Server-authoritative collision/knockback/KO beats a deliberately invalid client claim.
- [ ] A1: `AuthorityMode = Server` and the dependent settings are verified in the Studio Properties panel (screenshot). A failed script access is not unavailability evidence (D-025 / RobloxScriptSecurity).
- [ ] A2: each client calls `SetPredictionMode(ownRoot, Enum.PredictionMode.On)` client-side; the client reports `Predicted` and the server reports `Authoritative`.
- [ ] A3: local motion responds on the frame the input is fired; measured at 0 ms and 150 ms.
- [ ] A4: after a server kick and after a head-on hit, the client root converges to the server state within 0.5 stud within 1 s.
- [ ] A5: rollback reproducibility at 150 ms (5 kicks + 5 head-on runs, counters recorded); PASS needs at least one observed rollback and unique client FX = server hits + kicks; otherwise retry at 250 ms, then INCONCLUSIVE (Gate 0 BLOCKED, not PASS).
- [ ] A6: the input bridge is a world-space `Scriptable` binding with a magnitude clamp of <= 1 in the simulation; simulation callbacks have no side effects; AutoDrive is Studio-gated test code only.

## Path B - Pre-approved fallback only if Path A is genuinely unavailable
- [ ] Gate report records which Path A setting/API is absent and evidence. Do not use Path B solely to avoid debugging an available Path A.
- [ ] Each live sphere root is set server-owned via `SetNetworkOwner(nil)`.
- [ ] Clients send normalized input intent only, with sequence numbers and a maximum of 20 updates/second per player; no client-supplied transform, velocity, collision, impulse or KO is accepted.
- [ ] Server computes motion, hit outcomes, knockback, eliminations, queue state and results.
- [ ] Client extrapolation affects visual shell/camera presentation only.
- [ ] Two-client and four-client movement/collision tests pass; Studio Network Simulation representative-latency test passes or its unavailability is documented as a release risk.
- [ ] If responsiveness or integrity fails, mark `BLOCKED`; do not invent a third architecture.
- [ ] B2: every root reports `GetNetworkOwner() == nil` after spawn, after collisions and after 60 s.
- [ ] B3: NaN, infinite, non-Vector2, magnitude > 1, stale, replayed and wrong-lifecycle intents are each rejected and logged.
- [ ] B4: a client spamming 60 intents/s for 10 s gets at most 200 (+1 bucket) accepted.
- [ ] B5: input-to-visible-motion latency is measured and recorded at 0, 100 and 150 ms.
- [ ] Path B is not required to pass Path A prediction-status or rollback checks.

## Shared requirements
- [ ] No remote path makes a client-confirmed impulse/KO authoritative.
- [ ] Server validates input shape, range, rate and lifecycle state.
- [ ] C1-C5 common checks: solo speed (42 +/- 2, <= 55) and natural fall with single elimination; two-client server-only hit matching the §8.5 formula within 1 stud/s; tamper and oversized input rejected; stable no-roll camera; D-023 restore matrix in miniature (elimination, restore, repeat, disconnect).
- [ ] Produce `docs/GATE_0_REPORT.md` containing selected path, target versions, settings, exact tests/logs, screenshots, results and known limits.
