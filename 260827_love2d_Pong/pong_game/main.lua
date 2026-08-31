local WINDOW_WIDTH = 800
local WINDOW_HEIGHT = 600

local gameState = "menu"
local gameMode = nil
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

    -- AI 속도
    aiSpeed = 140,

    -- Player 2 속도
    playerSpeed = 300
}

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

local function resetBall()

    ball.x = WINDOW_WIDTH / 2 - ball.width / 2
    ball.y = WINDOW_HEIGHT / 2 - ball.height / 2

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
end

local function resetGame()

    playerScore = 0
    opponentScore = 0

    -- Player 1 중앙
    player.y = WINDOW_HEIGHT / 2 - player.height / 2

    -- 오른쪽 패들 중앙
    opponent.y = WINDOW_HEIGHT / 2 - opponent.height / 2

    resetBall()
end

local function startGame(mode)

    gameMode = mode
    gameState = "playing"

    resetGame()
end


function love.load()

    love.graphics.setBackgroundColor(0, 0, 0)

    love.math.setRandomSeed(os.time())
end


function love.update(dt)

    if gameState == "menu" then

        -- 메뉴에서는 게임 로직을 실행하지 않음
        return
    end
    
    if gameState == "playing" then

        if love.keyboard.isDown("w") then
            player.y = player.y - player.speed * dt
        end

        if love.keyboard.isDown("s") then
            player.y = player.y + player.speed * dt
        end


        -- Player 1 화면 경계
        if player.y < 0 then
            player.y = 0
        end

        if player.y + player.height > WINDOW_HEIGHT then
            player.y = WINDOW_HEIGHT - player.height
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

            -- O 키: 위
            if love.keyboard.isDown("o") then
                opponent.y =
                    opponent.y
                    - opponent.playerSpeed * dt
            end

            -- K 키: 아래
            if love.keyboard.isDown("k") then
                opponent.y =
                    opponent.y
                    + opponent.playerSpeed * dt
            end
        end

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
            ball.y = WINDOW_HEIGHT - ball.height
            ball.dy = -ball.dy
        end

        if checkCollision(ball, player)
            and ball.dx < 0 then

            ball.x = player.x + player.width
            ball.dx = -ball.dx
        end

        if checkCollision(ball, opponent)
            and ball.dx > 0 then

            ball.x = opponent.x - ball.width
            ball.dx = -ball.dx
        end

        if ball.x > WINDOW_WIDTH then

            playerScore = playerScore + 1

            resetBall()
        end

        if ball.x + ball.width < 0 then

            opponentScore = opponentScore + 1

            resetBall()
        end
    end
end

function love.keypressed(key)

    -- MENU 상태에서만 모드 선택
    if gameState == "menu" then

        -- 임시 테스트:
        -- 숫자 1 = Player vs AI
        if key == "1" then
            startGame("1P")
        end

        -- 임시 테스트:
        -- 숫자 2 = Player vs Player
        if key == "2" then
            startGame("2P")
        end
    end


    -- ESC 키로 메뉴 복귀
    if key == "escape" then

        gameState = "menu"
        gameMode = nil
    end
end


function love.draw()

    love.graphics.setColor(1, 1, 1)

    if gameState == "menu" then

        love.graphics.printf(
            "PONG",
            0,
            150,
            WINDOW_WIDTH,
            "center"
        )

        love.graphics.printf(
            "1 : Player 1  (Player vs AI)",
            0,
            260,
            WINDOW_WIDTH,
            "center"
        )

        love.graphics.printf(
            "2 : Player 2  (Player vs Player)",
            0,
            310,
            WINDOW_WIDTH,
            "center"
        )

        return
    end
    
    -- Player 1 점수
    love.graphics.print(
        "PLAYER 1: " .. playerScore,
        230,
        30
    )


    -- 오른쪽 점수 표시
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

    love.graphics.setColor(1, 1, 1)

    love.graphics.rectangle(
        "fill",
        player.x,
        player.y,
        player.width,
        player.height
    )

    if gameMode == "1P" then

        -- AI = 흰색
        love.graphics.setColor(1, 1, 1)

    elseif gameMode == "2P" then

        -- Player 2 = #FFD94D
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

    love.graphics.setColor(1, 1, 1)

    love.graphics.rectangle(
        "fill",
        ball.x,
        ball.y,
        ball.width,
        ball.height
    )

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
end
