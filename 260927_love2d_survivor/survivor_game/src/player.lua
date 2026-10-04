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

        moveX = moveX / length
        moveY = moveY / length
    end

    -- 실제 이동
    self.x =
        self.x + moveX * self.speed * dt

    self.y =
        self.y + moveY * self.speed * dt

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


function Player:takeDamage(damage)
    -- 죽었거나 무적 상태라면 피해 없음
    if self.dead or self.invincible then
        return
    end

    -- 체력 감소
    self.hp = self.hp - damage

    -- 사망 판정
    if self.hp <= 0 then
        self.hp = 0
        self.dead = true
        return
    end

    -- 피격 후 잠시 무적
    self.invincible = true
    self.invincibleTimer =
        self.invincibleDuration
end


function Player:draw()
    -- 피격 무적 상태에서는 색상을 변경
    if self.invincible then
        love.graphics.setColor(
            0.5,
            0.7,
            1
        )
    else
        love.graphics.setColor(
            1,
            1,
            1
        )
    end

    love.graphics.rectangle(
        "fill",
        self.x,
        self.y,
        self.width,
        self.height
    )
end


return Player
