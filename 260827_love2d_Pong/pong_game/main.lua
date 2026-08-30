local WINDOW_WIDTH = 800
local WINDOW_HEIGHT = 600

-- 플레이어 패들
local player = {
    x = 40,
    y = 250,
    width = 15,
    height = 100,
    speed = 300
}

-- AI 패들
local ai = {
    x = 745,
    y = 250,
    width = 15,
    height = 100,
    speed = 140
}

-- 공
local ball = {
    x = 390,
    y = 290,
    width = 20,
    height = 20,

    dx = 120,
    dy = 180
}
