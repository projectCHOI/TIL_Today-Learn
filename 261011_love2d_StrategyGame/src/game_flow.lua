local Flow={screen='title',axeSelected=false}
local roster={'도끼 전사','창 전사','궁수','마법사','소환사','샤먼','늑대인간'}
local vulkan={
 name='Vulkan',
 job='도끼전사',
 equipment='도끼',
 element='격투',
 color={224/255,156/255,48/255},
 stats={{'체력',40},{'공격력',80},{'방어력',35},{'특수공격',35},{'특수방어',45},{'스피드',70}},
 basic='도끼치기',
 special='카운터'
}
local ink={.10,.13,.19}
local accent={.80,.88,.98}
local titlePath='assets/images/Title_ImpossibilityGuild_Kor.png'
local titleImage
local titleLoaded=false

local function getTitleImage()
 if not titleLoaded then
  titleLoaded=true
  if love.filesystem.getInfo(titlePath,'file') then
   titleImage=love.graphics.newImage(titlePath)
  end
 end
 return titleImage
end

local function button(x,y,w,h,label,action,active)
 return {x=x,y=y,w=w,h=h,label=label,action=action,active=active}
end

function Flow:finish(success,reason)
 self.success=success
 self.reason=reason
 self.screen='result'
end

local function detailBounds(w,h)
 return w*.2,h*.2,w*.6,h*.6
end

local function drawCharacterDetail(g,w,h)
 local x,y,width,height=detailBounds(w,h)
 local left=math.floor(width*.38)
 local portraitWidth=left-20
 local portraitHeight=height-20
 local px,py=x+10,y+10
 g.setColor(.97,.97,.98)
 g.rectangle('fill',x,y,width,height,8,8)
 g.setColor(.10,.12,.16)
 g.rectangle('fill',px,py,portraitWidth,portraitHeight)
 local art=getTitleImage()
 if art then
  local iw,ih=art:getDimensions()
  local scale=math.min(portraitWidth/iw,(portraitHeight-86)/ih)
  g.setColor(1,1,1,1)
  g.draw(art,px+(portraitWidth-iw*scale)/2,py+(portraitHeight-86-ih*scale)/2,0,scale,scale)
 end
 g.setColor(vulkan.color)
 g.printf(vulkan.name,px,py+portraitHeight-70,portraitWidth,'center')
 g.printf(vulkan.job,px,py+portraitHeight-44,portraitWidth,'center')

 local rx=x+left+10
 local rw=width-left-24
 local line=y+14
 g.setColor(ink)
 g.print('현재 능력치',rx,line)
 local total=0
 for i,stat in ipairs(vulkan.stats) do
  local col=(i-1)%2
  local row=math.floor((i-1)/2)
  local sx=rx+col*rw/2
  g.print(stat[1],sx,line+28+row*22)
  g.printf(tostring(stat[2]),sx,line+28+row*22,rw/2-14,'right')
  total=total+stat[2]
 end
 g.print('총합',rx,line+94)
 g.printf(tostring(total),rx,line+94,rw-14,'right')
 g.print('하급 기본 공격기 · '..vulkan.basic,rx,line+124)
 g.print('하급 특수 공격기 · '..vulkan.special,rx,line+146)
 g.print('현재 속성',rx,line+174)
 g.setColor(.10,.12,.16)
 g.rectangle('fill',rx+78,line+170,58,25,4,4)
 g.setColor(vulkan.color)
 g.printf(vulkan.element,rx+78,line+174,58,'center')

 local inventoryY=y+height-146
 g.setColor(.89,.91,.94)
 g.rectangle('fill',rx,inventoryY,rw,82,5,5)
 g.setColor(ink)
 g.print('사용 장비 · '..vulkan.equipment,rx+10,inventoryY+8)
 g.print('획득 장비 · 없음',rx+10,inventoryY+31)
 g.print('회복 아이템 · 없음',rx+10,inventoryY+54)
end

