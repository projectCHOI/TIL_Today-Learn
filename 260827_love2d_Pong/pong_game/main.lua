local WINDOW_WIDTH = 800
local WINDOW_HEIGHT = 600

local WIN_SCORE = 5
local gameState = "menu"
local gameMode = nil
local winnerText = ""
local playerScore = 0
local opponentScore = 0

local player = {
    x = 40,
    y = 250,
    width = 15,
    height = 100,
    speed = 300
}

local opponent = {
    x = 745,
    y = 250,
    width = 15,
    height = 100,

    aiSpeed = 140,
    playerSpeed = 300
}

local ball = {
    x = 390,
    y = 290,
    width = 20,
    height = 20,

    dx = 0,
    dy = 0
}

local player1Button = {
    x = 250,
    y = 260,
    width = 300,
    height = 60,
    text = "Player 1"
}

local player2Button = {
    x = 250,
    y = 350,
    width = 300,
    height = 60,
    text = "Player 2"
}

local function checkCollision(a, b)
    return a.x < b.x + b.width
       and b.x < a.x + a.width
       and a.y < b.y + b.height
       and b.y < a.y + a.height
end

local function getHitPosition(ball, paddle)

    -- 공의 중심 Y 좌표
    local ballCenterY =
        ball.y + ball.height / 2

    -- 패들의 중심 Y 좌표
    local paddleCenterY =
        paddle.y + paddle.height / 2

    -- 패들 중심에서 공이 얼마나 떨어져 있는지 계산
    local distance =
        ballCenterY - paddleCenterY

    -- 패들 높이의 절반
    local halfPaddleHeight =
        paddle.height / 2

    -- 충돌 위치를 -1 ~ 1 범위로 변환
    local hitPosition =
        distance / halfPaddleHeight

    -- 혹시 범위를 넘어갈 경우 제한
    if hitPosition < -1 then
        hitPosition = -1
    elseif hitPosition > 1 then
        hitPosition = 1
    end

    return hitPosition
end

local function isMouseInsideButton(mouseX, mouseY, button)
    return mouseX >= button.x
       and mouseX <= button.x + button.width
       and mouseY >= button.y
       and mouseY <= button.y + button.height
end

local function placeBallAtCenter()
    ball.x = WINDOW_WIDTH / 2 - ball.width / 2
    ball.y = WINDOW_HEIGHT / 2 - ball.height / 2

    ball.dx = 0
    ball.dy = 0
end

local function serveBall()

    if love.math.random(0, 1) == 0 then
        ball.dx = -120
    else
        ball.dx = 120
    end

    if love.math.random(0, 1) == 0 then
        ball.dy = -180
    else
        ball.dy = 180
    end

    gameState = "playing"
end

local function resetGame()

    playerScore = 0
    opponentScore = 0
    winnerText = ""

    player.y =
        WINDOW_HEIGHT / 2
        - player.height / 2

    opponent.y =
        WINDOW_HEIGHT / 2
        - opponent.height / 2

    placeBallAtCenter()

    gameState = "ready"
end

local function startGame(mode)

    gameMode = mode

    resetGame()
end


local function prepareNextServe()
    placeBallAtCenter()

    gameState = "ready"
end

local function checkGameOver()
    if playerScore >= WIN_SCORE then

        winnerText = "PLAYER 1 WINS!"

        placeBallAtCenter()

        gameState = "gameover"

        return true
    end

    if opponentScore >= WIN_SCORE then

        if gameMode == "1P" then
            winnerText = "AI WINS!"
        else
            winnerText = "PLAYER 2 WINS!"
        end

        placeBallAtCenter()

        gameState = "gameover"

        return true
    end


    return false
end


function love.load()

    love.graphics.setBackgroundColor(0, 0, 0)

    love.math.setRandomSeed(os.time())
end


