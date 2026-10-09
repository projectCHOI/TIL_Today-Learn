
local Projectile = require("src.projectile")

local Weapon = {}

-- 원형 Projectile과 사각형 Enemy 충돌 검사
local function circleRectangleCollision(
    circleX,
    circleY,
    radius,
    rectX,
    rectY,
    rectWidth,
    rectHeight
)
    local closestX = math.max(
        rectX,
        math.min(circleX, rectX + rectWidth)
    )

    local closestY = math.max(
        rectY,
        math.min(circleY, rectY + rectHeight)
    )

    local dx = circleX - closestX
    local dy = circleY - closestY

    local distanceSquared =
        dx * dx + dy * dy

    return distanceSquared <= radius * radius
end


function Weapon:new()
    local weapon = {
        -- 현재 발사된 Projectile 목록
        projectiles = {},

        -- 무기 공격력
        damage = 1,

        -- 자동 공격 간격
        attackInterval = 0.8,

        -- 공격 타이머
        attackTimer = 0
    }

    setmetatable(weapon, self)
    self.__index = self

    return weapon
end


function Weapon:update(dt, player, enemies)
    -- 공격 타이머 증가
    self.attackTimer = self.attackTimer + dt

    -- 자동 공격
    if self.attackTimer >= self.attackInterval then
        local target = self:findNearestEnemy(
            player,
            enemies
        )

        if target then
            self:shoot(player, target)

            self.attackTimer =
                self.attackTimer - self.attackInterval
        end
    end

    