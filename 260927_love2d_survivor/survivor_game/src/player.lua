local Player = {}

function Player:new()
    local player = {
        x = 640,
        y = 360,

        width = 32,
        height = 32,

        speed = 220
    }

    setmetatable(player, self)
    self.__index = self

    return player
end

function Player:update(dt)


return Player