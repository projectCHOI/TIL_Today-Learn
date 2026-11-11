local H=require('src.grid')
local W=require('src.world')
local C=require('src.camera')
local PixelView=require('src.pixel_view')
local Battle=require('src.skirmish')
local battle,warriorSelected,message
local jumpTime=0
local map,shapes,buttons,selected,hover
local helpOpen=false
local objectNames={tree='나무',rock='바위',grass='풀'}
local function rebuild()
 map=W.new(nil,nil,true)
 battle=Battle.new(map)
 warriorSelected=false
 message=nil
 jumpTime=0
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
local function setView(index)
 C.top=index==nil
 if index~=nil then C.index=index end
end

local function unitPosition(tile)
 local x,y=H.center(tile,1)
 return C.project(x,y,tile.height)
end

local function dicePanel()
 return love.graphics.getWidth()-195,155
end

local function drawAxe(g,x,y)
 x=2*math.floor(x/2)
 y=2*math.floor(y/2)
 g.setColor(.17,.12,.09)
 g.rectangle('fill',x-4,y-18,8,34)
 g.rectangle('fill',x-16,y-18,16,18)
 g.setColor(.66,.43,.20)
 g.rectangle('fill',x-2,y-16,4,30)
 g.setColor(.75,.81,.84)
 g.rectangle('fill',x-14,y-16,12,14)
 g.setColor(.94,.97,.98)
 g.rectangle('fill',x-14,y-14,4,10)
end

