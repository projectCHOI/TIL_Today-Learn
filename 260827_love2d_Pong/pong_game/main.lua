-- 화면 크기
local WINDOW_WIDTH = 800
local WINDOW_HEIGHT = 600

-- 플레이어 패들
local player = {
    x = 40,
    y = 250,
    width = 15,
    height = 100
}

-- AI 패들
local ai = {
    x = 745,
    y = 250,
    width = 15,
    height = 100
}

-- 공
local ball = {
    x = 390,
    y = 290,
    width = 20,
    height = 20
}

function love.load()
    -- 검은 배경
    love.graphics.setBackgroundColor(0, 0, 0)
end

function love.update(dt)
    -- 현재 단계에서는 움직임 없음
end

function love.draw()
    -- 흰색
    love.graphics.setColor(1, 1, 1)

    -- 플레이어 패들
    love.graphics.rectangle(
        "fill",
        player.x,
        player.y,
        player.width,
        player.height
    )

    -- AI 패들
    love.graphics.rectangle(
        "fill",
        ai.x,
        ai.y,
        ai.width,
        ai.height
    )

    -- 공
    love.graphics.rectangle(
        "fill",
        ball.x,
        ball.y,
        ball.width,
        ball.height
    )
end