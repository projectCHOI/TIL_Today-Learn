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


-- ==========================================
-- Survivor Game
-- main.lua
-- ==========================================

-- 모듈 불러오기
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


-- ==========================================
-- 게임 초기화
-- ==========================================

function love.load()
    -- 배경색
    love.graphics.setBackgroundColor(
        0.08, 0.09, 0.12
    )

    -- 객체 생성
    player = Player:new()
    enemyManager = EnemyManager:new()
    weapon = Weapon:new()

    gameManager = GameManager:new()
    experienceManager = ExperienceManager:new()
    upgradeManager = UpgradeManager:new()
end


-- ==========================================
-- 게임 업데이트
-- ==========================================

function love.update(dt)

    -- PLAYING 상태가 아니면 전투 정지
    if not gameManager:isPlaying() then
        return
    end

    -- 1. 플레이어 이동 및 무적 시간
    player:update(dt)

    -- 2. 적 이동, 접촉 피해, 사망 적 제거
    enemyManager:update(
        dt,
        player,
        experienceManager
    )

    -- 적의 접촉 공격으로 플레이어가 사망했다면
    -- 무기 공격을 더 진행하지 않음
    if player.dead then
        gameManager:update(
            dt,
            player,
            experienceManager,
            upgradeManager
        )
        return
    end

    -- 3. 자동 공격 및 발사체 충돌
    weapon:update(
        dt,
        player,
        enemyManager.enemies
    )

    -- 4. 발사체 공격으로 죽은 적을
    -- 같은 프레임에서 제거하고 경험치 지급
    -- 다음 업데이트에서 EnemyManager가 처리하므로
    -- 여기서는 별도 제거하지 않음

    -- 5. 게임 상태 확인
    gameManager:update(
        dt,
        player,
        experienceManager,
        upgradeManager
    )
end


-- ==========================================
-- 화면 출력
-- ==========================================

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


-- ==========================================
-- 키보드 입력
-- ==========================================

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