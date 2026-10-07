local Enemy = require("src.enemy")

local EnemyManager = {}

local function checkAABBCollision(a, b)
    return
        a.x < b.x + b.width and
        a.x + a.width > b.x and
        a.y < b.y + b.height and
        a.y + a.height > b.y
end

function EnemyManager:new()
    local manager = {
        -- 현재 존재하는 모든 적
        enemies = {},

        -- 적 생성 타이머
        spawnTimer = 0,

        -- 적 생성 간격 (초)
        spawnInterval = 2
    }

    setmetatable(manager, self)
    self.__index = self

    return manager
end


function EnemyManager:update(dt, player, experienceManager)
    -- 생성 타이머 증가
    self.spawnTimer = self.spawnTimer + dt

    -- 일정 시간이 지나면 새로운 적 생성
    if self.spawnTimer >= self.spawnInterval then
        self:spawnEnemy()

        self.spawnTimer =
            self.spawnTimer - self.spawnInterval
    end

    -- 모든 적 업데이트
    for _, enemy in ipairs(self.enemies) do
        enemy:update(dt, player)
    
        -- 살아 있는 적만 플레이어와 충돌 검사
        if not enemy.dead and not player.dead then
            if checkAABBCollision(enemy, player) then
                player:takeDamage(enemy.damage)
            end
        end
    end

    -- 죽은 적의 경험치를 획득한 뒤 제거
    for i = #self.enemies, 1, -1 do
        local enemy = self.enemies[i]
    
        if enemy.dead then
            experienceManager:addExp(
                enemy.expValue
            )
    
            table.remove(
                self.enemies,
                i
            )
        end
    end


function EnemyManager:spawnEnemy()
    local screenWidth = love.graphics.getWidth()
    local screenHeight = love.graphics.getHeight()

    local enemySize = 32

    local x
    local y

    -- 화면의 어느 방향에서 생성할지 선택
    local side = love.math.random(1, 4)

    if side == 1 then
        -- 위쪽
        x = love.math.random(
            0,
            screenWidth - enemySize
        )

        y = -enemySize

    elseif side == 2 then
        -- 오른쪽
        x = screenWidth

        y = love.math.random(
            0,
            screenHeight - enemySize
        )

    elseif side == 3 then
        -- 아래쪽
        x = love.math.random(
            0,
            screenWidth - enemySize
        )

        y = screenHeight

    else
        -- 왼쪽
        x = -enemySize

        y = love.math.random(
            0,
            screenHeight - enemySize
        )
    end

    -- 새로운 적 생성
    local enemy = Enemy:new(
        x,
        y
    )

    -- 적 목록에 추가
    table.insert(
        self.enemies,
        enemy
    )
end


function EnemyManager:draw()
    -- 모든 적 그리기
    for _, enemy in ipairs(self.enemies) do
        enemy:draw()
    end
end


return EnemyManager
