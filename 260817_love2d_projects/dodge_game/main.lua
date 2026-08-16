function resetObstacle()
    obstacle.x = love.math.random(0, 480 - obstacle.width)
    obstacle.y = -obstacle.height
end

function love.load()
    player = {
        x = 215,
        y = 310,
        width = 50,
        height = 25,
        speed = 300
    }

    obstacle = {
        x = 0,
        y = -40,
        width = 35,
        height = 35,
        speed = 160
    }

    score = 0

    resetObstacle()
end

function love.update(dt)
    -- 플레이어 이동
    if love.keyboard.isDown("left") then
        player.x = player.x - player.speed * dt
    end

    if love.keyboard.isDown("right") then
        player.x = player.x + player.speed * dt
    end

    -- 플레이어가 화면 밖으로 나가지 않게 제한
    if player.x < 0 then
        player.x = 0
    end

    if player.x + player.width > 480 then
        player.x = 480 - player.width
    end

    -- 장애물을 아래쪽으로 이동
    obstacle.y = obstacle.y + obstacle.speed * dt

    -- 장애물이 화면 아래로 나가면 다시 위로 이동
    if obstacle.y > 360 then
        score = score + 1
        resetObstacle()
    end
end

function love.draw()
    -- 플레이어
    love.graphics.setColor(0.2, 0.7, 1.0)

    love.graphics.rectangle(
        "fill",
        player.x,
        player.y,
        player.width,
        player.height
    )

    -- 장애물
    love.graphics.setColor(1.0, 0.2, 0.2)

    love.graphics.rectangle(
        "fill",
        obstacle.x,
        obstacle.y,
        obstacle.width,
        obstacle.height
    )

    -- 점수
    love.graphics.setColor(1.0, 1.0, 1.0)
    love.graphics.print("Score: " .. score, 10, 10)
end