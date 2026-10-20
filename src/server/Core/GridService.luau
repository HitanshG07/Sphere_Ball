--!strict
-- GridService (Master Plan §6.1-6.5, §10.5, TASK-02): the only source of tile Live/PendingCollapse/Destroyed
-- state and of ring collapse. Server module, functions only: no loops, Heartbeat or connections run between calls.
-- Each cell has exactly one authoritative 12x2x12 collider and one separate non-colliding visual tile (D-012).
-- Nothing builds the arena at server start: RoundManager (TASK-07) calls ResetArena, and owns the 3 s collapse
-- warning (§6.4); cells stay Live during that warning and CollapseRing is called at the collapse timestamp.
local PhysicsService = game:GetService("PhysicsService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")
local Workspace = game:GetService("Workspace")

local Types = require(ReplicatedStorage.Shared.Types)
local GameConfig = require(ReplicatedStorage.Shared.Config.GameConfig)
local CoordinateUtils = require(ReplicatedStorage.Shared.Modules.CoordinateUtils)

local Arena = GameConfig.Arena
local TILE_GROUP = GameConfig.CollisionGroups.ArenaTile
local ARENA_NAME = "Arena" -- Workspace.Arena is owned by this service: Collision/<key> and Visual/<key>

-- D-028: friction 0, elasticity 0, weights 100; density is the Plastic default (no effect on anchored tiles).
local TILE_PHYSICS = PhysicalProperties.new(
	PhysicalProperties.new(Enum.Material.Plastic).Density,
	Arena.TileFriction,
	Arena.TileElasticity,
	Arena.TilePropertyWeight,
	Arena.TilePropertyWeight
)
local SINK_INFO = TweenInfo.new(Arena.CollapseSinkTime, Enum.EasingStyle.Quad, Enum.EasingDirection.In)

type Cell = {
	X: number,
	Z: number,
	Ring: number,
	State: Types.CellState,
	Collider: Part?, -- present exactly while the cell is Live
	Visual: Part?, -- present until the cell is Destroyed
}

local cells: { [string]: Cell } = {}
local order: { Cell } = {} -- X ascending, then Z ascending
local arenaFolder: Folder? = nil
local nextCollapse = 1 -- index into Arena.CollapseRings
local generation = 0 -- bumped by ResetArena; delayed callbacks from an older generation do nothing
local pendingThreads: { thread } = {}
local sinkTweens: { Tween } = {}

-- "+ 0" turns a negative zero into 0, so a key is never "-0".
local function cellKey(x: number, z: number): string
	return `{x + 0},{z + 0}`
end

local function find(x: number, z: number): Cell?
	if not CoordinateUtils.isOnBoard(x, z) then
		return nil
	end
	return cells[cellKey(x, z)]
end

local function copy(cell: Cell): Types.GridCell
	return { X = cell.X, Z = cell.Z, Ring = cell.Ring, State = cell.State }
end

local function newPart(name: string, size: Vector3, cframe: CFrame, parent: Instance): Part
	local part = Instance.new("Part")
	part.Name = name
	part.Anchored = true
	part.Size = size
	part.CFrame = cframe
	part.Parent = parent
	return part
end

local GridService = {}

