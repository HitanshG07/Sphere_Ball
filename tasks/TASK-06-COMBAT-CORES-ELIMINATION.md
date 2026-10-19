# TASK-06 - Validated Combat, Core Abilities, and Elimination Attribution

## Preconditions
TASK-04 and TASK-05 accepted; server-authority simulation passes Gate 0.

## Goal
Implement understandable, bounded, server-authoritative impact behavior and three core abilities.

## Files
- `src/server/Core/PhysicsValidator.luau`
- `src/server/Core/AbilityService.luau`
- `src/server/Core/EliminationService.luau`
- `src/server/Tests/Unit/PhysicsValidator.spec.luau`
- integration tests

## Required impact math
For horizontal vectors: `n = normalize(Pvictim - Pattacker)`, `closing = dot(Vattacker - Vvictim, n)`. Validate a small contact-distance tolerance and closing >=10 studs/s. Ignore invalid/eliminated/invulnerable/cooldown pair. Compute `rawDeltaV = (closing - 10) * 1.15 * outgoingFactor * victimResistanceFactor`, clamp [0,32]. Apply victim velocity delta along n and attacker recoil opposite n at 0.25 ratio. Cap total horizontal speed at 55.

Use server-authority synchronized simulation; never accept client-supplied positions, velocities, normals, players, result or KO decisions.

## Core abilities
Implement exactly as defined in Master Plan Section 8.3:
- Kinetic Overdrive Dash: 8-second cooldown, +22 studs/s toward input/current motion/facing fallback, max speed 55, 1.25 outgoing impact factor for 1 second.
- Cryo Anchor Brake: 9-second cooldown, remove 85% lateral drift, ignore ice/magnetic hazard forces for 2.5 seconds, incoming knockback factor 1/1.5 for 2 seconds.
- Magnetic Pulse Tether: 10-second cooldown, nearest eligible opponent within 24 studs, deterministic tie-break, +16 studs/s toward caster, speed cap. No valid target means feedback and no cooldown consumption.

## Elimination
- Void threshold Y<15.
- Credit a valid last hitter only within 5 seconds of a server-validated hit.
- Player eliminated exactly once; remove collision participation/input/ability before spectating.
- Disconnect and round reset clear last-hit references.

## Tests
- head-on closing speed 35 triggers bounded hit
- glancing/under-threshold contact ignored
- direction sign passes two-body tests
- A-B and B-A share cooldown
- ability cooldown, state, core type, immunity and caps work
- Magnetic no-target does not spend cooldown
- fall at 4 seconds after valid hit credited; fall at >5 seconds environmental
- no duplicate eliminations/rewards
