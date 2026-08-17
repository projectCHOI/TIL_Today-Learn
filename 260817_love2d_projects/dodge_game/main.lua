function resetObstacle()
    obstacle.x = love.math.random(0, 480 - obstacle.width)
    obstacle.y = -obstacle.height
end

function resetGame()
    player.x = 215
    player.y = 310

    obstacle.speed = 160

    score = 0
    gameState = "playing"

    resetObstacle()
end

function checkCollision(a, b)
    return
        a.x < b.x + b.width and
        b.x < a.x + a.width and
        a.y < b.y + b.height and
        b.y < a.y + a.height
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
    gameState = "playing"

    titleFont = love.graphics.newFont(28)
    normalFont = love.graphics.newFont(16)

    resetObstacle()
end

function love.update(dt)
    if gameState ~= "playing" then
        return
    end

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

    -- 장애물 이동
    obstacle.y = obstacle.y + obstacle.speed * dt

    -- 장애물이 화면을 통과하면 점수 증가
    if obstacle.y > 360 then
        score = score + 1
        resetObstacle()
    end

    -- 플레이어와 장애물의 충돌 확인
    if checkCollision(player, obstacle) then
        gameState = "gameover"
    end
end

function love.keypressed(key)
    if key == "r" and gameState == "gameover" then
        resetGame()
    end

    if key == "escape" then
        love.event.quit()
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
    love.graphics.setFont(normalFont)
    love.graphics.setColor(1.0, 1.0, 1.0)
    love.graphics.print("Score: " .. score, 10, 10)

    -- 게임 종료 화면
    if gameState == "gameover" then
        love.graphics.setColor(0, 0, 0, 0.7)
        love.graphics.rectangle("fill", 0, 0, 480, 360)

        love.graphics.setColor(1.0, 0.2, 0.2)
        love.graphics.setFont(titleFont)
        love.graphics.printf(
            "GAME OVER",
            0,
            125,
            480,
            "center"
        )

        love.graphics.setColor(1.0, 1.0, 1.0)
        love.graphics.setFont(normalFont)
        love.graphics.printf(
            "Score: " .. score,
            0,
            175,
            480,
            "center"
        )

        love.graphics.printf(
            "Press R to Restart",
            0,
            205,
            480,
            "center"
        )
    end
end