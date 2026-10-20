--!strict
-- Content IDs, kept apart from tuning values (TASK-01 item 7). Keys are the ids in assets/asset-manifest.json.
-- A value stays ASSET_PENDING until the asset is imported and permission-verified in this experience
-- (§11.1, D-010). Never put an invented or copied rbxassetid here; code must treat pending as "use the fallback".
local PENDING = "ASSET_PENDING"

return {
	PENDING = PENDING,
	Ids = {
		["sphere.shell.rammer"] = PENDING,
		["audio.hazard_warning"] = PENDING,
	} :: { [string]: string },
}
