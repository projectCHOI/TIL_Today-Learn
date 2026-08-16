function love.load()
    message = "Hello, LÖVE2D!"
end

function love.draw()
    love.graphics.print(message, 170, 170)
end