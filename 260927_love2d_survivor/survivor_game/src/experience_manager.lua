
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