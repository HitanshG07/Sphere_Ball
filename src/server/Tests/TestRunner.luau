--!strict
-- Minimal test runner (no framework). Runs every ModuleScript named "*.spec" below this folder.
-- A spec returns { [testName] = function() ... end }; a test fails when it errors (use assert/error).
-- Run in Studio (a Play session's Server is a fresh VM), for example through the Studio MCP execute_luau:
--   return require(game:GetService("ServerScriptService").Server.Tests.TestRunner).run()
-- `...any` only so pcall's result type has room for an error value; specs return nothing (§10.4 boundary).
export type Spec = { [string]: () -> ...any }

local TestRunner = {}

function TestRunner.run(): string
	local modules: { ModuleScript } = {}
	for _, d in script.Parent:GetDescendants() do
		if d:IsA("ModuleScript") and string.sub(d.Name, -5) == ".spec" then
			table.insert(modules, d)
		end
	end
	table.sort(modules, function(a, b)
		return a:GetFullName() < b:GetFullName()
	end)

	local passed, failures = 0, {}
	for _, m in modules do
		local ok, loaded = pcall(require, m)
		if not ok or type(loaded) ~= "table" then
			table.insert(failures, `{m.Name}: failed to load: {loaded}`)
			continue
		end
		local spec = loaded :: Spec
		local names = {}
		for name in spec do
			table.insert(names, name)
		end
		table.sort(names)
		for _, name in names do
			local okTest, err = pcall(spec[name])
			if okTest then
				passed += 1
			else
				table.insert(failures, `{m.Name} > {name}: {err}`)
			end
		end
	end

	-- An empty run is a failure, so a broken spec search never reads as a pass (RV-T01-09).
	if passed + #failures == 0 then
		table.insert(failures, "no tests found")
	end
	local report = `[TestRunner] {#modules} specs, {passed} passed, {#failures} failed`
	if #failures > 0 then
		report ..= "\n" .. table.concat(failures, "\n")
	end
	print(report)
	return report
end

return TestRunner
