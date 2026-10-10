
local ExperienceManager = {}

function ExperienceManager:new()
    local manager = {
        -- 현재 레벨
        level = 1,

        -- 현재 경험치
        exp = 0,

        -- 다음 레벨에 필요한 경험치
        expToNextLevel = 5,

        -- 아직 선택하지 않은 레벨업 강화 횟수
        pendingLevelUps = 0
    }

    setmetatable(manager, self)
    self.__index = self

    return manager
end


-- 경험치 획득
function ExperienceManager:addExp(amount)
    if type(amount) ~= "number" or amount <= 0 then
        return
    end

    self.exp = self.exp + amount

    self:checkLevelUp()
end


-- 레벨업 판정
function ExperienceManager:checkLevelUp()
    while self.exp >= self.expToNextLevel do

        -- 경험치 차감
        self.exp =
            self.exp - self.expToNextLevel

        -- 레벨 증가
        self.level =
            self.level + 1

        -- 강화 선택 횟수 누적
        self.pendingLevelUps =
            self.pendingLevelUps + 1

        -- 다음 레벨 필요 경험치 증가
        self.expToNextLevel = math.max(
            1,
            math.floor(self.expToNextLevel * 1.4)
        )
    end
end

-- 선택하지 않은 강화가 있는지 확인
function ExperienceManager:hasLevelUp()
    return self.pendingLevelUps > 0
end

-- 남아 있는 강화 선택 횟수 확인
function ExperienceManager:getPendingLevelUps()
    return self.pendingLevelUps
end

-- 강화 선택 완료 시 한 번 차감
function ExperienceManager:consumeLevelUp()
    if self.pendingLevelUps > 0 then
        self.pendingLevelUps =
            self.pendingLevelUps - 1

        return true
    end

    return false
end

-- 경험치 UI
function ExperienceManager:draw()
    local barX = 20
    local barY = 100
    local barWidth = 250
    local barHeight = 16

    local expRatio =
        self.exp / self.expToNextLevel

    -- 레벨 표시
    love.graphics.setColor(1, 1, 1)

    love.graphics.print(
        "LEVEL: " .. self.level,
        20,
        70
    )

    -- 경험치 바 배경
    love.graphics.setColor(0.2, 0.2, 0.2)

    love.graphics.rectangle(
        "fill",
        barX,
        barY,
        barWidth,
        barHeight
    )

    -- 현재 경험치 바
    love.graphics.setColor(0.3, 0.7, 1)

    love.graphics.rectangle(
        "fill",
        barX,
        barY,
        barWidth * expRatio,
        barHeight
    )

    -- 경험치 수치
    love.graphics.setColor(1, 1, 1)

    love.graphics.print(
        self.exp .. " / " .. self.expToNextLevel,
        barX + barWidth + 10,
        barY - 2
    )
end

return ExperienceManager