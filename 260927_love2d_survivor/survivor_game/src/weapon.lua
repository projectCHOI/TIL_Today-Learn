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
