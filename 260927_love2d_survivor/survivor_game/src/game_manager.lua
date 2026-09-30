local Enemy = require("src.enemy")

local EnemyManager = {}

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


function EnemyManager:update(dt, player)
    -- 생성 타이머 증가
    self.spawnTimer = self.spawnTimer + dt

    -- 일정 시간이 지나면 새로운 적 생성
    if self.spawnTimer >= self.spawnInterval then
        self:spawnEnemy()

        self.spawnTimer = self.spawnTimer - self.spawnInterval
    end

    -- 모든 적 업데이트
    for _, enemy in ipairs(self.enemies) do
        enemy:update(dt, player)
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
        x = love.math.random(0, screenWidth - enemySize)
        y = -enemySize

    elseif side == 2 then
        -- 오른쪽
        x = screenWidth
        y = love.math.random(0, screenHeight - enemySize)

    elseif side == 3 then
        -- 아래쪽
        x = love.math.random(0, screenWidth - enemySize)
        y = screenHeight

    else
        -- 왼쪽
        x = -enemySize
        y = love.math.random(0, screenHeight - enemySize)
    end

    local enemy = Enemy:new(x, y)

    table.insert(self.enemies, enemy)
end


function EnemyManager:draw()
    -- 모든 적 그리기
    for _, enemy in ipairs(self.enemies) do
        enemy:draw()
    end
end


return EnemyManager