-- Cancels pending collapse work, then rebuilds all 81 cells as Live with the collapse step back at the first ring.
function GridService.ResetArena()
	generation += 1
	for _, thread in pendingThreads do
		pcall(task.cancel, thread) -- a thread that already finished cannot throw here
	end
	for _, tween in sinkTweens do
		tween:Cancel()
	end
	table.clear(pendingThreads)
	table.clear(sinkTweens)
	for _, child in Workspace:GetChildren() do
		if child.Name == ARENA_NAME then
			child:Destroy()
		end
	end
	table.clear(cells)
	table.clear(order)
	nextCollapse = 1

	if not PhysicsService:IsCollisionGroupRegistered(TILE_GROUP) then
		PhysicsService:RegisterCollisionGroup(TILE_GROUP)
	end

	-- Built off the DataModel, then parented once.
	local folder = Instance.new("Folder")
	folder.Name = ARENA_NAME
	local collision = Instance.new("Folder")
	collision.Name = "Collision"
	collision.Parent = folder
	local visual = Instance.new("Folder")
	visual.Name = "Visual"
	visual.Parent = folder

	for x = -Arena.GridRadius, Arena.GridRadius do
		for z = -Arena.GridRadius, Arena.GridRadius do
			local key = cellKey(x, z)
			local center = CoordinateUtils.gridToWorld(x, z) :: Vector3 -- on-board by construction
			local cframe = CFrame.new(center) * Arena.CFrame.Rotation

			local collider = newPart(key, Arena.CollisionTileSize, cframe, collision)
			collider.CanCollide = true
			collider.Transparency = 1
			collider.CollisionGroup = TILE_GROUP
			collider.CustomPhysicalProperties = TILE_PHYSICS

			local tile = newPart(key, Arena.VisualTileSize, cframe, visual)
			tile.CanCollide = false
			tile.CanTouch = false
			tile.Material = Enum.Material.SmoothPlastic
			tile.Color = if (x + z) % 2 == 0 then GameConfig.Colors.TileDark else GameConfig.Colors.TileLight

			local cell: Cell = {
				X = x,
				Z = z,
				Ring = CoordinateUtils.ring(x, z) :: number,
				State = "Live",
				Collider = collider,
				Visual = tile,
			}
			cells[key] = cell
			table.insert(order, cell)
		end
	end

	folder.Parent = Workspace
	arenaFolder = folder
end

-- Collapses the next ring of Arena.CollapseRings (4, then 3). Anything else is rejected and changes nothing.
function GridService.CollapseRing(ring: number): boolean
	local expected = Arena.CollapseRings[nextCollapse]
	if arenaFolder == nil or expected == nil or ring ~= expected then
		warn(`[GridService] CollapseRing({ring}) rejected: next ring is {expected}, arena built: {arenaFolder ~= nil}`)
		return false
	end
	nextCollapse += 1

	local collapsing: { Cell } = {}
	for _, cell in order do
		if cell.Ring == ring then
			cell.State = "PendingCollapse" -- leaves the live index here, exactly once
			-- Collider first (TASK-02 item 6): no collidable tile ever moves through a sphere.
			local collider = cell.Collider :: Part
			collider:Destroy()
			cell.Collider = nil
			-- ponytail: the server tween replicates 32 parts x 0.65 s; move it client-side in TASK-09 if network
			-- cost matters.
			local tile = cell.Visual :: Part
			local tween = TweenService:Create(tile, SINK_INFO, {
				CFrame = tile.CFrame * CFrame.new(0, -Arena.CollapseSinkDepth, 0),
				Transparency = 1,
			})
			tween:Play()
			table.insert(sinkTweens, tween)
			table.insert(collapsing, cell)
		end
	end

	local scheduledIn = generation
	local thread: thread
	thread = task.delay(Arena.CollapseSinkTime, function()
		local index = table.find(pendingThreads, thread)
		if index then
			table.remove(pendingThreads, index)
		end
		if generation ~= scheduledIn then
			return -- ResetArena ran since this collapse; its cells no longer exist
		end
		for _, cell in collapsing do
			cell.State = "Destroyed"
			local tile = cell.Visual :: Part
			tile:Destroy()
			cell.Visual = nil
		end
	end)
	table.insert(pendingThreads, thread)
	return true
end

-- Copies of the Live cells, ordered by X ascending, then Z ascending.
function GridService.GetLiveCells(): { Types.GridCell }
	local live = {}
	for _, cell in order do
		if cell.State == "Live" then
			table.insert(live, copy(cell))
		end
	end
	return live
end

-- A copy of the cell, or nil when it is off the board, not an integer cell, NaN, or the arena is not built.
function GridService.GetCell(x: number, z: number): Types.GridCell?
	local cell = find(x, z)
	return if cell then copy(cell) else nil
end

function GridService.IsLive(x: number, z: number): boolean
	local cell = find(x, z)
	return cell ~= nil and cell.State == "Live"
end

return GridService
