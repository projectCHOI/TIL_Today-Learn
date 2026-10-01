local Projectile = require("src.projectile")

local Weapon = {}

function Weapon:new()
    local weapon = {
        -- 현재 존재하는 발사체
        projectiles = {},

        -- 공격 간격 (초)
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

    -- 공격 가능한 시간이 되었는지 확인
    if self.attackTimer >= self.attackInterval then

        local target = self:findNearestEnemy(
            player,
            enemies
        )

        -- 적이 있을 때만 공격
        if target then
            self:shoot(
                player,
                target
            )

            self.attackTimer =
                self.attackTimer - self.attackInterval
        end
    end

    -- 모든 발사체 업데이트
    for _, projectile in ipairs(self.projectiles) do
        projectile:update(dt)
    end

    -- dead 상태의 발사체 제거
    for i = #self.projectiles, 1, -1 do
        if self.projectiles[i].dead then
            table.remove(
                self.projectiles,
                i
            )
        end
    end
end


function Weapon:findNearestEnemy(player, enemies)
    local nearestEnemy = nil
    local nearestDistanceSquared = math.huge

    -- 플레이어 중심 좌표
    local playerCenterX =
        player.x + player.width / 2

    local playerCenterY =
        player.y + player.height / 2
    -- 모든 적 검사
    for _, enemy in ipairs(enemies) do

        if not enemy.dead then
            -- 적 중심 좌표
            local enemyCenterX =
                enemy.x + enemy.width / 2

            local enemyCenterY =
                enemy.y + enemy.height / 2

            -- 플레이어 → 적 거리
            local dx =
                enemyCenterX - playerCenterX

            local dy =
                enemyCenterY - playerCenterY

            local distanceSquared =
                dx * dx + dy * dy

            -- 지금까지 발견한 적보다 가까운 경우
            if distanceSquared < nearestDistanceSquared then
                nearestDistanceSquared = distanceSquared
                nearestEnemy = enemy
            end
        end
    end

    return nearestEnemy
end


function Weapon:shoot(player, target)
    -- 플레이어 중심
    local playerCenterX =
        player.x + player.width / 2

    local playerCenterY =
        player.y + player.height / 2

    -- 적 중심
    local targetCenterX =
        target.x + target.width / 2

    local targetCenterY =
        target.y + target.height / 2

    -- 플레이어 → 적 방향
    local directionX =
        targetCenterX - playerCenterX

    local directionY =
        targetCenterY - playerCenterY

    -- 방향 벡터 길이
    local length = math.sqrt(
        directionX * directionX +
        directionY * directionY
    )

    if length == 0 then
        return
    end

    -- 방향 정규화
    directionX = directionX / length
    directionY = directionY / length

    -- 새로운 발사체 생성
    local projectile = Projectile:new(
        playerCenterX,
        playerCenterY,
        directionX,
        directionY
    )

    table.insert(
        self.projectiles,
        projectile
    )
end


function Weapon:draw()
    -- 모든 발사체 그리기
    for _, projectile in ipairs(self.projectiles) do
        projectile:draw()
    end
end


return Weapon