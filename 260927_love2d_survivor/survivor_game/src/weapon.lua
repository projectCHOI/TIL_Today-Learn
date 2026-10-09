
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

    -- Projectile 이동 및 충돌 판정
    for _, projectile in ipairs(self.projectiles) do
        projectile:update(dt)

        if not projectile.dead then
            for _, enemy in ipairs(enemies) do
                if not enemy.dead then
                    local hit = circleRectangleCollision(
                        projectile.x,
                        projectile.y,
                        projectile.radius,
                        enemy.x,
                        enemy.y,
                        enemy.width,
                        enemy.height
                    )

                    if hit then
                        enemy:takeDamage(
                            projectile.damage
                        )

                        projectile.dead = true
                        break
                    end
                end
            end
        end
    end

    -- 사용이 끝난 Projectile 제거
    for i = #self.projectiles, 1, -1 do
        if self.projectiles[i].dead then
            table.remove(
                self.projectiles,
                i
            )
        end
    end
end


-- 가장 가까운 살아 있는 Enemy 탐색
function Weapon:findNearestEnemy(player, enemies)
    local nearestEnemy = nil
    local nearestDistanceSquared = math.huge

    local playerCenterX =
        player.x + player.width / 2

    local playerCenterY =
        player.y + player.height / 2

    for _, enemy in ipairs(enemies) do
        if not enemy.dead then
            local enemyCenterX =
                enemy.x + enemy.width / 2

            local enemyCenterY =
                enemy.y + enemy.height / 2

            local dx =
                enemyCenterX - playerCenterX

            local dy =
                enemyCenterY - playerCenterY

            local distanceSquared =
                dx * dx + dy * dy

            if distanceSquared < nearestDistanceSquared then
                nearestDistanceSquared = distanceSquared
                nearestEnemy = enemy
            end
        end
    end

    return nearestEnemy
end


-- Projectile 발사
function Weapon:shoot(player, target)
    local playerCenterX =
        player.x + player.width / 2

    local playerCenterY =
        player.y + player.height / 2

    local targetCenterX =
        target.x + target.width / 2

    local targetCenterY =
        target.y + target.height / 2

    local directionX =
        targetCenterX - playerCenterX

    local directionY =
        targetCenterY - playerCenterY

    local length = math.sqrt(
        directionX * directionX +
        directionY * directionY
    )

    if length == 0 then
        return
    end

    directionX = directionX / length
    directionY = directionY / length

    -- Projectile 생성
    local projectile = Projectile:new(
        playerCenterX,
        playerCenterY,
        directionX,
        directionY
    )

    -- 현재 무기 공격력을 Projectile에 전달
    projectile.damage = self.damage

    table.insert(
        self.projectiles,
        projectile
    )
end


function Weapon:draw()
    for _, projectile in ipairs(self.projectiles) do
        projectile:draw()
    end
end


return Weapon