local function buildUI()
 buttons={}
 local function add(x,width,text,action,active)
  buttons[#buttons+1]={x=x,y=65,w=width,h=34,text=text,action=action,active=active}
 end
 add(25,115,'위에서 보기',function() setView(nil) end,C.top)
 add(148,92,'왼쪽 45°',function() setView(-1) end,not C.top and C.index==-1)
 add(248,78,'정면',function() setView(0) end,not C.top and C.index==0)
 add(334,102,'오른쪽 45°',function() setView(1) end,not C.top and C.index==1)
 add(444,106,'조작 안내',function() helpOpen=not helpOpen end,helpOpen)
 if selected and selected.kind and selected.hp>0 then
  if selected.kind=='door' then
   add(575,104,selected.open and '문 닫기' or '문 열기',function() W.toggle(selected) end)
  end
  add(687,108,'시험 타격',function() W.damage(selected,25) end)
 end
end
local function refresh()
 local w,h=love.graphics.getDimensions()
 PixelView.resize(w,h)
 C.fit(map,w-190,h);scene();buildUI();hover=nil
end
local function pick(x,y)
 for i=#shapes,1,-1 do if inside(x,y,shapes[i].points) then return shapes[i].owner end end
end
function love.load()
 love.graphics.setBackgroundColor(1,1,1)
 love.graphics.setFont(love.graphics.newFont('assets/fonts/SLEIGothicOTF.otf',15))
 rebuild();refresh()
end
function love.resize() refresh() end
local function inMapArea(y)
 return y>=125 and y<love.graphics.getHeight()-70
end

function love.update(dt)
 jumpTime=math.max(0,jumpTime-(dt or 0))
 local x,y=love.mouse.getPosition()
 hover=not helpOpen and inMapArea(y) and pick(x,y) or nil
end
function love.mousepressed(x,y,button)
 if button==2 then
  if helpOpen then helpOpen=false else selected=nil;warriorSelected=false;message=nil end
  buildUI()
  return
 end
 if button~=1 then return end
 for _,b in ipairs(buttons) do
  if x>=b.x and x<b.x+b.w and y>=b.y and y<b.y+b.h then
   b.action()
   refresh()
   return
  end
 end
 if helpOpen then return end
 local panelX,panelY=dicePanel()
 if x>=panelX and x<panelX+170 and y>=panelY and y<panelY+285 then
  if x>=panelX+10 and x<panelX+160 and y>=panelY+45 and y<panelY+95 and warriorSelected and not battle.rolled and not battle.won then
   battle:roll(love.math.random)
   message=nil
  elseif x>=panelX+10 and x<panelX+160 and y>=panelY+142 and y<panelY+178 and battle.rolled and not battle.won then
   battle:endTurn()
   message='새 턴입니다. 주사위를 굴리세요.'
  elseif x>=panelX+10 and x<panelX+160 and y>=panelY+184 and y<panelY+220 and warriorSelected and map.pulleys[battle.warrior] and not battle.won then
   message=battle:act(map.pulleys[battle.warrior],true)
  elseif x>=panelX+10 and x<panelX+160 and y>=panelY+230 and y<panelY+266 then
   rebuild()
   refresh()
  end
  return
 end
 if not inMapArea(y) then return end
 local target=pick(x,y)
 local ux,uy=unitPosition(battle.warrior)
 local tx,ty=unitPosition(battle.target)
 if battle.hp>0 and math.abs(x-tx)<=12 and math.abs(y-ty)<=12 then target=battle.target end
 if target==battle.warrior or (math.abs(x-ux)<=18 and math.abs(y-uy)<=30) then
  warriorSelected=true
  selected=nil
  message=nil
  jumpTime=.28
 elseif target and not target.kind and warriorSelected then
  message=battle:act(target,false)
  selected=nil
 else
  selected=target
  warriorSelected=false
  message=nil
 end
 buildUI()
end
function love.keypressed(k,_,isRepeat)
 if isRepeat then return end
 if k=='q' then
  helpOpen=not helpOpen
 elseif k=='escape' then
  if helpOpen then helpOpen=false else selected=nil;warriorSelected=false;message=nil end
 elseif k=='w' then setView(nil)
 elseif k=='a' then setView(-1)
 elseif k=='s' then setView(0)
 elseif k=='d' then setView(1)
 else return
 end
 refresh()
end

local function describe(target)
 if not target then return '칸이나 시설물을 선택하세요.' end
 if target.kind then
  local state=target.hp==0 and '파괴됨' or (target.open and '열림' or '닫힘')
  local name=target.kind=='door' and ('문 · '..state) or (target.hp==0 and '벽 · 파괴됨' or '벽')
  return name..'   |   내구도 '..target.hp..'/'..target.maxhp
 end
 local terrain=target.building and '건물 내부' or objectNames[target.object] or '평지'
 if target.height~=0 and not target.object then terrain=target.height>0 and '고지대' or '저지대' end
 if target.flag then terrain=target.flag==1 and '아군 깃발' or '적군 깃발' end
 if map.pulleys[target] then terrain='도르래' end
 return terrain..'   |   좌표 ('..target.q..', '..target.r..')   |   높이 '..target.height
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
 local ux,uy=unitPosition(battle.warrior)
 local hop=math.sin(jumpTime/.28*math.pi)*10
 if warriorSelected then
  g.setColor(.16,.48,.84)
  g.rectangle('fill',ux-13,uy+12,26,4)
 end
 if battle.hp>0 then
  local tx,ty=unitPosition(battle.target)
  g.setColor(.59,.16,.12)
  g.rectangle('fill',tx-12,ty-12,24,24)
  g.setColor(.95,.75,.59)
  g.rectangle('fill',tx-7,ty-7,14,14)
  g.setColor(.59,.16,.12)
  g.rectangle('fill',tx-3,ty-3,6,6)
 end
 drawAxe(g,ux,uy-hop)
 PixelView.finish()
 for _,shape in ipairs(shapes) do
  if shape.owner==selected and (selected.kind or shape.layer==1) then
   g.setColor(.08,.10,.08)
   g.setLineWidth(2)
   g.polygon('line',shape.points)
  end
 end
 g.setColor(0,0,0)
 g.print('불가능 길드 / 폐허 초소',25,22)
 g.print('144칸 · 12 × 12',g.getWidth()-165,22)
 for _,button in ipairs(buttons) do
  g.setColor(button.active and {.79,.88,.80} or {.94,.94,.93})
  g.rectangle('fill',button.x,button.y,button.w,button.h,5,5)
  g.setColor(0,0,0)
  g.printf(button.text,button.x,button.y+8,button.w,'center')
 end
 local panelX,panelY=dicePanel()
 g.setColor(.95,.95,.94)
 g.rectangle('fill',panelX,panelY,170,285,6,6)
 local function panelButton(offset,label,enabled)
  g.setColor(enabled and {.79,.88,.80} or {.89,.89,.88})
  g.rectangle('fill',panelX+10,panelY+offset,150,offset==45 and 50 or 36,4,4)
  g.setColor(0,0,0)
  local labelInset=offset==45 and 45 or 10
  g.printf(label,panelX+labelInset,panelY+offset+8,160-labelInset,'center')
 end
 g.setColor(0,0,0)
 g.print('아군 행동',panelX+12,panelY+14)
 panelButton(45,battle.rolled and ('주사위 '..battle.rolled) or '주사위 굴리기',warriorSelected and not battle.rolled and not battle.won)
 g.setColor(1,1,1)
 g.rectangle('fill',panelX+18,panelY+57,24,24,3,3)
 g.setColor(0,0,0)
 local face=battle.rolled
 if face then
  local cx,cy=panelX+30,panelY+69
  if face%2==1 then g.circle('fill',cx,cy,2) end
  if face>=2 then g.circle('fill',cx-6,cy-6,2);g.circle('fill',cx+6,cy+6,2) end
  if face>=4 then g.circle('fill',cx+6,cy-6,2);g.circle('fill',cx-6,cy+6,2) end
  if face==6 then g.circle('fill',cx-6,cy,2);g.circle('fill',cx+6,cy,2) end
 else
  g.printf('?',panelX+18,panelY+59,24,'center')
 end
 g.print('남은 행동 '..battle.remaining..'/'..(battle.rolled or 0),panelX+12,panelY+105)
 panelButton(142,'턴 종료',battle.rolled and not battle.won)
 if map.pulleys[battle.warrior] then
  panelButton(184,'도르래 이용',warriorSelected and not battle.won)
 end
 panelButton(230,'다시 시작',true)
 local y=g.getHeight()-68
 g.setColor(.96,.96,.95)
 g.rectangle('fill',25,y,g.getWidth()-50,46,5,5)
 g.setColor(0,0,0)
 local label=selected and '선택  /  ' or ''
 local detail=describe(selected or hover)
 if warriorSelected then detail='도끼 전사  /  인접한 칸은 이동, 인접한 표적은 공격' end
 if hover==battle.target and battle.hp>0 and not message then detail='시험 표적  /  체력 '..battle.hp..'/30' end
 g.print(message or label..detail,41,y+13)
 if helpOpen then
  local x=g.getWidth()-380
  g.setColor(1,1,1)
  g.rectangle('fill',x,113,355,195,6,6)
  g.setColor(.2,.2,.2)
  g.setLineWidth(1)
  g.rectangle('line',x,113,355,195,6,6)
  g.setColor(0,0,0)
  local help={
   '도끼를 선택한 뒤 오른쪽 주사위를 클릭하세요.',
   '인접한 칸을 클릭해 이동하거나 표적을 공격하세요.',
   '좌클릭  /  칸 또는 시설물 선택',
   '우클릭 또는 Esc  /  선택 해제 또는 안내 닫기',
   'Q  /  조작 안내 열기·닫기',
   'W  /  위에서 보기    S  /  정면',
   'A  /  왼쪽 45°    D  /  오른쪽 45°'
  }
  for i,line in ipairs(help) do g.print(line,x+14,124+(i-1)*25) end
 end
end
