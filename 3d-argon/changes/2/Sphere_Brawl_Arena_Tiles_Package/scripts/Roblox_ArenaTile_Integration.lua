--!strict
--[[
    SPHERE BRAWL: ROLLING RAMPAGE — OPTIONAL ARENA TILE MATERIAL & VALIDATION HELPER (LUAU)
    =======================================================================================
    STATUS & SCOPE NOTICE:
      - OPTIONAL REFERENCE / ILLUSTRATIVE EXAMPLE ONLY — NOT PRODUCTION-READY GAMEPLAY INTEGRATION.
      - NOT EXECUTED OR TESTED IN ROBLOX STUDIO (authored in a headless Linux sandbox without
        a live Roblox Studio runtime).
      - Do NOT allow visual tile helpers to replace, resize, or mutate the authoritative
        12.0 x 2.0 x 12.0-stud gameplay collider owned by gameplay code.
]]

local ArenaTileReference = {}

ArenaTileReference.IS_OPTIONAL_EXAMPLE_ONLY = true
ArenaTileReference.TESTED_IN_ROBLOX_STUDIO = false

ArenaTileReference.GRID_PITCH_STUDS = 12.0
ArenaTileReference.EXPECTED_VISUAL_SIZE_STUDS = Vector3.new(11.8, 2.0, 11.8)
ArenaTileReference.AUTHORITATIVE_COLLIDER_SIZE_STUDS = Vector3.new(12.0, 2.0, 12.0)
ArenaTileReference.NEIGHBOR_VISUAL_GAP_STUDS = 0.2
ArenaTileReference.STANDARD_CENTER_Y = 50.0
ArenaTileReference.STANDARD_TOP_SURFACE_Y = 51.0
ArenaTileReference.DIMENSION_TOLERANCE_STUDS = 0.02

ArenaTileReference.Palette = {
    MAT_DarkNeutral = {
        ChildPartName = "Part_MAT_DarkNeutral",
        Hex = "#202636",
        RGB = { 32, 38, 54 },
        Color = Color3.fromRGB(32, 38, 54),
        Material = Enum.Material.Metal,
        Reflectance = 0.05,
        Emissive = false,
    },
    MAT_AltNeutral = {
        ChildPartName = "Part_MAT_AltNeutral",
        Hex = "#2A3246",
        RGB = { 42, 50, 70 },
        Color = Color3.fromRGB(42, 50, 70),
        Material = Enum.Material.Metal,
        Reflectance = 0.05,
        Emissive = false,
    },
    MAT_LightTrim = {
        ChildPartName = "Part_MAT_LightTrim",
        Hex = "#AABED7",
        RGB = { 170, 190, 215 },
        Color = Color3.fromRGB(170, 190, 215),
        Material = Enum.Material.Metal,
        Reflectance = 0.12,
        Emissive = false,
    },
    EMI_Cyan = {
        ChildPartName = "Part_EMI_Cyan",
        Hex = "#00C3FF",
        RGB = { 0, 195, 255 },
        Color = Color3.fromRGB(0, 195, 255),
        Material = Enum.Material.Neon,
        Reflectance = 0.0,
        Emissive = true,
    },
    EMI_Amber = {
        ChildPartName = "Part_EMI_Amber",
        Hex = "#FFAA00",
        RGB = { 255, 170, 0 },
        Color = Color3.fromRGB(255, 170, 0),
        Material = Enum.Material.Neon,
        Reflectance = 0.0,
        Emissive = true,
    },
    EMI_Ice = {
        ChildPartName = "Part_EMI_Ice",
        Hex = "#00EBFF",
        RGB = { 0, 235, 255 },
        Color = Color3.fromRGB(0, 235, 255),
        Material = Enum.Material.Neon,
        Reflectance = 0.0,
        Emissive = true,
    },
    EMI_Magnetic = {
        ChildPartName = "Part_EMI_Magnetic",
        Hex = "#A537FF",
        RGB = { 165, 55, 255 },
        Color = Color3.fromRGB(165, 55, 255),
        Material = Enum.Material.Neon,
        Reflectance = 0.0,
        Emissive = true,
    },
    EMI_Kinetic = {
        ChildPartName = "Part_EMI_Kinetic",
        Hex = "#FF7D00",
        RGB = { 255, 125, 0 },
        Color = Color3.fromRGB(255, 125, 0),
        Material = Enum.Material.Neon,
        Reflectance = 0.0,
        Emissive = true,
    },
    EMI_DangerRed = {
        ChildPartName = "Part_EMI_DangerRed",
        Hex = "#FF2828",
        RGB = { 255, 40, 40 },
        Color = Color3.fromRGB(255, 40, 40),
        Material = Enum.Material.Neon,
        Reflectance = 0.0,
        Emissive = true,
    },
}

