--!strict
-- CoordinateUtils asserts against the spec numbers (Master Plan §6.1, §6.5, Task 01 item 6).
-- Expected values are written here on purpose: they are the spec, checked independently of the config.
-- Vector3 stores 32-bit floats, so positions are compared with a 1e-4 tolerance.
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local GameConfig = require(ReplicatedStorage.Shared.Config.GameConfig)
local CoordinateUtils = require(ReplicatedStorage.Shared.Modules.CoordinateUtils)

local TOLERANCE = 1e-4

local function nearVec(actual: Vector3?, expected: Vector3, what: string)
	assert(actual ~= nil, `{what}: expected {expected}, got nil`)
	assert((actual - expected).Magnitude < TOLERANCE, `{what}: expected {expected}, got {actual}`)
end

local function expectCell(position: Vector3, x: number, z: number, what: string)
	local gx, gz = CoordinateUtils.worldToGrid(position)
	assert(gx == x and gz == z, `{what}: expected cell ({x}, {z}), got ({gx}, {gz})`)
end

local function expectNoCell(position: Vector3, what: string)
	local gx, gz = CoordinateUtils.worldToGrid(position)
	assert(gx == nil and gz == nil, `{what}: expected nil, nil, got ({gx}, {gz})`)
end

-- Every on-board cell found by scanning past the edge, so isOnBoard does the filtering.
local function boardCells(): { { X: number, Z: number } }
	local cells = {}
	for x = -5, 5 do
		for z = -5, 5 do
			if CoordinateUtils.isOnBoard(x, z) then
				table.insert(cells, { X = x, Z = z })
			end
		end
	end
	return cells
end

