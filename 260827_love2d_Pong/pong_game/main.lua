-- 화면 크기
local WINDOW_WIDTH = 800
local WINDOW_HEIGHT = 600

-- 플레이어 패들
local player = {
    x = 40,
    y = 250,
    width = 15,
    height = 100,
    speed = 300
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
    height = 20,

    -- 공의 이동 속도
    dx = 250,
    dy = 180
}

function love.load()
    -- 검은 배경
    love.graphics.setBackgroundColor(0, 0, 0)
end

function love.update(dt)

    -- =========================
    -- 플레이어 이동
    -- =========================

    -- W 키: 위로 이동
    if love.keyboard.isDown("w") then
        player.y = player.y - player.speed * dt
    end

    -- S 키: 아래로 이동
    if love.keyboard.isDown("s") then
        player.y = player.y + player.speed * dt
    end

    -- 화면 위쪽 제한
    if player.y < 0 then
        player.y = 0
    end

    -- 화면 아래쪽 제한
    if player.y + player.height > WINDOW_HEIGHT then
        player.y = WINDOW_HEIGHT - player.height
    end


    -- =========================
    -- 공 이동
    -- =========================

    ball.x = ball.x + ball.dx * dt
    ball.y = ball.y + ball.dy * dt


    -- =========================
    -- 공과 위쪽 / 아래쪽 벽 충돌
    -- =========================

    -- 위쪽 벽 충돌
    if ball.y <= 0 then
        ball.y = 0
        ball.dy = -ball.dy
    end

    -- 아래쪽 벽 충돌
    if ball.y + ball.height >= WINDOW_HEIGHT then
        ball.y = WINDOW_HEIGHT - ball.height
        ball.dy = -ball.dy
    end
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