local GameManager = {}

function GameManager:new()
    local manager = {
        -- 게임 상태
        state = "playing",

        -- 생존 시간
        survivalTime = 0,

        -- 최종 생존 시간
        finalSurvivalTime = 0
    }

    setmetatable(manager, self)
    self.__index = self

    return manager
end


function GameManager:update(dt, player)
    -- PLAYING 상태
    if self.state == "playing" then

        -- 생존 시간 증가
        self.survivalTime =
            self.survivalTime + dt

        -- 플레이어 사망 확인
        if player.dead then
            self.state = "gameover"

            self.finalSurvivalTime =
                self.survivalTime
        end
    end
end


function GameManager:isPlaying()
    return self.state == "playing"
end


function GameManager:isGameOver()
    return self.state == "gameover"
end


function GameManager:drawHUD(player)
    -- 기본 색상
    love.graphics.setColor(
        1,
        1,
        1
    )

    -- 플레이어 HP
    love.graphics.print(
        "HP: "
            .. player.hp
            .. " / "
            .. player.maxHp,
        20,
        20
    )

    -- 생존 시간
    love.graphics.print(
        string.format(
            "TIME: %.1f",
            self.survivalTime
        ),
        20,
        45
    )
end


function GameManager:drawGameOver()
    if self.state ~= "gameover" then
        return
    end

    local screenWidth =
        love.graphics.getWidth()

    local screenHeight =
        love.graphics.getHeight()

    love.graphics.setColor(
        1,
        1,
        1
    )

    love.graphics.printf(
        "GAME OVER",
        0,
        screenHeight / 2 - 40,
        screenWidth,
        "center"
    )

    love.graphics.printf(
        string.format(
            "SURVIVAL TIME: %.1f",
            self.finalSurvivalTime
        ),
        0,
        screenHeight / 2,
        screenWidth,
        "center"
    )
end


return GameManager
