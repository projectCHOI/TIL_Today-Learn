local View={}
local canvas
local scale=2

function View.resize(width,height)
 local w=math.max(1,math.ceil(width/scale))
 local h=math.max(1,math.ceil(height/scale))
 if canvas and canvas:getWidth()==w and canvas:getHeight()==h then return end
 canvas=love.graphics.newCanvas(w,h,{dpiscale=1})
 canvas:setFilter('nearest','nearest')
end

function View.begin()
 local g=love.graphics
 g.push('all')
 g.setCanvas(canvas)
 g.clear(1,1,1,1)
 g.origin()
 g.scale(1/scale)
end

function View.finish()
 local g=love.graphics
 g.setCanvas()
 g.pop()
 g.setColor(1,1,1,1)
 g.draw(canvas,0,0,0,scale,scale)
end

return View
