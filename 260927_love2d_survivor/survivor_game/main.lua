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

    enemyManager:update(
        dt,
        player,
        experienceManager
    )
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

    gameManager:update(
        dt,
        player,
        experienceManager,
        upgradeManager
    )
end
