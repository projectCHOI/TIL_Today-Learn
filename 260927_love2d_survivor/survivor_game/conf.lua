function love.conf(t)
    -- 게임 정보
    t.identity = "survivor_game"
    t.version = "11.5"

    -- 게임 창 설정
    t.window.title = "Survivor Game"
    t.window.width = 1280
    t.window.height = 720
    t.window.resizable = false

    -- 콘솔 창
    t.console = true
end