local UpgradeManager = {}

function UpgradeManager:new()
    local manager = {
        -- 현재 레벨업 선택 화면이 활성화되어 있는지
        active = false,

        -- 현재 표시할 강화 선택지
        choices = {}
    }

    setmetatable(manager, self)
    self.__index = self

    return manager
end


function UpgradeManager:open()
    self.active = true

    -- 현재 단계에서는 항상 3종류의 강화를 표시
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
end


function UpgradeManager:isActive()
    return self.active
end


function UpgradeManager:select(
    choiceIndex,
    player,
    weapon
)
    if not self.active then
        return
    end

    local choice =
        self.choices[choiceIndex]

    if not choice then
        return
    end


    -- 공격력 강화
    if choice.type == "damage" then
        weapon.damage =
            weapon.damage + 1


    -- 공격 속도 강화
    elseif choice.type == "attackSpeed" then
        weapon.attackInterval =
            weapon.attackInterval * 0.9

        -- 지나치게 빨라지는 것을 방지
        weapon.attackInterval =
            math.max(
                0.15,
                weapon.attackInterval
            )


    -- 이동 속도 강화
    elseif choice.type == "moveSpeed" then
        player.speed =
            player.speed + 20
    end


    -- 선택 완료
    self.active = false
    self.choices = {}
end
