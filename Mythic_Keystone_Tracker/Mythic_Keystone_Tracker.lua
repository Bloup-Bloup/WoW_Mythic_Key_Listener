
SLASH_MKST1 = "/mkst"

-- /mkst
local function MKSTHandler()
    local playerName= UnitName("player")
    keyStoneLevel = C_MythicPlus.GetOwnedKeystoneLevel()
    challengeMapID = C_MythicPlus.GetOwnedKeystoneChallengeMapID()
    name, id, timeLimit, texture, backgroundTexture = C_ChallengeMode.GetMapUIInfo(challengeMapID)
    print("Clef : ".. name .." ".. keyStoneLevel);     
    return name, keyStoneLevel
end


local frame = CreateFrame("FRAME", "FooAddonFrame");
frame:RegisterEvent("PLAYER_ENTERING_WORLD");

-- print keystone name when char is connected
local function eventHandler(self, event, ...)
    local playerName= UnitName("player")
    keyStoneLevel = C_MythicPlus.GetOwnedKeystoneLevel()
    challengeMapID = C_MythicPlus.GetOwnedKeystoneChallengeMapID()
    name, id, timeLimit, texture, backgroundTexture = C_ChallengeMode.GetMapUIInfo(challengeMapID)
    return name, keyStoneLevel
end
frame:SetScript("OnEvent", eventHandler);


SlashCmdList["MKST"] = MKSTHandler