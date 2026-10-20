--!strict
-- Config asserts against the spec numbers (Master Plan §3.3, §7.2, §8, D-008, D-015 to D-023).
-- Expected values are written here on purpose: they are the spec, checked independently of the config.
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Config = ReplicatedStorage.Shared.Config
local GameConfig = require(Config.GameConfig)
local ChassisConfig = require(Config.ChassisConfig)
local CoreConfig = require(Config.CoreConfig)
local AssetManifest = require(Config.AssetManifest)

local function near(a: number, b: number, what: string)
	assert(math.abs(a - b) < 1e-9, `{what}: expected {b}, got {a}`)
end

local function sameList<T>(actual: { T }, expected: { T }, what: string)
	assert(#actual == #expected, `{what}: expected {#expected} entries, got {#actual}`)
	for i, v in expected do
		assert(actual[i] == v, `{what}[{i}]: expected {v}, got {actual[i]}`)
	end
end

local function cycleTotal(phase: "Opening" | "MidGame" | "SuddenDeath"): number
	local c = GameConfig.Pulse.Cycles[phase]
	return c.SafeCombat + c.Warning + c.Active + c.Reset
end

return {
	["cycle totals are 28, 21 and 15 s (D-017)"] = function()
		near(cycleTotal("Opening"), 28, "Opening cycle")
		near(cycleTotal("MidGame"), 21, "MidGame cycle")
		near(cycleTotal("SuddenDeath"), 15, "SuddenDeath cycle")
	end,

	["named cycle values match §7.2"] = function()
		local o, m, s =
			GameConfig.Pulse.Cycles.Opening, GameConfig.Pulse.Cycles.MidGame, GameConfig.Pulse.Cycles.SuddenDeath
		assert(o.SafeCombat == 14 and o.Warning == 3.5 and o.Active == 7 and o.Reset == 3.5, "Opening 14/3.5/7/3.5")
		assert(m.SafeCombat == 10 and m.Warning == 2.5 and m.Active == 6 and m.Reset == 2.5, "MidGame 10/2.5/6/2.5")
		assert(s.SafeCombat == 6 and s.Warning == 2 and s.Active == 5 and s.Reset == 2, "SuddenDeath 6/2/5/2")
	end,

	["Opening lasts 56 s and MidGame 42 s"] = function()
		near(GameConfig.Pulse.CycleCount.Opening * cycleTotal("Opening"), 56, "Opening")
		near(GameConfig.Pulse.CycleCount.MidGame * cycleTotal("MidGame"), 42, "MidGame")
		assert(GameConfig.Round.HardTimeout == 150, "hard timeout 150")
	end,

	["speed caps are 42 and 55"] = function()
		assert(GameConfig.Movement.TopSpeed == 42, "top speed 42")
		assert(GameConfig.Movement.HorizontalCap == 55, "horizontal cap 55")
	end,

	["movement and combat values match §8.4-8.5"] = function()
		local mv, c = GameConfig.Movement, GameConfig.Combat
		assert(mv.Acceleration == 85 and mv.LateralDamping == 6.5 and mv.LongitudinalDrag == 1.8, "movement")
		assert(mv.BrakeDeceleration == 95, "brake 95")
		assert(c.MinClosingSpeed == 10 and c.KnockbackScale == 1.15 and c.KnockbackMax == 32, "knockback")
		assert(c.RecoilRatio == 0.25 and c.PairCooldown == 0.35, "recoil and pair cooldown")
		assert(c.KoAttributionWindow == 5 and c.SpawnInvulnerability == 2.5, "KO window and invulnerability")
	end,

	["Burst boost matches D-019"] = function()
		local b = GameConfig.BurstBoost
		assert(b.DeltaV == 12 and b.Cooldown == 4 and b.OutgoingFactor == 1.0, "boost 12 / 4 s / 1.0")
	end,

	["hazard values match §7.4-7.6"] = function()
		local h = GameConfig.Hazards
		near(GameConfig.Movement.LateralDamping * h.Ice.LateralDampingMultiplier, 1.625, "ice lateral damping")
		assert(h.Ice.SteeringMultiplier == 0.45, "ice steering 0.45")
		assert(h.Ice.CardinalHalfWidth.Opening == 1.0 and h.Ice.CardinalHalfWidth.MidGame == 0.5, "ice width")
		assert(h.Ice.CardinalHalfWidth.SuddenDeath == 0.5 and h.Ice.DiagonalHalfWidth == 0.71, "ice width")
		assert(h.Ice.DiagonalAlongLimit.Opening == nil, "Opening diagonal is full length")
		assert(h.Ice.DiagonalAlongLimit.MidGame == 2.8 and h.Ice.DiagonalAlongLimit.SuddenDeath == 1.42, "diag")
		local r = h.Magnetic.RadiusTiles
		assert(r.Opening == 2.8 and r.MidGame == 2.0 and r.SuddenDeath == 1.0, "magnetic radius")
		assert(h.Magnetic.MaxAcceleration == 22 and h.Magnetic.InwardSpeedCap == 12, "magnetic pull")
		assert(h.BoostRunway.DeltaV == 18 and h.BoostRunway.HalfWidth == 0.5, "boost runway")
		sameList(h.Ice.Angles, { 0, 45, 90, 135 }, "ice angles")
		sameList(h.BoostRunway.Angles, { 0, 90, 180, 270 }, "boost runway angles (cardinal only)")
	end,

	["hazard cap is floor(live * 0.35)"] = function()
		local ratio = GameConfig.Arena.HazardCapRatio
		assert(ratio == 0.35, `hazard cap ratio {ratio}`)
		assert(math.floor(81 * ratio) == 28, "81 cells -> 28")
		assert(math.floor(49 * ratio) == 17, "49 cells -> 17")
		assert(math.floor(25 * ratio) == 8, "25 cells -> 8")
	end,

	["arena geometry matches §3.3 and §6"] = function()
		local a = GameConfig.Arena
		assert(a.CFrame.Position == Vector3.new(0, 50, 0), "arena center (0, 50, 0)")
		assert(a.CFrame.Rotation == CFrame.identity, "arena is axis-aligned")
		assert(a.Pitch == 12 and a.GridRadius == 4, "pitch 12, radius 4")
		near(a.CFrame.Y + a.CollisionTileSize.Y / 2, 51, "tile top surface Y")
		near(a.CFrame.Y + a.SpawnLocalY, 54.15, "spawn center Y")
		assert(a.CollisionTileSize == Vector3.new(12, 2, 12), "collision tile 12x2x12")
		assert(a.VisualTileSize == Vector3.new(11.8, 2, 11.8), "visual tile 11.8x2x11.8")
		assert(a.SphereDiameter == 6 and a.VoidY == 15 and a.TileElasticity == 0, "sphere, void, elasticity")
		assert(a.CollapseRings[1] == 4 and a.CollapseRings[2] == 3 and #a.CollapseRings == 2, "D-005 order")
		assert(a.CollapseWarning == 3, "collapse warning 3 s")
	end,

	["tile physics and collapse visual match D-028"] = function()
		local a = GameConfig.Arena
		assert(a.TileFriction == 0 and a.TileElasticity == 0, "tile friction 0, elasticity 0")
		assert(a.TilePropertyWeight == 100, "tile property weights 100")
		assert(a.CollapseSinkTime == 0.65 and a.CollapseSinkDepth == 4, "sink 4 studs over 0.65 s")
		assert(a.CollapseSinkTime >= 0.5 and a.CollapseSinkTime <= 0.8, "sink time inside §11.4's 0.5-0.8 s")
	end,

	["round and queue values match §3.3 and §4.3"] = function()
		local r = GameConfig.Round
		assert(r.MinPlayers == 4 and r.MaxPlayers == 6 and r.HubCapacity == 12, "players")
		assert(r.FullCountdown == 8 and r.PartialWait == 25 and r.PartialCountdown == 10, "countdowns")
		assert(r.LoadoutLockBefore == 5 and r.PortalDwell == 1.0 and r.PortalExitGrace == 0.5, "lock and portal")
		assert(r.ResultsDuration == 8, "results 8 s")
		assert(GameConfig.Mode == "FreeForAll", "mode")
	end,

	["chassis are cosmetic with all multipliers 1.0 (D-008)"] = function()
		sameList(ChassisConfig.Ids, { "Rammer", "Trickster", "Magnetar", "Bulwark" }, "chassis ids")
		for _, id in ChassisConfig.Ids do
			local s = ChassisConfig.Stats[id]
			assert(s.OutgoingFactor == 1.0 and s.ResistanceFactor == 1.0, `{id} multipliers must be 1.0`)
		end
	end,

	["core abilities match §8.3"] = function()
		sameList(CoreConfig.Ids, { "Kinetic", "Cryo", "Magnetic" }, "core ids")
		local k, c, m = CoreConfig.Kinetic, CoreConfig.Cryo, CoreConfig.Magnetic
		assert(k.Cooldown == 8 and k.DeltaV == 22 and k.OutgoingFactor == 1.25 and k.OutgoingDuration == 1.0, "Kinetic")
		assert(c.Cooldown == 9 and c.DriftRemoval == 0.85 and c.HazardImmunityDuration == 2.5, "Cryo")
		near(c.ResistanceFactor, 1 / 1.5, "Cryo resistance")
		assert(c.ResistanceDuration == 2.0, "Cryo resistance duration")
		assert(m.Cooldown == 10 and m.Range == 24 and m.PullDeltaV == 16, "Magnetic")
	end,

	["cosmetic ids and unlocks match D-020 and D-021"] = function()
		local cos = GameConfig.Cosmetics
		sameList(cos.Skins, { "Default", "Neon", "Gold", "Void" }, "skins")
		sameList(cos.UnlockedSkins, { "Default", "Neon" }, "unlocked skins")
		sameList(cos.Trails, { "None", "CoreStreak", "CyanStreak" }, "trails")
		sameList(cos.Effects, { "StandardSpark", "CoreBurst" }, "effects")
	end,

	["palette matches §2.2"] = function()
		local c = GameConfig.Colors
		local expected: { [string]: { number } } = {
			TileDark = { 32, 38, 54 },
			TileLight = { 42, 50, 70 },
			PrimaryCyan = { 0, 195, 255 },
			Ice = { 0, 235, 255 },
			Magnetic = { 165, 55, 255 },
			Boost = { 255, 125, 0 },
			WarningAmber = { 255, 170, 0 },
			CollapseRed = { 255, 40, 40 },
			TextPrimary = { 245, 248, 255 },
			TextSecondary = { 170, 190, 215 },
		}
		local count = 0
		for name, rgb in expected do
			local col = (c :: any)[name] :: Color3 -- narrow boundary cast: lookup by name from the expected table
			count += 1
			assert(col == Color3.fromRGB(rgb[1], rgb[2], rgb[3]), `color {name}`)
		end
		local actual = 0
		for _ in c do
			actual += 1
		end
		assert(actual == count, `palette has {actual} colors, expected {count}`)
	end,

	["collision groups match the §6.2 matrix"] = function()
		local g = GameConfig.CollisionGroups
		local function joinPairs(list: { { string } }): string
			local out = {}
			for _, pair in list do
				table.insert(out, pair[1] .. "-" .. pair[2])
			end
			return table.concat(out, ",")
		end
		assert(
			joinPairs(g.Colliding) == "ArenaSphere-ArenaTile,ArenaSphere-ArenaSphere,LobbyAvatar-LobbyWorld",
			"Yes rows"
		)
		assert(
			joinPairs(g.NonColliding) == "ArenaSphere-LobbyAvatar,ArenaSphere-LobbyWorld,LobbyAvatar-ArenaTile",
			"No rows"
		)
		sameList(g.CollidesWithNothing, { "SphereVisual" }, "SphereVisual collides with no group")
	end,

	["lobby spawn faces the queue portal (D-015) and pods match D-023"] = function()
		local l = GameConfig.Lobby
		local spawn = l.SpawnCFrame
		assert(spawn.Position == Vector3.new(0, 150, -334), "spawn position")
		local toPortal = (l.QueuePortal - spawn.Position) * Vector3.new(1, 0, 1)
		assert(spawn.LookVector:Dot(toPortal.Unit) > 0.99, "spawn LookVector must face the portal")
		local p = l.Pods
		assert(p.Count == 6 and p.FloorSize == Vector3.new(10, 1, 10) and p.TopY == 200, "pods")
		assert(p.FirstX == 2000 and p.Spacing == 20 and p.Z == 2000 and p.CollisionGroup == "LobbyAvatar", "pods")
	end,

	["asset manifest holds no unverified ids (D-010)"] = function()
		local count = 0
		for key, value in AssetManifest.Ids do
			count += 1
			local verified = string.match(value, "^rbxassetid://%d+$") ~= nil
			assert(value == AssetManifest.PENDING or verified, `{key} has a malformed id`)
			-- No asset is imported and permission-verified yet; update this line when the first one is.
			assert(value == AssetManifest.PENDING, `{key} is set before verification`)
		end
		assert(count > 0, "manifest is empty")
	end,
}
