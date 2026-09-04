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