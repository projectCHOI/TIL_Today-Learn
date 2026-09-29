-- 플레이어 모듈 불러오기
local Player = require("src.player")

-- 플레이어 객체
local player


function love.load()
    -- 배경색 설정
    love.graphics.setBackgroundColor(0.08, 0.08, 0.10)

    -- 플레이어 생성
    player = Player:new()
end


function love.update(dt)
    -- 플레이어 업데이트
    player:update(dt)
end


function love.draw()
    -- 플레이어 그리기
    player:draw()
end