local function layout(flow,w,h)
 local cx,cy=w/2,h/2
 local function centered(y,label,action)
  return button(cx-120,y,240,48,label,action)
 end
 if flow.screen=='title' then
  local art=getTitleImage()
  return art and '' or '불가능 길드',nil,{
   centered(art and h-74 or cy+35,'게임 시작',function() flow.screen='lobby' end)
  }
 elseif flow.screen=='lobby' then
  local party=flow.axeSelected and '출전 캐릭터 · 도끼 전사' or '출전 캐릭터를 선택하세요.'
  return '게임 대기실',party,{
   centered(cy+18,'캐릭터 선택',function() flow.screen='roster' end),
   centered(cy+78,'게임 실행',flow.axeSelected and function()
    flow.screen='battle'
    return 'start'
   end)
  }
 elseif flow.screen=='roster' then
  local cards={}
  local gap=12
  local gaps=(#roster-1)*gap
  local width=math.min(180,(w-80-gaps)/#roster)
  local left=cx-(#roster*width+gaps)/2
  for index,name in ipairs(roster) do
   local card=button(left+(index-1)*(width+gap),cy-64,width,160,name,
    index==1 and function() flow.screen='character_detail' end,
    index==1 and flow.axeSelected)
   card.detail=index==1 and (flow.axeSelected and '선택됨' or '격투 · 근접') or '준비 중'
   cards[#cards+1]=card
  end
  cards[#cards+1]=centered(cy+120,'대기실로 돌아가기',function() flow.screen='lobby' end)
  local count=flow.axeSelected and '1' or '0'
  return '캐릭터 선택','선택 '..count..' / 3 · 현재 출전 가능 1명',cards
 elseif flow.screen=='character_detail' then
  local x,y,width,height=detailBounds(w,h)
  local actionY=y+height-52
  return nil,nil,{
   button(x+width-254,actionY,112,38,'카드 목록',function() flow.screen='roster' end),
   button(x+width-132,actionY,118,38,flow.axeSelected and '선택 해제' or '출전 선택',function()
    flow.axeSelected=not flow.axeSelected
    flow.screen='roster'
   end,true)
  }
 elseif flow.screen=='retreat' then
  return '전투를 포기할까요?','포기하면 이번 전투는 실패로 끝납니다.',{
   centered(cy+18,'전투로 돌아가기',function() flow.screen='battle' end),
   centered(cy+78,'포기 확정',function()
    flow:finish(false,'전투를 포기했습니다.')
   end)
  }
 end
 return flow.success and '전투 성공' or '전투 실패',flow.reason,{
  centered(cy+35,'대기실로 돌아가기',function()
   flow.axeSelected=false
   flow.screen='lobby'
  end)
 }
end

function Flow:mousepressed(x,y,mouseButton)
 if mouseButton~=1 then return end
 local _,_,controls=layout(self,love.graphics.getDimensions())
 for _,control in ipairs(controls) do
  if control.action and x>=control.x and x<control.x+control.w
   and y>=control.y and y<control.y+control.h then
   return control.action()
  end
 end
end

function Flow:draw(fonts)
 local g=love.graphics
 local w,h=g.getDimensions()
 local heading,detail,controls=layout(self,w,h)
 local art=self.screen=='title' and titleImage
 if art then
  local iw,ih=art:getDimensions()
  local scale=math.min(w/iw,h/ih)
  g.clear(.055,.063,.075,1)
  g.setColor(1,1,1,1)
  g.draw(art,(w-iw*scale)/2,(h-ih*scale)/2,0,scale,scale)
 elseif heading then
  g.setColor(ink)
  g.setFont(fonts.heading)
  g.printf(heading,0,h/2-155,w,'center')
 end
 g.setFont(fonts.body)
 if self.screen=='character_detail' then drawCharacterDetail(g,w,h) end
 if detail then g.printf(detail,0,h/2-96,w,'center') end
 for _,control in ipairs(controls) do
  g.setColor(control.active and accent or {.96,.96,.97})
  g.rectangle('fill',control.x,control.y,control.w,control.h,8,8)
  g.setColor(control.active and {.29,.44,.66} or {.83,.85,.89})
  g.setLineWidth(control.active and 2 or 1)
  g.rectangle('line',control.x,control.y,control.w,control.h,8,8)
  g.setColor(control.action and ink or {.36,.38,.44})
  local labelY=control.detail and control.y+52 or control.y+15
  g.printf(control.label,control.x,labelY,control.w,'center')
  if control.detail then g.printf(control.detail,control.x,control.y+83,control.w,'center') end
 end
end

return Flow