return {
	["round trip returns the same cell for all 81 cells"] = function()
		local count = 0
		for x = -4, 4 do
			for z = -4, 4 do
				local world = CoordinateUtils.gridToWorld(x, z)
				assert(world ~= nil, `({x}, {z}) has no world position`)
				expectCell(world, x, z, `round trip ({x}, {z})`)
				count += 1
			end
		end
		assert(count == 81, `expected 81 cells, visited {count}`)
	end,

	["off-board input returns nil"] = function()
		assert(CoordinateUtils.gridToWorld(5, 0) == nil, "gridToWorld(5, 0)")
		assert(CoordinateUtils.gridToWorld(0, -5) == nil, "gridToWorld(0, -5)")
		assert(CoordinateUtils.gridToWorld(0.5, 0) == nil, "gridToWorld(0.5, 0)")
		assert(CoordinateUtils.gridToWorld(0 / 0, 0) == nil, "gridToWorld(NaN, 0)")
		assert(CoordinateUtils.gridToWorld(math.huge, 0) == nil, "gridToWorld(inf, 0)")
		expectNoCell(Vector3.new(54, 50, 0), "world x = 54 rounds to 5")
		expectNoCell(Vector3.new(-54, 50, 0), "world x = -54 rounds to -5")
		expectNoCell(Vector3.new(0, 50, 54), "world z = 54 rounds to 5")
		expectNoCell(Vector3.new(1000, 50, 0), "world x = 1000")
		expectNoCell(Vector3.new(0 / 0, 50, 0), "NaN position")
		expectNoCell(Vector3.new(math.huge, 50, 0), "infinite position")
		assert(CoordinateUtils.ring(5, 0) == nil, "ring(5, 0)")
		assert(CoordinateUtils.isOnBoard(4, -4), "isOnBoard(4, -4)")
	end,

	["the arena center is applied once"] = function()
		nearVec(CoordinateUtils.gridToWorld(0, 0), Vector3.new(0, 50, 0), "cell (0, 0)")
		nearVec(CoordinateUtils.gridToWorld(1, 0), Vector3.new(12, 50, 0), "cell (1, 0)")
		nearVec(CoordinateUtils.gridToWorld(0, 0, 1), Vector3.new(0, 51, 0), "cell (0, 0) at local Y 1")
	end,

	["rounding is deterministic at interior edges and Y is ignored"] = function()
		expectCell(Vector3.new(6, 50, 0), 1, 0, "world x = 6 (half rounds away from zero)")
		expectCell(Vector3.new(-6, 50, 0), -1, 0, "world x = -6")
		expectCell(Vector3.new(53.999, 50, 0), 4, 0, "world x = 53.999")
		expectCell(Vector3.new(5.999, 50, 0), 0, 0, "world x = 5.999")
		expectCell(Vector3.new(12, -500, -12), 1, -1, "a falling sphere keeps its cell")
		-- A negative zero would print as "-0" in a cell key such as `{x},{z}`.
		local gx, gz = CoordinateUtils.worldToGrid(Vector3.new(-5.999, 50, -5.999))
		assert(tostring(gx) == "0" and tostring(gz) == "0", `expected cell 0, 0 without a sign, got {gx}, {gz}`)
	end,

	["ring counts are 81, 32, 24, then 49 and 25 after the collapses"] = function()
		local cells = boardCells()
		local seen: { [string]: boolean } = {}
		local unique, ring4, ring3, afterRing4, afterRing3 = 0, 0, 0, 0, 0
		for _, c in cells do
			local key = `{c.X},{c.Z}`
			if not seen[key] then
				seen[key] = true
				unique += 1
			end
			local ring = CoordinateUtils.ring(c.X, c.Z)
			assert(ring ~= nil, `({c.X}, {c.Z}) is on the board but has no ring`)
			assert(ring == math.max(math.abs(c.X), math.abs(c.Z)), `ring of ({c.X}, {c.Z})`)
			if ring == 4 then
				ring4 += 1
			elseif ring == 3 then
				ring3 += 1
			end
			if ring < 4 then
				afterRing4 += 1
			end
			if ring < 3 then
				afterRing3 += 1
			end
		end
		assert(unique == 81 and #cells == 81, `expected 81 unique cells, got {unique} of {#cells}`)
		assert(ring4 == 32, `ring 4 should have 32 cells, got {ring4}`)
		assert(ring3 == 24, `ring 3 should have 24 cells, got {ring3}`)
		assert(afterRing4 == 49, `removing ring 4 should leave 49 cells, got {afterRing4}`)
		assert(afterRing3 == 25, `removing ring 3 should leave 25 cells, got {afterRing3}`)
	end,

	["spawn slots match §6.5"] = function()
		local slots = GameConfig.Arena.SpawnSlots
		local expected = {
			Vector3.new(0, 54.15, -36),
			Vector3.new(36, 54.15, -24),
			Vector3.new(36, 54.15, 24),
			Vector3.new(0, 54.15, 36),
			Vector3.new(-36, 54.15, 24),
			Vector3.new(-36, 54.15, -24),
		}
		assert(#slots == 6, `expected 6 spawn slots, got {#slots}`)
		local centers: { Vector3 } = {}
		for i, slot in slots do
			local world = CoordinateUtils.gridToWorld(slot.X, slot.Z, GameConfig.Arena.SpawnLocalY)
			assert(world ~= nil, `spawn slot {i} has no world position`)
			nearVec(world, expected[i], `spawn slot {i}`)
			assert(CoordinateUtils.ring(slot.X, slot.Z) == 3, `spawn slot {i} must be in ring 3`)
			table.insert(centers, world)
		end
		local minDistance = math.huge
		for i = 1, #centers - 1 do
			for j = i + 1, #centers do
				local d = (centers[i] - centers[j]).Magnitude
				assert(d >= 12, `spawn slots {i} and {j} are {d} studs apart, need at least 12`)
				minDistance = math.min(minDistance, d)
			end
		end
		assert(
			minDistance > 37.9 and minDistance < 38.0,
			`minimum slot distance should be about 37.95, got {minDistance}`
		)
	end,
}