function love.update(dt)
    if gameState == "menu"
        or gameState == "ready"
        or gameState == "paused"
        or gameState == "gameover" then

        return
    end

    if gameState == "playing" then

        if love.keyboard.isDown("w") then
            player.y =
                player.y
                - player.speed * dt
        end

        if love.keyboard.isDown("s") then
            player.y =
                player.y
                + player.speed * dt
        end


        -- Player 1 화면 경계
        if player.y < 0 then
            player.y = 0
        end

        if player.y + player.height > WINDOW_HEIGHT then
            player.y =
                WINDOW_HEIGHT - player.height
        end

        if gameMode == "1P" then

            local ballCenterY =
                ball.y + ball.height / 2

            local opponentCenterY =
                opponent.y + opponent.height / 2

            if ballCenterY < opponentCenterY then

                opponent.y =
                    opponent.y
                    - opponent.aiSpeed * dt

            elseif ballCenterY > opponentCenterY then

                opponent.y =
                    opponent.y
                    + opponent.aiSpeed * dt
            end
        end

        if gameMode == "2P" then

            if love.keyboard.isDown("o") then
                opponent.y =
                    opponent.y
                    - opponent.playerSpeed * dt
            end

            if love.keyboard.isDown("k") then
                opponent.y =
                    opponent.y
                    + opponent.playerSpeed * dt
            end
        end

        -- 오른쪽 패들 화면 경계
        if opponent.y < 0 then
            opponent.y = 0
        end

        if opponent.y + opponent.height > WINDOW_HEIGHT then
            opponent.y =
                WINDOW_HEIGHT - opponent.height
        end

        ball.x = ball.x + ball.dx * dt
        ball.y = ball.y + ball.dy * dt

        if ball.y <= 0 then
            ball.y = 0
            ball.dy = -ball.dy
        end

        if ball.y + ball.height >= WINDOW_HEIGHT then
            ball.y =
                WINDOW_HEIGHT - ball.height

            ball.dy = -ball.dy
        end

        if checkCollision(ball, player)
            and ball.dx < 0 then

            ball.x =
                player.x + player.width

            ball.dx = -ball.dx
        end

        if checkCollision(ball, opponent)
            and ball.dx > 0 then

            ball.x =
                opponent.x - ball.width

            ball.dx = -ball.dx
        end

        if ball.x > WINDOW_WIDTH then

            playerScore =
                playerScore + 1

            if not checkGameOver() then
                prepareNextServe()
            end

            return
        end

        if ball.x + ball.width < 0 then

            opponentScore =
                opponentScore + 1

            if not checkGameOver() then
                prepareNextServe()
            end

            return
        end
    end
end

function love.keypressed(key)

    -- READY → SPACE → PLAYING
    if gameState == "ready"
        and key == "space" then

        serveBall()

        return
    end

    -- PLAYING → P → PAUSED
    if gameState == "playing"
        and key == "p" then

        gameState = "paused"

        return
    end

    -- PAUSED → P → PLAYING
    if gameState == "paused"
        and key == "p" then

        gameState = "playing"

        return
    end

    -- GAMEOVER → R → 같은 모드 재시작
    if gameState == "gameover"
        and key == "r" then

        resetGame()

        return
    end

    -- ESC → 메뉴
    if key == "escape" then

        gameState = "menu"
        gameMode = nil
        winnerText = ""

        placeBallAtCenter()

        return
    end
end

function love.mousepressed(x, y, button)

    if gameState ~= "menu" then
        return
    end

    if button ~= 1 then
        return
    end

    if isMouseInsideButton(
        x,
        y,
        player1Button
    ) then

        startGame("1P")

        return
    end

    if isMouseInsideButton(
        x,
        y,
        player2Button
    ) then

        startGame("2P")

        return
    end
end

local function drawButton(button)

    local mouseX, mouseY =
        love.mouse.getPosition()

    local isHover =
        isMouseInsideButton(
            mouseX,
            mouseY,
            button
        )

    if isHover then
        love.graphics.setColor(
            0.35,
            0.35,
            0.35
        )
    else
        love.graphics.setColor(
            0.2,
            0.2,
            0.2
        )
    end

    love.graphics.rectangle(
        "fill",
        button.x,
        button.y,
        button.width,
        button.height
    )

    love.graphics.setColor(1, 1, 1)

    love.graphics.rectangle(
        "line",
        button.x,
        button.y,
        button.width,
        button.height
    )

    love.graphics.printf(
        button.text,
        button.x,
        button.y + 21,
        button.width,
        "center"
    )
