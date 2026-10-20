--!strict
-- GridService asserts against the spec numbers (TASK-02 card, Master Plan §6.1-6.5, §13.2 items 2-3, D-005, D-012,
-- D-016, D-028). Expected values are written here on purpose: they are the spec, checked independently of the config.
-- Every test starts with ResetArena(), so the alphabetical run order does not matter. Run only on a Play server:
-- the tests build Workspace.Arena and the collapse and physics tests yield.
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerScriptService = game:GetService("ServerScriptService")
local Workspace = game:GetService("Workspace")

local GameConfig = require(ReplicatedStorage.Shared.Config.GameConfig)
local CoordinateUtils = require(ReplicatedStorage.Shared.Modules.CoordinateUtils)
local Types = require(ReplicatedStorage.Shared.Types)
local GridService = require(ServerScriptService.Server.Core.GridService)

local TOLERANCE = 1e-4 -- Vector3 stores 32-bit floats
local SINK_WAIT = GameConfig.Arena.CollapseSinkTime + 0.3
local TEMP_NAME = "GridSpecTemp"

local function nearVec(actual: Vector3, expected: Vector3, what: string)
	assert((actual - expected).Magnitude < TOLERANCE, `{what}: expected {expected}, got {actual}`)
end

local function arena(): (Folder, Folder)
	local folder = Workspace:FindFirstChild("Arena")
	assert(folder and folder:IsA("Folder"), "Workspace.Arena folder is missing")
	local collision = folder:FindFirstChild("Collision")
	local visual = folder:FindFirstChild("Visual")
	assert(collision and collision:IsA("Folder"), "Arena.Collision folder is missing")
	assert(visual and visual:IsA("Folder"), "Arena.Visual folder is missing")
	return collision, visual
end

local function part(parent: Instance, key: string): Part
	local p = parent:FindFirstChild(key)
	assert(p and p:IsA("Part"), `{parent.Name}/{key} is missing`)
	return p
end

local function allCells(): { Types.GridCell }
	local out = {}
	for x = -4, 4 do
		for z = -4, 4 do
			local cell = GridService.GetCell(x, z)
			assert(cell ~= nil, `GetCell({x}, {z}) returned nil on a built arena`)
			table.insert(out, cell)
		end
	end
	return out
end

