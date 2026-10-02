local Enemy = {}

function Enemy:new(x, y)
    local enemy = {
        -- 위치
        x = x,
        y = y,

        -- 크기
        width = 32,
        height = 32,

        -- 이동 속도
        speed = 100
    }

    setmetatable(enemy, self)
    self.__index = self

    return enemy
end


function Enemy:update(dt, player)
    -- 적 중심 좌표
    local enemyCenterX = self.x + self.width / 2
    local enemyCenterY = self.y + self.height / 2

    -- 플레이어 중심 좌표
    local playerCenterX = player.x + player.width / 2
    local playerCenterY = player.y + player.height / 2

    -- 적 → 플레이어 방향
    local directionX = playerCenterX - enemyCenterX
    local directionY = playerCenterY - enemyCenterY

    -- 두 점 사이 거리
    local distance = math.sqrt(
        directionX * directionX +
        directionY * directionY
    )

    -- 방향 벡터 정규화
    if distance > 0 then
        directionX = directionX / distance
        directionY = directionY / distance

        -- 플레이어 방향으로 이동
        self.x = self.x + directionX * self.speed * dt
        self.y = self.y + directionY * self.speed * dt
    end
end


function Enemy:draw()
    -- 적 색상: 빨간색
    love.graphics.setColor(0.9, 0.2, 0.2)

    love.graphics.rectangle(
        "fill",
        self.x,
        self.y,
        self.width,
        self.height
    )
end


return Enemy