end

function love.draw()
    if gameState == "menu" then

        love.graphics.setColor(1, 1, 1)

        love.graphics.printf(
            "PONG",
            0,
            130,
            WINDOW_WIDTH,
            "center"
        )

        love.graphics.printf(
            "Select Game Mode",
            0,
            190,
            WINDOW_WIDTH,
            "center"
        )

        drawButton(player1Button)
        drawButton(player2Button)

        love.graphics.setColor(1, 1, 1)

        love.graphics.printf(
            "Player 1 : Player vs AI",
            0,
            440,
            WINDOW_WIDTH,
            "center"
        )

        love.graphics.printf(
            "Player 2 : Player vs Player",
            0,
            470,
            WINDOW_WIDTH,
            "center"
        )

        return
    end

    love.graphics.setColor(1, 1, 1)


    love.graphics.print(
        "PLAYER 1: " .. playerScore,
        230,
        30
    )

    if gameMode == "1P" then

        love.graphics.print(
            "AI: " .. opponentScore,
            520,
            30
        )

    elseif gameMode == "2P" then

        love.graphics.print(
            "PLAYER 2: " .. opponentScore,
            500,
            30
        )
    end

    -- Player 1 패들
    love.graphics.setColor(1, 1, 1)

    love.graphics.rectangle(
        "fill",
        player.x,
        player.y,
        player.width,
        player.height
    )

    -- 오른쪽 패들
    if gameMode == "1P" then

        love.graphics.setColor(1, 1, 1)

    elseif gameMode == "2P" then

        love.graphics.setColor(
            255 / 255,
            217 / 255,
            77 / 255
        )
    end

    love.graphics.rectangle(
        "fill",
        opponent.x,
        opponent.y,
        opponent.width,
        opponent.height
    )

    -- 공
    love.graphics.setColor(1, 1, 1)

    love.graphics.rectangle(
        "fill",
        ball.x,
        ball.y,
        ball.width,
        ball.height
    )

    -- 상태 안내
    love.graphics.print(
        "MODE: " .. gameMode,
        20,
        20
    )

    love.graphics.print(
        "ESC : MENU",
        20,
        45
    )

    if gameState == "ready" then

        love.graphics.printf(
            "READY",
            0,
            220,
            WINDOW_WIDTH,
            "center"
        )

        love.graphics.printf(
            "Press SPACE to Serve",
            0,
            260,
            WINDOW_WIDTH,
            "center"
        )
    end

    if gameState == "paused" then

        love.graphics.setColor(
            0,
            0,
            0,
            0.65
        )

        love.graphics.rectangle(
            "fill",
            0,
            0,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        love.graphics.setColor(1, 1, 1)

        love.graphics.printf(
            "PAUSED",
            0,
            220,
            WINDOW_WIDTH,
            "center"
        )

        love.graphics.printf(
            "Press P to Resume",
            0,
            260,
            WINDOW_WIDTH,
            "center"
        )

        love.graphics.printf(
            "ESC : MENU",
            0,
            300,
            WINDOW_WIDTH,
            "center"
        )
    end

    if gameState == "gameover" then

        love.graphics.setColor(
            0,
            0,
            0,
            0.75
        )

        love.graphics.rectangle(
            "fill",
            0,
            0,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        love.graphics.setColor(1, 1, 1)

        love.graphics.printf(
            "GAME OVER",
            0,
            190,
            WINDOW_WIDTH,
            "center"
        )

        love.graphics.printf(
            winnerText,
            0,
            235,
            WINDOW_WIDTH,
            "center"
        )

        love.graphics.printf(
            "FINAL SCORE",
            0,
            290,
            WINDOW_WIDTH,
            "center"
        )

        love.graphics.printf(
            playerScore .. "  :  " .. opponentScore,
            0,
            325,
            WINDOW_WIDTH,
            "center"
        )

        love.graphics.printf(
            "R : RESTART",
            0,
            390,
            WINDOW_WIDTH,
            "center"
        )

        love.graphics.printf(
            "ESC : MENU",
            0,
            425,
            WINDOW_WIDTH,
            "center"
        )
    end
end
