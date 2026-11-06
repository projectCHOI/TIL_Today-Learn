local H=require('src.grid')
local W=require('src.world')
local C=require('src.camera')
local Movement=require('src.movement')
local preset=true
local unit,occupied,remaining,message
local moveLimit=4
local map,shapes,buttons,selected,hover
local allied,enemy=25,25
local status='타일이나 지형지물을 클릭해 정보를 확인하세요.'
local objectNames={tree='나무',rock='바위',grass='풀'}
local function rebuild()
 map=W.new(allied,enemy,preset)
 unit=map.start or map.tiles[1]
 occupied={}
 remaining=moveLimit
 selected=nil
 hover=nil
 message=nil
end
local function resizeMap(a,e)
 allied,enemy,preset=a,e,false
 rebuild()
end
local function move(to,usePulley)
 local cost,reason=Movement.step(map,unit,to,occupied,usePulley)
 if not cost then message=reason; return end
 if remaining<cost then message='이동력이 부족합니다. 스페이스로 보충하세요.'; return end
 unit=to
 remaining=remaining-cost
 selected=to
 message=usePulley and '도르래를 이용했습니다.' or '한 칸 이동했습니다.'
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
  local color=t.side==1 and {0.19,0.36,0.43} or {0.43,0.27,0.27}
  if t.height>0 then color={0.40,0.45,0.28} elseif t.height<0 then color={0.22,0.29,0.35} end
  if t.building then color={0.50,0.46,0.37} end
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
  if t==unit then marker(.31,.21,{.1,.65,1}) end
  if occupied[t] then marker(.31,.21,{.95,.28,.25}) end
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
 b(25,90,35,'-',function() resizeMap(math.max(10,allied-1),enemy) end)
 b(170,90,35,'+',function() resizeMap(math.min(50,allied+1),enemy) end)
 b(235,90,35,'-',function() resizeMap(allied,math.max(10,enemy-1)) end)
 b(380,90,35,'+',function() resizeMap(allied,math.min(50,enemy+1)) end)
 b(445,90,85,'최소 20',function() resizeMap(10,10) end)
 b(540,90,90,'최대 100',function() resizeMap(50,50) end)
 b(640,90,80,'초기화',rebuild)
 b(735,90,90,'개폐 [E]',function() if selected and selected.kind then W.toggle(selected) end end)
 b(840,90,130,'피해 [X]',function() if selected and selected.kind then W.damage(selected,25) end end)
 local w,h=love.graphics.getDimensions()
 b(20,h/2,70,'< -45',function() C.top=false;C.turn(-1) end)
 b(w-90,h/2,70,'+45 >',function() C.top=false;C.turn(1) end)
end
local function refresh()
 C.fit(map,love.graphics.getDimensions());scene();buildUI()
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
 if button==2 then
  local target=pick(x,y,C.top)
  if target and target.kind then target=nil end
  move(target,false)
  refresh()
  return
 end
 if button~=1 then return end
 message=nil
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
 elseif k=='f' then allied,enemy,preset=25,25,true;rebuild()
 elseif k=='space' then remaining=moveLimit;message='이동력을 보충했습니다.'
 elseif k=='p' then
  local destination=map.pulleys[unit]
  if destination then move(destination,true)
  else message='도르래가 있는 칸에서 이용할 수 있습니다.' end
 elseif k=='b' then
  local target=selected and not selected.kind and selected~=unit and selected or map.pulleys[unit]
  if target and target~=unit then
   occupied[target]=not occupied[target]
   message=occupied[target] and '시험 점유를 설정했습니다.' or '시험 점유를 해제했습니다.'
  end
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
 g.setColor(0,0,0);g.print(preset and '불가능 길드 / 폐허 초소' or '불가능 길드 / 가변 맵',25,20)
 local view=C.top and '탑다운' or ('경사 '..C.index*45 ..'도')
 g.setColor(0,0,0);g.print(view..' | T: 시점 전환 | Q / D: 경사 회전 | 이동력 '..remaining..'/'..moveLimit,25,48)
 if hover and not hover.kind then
  g.print('가리킨 칸까지 거리: '..H.distance(unit,hover)..'칸',550,48)
 end
 g.setColor(0,0,0);g.print('아군 '..allied,70,98)
 g.setColor(0,0,0);g.print('적군 '..enemy,280,98)
 for _,b in ipairs(buttons) do
  g.setColor(b.y>150 and {1,.65,.65} or {.9,.9,.9});g.rectangle('fill',b.x,b.y,b.w,b.h,5,5)
  g.setColor(0,0,0);g.printf(b.text,b.x,b.y+7,b.w,'center')
 end
 local info='전체 '..#map.tiles..'칸 | 파란 표식: 시험 유닛 / 빨간 표식: 점유 / 금색 표식: 도르래'
 g.setColor(0,0,0);g.print(info,25,139)
 if selected then
  if selected.kind then
   status=(selected.kind=='door' and '문' or '벽')..' | 내구도 '..selected.hp..'/'..selected.maxhp..' | '..(selected.hp==0 and '파괴됨 / 통과 가능' or selected.open and '열림' or '닫힘 / 통과 불가')
  else
   local heightName=selected.height>0 and '위 지역' or selected.height<0 and '아래 지역' or '평지'
   status='타일 '..selected.q..','..selected.r..' | '..heightName..' ('..selected.height..') | '..(selected.building and '건물 내부' or objectNames[selected.object] or '지면')
  end
 else status='타일·벽·문을 클릭하세요. E: 선택한 문 개폐 | X: 벽·문에 시험 피해 (내구도 -25)' end
 g.setColor(0,0,0);g.print(message or status,25,g.getHeight()-62)
 g.setColor(0,0,0);g.print('우클릭: 걷기 | P: 도르래 | B: 시험 점유 | 스페이스: 이동력 보충 | F: 폐허 초소 | R: 초기화',25,g.getHeight()-34)
end
