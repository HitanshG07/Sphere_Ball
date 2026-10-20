--!strict
-- Canonical locked constants (Master Plan v1.2, specs/DESIGN_CONSTANTS.md, D-015 to D-027). Owner: lead agent.
-- Services read values from here; never copy a literal timing or limit into service code.
-- Derived values (81 cells, top surface Y 51, spawn Y 54.15, cycle totals) are asserted by tests, not stored twice.
-- Changing any value needs an approved DECISION_LOG.md entry. Camera and presentation values (§8.1, §11.2, §11.4,
-- §11.5) are not here yet: TASK-04 and TASK-09 add them to this file through the lead (RV-T01-04).
local Types = require(script.Parent.Parent.Types)

export type CycleTiming = {
	SafeCombat: number,
	Warning: number,
	Active: number,
	Reset: number,
}

export type GridPoint = { X: number, Z: number }

-- One value per Board Pulse phase (Types.PulsePhase); readable by name or with a PulsePhase variable.
export type PerPhase<T> = { Opening: T, MidGame: T, SuddenDeath: T }

-- Typed locals (not casts) so a misspelled ID fails analysis.
local mode: Types.GameMode = "FreeForAll"
local skins: { Types.SphereSkinId } = { "Default", "Neon", "Gold", "Void" }
local unlockedSkins: { Types.SphereSkinId } = { "Default", "Neon" } -- D-020; Gold and Void are locked
local trails: { Types.TrailId } = { "None", "CoreStreak", "CyanStreak" } -- D-021, all unlocked
local effects: { Types.EffectId } = { "StandardSpark", "CoreBurst" } -- D-021, all unlocked

-- Per-phase tables are typed locals too, so a missing phase or field fails analysis (RV-T01-06).
local cycles: PerPhase<CycleTiming> = {
	Opening = { SafeCombat = 14, Warning = 3.5, Active = 7, Reset = 3.5 },
	MidGame = { SafeCombat = 10, Warning = 2.5, Active = 6, Reset = 2.5 },
	SuddenDeath = { SafeCombat = 6, Warning = 2, Active = 5, Reset = 2 },
}
local iceCardinalHalfWidth: PerPhase<number> = { Opening = 1.0, MidGame = 0.5, SuddenDeath = 0.5 }
-- Diagonal lane limit |along| <= value; nil = full length (§7.4).
local iceDiagonalAlongLimit: PerPhase<number?> = { MidGame = 2.8, SuddenDeath = 1.42 }
local magneticRadiusTiles: PerPhase<number> = { Opening = 2.8, MidGame = 2.0, SuddenDeath = 1.0 }

local GameConfig = {}

GameConfig.Mode = mode

GameConfig.Arena = {
	CFrame = CFrame.new(0, 50, 0), -- ArenaCFrame: axis-aligned, position = grid center (§6.1)
	Pitch = 12,
	GridRadius = 4, -- coordinates -4..4 inclusive
	CollisionTileSize = Vector3.new(12, 2, 12),
	VisualTileSize = Vector3.new(11.8, 2, 11.8),
	HazardOverlaySize = Vector3.new(11.4, 0.05, 11.4), -- "around" this size (§6.2)
	TileElasticity = 0,
	TileFriction = 0, -- D-028: traction comes from the movement code (§6.2, §6.3)
	TilePropertyWeight = 100, -- D-028: FrictionWeight and ElasticityWeight, so the tile values dominate contacts
	CollapseSinkTime = 0.65, -- D-028: seconds the visual sinks and fades after the collider is removed (§11.4)
	CollapseSinkDepth = 4, -- D-028: studs the visual sinks during CollapseSinkTime
	SphereDiameter = 6,
	SpawnLocalY = 4.15, -- sphere center above ArenaCFrame at spawn (§6.5)
	VoidY = 15, -- eliminated below this world Y
	HazardCapRatio = 0.35, -- max hazard cells = floor(liveCellCount * ratio)
	CollapseRings = { 4, 3 }, -- Collapse1 removes ring 4, Collapse2 removes ring 3 (D-005)
	CollapseWarning = 3, -- seconds of visual warning before a ring collapses (§6.4)
	-- Initial match spawn slots in fixed order (D-016); assigned by stable player order, never random.
	SpawnSlots = {
		{ X = 0, Z = -3 },
		{ X = 3, Z = -2 },
		{ X = 3, Z = 2 },
		{ X = 0, Z = 3 },
		{ X = -3, Z = 2 },
		{ X = -3, Z = -2 },
	} :: { GridPoint },
}

GameConfig.Round = {
	MinPlayers = 4,
	MaxPlayers = 6,
	HubCapacity = 12,
	FullCountdown = 8,
	PartialWait = 25,
	PartialCountdown = 10,
	LoadoutLockBefore = 5, -- loadouts lock at countdown T-minus 5 s
	PortalDwell = 1.0,
	PortalExitGrace = 0.5,
	ResultsDuration = 8,
	HardTimeout = 150, -- seconds of match time
}

GameConfig.Pulse = {
	Cycles = cycles,
	-- Complete cycles before the next collapse. SuddenDeath repeats until one survivor or the hard timeout.
	CycleCount = { Opening = 2, MidGame = 2 },
	ScheduleTolerance = 0.05, -- §13.2 test 9
}

