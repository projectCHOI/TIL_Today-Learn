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
