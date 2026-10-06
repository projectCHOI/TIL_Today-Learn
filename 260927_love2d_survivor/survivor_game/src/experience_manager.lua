local ExperienceManager = {}

function ExperienceManager:new()
    local manager = {
        -- 현재 레벨
        level = 1,

        -- 현재 경험치
        exp = 0,

        -- 다음 레벨까지 필요한 경험치
        expToNextLevel = 5,

        -- 레벨업 발생 여부
        levelUpPending = false
    }

    setmetatable(manager, self)
    self.__index = self

    return manager
end


function ExperienceManager:addExp(amount)
    -- 잘못된 값 방지
    if amount <= 0 then
        return
    end

    -- 경험치 획득
    self.exp = self.exp + amount

    -- 레벨업 판정
    self:checkLevelUp()
end


function ExperienceManager:checkLevelUp()
    -- 한 번에 많은 경험치를 얻었을 경우
    -- 여러 레벨이 오를 수 있도록 while 사용
    while self.exp >= self.expToNextLevel do

        -- 필요한 경험치 차감
        self.exp =
            self.exp - self.expToNextLevel

        -- 레벨 증가
        self.level =
            self.level + 1

        -- 레벨업 발생 표시
        self.levelUpPending = true

        -- 다음 레벨 필요 경험치 증가
        self.expToNextLevel =
            math.floor(
                self.expToNextLevel * 1.4
            )
    end
end


function ExperienceManager:hasLevelUp()
    return self.levelUpPending
end


function ExperienceManager:consumeLevelUp()
    self.levelUpPending = false
end

function ExperienceManager:draw()
    local screenWidth =
        love.graphics.getWidth()

    -- 레벨 표시
    love.graphics.setColor(
        1,
        1,
        1
    )

    love.graphics.print(
        "LEVEL: " .. self.level,
        20,
        70
    )

    -- 경험치 바 설정
    local barX = 20
    local barY = 100
    local barWidth = 250
    local barHeight = 16

    -- 경험치 비율
    local expRatio =
        self.exp / self.expToNextLevel

    -- 경험치 바 배경
    love.graphics.setColor(
        0.2,
        0.2,
        0.2
    )

    love.graphics.rectangle(
        "fill",
        barX,
        barY,
        barWidth,
        barHeight
    )

    -- 현재 경험치
    love.graphics.setColor(
        0.3,
        0.7,
        1
    )

    love.graphics.rectangle(
        "fill",
        barX,
        barY,
        barWidth * expRatio,
        barHeight
    )

    -- 경험치 숫자
    love.graphics.setColor(
        1,
        1,
        1
    )

    love.graphics.print(
        self.exp
            .. " / "
            .. self.expToNextLevel,
        barX + barWidth + 10,
        barY - 2
    )
end

return ExperienceManager
