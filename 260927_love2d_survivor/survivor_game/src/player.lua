local Player = {}

function Player:new()
    local player = {
        -- 위치
        x = 640,
        y = 360,

        -- 크기
        width = 32,
        height = 32,

        -- 이동 속도
        speed = 220,

        -- 체력
        maxHp = 100,
        hp = 100,

        -- 생존 여부
        dead = false,

        -- 피격 후 무적 시간
        invincible = false,
        invincibleTimer = 0,
        invincibleDuration = 0.5
    }

    setmetatable(player, self)
    self.__index = self

    return player
end


function Player:update(dt)
    -- 죽은 플레이어는 움직이지 않음
    if self.dead then
        return
    end

    -- 무적 시간 처리
    if self.invincible then
        self.invincibleTimer =
            self.invincibleTimer - dt

        if self.invincibleTimer <= 0 then
            self.invincible = false
            self.invincibleTimer = 0
        end
    end

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
