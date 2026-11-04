local H=require('src.hexmap')
local W=require('src.world')
local C=require('src.camera')
local map,shapes,buttons,selected,hover
local allied,enemy=25,25
local status='Click a tile, object, wall or door to inspect.'
local function rebuild() map=W.new(allied,enemy);selected=nil;hover=nil end
local function inside(x,y,p)
 local hit=false;local j=#p-1
 for i=1,#p,2 do
  if (p[i+1]>y)~=(p[j+1]>y) and x<(p[j]-p[i])*(y-p[i+1])/(p[j+1]-p[i+1])+p[i] then hit=not hit end
  j=i
 end
 return hit
end
local function scene()
 shapes={}
 local function poly(points,color,owner,layer)
  local p,depth,z={},0,0
  for _,v in ipairs(points) do
   local x,y,d=C.project(v[1],v[2],v[3]);p[#p+1]=x;p[#p+1]=y;depth=depth+d;z=z+v[3]
  end
  shapes[#shapes+1]={points=p,color=color,owner=owner,depth=depth/#points,layer=layer or 0,z=z/#points}
 end
 for _,t in ipairs(map.tiles) do
  local v=H.vertices(t,1);local top={}
  for i=1,12,2 do top[#top+1]={v[i],v[i+1],t.height} end
  -- Draw only exposed vertical terrain sides, including the depressed ground.
  local dirs={{1,0},{0,1},{-1,1},{-1,0},{0,-1},{1,-1}}
  for i,d in ipairs(dirs) do
   local n=H.get(map,t.q+d[1],t.r+d[2]);local bottom=n and n.height or -0.65
   if t.height>bottom then
    local j=i==6 and 1 or i*2+1
    poly({{v[i*2-1],v[i*2],bottom},{v[j],v[j+1],bottom},{v[j],v[j+1],t.height},{v[i*2-1],v[i*2],t.height}}, {0.23,0.25,0.27},t)
   end
  end
  local color=t.side==1 and {0.19,0.36,0.43} or {0.43,0.27,0.27}
  if t.height>0 then color={0.40,0.45,0.28} elseif t.height<0 then color={0.22,0.29,0.35} end
  if t.building then color={0.50,0.46,0.37} end
  poly(top,color,t,1)
  local x,y=H.center(t,1)
  if t.object=='tree' then
   poly({{x-.10,y,t.height},{x+.10,y,t.height},{x+.10,y,t.height+1.7},{x-.10,y,t.height+1.7}},{0.37,0.23,0.12},t,2)
   -- Camera-facing silhouette keeps the natural object readable in all three views.
   local a=math.rad(-90+C.index*45);local dx,dy=math.cos(a)*.68,-math.sin(a)*.68
   poly({{x-dx,y-dy,t.height+1},{x+dx,y+dy,t.height+1},{x,y,t.height+2.5}},{0.12,0.40,0.24},t,3)
  elseif t.object=='rock' then
   poly({{x-.55,y-.25,t.height},{x+.50,y-.2,t.height},{x+.35,y+.35,t.height+.65},{x-.2,y+.25,t.height+.8}},{0.52,0.56,0.60},t,2)
  elseif t.object=='grass' then
   for k=-1,1 do
    poly({{x+k*.2-.07,y,t.height},{x+k*.2+.07,y,t.height},{x+k*.2,y,t.height+.4}},{0.37,0.65,0.32},t,2)
   end
  end
 end
 for _,e in ipairs(map.edges) do
  if e.hp>0 then
   local ax,ay,bx,by=e.ax,e.ay,e.bx,e.by
   if e.open then
    local dx,dy=bx-ax,by-ay;bx,by=ax-dy,ay+dx
   end
   local z=e.tile.height
   poly({{ax,ay,z},{bx,by,z},{bx,by,z+e.height},{ax,ay,z+e.height}},e.kind=='door' and {0.57,0.34,0.16} or {0.64,0.65,0.69},e,4)
  else
   local z=e.tile.height+.025
   poly({{e.ax,e.ay,z},{e.bx,e.by,z},{e.bx,e.by,z+.08},{e.ax,e.ay,z+.08}},{0.45,0.37,0.31},e,2)
  end
 end
 table.sort(shapes,function(a,b)
  -- Terrain first; upright props use their ground depth to cover tiles behind them.
  if (a.layer<=1)~=(b.layer<=1) then return a.layer<=1 end
  if math.abs(a.depth-b.depth)>.00001 then return a.depth<b.depth end
  return a.layer<b.layer
 end)
end
local function buildUI()
 buttons={}
 local function b(x,y,w,text,action) buttons[#buttons+1]={x=x,y=y,w=w,h=32,text=text,action=action} end
 b(25,90,35,'-',function() allied=math.max(10,allied-1);rebuild() end)
 b(170,90,35,'+',function() allied=math.min(50,allied+1);rebuild() end)
 b(235,90,35,'-',function() enemy=math.max(10,enemy-1);rebuild() end)
 b(380,90,35,'+',function() enemy=math.min(50,enemy+1);rebuild() end)
 b(445,90,85,'MIN 20',function() allied,enemy=10,10;rebuild() end)
 b(540,90,90,'MAX 100',function() allied,enemy=50,50;rebuild() end)
 b(640,90,80,'RESET',rebuild)
 b(735,90,90,'OPEN [E]',function() if selected and selected.kind then W.toggle(selected) end end)
 b(840,90,130,'DAMAGE [X]',function() if selected and selected.kind then W.damage(selected,25) end end)
 local w,h=love.graphics.getDimensions()
 b(20,h/2,70,'< -45',function() C.turn(-1) end)
 b(w-90,h/2,70,'+45 >',function() C.turn(1) end)
end
local function refresh()
 C.fit(map,love.graphics.getDimensions());scene();buildUI()
end
local function pick(x,y)
 for i=#shapes,1,-1 do if inside(x,y,shapes[i].points) then return shapes[i].owner end end
end
function love.load()
 love.graphics.setBackgroundColor(.055,.065,.09)
 love.graphics.setFont(love.graphics.newFont(15));rebuild();refresh()
end
function love.resize() refresh() end
function love.update() local x,y=love.mouse.getPosition();hover=pick(x,y) end
function love.mousepressed(x,y,button)
 if button~=1 then return end
 for _,b in ipairs(buttons) do
  if x>=b.x and x<=b.x+b.w and y>=b.y and y<=b.y+b.h then b.action();refresh();return end
 end
 selected=pick(x,y)
end
function love.keypressed(k)
 if k=='q' or k=='left' then C.turn(-1)
 elseif k=='d' or k=='right' then C.turn(1)
 elseif k=='0' then C.index=0
 elseif k=='r' then rebuild()
 elseif k=='e' and selected and selected.kind then W.toggle(selected)
 elseif k=='x' and selected and selected.kind then W.damage(selected,25)
 elseif k=='escape' then selected=nil end
 refresh()
end
function love.draw()
 local g=love.graphics
 for _,s in ipairs(shapes) do
  g.setColor(s.color);g.polygon('fill',s.points)
  g.setLineWidth(1);g.setColor(.06,.09,.12,.65);g.polygon('line',s.points)
  if s.owner==selected then g.setColor(1,.83,.3);g.setLineWidth(2);g.polygon('line',s.points) end
 end
 g.setColor(.94,.96,1);g.print('impossibility Guild / TERRAIN & STRUCTURES',25,20)
 g.setColor(.63,.7,.8);g.print('Camera: '..C.index*45 ..' degrees | Q / D or side arrows | 0 = front | No turn cost',25,48)
 g.setColor(.6,.84,1);g.print('Allied '..allied,70,98)
 g.setColor(1,.68,.62);g.print('Enemy '..enemy,280,98)
 for _,b in ipairs(buttons) do
  g.setColor(b.y>150 and {.55,.12,.15} or {.16,.2,.28});g.rectangle('fill',b.x,b.y,b.w,b.h,5,5)
  g.setColor(.95,.96,1);g.printf(b.text,b.x,b.y+7,b.w,'center')
 end
 local info='Total '..#map.tiles..' | Blue: allied / Red: enemy / Olive: high / Dark: low / Beige: interior'
 g.setColor(.76,.81,.89);g.print(info,25,139)
 if selected then
  if selected.kind then status=selected.kind:upper()..' | HP '..selected.hp..'/'..selected.maxhp..' | '..(selected.hp==0 and 'DESTROYED / passage clear' or selected.open and 'OPEN' or 'CLOSED / blocks passage')
  else status='Tile '..selected.q..','..selected.r..' | Height '..selected.height..' | '..(selected.building and 'Building interior' or selected.object or 'Ground') end
 else status='Click a tile or a wall/door. E: open/close selected door. X: test damage (-25 HP).' end
 g.setColor(.9,.91,.95);g.print(status,25,g.getHeight()-62)
 g.setColor(.57,.65,.75);g.print('Map-only prototype | No units, combat, AI, damage modifiers or roof | R: rebuild',25,g.getHeight()-34)
end
