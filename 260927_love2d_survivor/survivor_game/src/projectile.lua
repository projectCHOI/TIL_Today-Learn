local Projectile = {}

function Projectile:new(x, y, directionX, directionY)
    local projectile = {
        -- 위치
        x = x,
        y = y,

        -- 크기
        radius = 6,

        -- 이동 방향
        directionX = directionX,
        directionY = directionY,

        -- 이동 속도
        speed = 450,

        -- 공격력
        damage = 1,

        -- 삭제 여부
        dead = false
    }

    setmetatable(projectile, self)
    self.__index = self

    return projectile
end


function Projectile:update(dt)
    -- 발사체 이동
    self.x = self.x + self.directionX * self.speed * dt
    self.y = self.y + self.directionY * self.speed * dt

    -- 화면 밖으로 충분히 벗어나면 삭제 대상으로 표시
    local screenWidth = love.graphics.getWidth()
    local screenHeight = love.graphics.getHeight()

    local margin = 50

    if self.x < -margin
        or self.x > screenWidth + margin
        or self.y < -margin
        or self.y > screenHeight + margin then

        self.dead = true
    end
end


function Projectile:draw()
    -- 발사체 색상
    love.graphics.setColor(1, 0.85, 0.2)

    love.graphics.circle(
        "fill",
        self.x,
        self.y,
        self.radius
    )
end


return Projectile
