local H=require('src.grid')
local W=require('src.world')
local C=require('src.camera')
local PixelView=require('src.pixel_view')
local Battle=require('src.skirmish')
local Flow=require('src.game_flow')
local Items=require('src.items')
local Skills=require('src.skills')
local Combat=require('src.combat')
local Progress=require('src.progression')
local typeColors=require('src.type_colors')
local bags={}
local modal
local itemImages={}
local fonts
local battle,warriorSelected,message
local jumpTime=0
local map,shapes,buttons,selected,hover
local helpOpen=false
local moveColor={255/255,169/255,92/255}
local attackColor={255/255,46/255,45/255}
local pulleyColor={67/255,226/255,189/255}

local function actionHighlights()
 local colors={}
 if not warriorSelected or battle.won or battle.lost or (battle.rolled and battle.remaining==0 and not battle.pendingCharge) then return colors end
 for _,tile in ipairs(map.tiles) do
  if Skills[battle.skillId].charge then
   if battle:canCharge(tile) then colors[tile]={.2,.4,1} end
  elseif battle:canMove(tile,false) then colors[tile]=moveColor end
 end
 if Skills[battle.skillId].area then
  for tile in pairs(battle:areaCells()) do
   colors[tile]=Skills[battle.skillId].area=='center' and {.2,.4,1} or attackColor
  end
 end
 local landing=map.pulleys[battle.warrior]
 if landing and battle:canMove(landing,true) then
  colors[battle.warrior]=pulleyColor
  colors[landing]=pulleyColor
 end
 for _,edge in ipairs(map.edges) do
  if battle:canAttack(edge) then
   local other=edge.tile==battle.warrior and edge.neighbor or edge.tile
   colors[other]=attackColor
   colors[edge]=attackColor
  end
 end
 for _,enemy in ipairs(battle.enemies) do
  if battle:canAttack(enemy.tile) then colors[enemy.tile]=attackColor end
 end
 return colors
end
local objectNames={tree='나무',rock='바위',grass='풀'}
local function rebuild()
 map=W.new(nil,nil,true)
 local character=assert(Flow:getSelectedCharacter(),'출전 캐릭터를 선택하세요.')
 bags[character.name]=bags[character.name] or {}
 battle=Battle.new(map,character,bags[character.name])
 modal=nil
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
 return love.graphics.getWidth()-195,195
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

local function drawSpear(g,x,y)
 x=2*math.floor(x/2);y=2*math.floor(y/2)
 g.setColor(.17,.12,.09)
 g.rectangle('fill',x-3,y-12,6,30)
 g.setColor(.66,.43,.20)
 g.rectangle('fill',x-1,y-10,2,26)
 g.setColor(.75,.81,.84)
 g.polygon('fill',x,y-26,x-8,y-10,x+8,y-10)
 g.setColor(.94,.97,.98)
 g.polygon('fill',x,y-24,x-5,y-12,x,y-12)
end

local function drawBow(g,x,y)
 x=2*math.floor(x/2);y=2*math.floor(y/2)
 g.setColor(.38,.23,.10)
 g.rectangle('fill',x-10,y-17,6,6)
 g.rectangle('fill',x-5,y-13,6,8)
 g.rectangle('fill',x,y-7,6,14)
 g.rectangle('fill',x-5,y+5,6,8)
 g.rectangle('fill',x-10,y+11,6,6)
 g.setColor(.75,.81,.84)
 g.rectangle('fill',x-10,y-15,2,30)
 g.rectangle('fill',x-17,y-1,32,2)
 g.polygon('fill',x+18,y,x+10,y-5,x+10,y+5)
end

local function drawItemImage(g,file,x,y,size)
 if itemImages[file]==nil then
  local path='assets/images/'..file
  local ok,art=pcall(g.newImage,path)
  itemImages[file]=ok and art or false
  if ok then art:setFilter('nearest','nearest') end
 end
 local art=itemImages[file]
 if not art then return false end
 local w,h=art:getDimensions()
 local scale=math.min(size/w,size/h)
 g.setColor(1,1,1)
 g.draw(art,x-w*scale/2,y-h*scale/2,0,scale,scale)
 return true
end

