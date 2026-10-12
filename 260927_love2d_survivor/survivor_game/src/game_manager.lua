local GameManager = {}

function GameManager:new()
    local manager = {
        -- 게임 상태
        -- playing / levelup / gameover
        state = "playing",

        -- 현재 생존 시간
        survivalTime = 0,

        -- 최종 생존 시간
        finalSurvivalTime = 0
    }

    setmetatable(manager, self)
    self.__index = self

    return manager
end

-- 게임 상태 업데이트
function GameManager:update(
    dt,
    player,
    experienceManager,
    upgradeManager
)
    -- 게임 종료 상태에서는 업데이트하지 않음
    if self.state == "gameover" then
        return
    end

    -- 레벨업 선택 상태에서는 시간 정지
    if self.state == "levelup" then
        return
    end

    -- PLAYING 상태에서만 진행
    if self.state == "playing" then

        -- 플레이어 사망을 먼저 확인
        if player.dead then
            self.state = "gameover"

            self.finalSurvivalTime =
                self.survivalTime

            return
        end

        -- 레벨업 발생 확인
        if experienceManager:hasLevelUp() then

            -- 강화 선택 화면 열기
            local opened =
                upgradeManager:open()

            if opened then
                self.state = "levelup"
            end

            return
        end

        -- 생존 시간 증가
        self.survivalTime =
            self.survivalTime + dt
    end
end

-- 게임 진행 상태 확인
function GameManager:isPlaying()
    return self.state == "playing"
end

-- 레벨업 상태 확인
function GameManager:isLevelUp()
    return self.state == "levelup"
end

-- 게임 종료 상태 확인
function GameManager:isGameOver()
    return self.state == "gameover"
end

-- 강화 선택 처리
function GameManager:selectUpgrade(
    choiceIndex,
    player,
    weapon,
    experienceManager,
    upgradeManager
)
    -- 레벨업 상태가 아니면 선택 불가
    if self.state ~= "levelup" then
        return false
    end

    -- 강화 선택 및 적용
    local success = upgradeManager:select(
        choiceIndex,
        player,
        weapon
    )

    if not success then
        return false
    end

    -- 강화 선택권 1회 소비
    experienceManager:consumeLevelUp()

    -- 남은 강화 선택권 확인
    if experienceManager:hasLevelUp() then

        -- 다음 강화 선택 화면 열기
        upgradeManager:open()

    else
        -- 모든 강화 선택 완료
        self.state = "playing"
    end

    return true
end

-- HP 및 생존 시간 표시
function GameManager:drawHUD(player)
    love.graphics.setColor(1, 1, 1)

    love.graphics.print(
        "HP: "
            .. player.hp
            .. " / "
            .. player.maxHp,
        20,
        20
    )

    love.graphics.print(
        string.format(
            "TIME: %.1f",
            self.survivalTime
        ),
        20,
        45
    )
end

-- GAME OVER 화면
function GameManager:drawGameOver()
    if self.state ~= "gameover" then
        return
    end

    local screenWidth =
        love.graphics.getWidth()

    local screenHeight =
        love.graphics.getHeight()

    -- 반투명 배경
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
        screenWidth,
        screenHeight
    )

    -- GAME OVER 제목
    love.graphics.setColor(1, 1, 1)

    love.graphics.printf(
        "GAME OVER",
        0,
        screenHeight / 2 - 50,
        screenWidth,
        "center"
    )

    -- 최종 생존 시간
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
