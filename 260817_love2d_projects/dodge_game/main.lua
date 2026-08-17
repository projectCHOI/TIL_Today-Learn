function resetObstacle()
    obstacle.x = love.math.random(0, 480 - obstacle.width)
    obstacle.y = -obstacle.height
end

function updateDifficulty()
    level = math.floor(score / 5) + 1

    if level > obstacle.maxLevel then
        level = obstacle.maxLevel
    end

    obstacle.speed =
        obstacle.baseSpeed +
        (level - 1) * obstacle.speedStep
end

function resetGame()
    player.x = 215
    player.y = 310

    score = 0
    level = 1
    gameState = "playing"

    updateDifficulty()
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

        baseSpeed = 160,
        speed = 160,
        speedStep = 35,
        maxLevel = 7
    }

    score = 0
    level = 1
    gameState = "playing"

    titleFont = love.graphics.newFont(28)
    normalFont = love.graphics.newFont(16)
    smallFont = love.graphics.newFont(13)

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

    -- 화면 왼쪽 경계
    if player.x < 0 then
        player.x = 0
    end

    -- 화면 오른쪽 경계
    if player.x + player.width > 480 then
        player.x = 480 - player.width
    end

    -- 장애물 이동
    obstacle.y = obstacle.y + obstacle.speed * dt

    -- 장애물을 피했을 때
    if obstacle.y > 360 then
        score = score + 1

        updateDifficulty()
        resetObstacle()
    end

    -- 충돌 판정
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

    -- 위쪽 게임 정보
    love.graphics.setFont(normalFont)
    love.graphics.setColor(1.0, 1.0, 1.0)

    love.graphics.print(
        "Score: " .. score,
        10,
        10
    )

    love.graphics.printf(
        "Level: " .. level,
        0,
        10,
        480,
        "center"
    )

    love.graphics.printf(
        "Speed: " .. obstacle.speed,
        0,
        10,
        470,
        "right"
    )

    -- 아래쪽 조작 안내
    if gameState == "playing" then
        love.graphics.setFont(smallFont)
        love.graphics.setColor(0.75, 0.75, 0.75)

        love.graphics.printf(
            "Move: Left / Right    Esc: Quit",
            0,
            338,
            480,
            "center"
        )
    end

    -- 게임 종료 화면
    if gameState == "gameover" then
        love.graphics.setColor(0, 0, 0, 0.75)
        love.graphics.rectangle("fill", 0, 0, 480, 360)

        love.graphics.setFont(titleFont)
        love.graphics.setColor(1.0, 0.2, 0.2)

        love.graphics.printf(
            "GAME OVER",
            0,
            110,
            480,
            "center"
        )

        love.graphics.setFont(normalFont)
        love.graphics.setColor(1.0, 1.0, 1.0)

        love.graphics.printf(
            "Final Score: " .. score,
            0,
            160,
            480,
            "center"
        )

        love.graphics.printf(
            "Reached Level: " .. level,
            0,
            185,
            480,
            "center"
        )

        love.graphics.printf(
            "Press R to Restart",
            0,
            225,
            480,
            "center"
        )

        love.graphics.setFont(smallFont)
        love.graphics.setColor(0.75, 0.75, 0.75)

        love.graphics.printf(
            "Press Esc to Quit",
            0,
            255,
            480,
            "center"
        )
    end
end