ArenaTileReference.States = {
    SafeNormal = {
        Id = 1,
        StateName = "Safe / Normal",
        CompleteMeshName = "SM_ArenaTile_01_SafeNormal",
        OverlayMeshName  = "SM_ArenaTile_Overlay_01_SafeNormal",
        PrimaryEmissive  = "EMI_Cyan",
        BaseTris         = 84,
        OverlayTris      = 130,
        TriangleCount    = 214,
        ExpectedCompleteSize = Vector3.new(11.8, 2.0, 11.8),
        ExpectedOverlaySize  = Vector3.new(9.10, 0.13, 9.10),
    },
    Warning = {
        Id = 2,
        StateName = "Warning",
        CompleteMeshName = "SM_ArenaTile_02_Warning",
        OverlayMeshName  = "SM_ArenaTile_Overlay_02_Warning",
        PrimaryEmissive  = "EMI_Amber",
        BaseTris         = 84,
        OverlayTris      = 140,
        TriangleCount    = 224,
        ExpectedCompleteSize = Vector3.new(11.8, 2.0, 11.8),
        ExpectedOverlaySize  = Vector3.new(9.30, 0.14, 9.30),
    },
    IceCorridor = {
        Id = 3,
        StateName = "Ice Corridor — active",
        CompleteMeshName = "SM_ArenaTile_03_IceCorridor",
        OverlayMeshName  = "SM_ArenaTile_Overlay_03_IceCorridor",
        PrimaryEmissive  = "EMI_Ice",
        BaseTris         = 84,
        OverlayTris      = 130,
        TriangleCount    = 214,
        ExpectedCompleteSize = Vector3.new(11.8, 2.0, 11.8),
        ExpectedOverlaySize  = Vector3.new(7.24, 0.13, 9.60),
    },
    MagneticStorm = {
        Id = 4,
        StateName = "Magnetic Storm — active",
        CompleteMeshName = "SM_ArenaTile_04_MagneticStorm",
        OverlayMeshName  = "SM_ArenaTile_Overlay_04_MagneticStorm",
        PrimaryEmissive  = "EMI_Magnetic",
        BaseTris         = 84,
        OverlayTris      = 146,
        TriangleCount    = 230,
        ExpectedCompleteSize = Vector3.new(11.8, 2.0, 11.8),
        ExpectedOverlaySize  = Vector3.new(9.10, 0.13, 9.10),
    },
    BoostRunway = {
        Id = 5,
        StateName = "Boost Runway — active",
        CompleteMeshName = "SM_ArenaTile_05_BoostRunway",
        OverlayMeshName  = "SM_ArenaTile_Overlay_05_BoostRunway",
        PrimaryEmissive  = "EMI_Kinetic",
        BaseTris         = 84,
        OverlayTris      = 128,
        TriangleCount    = 212,
        ExpectedCompleteSize = Vector3.new(11.8, 2.0, 11.8),
        ExpectedOverlaySize  = Vector3.new(8.90, 0.14, 8.90),
    },
    RingCollapse = {
        Id = 6,
        StateName = "Ring Collapse — warning",
        CompleteMeshName = "SM_ArenaTile_06_RingCollapse",
        OverlayMeshName  = "SM_ArenaTile_Overlay_06_RingCollapse",
        PrimaryEmissive  = "EMI_DangerRed",
        BaseTris         = 84,
        OverlayTris      = 150,
        TriangleCount    = 234,
        ExpectedCompleteSize = Vector3.new(11.8, 2.0, 11.8),
        ExpectedOverlaySize  = Vector3.new(11.20, 0.14, 11.20),
    },
}

function ArenaTileReference.ApplyApprovedMaterialsToImportedModel(tileInstance: Instance, clearTextureId: boolean?): number
    local stripTex = if clearTextureId == nil then true else clearTextureId
    local matchedCount = 0

    for _, desc in ipairs(tileInstance:GetDescendants()) do
        if desc:IsA("BasePart") then
            for matKey, spec in pairs(ArenaTileReference.Palette) do
                if string.find(desc.Name, matKey, 1, true) ~= nil then
                    desc.Color = spec.Color
                    desc.Material = spec.Material
                    desc.Reflectance = spec.Reflectance
                    if stripTex and desc:IsA("MeshPart") then
                        desc.TextureID = ""
                    end
                    matchedCount += 1
                    break
                end
            end
        end
    end
    return matchedCount
end

function ArenaTileReference.MeasureVisualBounds(
    visualInstance: Model | BasePart,
    expectedSize: Vector3?,
    tolerance: number?
): (boolean, Vector3, Vector3, string)
    local target = expectedSize or ArenaTileReference.EXPECTED_VISUAL_SIZE_STUDS
    local tol = tolerance or ArenaTileReference.DIMENSION_TOLERANCE_STUDS

    local actualSize: Vector3
    if visualInstance:IsA("Model") then
        actualSize = visualInstance:GetExtentsSize()
    elseif visualInstance:IsA("BasePart") then
        actualSize = visualInstance.Size
    else
        return false, Vector3.zero, Vector3.zero, "Unsupported instance type for visual bounds measurement"
    end

    local delta = Vector3.new(
        math.abs(actualSize.X - target.X),
        math.abs(actualSize.Y - target.Y),
        math.abs(actualSize.Z - target.Z)
    )
    local isMatch = (delta.X <= tol) and (delta.Y <= tol) and (delta.Z <= tol)
    local report = string.format(
        "[ArenaTileReference] Instance='%s' | Expected=(%.3f, %.3f, %.3f) | Measured=(%.3f, %.3f, %.3f) | Delta=(%.4f, %.4f, %.4f) | Status=%s",
        visualInstance.Name,
        target.X, target.Y, target.Z,
        actualSize.X, actualSize.Y, actualSize.Z,
        delta.X, delta.Y, delta.Z,
        if isMatch then "PASS" else "MISMATCH"
    )
    if not isMatch then
        warn(report)
    end
    return isMatch, actualSize, delta, report
end

return ArenaTileReference
