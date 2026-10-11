local UpgradeManager = {}

function UpgradeManager:new()
    local manager = {
        -- 강화 선택 화면 활성화 여부
        active = false,

        -- 현재 강화 선택지
        choices = {}
    }

    setmetatable(manager, self)
    self.__index = self

    return manager
end

-- 강화 선택 화면 열기
function UpgradeManager:open()
    -- 이미 열려 있다면 중복 실행 방지
    if self.active then
        return false
    end

    self.active = true

    -- 현재는 고정된 3가지 강화
    self.choices = {
        {
            name = "POWER UP",
            description = "Projectile damage +1",
            type = "damage"
        },

        {
            name = "ATTACK SPEED",
            description = "Attack interval -10%",
            type = "attackSpeed"
        },

        {
            name = "MOVE SPEED",
            description = "Movement speed +20",
            type = "moveSpeed"
        }
    }

    return true
end

-- 강화 선택 화면 활성화 확인
function UpgradeManager:isActive()
    return self.active
end

-- 강화 선택 및 적용
function UpgradeManager:select(
    choiceIndex,
    player,
    weapon
)
    -- 선택 화면이 열려 있지 않으면 실패
    if not self.active then
        return false
    end

    -- 선택 번호가 정수가 아니면 실패
    if type(choiceIndex) ~= "number"
        or choiceIndex % 1 ~= 0 then
        return false
    end

    local choice = self.choices[choiceIndex]

    -- 존재하지 않는 선택지
    if not choice then
        return false
    end

    -- 강화 대상 확인
    if not player or not weapon then
        return false
    end

    -- 공격력 강화
    if choice.type == "damage" then
        if type(weapon.damage) ~= "number" then
            return false
        end

        weapon.damage = weapon.damage + 1

    -- 공격 속도 강화
    elseif choice.type == "attackSpeed" then
        if type(weapon.attackInterval) ~= "number" then
            return false
        end

        weapon.attackInterval = math.max(
            0.15,
            weapon.attackInterval * 0.9
        )

    -- 이동 속도 강화
    elseif choice.type == "moveSpeed" then
        if type(player.speed) ~= "number" then
            return false
        end

        player.speed = player.speed + 20

    else
        return false
    end

    -- 강화 적용 완료
    self.active = false
    self.choices = {}

    return true
end

-- 강화 선택 화면 출력
function UpgradeManager:draw()
    if not self.active then
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
    -- 제목
    love.graphics.setColor(1, 1, 1)

    love.graphics.printf(
        "LEVEL UP!",
        0,
        150,
        screenWidth,
        "center"
    )
    -- 강화 선택지
    for i, choice in ipairs(self.choices) do
        local y = 230 + (i - 1) * 100

        love.graphics.printf(
            i .. ". " .. choice.name,
            0,
            y,
            screenWidth,
            "center"
        )

        love.graphics.printf(
            choice.description,
            0,
            y + 25,
            screenWidth,
            "center"
        )
    end
    -- 조작 안내
    love.graphics.printf(
        "Press 1, 2, or 3",
        0,
        550,
        screenWidth,
        "center"
    )
end

return UpgradeManager