GameConfig.Hazards = {
	Ice = {
		Angles = { 0, 45, 90, 135 },
		CardinalHalfWidth = iceCardinalHalfWidth,
		DiagonalHalfWidth = 0.71,
		DiagonalAlongLimit = iceDiagonalAlongLimit,
		SteeringMultiplier = 0.45,
		LateralDampingMultiplier = 0.25, -- 25% of Movement.LateralDamping = 1.625
	},
	Magnetic = {
		RadiusTiles = magneticRadiusTiles,
		MaxAcceleration = 22, -- a = Max * (1 - d / radiusStuds)^2, horizontal only
		InwardSpeedCap = 12,
	},
	BoostRunway = {
		Angles = { 0, 90, 180, 270 },
		HalfWidth = 0.5,
		DeltaV = 18, -- one-time per sphere per event
	},
}

GameConfig.Movement = {
	Acceleration = 85,
	TopSpeed = 42,
	HorizontalCap = 55,
	LateralDamping = 6.5,
	LongitudinalDrag = 1.8,
	BrakeDeceleration = 95,
}

-- §8.5: deltaV = clamp((closing - MinClosingSpeed) * KnockbackScale * outgoing * resistance, 0, KnockbackMax).
-- D-027: the engine's own sphere contact stays; tune only through a playtest-backed TUNING decision.
GameConfig.Combat = {
	MinClosingSpeed = 10,
	KnockbackScale = 1.15,
	KnockbackMax = 32,
	RecoilRatio = 0.25,
	PairCooldown = 0.35,
	KoAttributionWindow = 5,
	SpawnInvulnerability = 2.5,
}

-- D-019 Burst boost (Shift / touch Boost). Direction: move input, else horizontal velocity, else facing.
GameConfig.BurstBoost = {
	DeltaV = 12,
	Cooldown = 4,
	OutgoingFactor = 1.0,
}

GameConfig.Cosmetics = {
	Skins = skins,
	UnlockedSkins = unlockedSkins,
	Trails = trails,
	Effects = effects,
}

GameConfig.Colors = {
	TileDark = Color3.fromRGB(32, 38, 54),
	TileLight = Color3.fromRGB(42, 50, 70),
	PrimaryCyan = Color3.fromRGB(0, 195, 255),
	Ice = Color3.fromRGB(0, 235, 255),
	Magnetic = Color3.fromRGB(165, 55, 255),
	Boost = Color3.fromRGB(255, 125, 0),
	WarningAmber = Color3.fromRGB(255, 170, 0),
	CollapseRed = Color3.fromRGB(255, 40, 40),
	TextPrimary = Color3.fromRGB(245, 248, 255),
	TextSecondary = Color3.fromRGB(170, 190, 215),
}

-- §6.2 collision-group matrix, exactly as specified. Pairs the matrix does not list (for example LobbyAvatar with
-- LobbyAvatar, or any group with Default) are undecided: raise them in TASK-02/03, do not guess.
GameConfig.CollisionGroups = {
	ArenaSphere = "ArenaSphere",
	ArenaTile = "ArenaTile",
	LobbyAvatar = "LobbyAvatar",
	LobbyWorld = "LobbyWorld",
	SphereVisual = "SphereVisual",
	Colliding = {
		{ "ArenaSphere", "ArenaTile" },
		{ "ArenaSphere", "ArenaSphere" },
		{ "LobbyAvatar", "LobbyWorld" },
	},
	-- Roblox groups collide by default, so these must be set non-collidable explicitly (RV-T01-03).
	NonColliding = {
		{ "ArenaSphere", "LobbyAvatar" },
		{ "ArenaSphere", "LobbyWorld" },
		{ "LobbyAvatar", "ArenaTile" },
	},
	-- Groups that collide with no group at all, including Default and themselves.
	CollidesWithNothing = { "SphereVisual" },
}

-- §2.4 layout (top walking surface at Y 150) and D-023 holding pods. LobbyConfig is this section (D-023).
GameConfig.Lobby = {
	HubCenter = Vector3.new(0, 150, -300),
	SpawnCFrame = CFrame.lookAt(Vector3.new(0, 150, -334), Vector3.new(0, 150, -300)), -- D-015: faces +Z
	QueuePortal = Vector3.new(0, 150, -300),
	QueuePadRadius = 14,
	PlazaDiameter = 140,
	Customize = Vector3.new(-43, 150, -300),
	Shop = Vector3.new(43, 150, -300),
	ModeBoard = Vector3.new(35, 150, -326),
	Leaderboard = Vector3.new(35, 150, -274),
	RewardDisplay = Vector3.new(-38, 150, -326),
	Pods = {
		Count = 6,
		FloorSize = Vector3.new(10, 1, 10), -- anchored
		TopY = 200,
		-- Pod i (1..6) is centred at (FirstX + Spacing * (i - 1), TopY, Z).
		FirstX = 2000,
		Spacing = 20,
		Z = 2000,
		CollisionGroup = GameConfig.CollisionGroups.LobbyAvatar,
	},
	-- D-026 (mandatory, not a setting): after parking, AddReplicationFocus(avatar HumanoidRootPart); remove it
	-- (pcall-guarded) at restore, cleanup and disconnect.
}

return GameConfig
