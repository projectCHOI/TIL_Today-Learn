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
