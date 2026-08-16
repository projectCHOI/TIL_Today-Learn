function love.load()
    player = {
        x = 215,
        y = 310,
        width = 50,
        height = 25,
        speed = 300
    }
end

function love.update(dt)
    if love.keyboard.isDown("left") then
        player.x = player.x - player.speed * dt
    end

    if love.keyboard.isDown("right") then
        player.x = player.x + player.speed * dt
    end

    if player.x < 0 then
        player.x = 0
    end

    if player.x + player.width > 480 then
        player.x = 480 - player.width
    end
end

function love.draw()
    love.graphics.setColor(0.2, 0.7, 1.0)

    love.graphics.rectangle(
        "fill",
        player.x,
        player.y,
        player.width,
        player.height
    )
end