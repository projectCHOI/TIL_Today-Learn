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

    local moveX = 0
    local moveY = 0

    -- 좌우 이동
    if love.keyboard.isDown("a") then
        moveX = moveX - 1
    end

    if love.keyboard.isDown("d") then
        moveX = moveX + 1
    end

    -- 상하 이동
    if love.keyboard.isDown("w") then
        moveY = moveY - 1
    end

    if love.keyboard.isDown("s") then
        moveY = moveY + 1
    end

    -- 대각선 이동속도 보정
    if moveX ~= 0 or moveY ~= 0 then

        local length = math.sqrt(
            moveX * moveX +
            moveY * moveY
        )

        moveX = moveX / length
        moveY = moveY / length
    end

    -- 실제 이동
    self.x = self.x + moveX * self.speed * dt
    self.y = self.y + moveY * self.speed * dt

    -- 화면 경계 제한
    self.x = math.max(
        0,
        math.min(
            self.x,
            love.graphics.getWidth() - self.width
        )
    )

    self.y = math.max(
        0,
        math.min(
            self.y,
            love.graphics.getHeight() - self.height
        )
    )
end

function Player:draw()

    love.graphics.setColor(1, 1, 1)

    love.graphics.rectangle(
        "fill",
        self.x,
        self.y,
        self.width,
        self.height
    )
end

return Player