-- Checks the state counts, that the colliders are exactly the Live cells (one each), and the visual count.
local function expectBoard(live: number, pending: number, destroyed: number, visuals: number, what: string)
	local collision, visual = arena()
	local counts = { Live = 0, PendingCollapse = 0, Destroyed = 0 }
	for _, cell in allCells() do
		counts[cell.State] += 1
		local hasCollider = collision:FindFirstChild(`{cell.X},{cell.Z}`) ~= nil
		assert(
			hasCollider == (cell.State == "Live"),
			`{what}: cell {cell.X},{cell.Z} is {cell.State}, collider {hasCollider}`
		)
	end
	local got = `{counts.Live}/{counts.PendingCollapse}/{counts.Destroyed}`
	assert(
		got == `{live}/{pending}/{destroyed}`,
		`{what}: expected Live/Pending/Destroyed {live}/{pending}/{destroyed}, got {got}`
	)
	assert(#collision:GetChildren() == live, `{what}: expected {live} colliders, got {#collision:GetChildren()}`)
	assert(#GridService.GetLiveCells() == live, `{what}: GetLiveCells returned {#GridService.GetLiveCells()}`)
	assert(#visual:GetChildren() == visuals, `{what}: expected {visuals} visuals, got {#visual:GetChildren()}`)
end

-- Runs check while the temporary parts exist; always destroys them, then re-raises any failure.
-- `...any` only so pcall's result type has room for an error value (as in TestRunner).
local function withParts(parts: { Part }, check: () -> ...any)
	for _, p in parts do
		p.Name = TEMP_NAME
		p.Parent = Workspace
	end
	local ok, err = pcall(check)
	for _, p in parts do
		p:Destroy()
	end
	if not ok then
		error(err, 0)
	end
end

local function withTempPart(canCollide: boolean, check: () -> ...any)
	local p = Instance.new("Part")
	p.Anchored, p.CanCollide, p.Size = true, canCollide, Vector3.new(4, 1, 4)
	p.CFrame = CFrame.new(CoordinateUtils.gridToWorld(0, 0) :: Vector3) -- inside tile (0, 0): a stacked collider
	withParts({ p }, check)
end

-- Every collidable part in the board volume; visual tiles are excluded by RespectCanCollide itself.
local function boardQuery(): { BasePart }
	local params = OverlapParams.new()
	params.RespectCanCollide = true
	-- The explicit config CFrame (0, 50, 0): Workspace.Arena is a Folder and has no CFrame.
	-- 107.9 x 1.9 x 107.9 lies inside the 108 x 2 x 108 board, so it touches all 81 colliders and nothing outside.
	return Workspace:GetPartBoundsInBox(GameConfig.Arena.CFrame, Vector3.new(107.9, 1.9, 107.9), params)
end

local function ball(at: Vector3): Part
	local p = Instance.new("Part")
	p.Shape = Enum.PartType.Ball
	p.Size = Vector3.one * 6 -- sphere diameter 6 (§6.3)
	p.Position = at
	return p
end

return {
	["01 counts and IDs: 81 unique cells, one collider and one visual each, no scripts"] = function()
		GridService.ResetArena()
		local collision, visual = arena()
		local seen: { [string]: boolean } = {}
		for _, cell in GridService.GetLiveCells() do
			local key = `{cell.X},{cell.Z}`
			assert(string.match(key, "^-?%d,-?%d$") ~= nil, `key {key} has the wrong format`)
			assert(not seen[key], `duplicate cell {key}`)
			seen[key] = true
			assert(cell.State == "Live", `{key} is {cell.State}`)
			part(collision, key)
			part(visual, key)
		end
		local count = 0
		for _ in seen do
			count += 1
		end
		assert(count == 81, `expected 81 unique cells, got {count}`)
		for _, folder in { collision, visual } do
			local names: { [string]: boolean } = {}
			for _, child in folder:GetChildren() do
				assert(not names[child.Name], `duplicate part name {folder.Name}/{child.Name}`)
				names[child.Name] = true
			end
			assert(#folder:GetChildren() == 81, `{folder.Name} has {#folder:GetChildren()} parts`)
		end
		for _, d in (collision.Parent :: Instance):GetDescendants() do
			assert(not d:IsA("LuaSourceContainer"), `script under Arena: {d:GetFullName()}`)
		end
	end,

	["02 collider geometry and D-028 physics"] = function()
		GridService.ResetArena()
		local collision = arena()
		for _, cell in GridService.GetLiveCells() do
			local key = `{cell.X},{cell.Z}`
			local c = part(collision, key)
			assert(c.Size == Vector3.new(12, 2, 12), `{key} size {c.Size}`)
			assert(c.Anchored and c.CanCollide and c.Transparency == 1, `{key} must be anchored, collidable, invisible`)
			assert(c.CollisionGroup == "ArenaTile", `{key} group {c.CollisionGroup}`)
			local pp = c.CustomPhysicalProperties :: PhysicalProperties? -- nil at runtime when not set
			assert(pp, `{key} has no CustomPhysicalProperties`)
			assert(pp.Friction == 0 and pp.Elasticity == 0, `{key} friction {pp.Friction}, elasticity {pp.Elasticity}`)
			assert(pp.FrictionWeight == 100 and pp.ElasticityWeight == 100, `{key} property weights`)
			nearVec(c.Position, CoordinateUtils.gridToWorld(cell.X, cell.Z) :: Vector3, `{key} center`)
			nearVec(c.Position, Vector3.new(12 * cell.X, 50, 12 * cell.Z), `{key} world center`)
			assert(math.abs(c.Position.Y + c.Size.Y / 2 - 51) < TOLERANCE, `{key} top surface is not Y 51`)
		end
	end,

	["03 visual geometry: inset, non-colliding, checkerboard"] = function()
		GridService.ResetArena()
		local collision, visual = arena()
		for _, cell in GridService.GetLiveCells() do
			local key = `{cell.X},{cell.Z}`
			local v = part(visual, key)
			assert(v.Size == Vector3.new(11.8, 2, 11.8), `{key} visual size {v.Size}`)
			assert(
				v.Anchored and not v.CanCollide and not v.CanTouch,
				`{key} visual must be anchored, CanCollide and CanTouch false`
			)
			nearVec(v.Position, part(collision, key).Position, `{key} visual center`)
			local expected = if (cell.X + cell.Z) % 2 == 0
				then Color3.fromRGB(32, 38, 54)
				else Color3.fromRGB(42, 50, 70)
			assert(v.Color:ToHex() == expected:ToHex(), `{key} color {v.Color:ToHex()}`)
		end
	end,

	["04 edge to edge with no stacked colliders (query and negative controls)"] = function()
		GridService.ResetArena()
		local collision, visual = arena()
		for x = -4, 4 do
			for z = -4, 4 do
				local here = part(collision, `{x},{z}`).Position
				if x < 4 then
					local d = part(collision, `{x + 1},{z}`).Position - here
					assert(
						math.abs(d.X - 12) < TOLERANCE and math.abs(d.Y) < TOLERANCE and math.abs(d.Z) < TOLERANCE,
						`+X neighbour of {x},{z}: {d}`
					)
				end
				if z < 4 then
					local d = part(collision, `{x},{z + 1}`).Position - here
					assert(
						math.abs(d.Z - 12) < TOLERANCE and math.abs(d.Y) < TOLERANCE and math.abs(d.X) < TOLERANCE,
						`+Z neighbour of {x},{z}: {d}`
					)
				end
			end
		end
		assert(81 * 12 * 12 == 108 * 108, "81 tiles of 12 x 12 cover the 108 x 108 board exactly")

		local function expectHits(n: number, what: string): { BasePart }
			local hits = boardQuery()
			assert(#hits == n, `{what}: expected {n} collidable hits, got {#hits}`)
			return hits
		end

		-- Baseline: exactly the 81 colliders.
		local names: { [string]: boolean } = {}
		for _, hit in expectHits(81, "baseline") do
			assert(hit.CanCollide and hit.Parent == collision, `foreign or visual hit {hit:GetFullName()}`)
			assert(not hit:IsDescendantOf(visual), `visual tile in collider query: {hit:GetFullName()}`)
			names[hit.Name] = true
		end
		for x = -4, 4 do
			for z = -4, 4 do
				assert(names[`{x},{z}`], `collider {x},{z} not returned by the query`)
			end
		end

		-- Negative controls, each asserted while its temporary part is present.
		withTempPart(true, function()
			expectHits(82, "with a colliding part stacked in tile 0,0")
		end)
		assert(Workspace:FindFirstChild(TEMP_NAME) == nil, "colliding temporary part was not cleaned up")
		withTempPart(false, function()
			expectHits(81, "with a non-colliding part in tile 0,0")
		end)
		expectHits(81, "after both controls")
		assert(Workspace:FindFirstChild(TEMP_NAME) == nil, "a temporary part remains in Workspace")
	end,

	["05 ring 4 has 32 cells and ring 3 has 24"] = function()
		GridService.ResetArena()
		local byRing: { [number]: number } = {}
		for _, cell in GridService.GetLiveCells() do
			assert(cell.Ring == math.max(math.abs(cell.X), math.abs(cell.Z)), `ring of {cell.X},{cell.Z}`)
			byRing[cell.Ring] = (byRing[cell.Ring] or 0) + 1
		end
		assert(byRing[4] == 32, `ring 4 has {byRing[4]} cells`)
		assert(byRing[3] == 24, `ring 3 has {byRing[3]} cells`)
	end,

	["06 collapse sequence 81 -> 49 -> 25, collider removed first"] = function()
		GridService.ResetArena()
		assert(GridService.CollapseRing(3) == false, "ring 3 before ring 4 must be rejected")
		expectBoard(81, 0, 0, 81, "after rejected ring 3")

		assert(GridService.CollapseRing(4) == true, "CollapseRing(4) failed")
		expectBoard(49, 32, 0, 81, "right after CollapseRing(4)") -- colliders gone, visuals still sinking
		assert(not GridService.IsLive(4, 0), "IsLive(4, 0) after the ring-4 collapse")
		for _, cell in GridService.GetLiveCells() do
			assert(cell.Ring < 4, `GetLiveCells returned ring-4 cell {cell.X},{cell.Z}`)
		end
		assert(GridService.CollapseRing(4) == false, "a repeated CollapseRing(4) must be rejected")
		expectBoard(49, 32, 0, 81, "after repeated ring 4")

		task.wait(SINK_WAIT)
		expectBoard(49, 0, 32, 49, "after the ring-4 sink")

		assert(GridService.CollapseRing(3) == true, "CollapseRing(3) failed")
		expectBoard(25, 24, 32, 49, "right after CollapseRing(3)")
		task.wait(SINK_WAIT)
		expectBoard(25, 0, 56, 25, "after the ring-3 sink")
		for _, ring in { 4, 3, 2, 1 } do
			assert(
				GridService.CollapseRing(ring) == false,
				`CollapseRing({ring}) after both collapses must be rejected`
			)
		end
		expectBoard(25, 0, 56, 25, "after further calls")
	end,

	["07 invalid inputs are rejected without change"] = function()
		GridService.ResetArena()
		for _, v in { 0, 2, 5, 2.5, 0 / 0, -4, math.huge, -math.huge } do
			assert(GridService.CollapseRing(v) == false, `CollapseRing({v}) must be rejected`)
		end
		expectBoard(81, 0, 0, 81, "after invalid CollapseRing calls")
		for _, xz in { { 5, 0 }, { 0.5, 0 }, { 0 / 0, 0 }, { math.huge, 0 }, { 0, -5 } } do
			assert(GridService.GetCell(xz[1], xz[2]) == nil, `GetCell({xz[1]}, {xz[2]}) must be nil`)
			assert(GridService.IsLive(xz[1], xz[2]) == false, `IsLive({xz[1]}, {xz[2]}) must be false`)
		end
		local negZero = GridService.GetCell(-0, 0)
		assert(negZero ~= nil and negZero.X == 0, "GetCell(-0, 0) must return cell 0,0")
	end,

	["08 reset twice after both collapses restores 81 cells with the same order"] = function()
		GridService.ResetArena()
		local function orderKeys(): string
			local keys = {}
			for _, cell in GridService.GetLiveCells() do
				table.insert(keys, `{cell.X},{cell.Z}`)
			end
			return table.concat(keys, ";")
		end
		local first = orderKeys()
		local prevX, prevZ = -math.huge, -math.huge
		for _, cell in GridService.GetLiveCells() do
			assert(cell.X > prevX or (cell.X == prevX and cell.Z > prevZ), "GetLiveCells is not ordered by X, then Z")
			prevX, prevZ = cell.X, cell.Z
		end
		for round = 1, 2 do
			assert(GridService.CollapseRing(4) and GridService.CollapseRing(3), `round {round}: collapses failed`)
			GridService.ResetArena()
			expectBoard(81, 0, 0, 81, `after reset {round}`)
			local arenas = 0
			for _, child in Workspace:GetChildren() do
				if child.Name == "Arena" then
					arenas += 1
				end
			end
			assert(arenas == 1, `reset {round}: {arenas} Arena folders`)
			local collision, visual = arena()
			for _, folder in { collision, visual } do
				local names: { [string]: boolean } = {}
				for _, child in folder:GetChildren() do
					assert(not names[child.Name], `reset {round}: duplicate {folder.Name}/{child.Name}`)
					names[child.Name] = true
				end
			end
			assert(orderKeys() == first, `reset {round}: GetLiveCells order changed`)
		end
	end,

	["09 reset during a collapse cancels the pending sink"] = function()
		local function expectIntact(what: string)
			expectBoard(81, 0, 0, 81, what)
			local collision, visual = arena()
			for _, cell in allCells() do
				local key = `{cell.X},{cell.Z}`
				local center = CoordinateUtils.gridToWorld(cell.X, cell.Z) :: Vector3
				nearVec(part(collision, key).Position, center, `{what}: collider {key}`)
				local v = part(visual, key)
				nearVec(v.Position, center, `{what}: visual {key}`)
				assert(v.Transparency == 0, `{what}: visual {key} transparency {v.Transparency}`)
			end
		end

		GridService.ResetArena()
		assert(GridService.CollapseRing(4), "CollapseRing(4) failed")
		GridService.ResetArena()
		task.wait(SINK_WAIT)
		expectIntact("one reset mid-sink")

		-- Two quick resets in a row, with a collapse from the newer generation also pending.
		assert(GridService.CollapseRing(4), "CollapseRing(4) failed (second pass)")
		GridService.ResetArena()
		assert(GridService.CollapseRing(4), "CollapseRing(4) failed (third pass)")
		GridService.ResetArena()
		GridService.ResetArena()
		task.wait(SINK_WAIT)
		expectIntact("two quick resets mid-sink")
	end,

	["10 returned cells are copies"] = function()
		GridService.ResetArena()
		local cell = GridService.GetCell(0, 0) :: Types.GridCell
		cell.State = "Destroyed"
		cell.X = 99
		local live = GridService.GetLiveCells()
		live[1].State = "PendingCollapse"
		table.clear(live)
		assert(GridService.IsLive(0, 0), "mutating a GetCell result changed the service")
		local again = GridService.GetCell(0, 0) :: Types.GridCell
		assert(again.X == 0 and again.State == "Live", "GetCell(0, 0) changed")
		assert(#GridService.GetLiveCells() == 81, "mutating the GetLiveCells result changed the service")
		assert(GridService.GetLiveCells()[1].State == "Live", "first live cell changed")
	end,

	["11 the six spawn slots are live and each sphere fits inside its tile (D-016)"] = function()
		GridService.ResetArena()
		local collision = arena()
		assert(#GameConfig.Arena.SpawnSlots == 6, "six spawn slots")
		for i, slot in GameConfig.Arena.SpawnSlots do
			assert(GridService.IsLive(slot.X, slot.Z), `spawn slot {i} cell {slot.X},{slot.Z} is not live`)
			local tile = part(collision, `{slot.X},{slot.Z}`)
			local spawn = CoordinateUtils.gridToWorld(slot.X, slot.Z, GameConfig.Arena.SpawnLocalY) :: Vector3
			local offset = spawn - tile.Position
			local radius = 3
			assert(
				math.max(math.abs(offset.X), math.abs(offset.Z)) + radius <= tile.Size.X / 2,
				`slot {i} footprint leaves the tile`
			)
			assert(spawn.Y - radius >= tile.Position.Y + tile.Size.Y / 2, `slot {i} sphere starts inside the tile`)
		end
	end,

	["12 physics: balls rest on a center, a seam and a corner, and fall through a collapsed cell"] = function()
		GridService.ResetArena()
		local y = GameConfig.Arena.CFrame.Y + GameConfig.Arena.SpawnLocalY -- 54.15
		local drops = {
			{ name = "cell center", ball = ball(Vector3.new(0, y, 0)) },
			{ name = "seam x = 6", ball = ball(Vector3.new(6, y, 0)) },
			{ name = "4-cell corner (6, 6)", ball = ball(Vector3.new(6, y, 6)) },
		}
		local parts = {}
		for _, d in drops do
			table.insert(parts, d.ball)
		end
		withParts(parts, function()
			task.wait(1.5)
			for _, d in drops do
				local p = d.ball.Position
				assert(math.abs(p.Y - 54) <= 0.1, `{d.name}: ball rests at Y {p.Y}, expected 54 +- 0.1`)
			end
		end)

		assert(GridService.CollapseRing(4), "CollapseRing(4) failed")
		local falling = ball(CoordinateUtils.gridToWorld(4, 0, GameConfig.Arena.SpawnLocalY) :: Vector3)
		withParts({ falling }, function()
			task.wait(1.5)
			local fy = falling.Position.Y
			assert(fy < GameConfig.Arena.VoidY, `ball over collapsed cell 4,0 is at Y {fy}, expected below 15`)
		end)
	end,
}
