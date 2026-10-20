--!strict
-- Grid <-> world conversion for the 9x9 arena board (Master Plan §6.1, §6.5). Pure functions, no state.
-- Every number is read from GameConfig.Arena. The arena center is applied once, through Arena.CFrame;
-- never add Arena.CFrame.Position to a result. Cells off the board return nil, never a clamped cell.
local GameConfig = require(script.Parent.Parent.Config.GameConfig)

local Arena = GameConfig.Arena

local CoordinateUtils = {}

local function isFinite(n: number): boolean
	return math.abs(n) < math.huge -- false for NaN and for both infinities
end

-- True only for integer cells inside the board. NaN fails the integer test, infinities fail the radius test.
function CoordinateUtils.isOnBoard(x: number, z: number): boolean
	return x == math.floor(x)
		and z == math.floor(z)
		and math.abs(x) <= Arena.GridRadius
		and math.abs(z) <= Arena.GridRadius
end

-- Ring index: 0 at the center, GridRadius at the outer edge (§6.1).
function CoordinateUtils.ring(x: number, z: number): number?
	if not CoordinateUtils.isOnBoard(x, z) then
		return nil
	end
	return math.max(math.abs(x), math.abs(z))
end

-- World position of a cell center, localY studs above the arena plane (0 = tile center, Arena.SpawnLocalY = spawn).
function CoordinateUtils.gridToWorld(x: number, z: number, localY: number?): Vector3?
	if not CoordinateUtils.isOnBoard(x, z) then
		return nil
	end
	return Arena.CFrame:PointToWorldSpace(Vector3.new(Arena.Pitch * x, localY or 0, Arena.Pitch * z))
end

-- Cell under a world position, or nil, nil when that cell is off the board or an input is NaN or infinite.
-- Y is ignored on purpose: a falling sphere still maps to the cell directly above or below its (X, Z).
-- math.round rounds halves away from zero, so a position exactly on a cell edge always lands on the outer cell.
function CoordinateUtils.worldToGrid(position: Vector3): (number?, number?)
	if not (isFinite(position.X) and isFinite(position.Y) and isFinite(position.Z)) then
		return nil, nil
	end
	local p = Arena.CFrame:PointToObjectSpace(position)
	-- "+ 0" turns a negative zero into 0, so a cell key built from the result is never "-0".
	local x = math.round(p.X / Arena.Pitch) + 0
	local z = math.round(p.Z / Arena.Pitch) + 0
	if not CoordinateUtils.isOnBoard(x, z) then
		return nil, nil
	end
	return x, z
end

return CoordinateUtils
