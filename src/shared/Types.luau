--!strict
-- Shared type contracts (Master Plan §10.4). Types only, no runtime state. Owner: lead agent.
-- All timestamps are Workspace:GetServerTimeNow() values. UserIds are numbers.

export type RoundPhase =
	"Lobby"
	| "Countdown"
	| "Opening"
	| "Collapse1"
	| "MidGame"
	| "Collapse2"
	| "SuddenDeath"
	| "Results"
	| "Cleanup"
-- The round phases that run Board Pulse cycles (§7.2).
export type PulsePhase = "Opening" | "MidGame" | "SuddenDeath"
export type HazardPattern = "IceCorridor" | "MagneticStorm" | "BoostRunway"
export type PulseState = "SafeCombat" | "Warning" | "Active" | "Reset"

export type GameMode = "FreeForAll"
export type QueueSource = "Portal" | "QuickQueue"
-- Client queue intents (§5.2); the client never sends counts, rosters or timers.
export type QueueAction = "JoinQuickQueue" | "LeaveQueue" | "SelectMode"
-- Waiting: fewer than 4 queued. PartialWait: 4-5 queued, up to 25 s. Countdown: 8 s full or 10 s partial (§4.3).
export type QueueStatus = "Waiting" | "PartialWait" | "Countdown"

export type ChassisId = "Rammer" | "Trickster" | "Magnetar" | "Bulwark"
export type CoreId = "Kinetic" | "Cryo" | "Magnetic"
export type SphereSkinId = "Default" | "Neon" | "Gold" | "Void" -- D-020
export type TrailId = "None" | "CoreStreak" | "CyanStreak" -- D-021
export type EffectId = "StandardSpark" | "CoreBurst" -- D-021
export type LoadoutCategory = "Chassis" | "Skin" | "Core" | "Trail" | "Effect"

export type PlayerLoadout = {
	Chassis: ChassisId,
	Skin: SphereSkinId,
	Core: CoreId,
	Trail: TrailId,
	Effect: EffectId,
}

export type CellState = "Live" | "PendingCollapse" | "Destroyed"

export type GridCell = {
	X: number, -- integer in [-4, 4]
	Z: number,
	Ring: number, -- max(|X|, |Z|)
	State: CellState,
}

-- Pattern metadata shared by server gameplay and every client visualizer (§7.3-7.6).
-- Corridors and runways pass through the board center; AngleDegrees selects the orientation.
export type PatternMeta =
	{
		Pattern: "IceCorridor",
		AngleDegrees: number, -- 0, 45, 90 or 135
	}
	| {
		Pattern: "MagneticStorm",
		AnchorX: number,
		AnchorZ: number,
		RadiusTiles: number,
	}
	| {
		Pattern: "BoostRunway",
		AngleDegrees: number, -- 0, 90, 180 or 270
	}

-- One payload per cycle (§7.1); also the snapshot sent to late or rejoining clients.
-- Pulse state at time t: SafeCombat in [StartAt, WarningAt), Warning, Active, Reset in [ResetAt, EndAt).
export type BoardPulsePayload = {
	RoundId: number,
	CycleId: number, -- increases every cycle of a round; doubles as the Boost Runway event stamp
	Phase: PulsePhase,
	Meta: PatternMeta,
	StartAt: number,
	WarningAt: number,
	ActiveAt: number,
	ResetAt: number,
	EndAt: number,
}

-- Sent per player: IsQueued and Source describe the receiving player.
export type QueueStatePayload = {
	Mode: GameMode,
	Count: number, -- unique eligible UserIds
	Status: QueueStatus,
	TimerEndsAt: number?, -- end of the partial wait or the countdown; nil while Waiting
	LoadoutLocked: boolean,
	IsQueued: boolean,
	Source: QueueSource?,
	Roster: { number }?, -- UserIds once the roster is locked
	Reason: string?, -- why a countdown was cancelled or a launch failed
}

export type MatchStatePayload = {
	RoundId: number,
	Phase: RoundPhase,
	PhaseEndsAt: number?, -- nil when the phase has no fixed end
	HardTimeoutAt: number?, -- 150 s after the match starts
	NextCollapseAt: number?,
	Participants: { number },
	Alive: { number },
}

export type EndReason = "LastSurvivor" | "HardTimeout"

export type PlayerResult = {
	UserId: number,
	Placement: number, -- 1 is best; tied players share a placement (D-022)
	Knockouts: number,
	HazardKnockouts: number,
	SurvivalTime: number,
	Eliminated: boolean,
}

-- Winners are the entries with Placement 1; more than one means a shared tie.
export type ResultPayload = {
	RoundId: number,
	EndReason: EndReason,
	Players: { PlayerResult },
}

return nil