local function itemModalLayout(w,h)
 local rows={}
 if modal=='bag' then
  for index,item in ipairs(Items) do
   local quantity=battle.bag[index] or 0
   if quantity>0 then
    rows[#rows+1]={item=item,label=item.name..' ×'..quantity..(item.revive and ' · 사망 시 자동 사용' or ''),
     button=item.heal and '사용' or '속성 적용',action=not item.revive and function()
      return battle:useItem(index)
     end or nil}
   end
  end
  if #rows==0 then rows[1]={label='가방이 비어 있습니다.'} end
 else
  local item=Items[battle.chests[modal].item]
  rows[1]={item=item,label=item.name..(item.heal and ' · 회복 '..item.heal or item.revive and ' · 사망 시 최대 체력으로 부활' or ''),
   button='획득',action=function()
    local result=battle:takeItem(modal)
    modal=nil
    return result
   end}
 end
 local height=110+#rows*27
 return rows,(w-460)/2,(h-height)/2,height
end

local function drawItemModal(g)
 local rows,x,y,h=itemModalLayout(g.getDimensions())
 g.setColor(0,0,0,.4)
 g.rectangle('fill',0,0,g.getDimensions())
 g.setColor(1,1,1)
 g.rectangle('fill',x,y,460,h,8,8)
 g.setColor(0,0,0)
 g.print(modal=='bag' and (battle.character.korean..'의 가방') or '상자 안의 아이템',x+18,y+13)
 local function drawButton(label,bx,by,bw)
  g.setColor(.86,.89,.93)
  g.rectangle('fill',bx,by,bw,24,4,4)
  g.setColor(0,0,0)
  g.printf(label,bx,by+3,bw,'center')
 end
 for i,row in ipairs(rows) do
  local ry=y+38+(i-1)*27
  if row.item and not drawItemImage(g,row.item.image,x+29,ry+12,24) then
   g.setColor(row.item.element and typeColors[row.item.element] or {.78,.23,.20})
   g.circle('fill',x+29,ry+12,7)
  end
  g.setColor(0,0,0)
  g.print(row.label,x+48,ry+3)
  if row.action then drawButton(row.button,x+335,ry,107) end
 end
 g.setColor(0,0,0)
 g.printf(message or '',x+18,y+h-64,424,'left')
 drawButton(modal=='bag' and '닫기' or '그대로 두기',x+335,y+h-35,107)
end

local function clickItemModal(x,y,button)
 if button==2 then modal=nil; return end
 if button~=1 then return end
 local rows,mx,my,h=itemModalLayout(love.graphics.getDimensions())
 if x<mx+335 or x>=mx+442 then return end
 if y>=my+h-35 and y<my+h-11 then modal=nil; return end
 for i,row in ipairs(rows) do
  local ry=my+38+(i-1)*27
  if row.action and y>=ry and y<ry+24 then
   message=row.action()
   return
  end
 end
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
 add(815,92,'가방',function() modal='bag'; message=nil end)
 for i,id in ipairs(battle:skillIds()) do
  local skill=Skills[id]
  local skillId=id
  local width=math.max(160,(love.graphics.getWidth()-240)/3)
  buttons[#buttons+1]={x=25+((i-1)%3)*width,y=105+math.floor((i-1)/3)*36,w=width-8,h=32,
   text=skill.name..' · 행동 '..skill.cost..' · 명중 '..skill.accuracy..'%',
   active=battle.skillId==id,action=function() battle:selectSkill(skillId);message=nil end}
 end
 if warriorSelected and not selected and Skills[battle.skillId].area=='center' then
  add(575,140,'기술 사용',function() message=battle:castArea(1) end)
 end
 if selected and battle:canInspect(selected) then
  add(575,140,battle.chests[selected].open and '상자 안을 본다' or '상자 열기',function()
   local chest,problem=battle:inspect(selected)
   message=problem
   if chest then modal=selected end
  end)
 end
 if warriorSelected and selected and selected.kind and not battle:actionError() then
  if battle:canToggleDoor(selected) then
   add(575,104,selected.open and '문 닫기' or '문 열기',function()
    message=battle:toggleDoor(selected)
   end)
  end
  if battle:canAttack(selected) then
   add(687,108,'공격',function() message=battle:attack(selected) end)
  end
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
 local fontPath='assets/fonts/SLEIGothicOTF.otf'
 fonts={body=love.graphics.newFont(fontPath,15),heading=love.graphics.newFont(fontPath,42)}
 love.graphics.setFont(fonts.body)
end
function love.resize()
 if Flow.screen=='battle' then refresh() end
end
local function inMapArea(y)
 return y>=180 and y<love.graphics.getHeight()-70
end

function love.update(dt)
 if Flow.screen~='battle' then return end
 jumpTime=math.max(0,jumpTime-(dt or 0))
 local x,y=love.mouse.getPosition()
 hover=not helpOpen and inMapArea(y) and pick(x,y) or nil
