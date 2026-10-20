--!strict
-- Remote contract (Master Plan §10.3): each remote exists exactly once with the right class; no KnockbackEvent.
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local EXPECTED: { [string]: string } = {
	BoardPulseEvent = "RemoteEvent",
	MatchStateEvent = "RemoteEvent",
	QueueRequest = "RemoteEvent",
	QueueStateEvent = "RemoteEvent",
	LoadoutRequest = "RemoteEvent",
	LoadoutStateEvent = "RemoteEvent",
	AbilityRequest = "RemoteEvent",
	InputIntentRemote = "RemoteEvent", -- Path B only; never fired under Path A (D-024)
	CombatFXEvent = "UnreliableRemoteEvent",
	ResultEvent = "RemoteEvent",
}

-- Scope: the containers where game code places instances. Engine-managed services are not scanned.
local CONTAINERS = {
	"ReplicatedStorage",
	"ReplicatedFirst",
	"ServerScriptService",
	"ServerStorage",
	"Workspace",
	"StarterPlayer",
	"StarterGui",
	"StarterPack",
}

return {
	["Remotes folder holds exactly the 10 contract remotes"] = function()
		local folder = ReplicatedStorage:FindFirstChild("Remotes")
		assert(folder and folder:IsA("Folder"), "ReplicatedStorage.Remotes folder is missing")
		local seen: { [string]: number } = {}
		for _, child in folder:GetChildren() do
			local class = EXPECTED[child.Name]
			assert(class, `unexpected remote {child.Name}`)
			assert(child.ClassName == class, `{child.Name} is {child.ClassName}, expected {class}`)
			seen[child.Name] = (seen[child.Name] or 0) + 1
		end
		for name in EXPECTED do
			assert(seen[name] == 1, `{name} appears {seen[name] or 0} times`)
		end
	end,

	["no remotes outside the Remotes folder and no KnockbackEvent (game containers)"] = function()
		local remotes = ReplicatedStorage:FindFirstChild("Remotes")
		for _, service in CONTAINERS do
			for _, d in game:GetService(service):GetDescendants() do
				assert(d.Name ~= "KnockbackEvent", `KnockbackEvent found at {d:GetFullName()}`)
				if d:IsA("BaseRemoteEvent") or d:IsA("RemoteFunction") then
					assert(d.Parent == remotes, `stray remote {d:GetFullName()}`)
				end
			end
		end
	end,
}
