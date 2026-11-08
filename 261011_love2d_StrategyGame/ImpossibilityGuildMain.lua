local H=require('src.grid')
local W=require('src.world')
local C=require('src.camera')
local PixelView=require('src.pixel_view')
local map,shapes,buttons,selected,hover
local objectNames={tree='나무',rock='바위',grass='풀'}
local function rebuild()
 map=W.new(nil,nil,true)
 selected=nil
 hover=nil
end
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
  for i=1,8,2 do top[#top+1]={v[i],v[i+1],t.height} end
  -- Draw only exposed vertical terrain sides, including the depressed ground.
  local dirs={{1,0},{0,1},{-1,0},{0,-1}}
  for i,d in ipairs(dirs) do
   local n=H.get(map,t.q+d[1],t.r+d[2]);local bottom=n and n.height or -0.65
   if not C.top and t.height>bottom then
    local j=i==4 and 1 or i*2+1
    poly({{v[i*2-1],v[i*2],bottom},{v[j],v[j+1],bottom},{v[j],v[j+1],t.height},{v[i*2-1],v[i*2],t.height}}, {0.23,0.25,0.27},t)
   end
  end
  local color=(t.q+t.r)%2==0 and {.69,.72,.57} or {.66,.69,.54}
  if t.height>0 then color=t.height==2 and {.49,.56,.34} or {.59,.64,.41} elseif t.height<0 then color={.44,.57,.59} end
  if t.building then color={.68,.59,.46} end
  poly(top,color,t,1)
  local x,y=H.center(t,1)
  local function marker(radius,z,color,layer)
   local points={}
   for i=0,5 do
    local angle=math.rad(i*60)
    points[#points+1]={x+radius*math.cos(angle),y+radius*math.sin(angle),t.height+z}
   end
   poly(points,color,t,layer or 3)
  end
  if map.pulleys[t] then marker(.47,.07,{.9,.66,.12},2) end
  if t.flag then
   local color=t.flag==1 and {.30,.68,1} or {1,.37,.32}
   local z=t.height+.04
   poly({{x-.43,y-.52,z},{x+.43,y-.52,z},{x+.43,y+.08,z},{x-.43,y+.08,z}},color,t,3)
   poly({{x-.49,y-.52,z},{x-.35,y-.52,z},{x-.35,y+.48,z},{x-.49,y+.48,z}},{.95,.94,.87},t,3)
  end
  if C.top then
   if t.object=='tree' then marker(.26,0,{.12,.4,.24})
   elseif t.object=='rock' then marker(.26,0,{.52,.56,.60})
   elseif t.object=='grass' then marker(.19,0,{.37,.65,.32}) end
  elseif t.object=='tree' then
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
  if C.top then
   local ax,ay,bx,by=e.ax,e.ay,e.bx,e.by
   if e.open then
    local dx,dy=bx-ax,by-ay;bx,by=ax-dy,ay+dx
   end
   local nx,ny=(by-ay)*.045,(ax-bx)*.045
   local color=e.hp==0 and {.44,.36,.30} or e.kind=='door' and {.57,.34,.16} or {.67,.69,.72}
   poly({{ax+nx,ay+ny,0},{bx+nx,by+ny,0},{bx-nx,by-ny,0},{ax-nx,ay-ny,0}},color,e,4)
  elseif e.hp>0 then
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
  if C.top and a.layer~=b.layer then return a.layer<b.layer end
  -- Terrain first; upright props use their ground depth to cover tiles behind them.
  if (a.layer<=1)~=(b.layer<=1) then return a.layer<=1 end
  if math.abs(a.depth-b.depth)>.00001 then return a.depth<b.depth end
  return a.layer<b.layer
 end)
end
local function buildUI()
 buttons={}
 local function b(x,y,w,text,action) buttons[#buttons+1]={x=x,y=y,w=w,h=32,text=text,action=action} end
 b(25,90,100,'시점 [T]',function() C.top=not C.top end)
 b(135,90,100,'초기화 [R]',rebuild)
 b(245,90,100,'개폐 [E]',function() if selected and selected.kind then W.toggle(selected) end end)
 b(355,90,100,'피해 [X]',function() if selected and selected.kind then W.damage(selected,25) end end)
 local w,h=love.graphics.getDimensions()
 b(20,h/2,70,'< -45',function() C.top=false;C.turn(-1) end)
 b(w-90,h/2,70,'+45 >',function() C.top=false;C.turn(1) end)
end
local function refresh()
 local w,h=love.graphics.getDimensions()
 PixelView.resize(w,h)
 C.fit(map,w,h);scene();buildUI();hover=nil
end
local function pick(x,y,tilesOnly)
 for i=#shapes,1,-1 do if (not tilesOnly or shapes[i].layer==1) and inside(x,y,shapes[i].points) then return shapes[i].owner end end
end
function love.load()
 love.graphics.setBackgroundColor(1,1,1)
 love.graphics.setFont(love.graphics.newFont('assets/fonts/SLEIGothicOTF.otf',15))
 rebuild();refresh()
end
function love.resize() refresh() end
function love.update() local x,y=love.mouse.getPosition();hover=pick(x,y,C.top) end
function love.mousepressed(x,y,button)
 if button~=1 then return end
 for _,b in ipairs(buttons) do
  if x>=b.x and x<=b.x+b.w and y>=b.y and y<=b.y+b.h then b.action();refresh();return end
 end
 selected=pick(x,y)
end
function love.keypressed(k)
 if k=='t' then C.top=not C.top
 elseif k=='q' or k=='left' then C.top=false;C.turn(-1)
 elseif k=='d' or k=='right' then C.top=false;C.turn(1)
 elseif k=='0' then C.top=false;C.index=0
 elseif k=='r' then rebuild()
 elseif k=='e' and selected and selected.kind then W.toggle(selected)
 elseif k=='x' and selected and selected.kind then W.damage(selected,25)
 elseif k=='escape' then selected=nil end
 refresh()
end
function love.draw()
 local g=love.graphics
 PixelView.begin()
 for _,shape in ipairs(shapes) do
  g.setColor(shape.color)
  g.polygon('fill',shape.points)
  g.setLineWidth(shape.layer==1 and 1 or 2)
  g.setColor(.18,.22,.16,.48)
  g.polygon('line',shape.points)
 end
 PixelView.finish()
 for _,shape in ipairs(shapes) do
  if shape.owner==selected and (selected.kind or shape.layer==1) then
   g.setColor(.08,.10,.08)
   g.setLineWidth(2)
   g.polygon('line',shape.points)
  end
 end
 g.setColor(0,0,0)
 g.print('불가능 길드 / 폐허 초소',25,20)
 local view=C.top and '탑다운' or ('경사 '..C.index*45 ..'도')
 g.print(view..' | T: 시점 전환 | Q / D: 경사 회전 | 0: 정면',25,48)
 if hover and not hover.kind then
  g.print('가리킨 칸: '..hover.q..', '..hover.r..' | 높이 '..hover.height,580,48)
 end
 for _,b in ipairs(buttons) do
  g.setColor(b.y>150 and {1,.65,.65} or {.9,.9,.9});g.rectangle('fill',b.x,b.y,b.w,b.h,5,5)
  g.setColor(0,0,0);g.printf(b.text,b.x,b.y+7,b.w,'center')
 end
 g.setColor(0,0,0)
 g.print('12 × 12 / 144칸 | 파란 깃발: 아군 | 붉은 깃발: 적군 | 금색: 도르래',25,139)
 local status='타일을 클릭해 높이와 지형을 확인하세요.'
 if selected and selected.kind then
  local state=selected.hp==0 and '파괴됨' or selected.open and '열림' or '닫힘'
  status=(selected.kind=='door' and '문' or '벽')..' | 내구도 '..selected.hp..'/'..selected.maxhp..' | '..state
 elseif selected then
  local terrain=selected.building and '건물 내부' or objectNames[selected.object] or '지면'
  if selected.flag then terrain=selected.flag==1 and '아군 깃발' or '적군 깃발' end
  status='타일 '..selected.q..', '..selected.r..' | 높이 '..selected.height..' | '..terrain
 end
 g.print(status,25,g.getHeight()-62)
 g.print('좌클릭: 조사 | E: 문 개폐 | X: 벽·문에 시험 피해 | R: 초기화',25,g.getHeight()-34)
end