end
local function battleClick(x,y,button)
 if modal then clickItemModal(x,y,button); buildUI(); return end
 if button==2 then
  battle:cancelCharge()
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
   message=battle:endTurn()
  elseif x>=panelX+10 and x<panelX+160 and y>=panelY+184 and y<panelY+220 and warriorSelected and not battle:actionError() and battle:canMove(map.pulleys[battle.warrior],true) then
   message=battle:act(map.pulleys[battle.warrior],true)
   selected=nil
  elseif x>=panelX+10 and x<panelX+160 and y>=panelY+230 and y<panelY+266 then
   battle:cancelCharge()
   Flow.screen='retreat'
  end
  buildUI()
  return
 end
 if not inMapArea(y) then return end
 local target=pick(x,y)
 local ux,uy=unitPosition(battle.warrior)
 for _,enemy in ipairs(battle.enemies) do
  local tx,ty=unitPosition(enemy.tile)
  if enemy.health>0 and math.abs(x-tx)<=12 and math.abs(y-ty)<=12 then target=enemy.tile end
 end
 if warriorSelected and Skills[battle.skillId].area=='groups' and target and not target.kind and battle:areaGroupAt(target) then
  selected=nil
  message=battle:castArea(battle:areaGroupAt(target))
 elseif target and (target.kind or battle.chests[target]) then
  selected=target
  message=nil
 elseif target==battle.warrior or (math.abs(x-ux)<=18 and math.abs(y-uy)<=30) then
  warriorSelected=true
  selected=nil
  message=nil
  jumpTime=.28
 elseif target and warriorSelected then
  selected=nil
  for _,edge in ipairs(map.edges) do
   if not edge.open and battle:canAttack(edge)
    and ((edge.tile==battle.warrior and edge.neighbor==target)
     or (edge.neighbor==battle.warrior and edge.tile==target)) then
    selected=edge
    break
   end
  end
  if selected then
   message=nil
  elseif target==map.pulleys[battle.warrior] and battle:canMove(target,true)
   and not battle:canMove(target,false) then
   message=battle:act(target,true)
  else
   message=battle:act(target,false)
  end
 else
  selected=target
  warriorSelected=false
  message=nil
 end
 buildUI()
end
function love.mousepressed(x,y,button)
 if Flow.screen~='battle' then
  local action=Flow:mousepressed(x,y,button)
  if action=='start' then
   rebuild()
   helpOpen=false
   setView(nil)
   refresh()
  elseif Flow.screen=='battle' then
   refresh()
  end
  return
 end
 battleClick(x,y,button)
 if battle.won then Flow:finish(true,message)
 elseif battle.lost then Flow:finish(false,message) end
end

