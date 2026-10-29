local Player = require("src.player")
local EnemyManager = require("src.enemy_manager")
local Weapon = require("src.weapon")
local GameManager = require("src.game_manager")
local ExperienceManager = require("src.experience_manager")
local UpgradeManager = require("src.upgrade_manager")

-- 게임 객체
local player
local enemyManager
local weapon
local gameManager
local experienceManager
local upgradeManager

function love.load()
    love.graphics.setBackgroundColor(
        0.08, 0.09, 0.12
    )

    player = Player:new()
    enemyManager = EnemyManager:new()
    weapon = Weapon:new()

    gameManager = GameManager:new()
    experienceManager = ExperienceManager:new()
    upgradeManager = UpgradeManager:new()
end

function love.update(dt)
    if not gameManager:isPlaying() then
        return
    end

    player:update(dt)

    enemyManager:update(dt, player)
    if player.dead then
        gameManager:update(
            dt,
            player,
            experienceManager,
            upgradeManager
        )
        return
    end

    weapon:update(
        dt,
        player,
        enemyManager.enemies
    )

    -- 발사체에 맞아 사망한 적을 같은 프레임에 정리
    enemyManager:removeDeadEnemies(experienceManager)

    gameManager:update(
        dt,
        player,
        experienceManager,
        upgradeManager
    )
end

function love.draw()
    -- 1. 플레이어
    player:draw()
    -- 2. 적
    enemyManager:draw()
    -- 3. 발사체
    weapon:draw()
    -- 4. 체력 및 생존 시간
    gameManager:drawHUD(player)
    -- 5. 레벨 및 경험치
    experienceManager:draw()
    -- 6. 레벨업 선택 화면
    if gameManager:isLevelUp() then
        upgradeManager:draw()
    end
    -- 7. 게임 종료 화면
    if gameManager:isGameOver() then
        gameManager:drawGameOver()
    end
end

function love.keypressed(key)
    -- ESC: 게임 종료
    if key == "escape" then
        love.event.quit()
        return
    end

    -- LEVEL UP 상태
    if gameManager:isLevelUp() then

        -- 숫자 1, 2, 3만 허용
        local choiceIndex = tonumber(key)

        if choiceIndex
            and choiceIndex >= 1
            and choiceIndex <= 3 then

            gameManager:selectUpgrade(
                choiceIndex,
                player,
                weapon,
                experienceManager,
                upgradeManager
            )
        end

        return
    end
end