--!strict
-- Core abilities (Master Plan §8.3, LOCKED Alpha behavior). The server owns cooldowns and effects.
-- Speed caps use GameConfig.Movement.HorizontalCap. Owner: lead agent.
local Types = require(script.Parent.Parent.Types)

local ids: { Types.CoreId } = { "Kinetic", "Cryo", "Magnetic" }

return {
	Ids = ids,
	-- Overdrive Dash: +DeltaV along input, else horizontal velocity, else facing; no charges, no reset on hit.
	Kinetic = {
		AbilityName = "Overdrive Dash",
		Cooldown = 8,
		DeltaV = 22,
		OutgoingFactor = 1.25,
		OutgoingDuration = 1.0,
	},
	-- Anchor Brake: removes 85% of lateral drift; hazard immunity and knockback resistance use simulation time.
	Cryo = {
		AbilityName = "Anchor Brake",
		Cooldown = 9,
		DriftRemoval = 0.85,
		HazardImmunityDuration = 2.5, -- ignores Ice penalties and Magnetic pull
		ResistanceFactor = 1 / 1.5, -- victimResistanceFactor
		ResistanceDuration = 2.0,
	},
	-- Pulse Tether: nearest live opponent within Range (tie-break by UserId) gets +PullDeltaV toward the caster.
	-- No valid target: the ability fails with NO TARGET and does not consume the cooldown.
	Magnetic = {
		AbilityName = "Pulse Tether",
		Cooldown = 10,
		Range = 24,
		PullDeltaV = 16,
	},
}