function love.keypressed(k,_,isRepeat)
 if isRepeat or Flow.screen~='battle' then return end
 if modal then
  if k=='escape' then modal=nil end
  return
 end
 if k=='q' then
  helpOpen=not helpOpen
 elseif k=='escape' then
  battle:cancelCharge()
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
 if Flow.screen~='battle' then
  Flow:draw(fonts)
  return
 end
 local g=love.graphics
 local colors=actionHighlights()
 PixelView.begin()
 for _,shape in ipairs(shapes) do
  local highlight=(shape.layer==1 or shape.owner.kind) and colors[shape.owner]
  g.setColor(highlight or shape.color)
  g.polygon('fill',shape.points)
  g.setLineWidth(shape.layer==1 and 1 or 2)
  g.setColor(.18,.22,.16,.48)
  g.polygon('line',shape.points)
 end
 for tile,chest in pairs(battle.chests) do
  local x,y=unitPosition(tile)
  local file=chest.open and 'mob_box_on.png' or 'mob_box_off.png'
  if not drawItemImage(g,file,x,y-7,27) then
   g.setColor(.42,.25,.12)
   g.rectangle('fill',x-10,y-15,20,14)
   g.setColor(chest.open and {.19,.12,.08} or {.94,.69,.22})
   g.rectangle('fill',x-8,y-14,16,chest.open and 6 or 3)
  end
 end
 local ux,uy=unitPosition(battle.warrior)
 local hop=math.sin(jumpTime/.28*math.pi)*10
 if warriorSelected then
  g.setColor(.16,.48,.84)
  g.rectangle('fill',ux-13,uy+12,26,4)
 end
 for _,enemy in ipairs(battle.enemies) do
  if enemy.health>0 then
   local tx,ty=unitPosition(enemy.tile)
   g.setColor(typeColors[enemy.element])
   g.rectangle('fill',tx-12,ty-12,24,24)
   g.setColor(1,1,1)
   g.rectangle('fill',tx-8,ty-17,16,3)
   g.setColor(.85,.12,.12)
   g.rectangle('fill',tx-8,ty-17,16*enemy.health/45,3)
  end
 end
 if battle.character.name=='Fulgrim' then drawSpear(g,ux,uy-hop)
 elseif battle.character.name=='Konrad' then drawBow(g,ux,uy-hop) else drawAxe(g,ux,uy-hop) end
 PixelView.finish()
 local group=warriorSelected and not selected and Skills[battle.skillId].area=='groups' and battle:areaGroupAt(hover)
 local area=group and battle:areaCells(group) or {}
 for _,shape in ipairs(shapes) do
  if shape.layer==1 and area[shape.owner] then
   g.setColor(.65,0,0);g.setLineWidth(3);g.polygon('line',shape.points)
  end
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
 g.print(battle.character.korean..' · '..Progress.label(battle.character),panelX+12,panelY+14)
 g.print('체력 '..battle.health..'/'..battle.maxHealth,panelX+12,panelY+122)
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
  panelButton(184,'도르래 이용',warriorSelected and not battle:actionError()
   and battle:canMove(map.pulleys[battle.warrior],true))
 end
 panelButton(230,'전투 포기',true)
 g.setColor(0,0,0)
 local progress=Progress.get(battle.character)
 for index,rule in ipairs(battle.character.promotions or {}) do
  g.print(Skills[rule.skill].name..' '..(progress.uses[rule.skill] or 0)..'/'..rule.count,
   panelX+12,panelY+278+index*22)
 end
 if battle.character.name=='Vulkan' and progress.rank>=2 then
  g.print('분노 위력 '..(30+30*battle.rageStacks),panelX+12,panelY+344)
 end
 local y=g.getHeight()-68
 g.setColor(.96,.96,.95)
 g.rectangle('fill',25,y,g.getWidth()-50,46,5,5)
 g.setColor(0,0,0)
 local label=selected and '선택  /  ' or ''
 local detail=describe(selected or hover)
 if warriorSelected and not selected then
  local types=battle.baseElement
  if battle.extraElement and battle.extraElement~=types then types=types..' / '..battle.extraElement end
  detail=battle.character.korean..'  /  '..types
  if Skills[battle.skillId].area=='center' then detail=detail..' · 파란 범위 확인 후 위쪽 기술 사용 클릭'
  elseif Skills[battle.skillId].area=='groups' then detail=detail..' · 빨간 구역의 칸을 클릭하세요.' end
 end
 if selected and battle.chests[selected] then
  detail=battle.chests[selected].open and '열린 상자' or '닫힌 상자'
 end
 local enemy=battle:enemyAt(hover)
 if enemy and not selected and not message then
  detail=enemy.name..' · 체력 '..enemy.health..'/45'
  if battle:canAttack(enemy.tile) then
   local low,high=Combat.preview(battle,enemy,Skills[battle.skillId])
   detail=detail..' · 예상 피해 '..low..'~'..high
   if battle.attackers[enemy] then detail=detail..' · 반격 대상' end
  end
 end
 g.print(message or label..detail,41,y+13)
 if helpOpen then
  local x=g.getWidth()-380
  g.setColor(1,1,1)
  g.rectangle('fill',x,113,355,245,6,6)
  g.setColor(.2,.2,.2)
  g.setLineWidth(1)
  g.rectangle('line',x,113,355,245,6,6)
  g.setColor(0,0,0)
  local help={
   '유닛을 선택한 뒤 오른쪽 주사위를 클릭하세요.',
   '주황 이동 / 빨강 공격 / 민트 도르래',
   '이동형 기술: 파란 칸 이동 후 빨간 칸 공격',
   '콘라드: 빨간 구역 클릭 / 바람은 위쪽 기술 사용',
   '문을 선택하면 화면 위에서 열기·닫기 또는 공격',
   '우클릭 또는 Esc  /  선택 해제 또는 안내 닫기',
   'Q  /  조작 안내 열기·닫기',
   'W  /  위에서 보기    S  /  정면',
   'A  /  왼쪽 45°    D  /  오른쪽 45°'
  }
  for i,line in ipairs(help) do g.print(line,x+14,124+(i-1)*25) end
 end
 if modal then drawItemModal(g) end
end
