--!strict
-- Alpha chassis (Master Plan §8.2, D-008): cosmetic silhouettes only; every combat multiplier is 1.0.
-- Sidegrade stats need a separate balance milestone and owner approval. Owner: lead agent.
local Types = require(script.Parent.Parent.Types)

export type ChassisStats = {
	OutgoingFactor: number, -- attackerOutgoingFactor in §8.5
	ResistanceFactor: number, -- victimResistanceFactor in §8.5
}

local IDENTICAL: ChassisStats = { OutgoingFactor = 1.0, ResistanceFactor = 1.0 }

local ids: { Types.ChassisId } = { "Rammer", "Trickster", "Magnetar", "Bulwark" }

-- Readable by name or with a ChassisId variable.
local stats: { Rammer: ChassisStats, Trickster: ChassisStats, Magnetar: ChassisStats, Bulwark: ChassisStats } = {
	Rammer = IDENTICAL,
	Trickster = IDENTICAL,
	Magnetar = IDENTICAL,
	Bulwark = IDENTICAL,
}

return {
	Ids = ids,
	Stats = stats,
}
