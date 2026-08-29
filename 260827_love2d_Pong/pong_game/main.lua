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

    dx = 120,
    dy = 180
}

local function checkCollision(a, b)
    return a.x < b.x + b.width
       and b.x < a.x + a.width
       and a.y < b.y + b.height
       and b.y < a.y + a.height
end


function love.load()
    love.graphics.setBackgroundColor(0, 0, 0)
end


function love.update(dt)

    if love.keyboard.isDown("w") then
        player.y = player.y - player.speed * dt
    end

    if love.keyboard.isDown("s") then
        player.y = player.y + player.speed * dt
    end

    -- 플레이어 화면 경계
    if player.y < 0 then
        player.y = 0
    end

    if player.y + player.height > WINDOW_HEIGHT then
        player.y = WINDOW_HEIGHT - player.height
    end

    ball.x = ball.x + ball.dx * dt
    ball.y = ball.y + ball.dy * dt

    -- 위쪽 벽
    if ball.y <= 0 then
        ball.y = 0
        ball.dy = -ball.dy
    end

    -- 아래쪽 벽
    if ball.y + ball.height >= WINDOW_HEIGHT then
        ball.y = WINDOW_HEIGHT - ball.height
        ball.dy = -ball.dy
    end

    if checkCollision(ball, player) and ball.dx < 0 then

        -- 공을 플레이어 패들 오른쪽으로 이동
        ball.x = player.x + player.width

        -- 좌우 방향 반전
        ball.dx = -ball.dx
    end

    if checkCollision(ball, ai) and ball.dx > 0 then

        -- 공을 AI 패들 왼쪽으로 이동
        ball.x = ai.x - ball.width

        -- 좌우 방향 반전
        ball.dx = -ball.dx
    end
end


function love.draw()

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