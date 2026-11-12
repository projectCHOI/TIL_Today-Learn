local Flow={screen='title',axeSelected=false}
local roster={'도끼 전사','창 전사','궁수','마법사','소환사','샤먼','늑대인간'}
local ink={.10,.13,.19}
local accent={.80,.88,.98}

local function button(x,y,w,h,label,action,active)
 return {x=x,y=y,w=w,h=h,label=label,action=action,active=active}
end

function Flow:finish(success,reason)
 self.success=success
 self.reason=reason
 self.screen='result'
end

local function layout(flow,w,h)
 local cx,cy=w/2,h/2
 local function centered(y,label,action)
  return button(cx-120,y,240,48,label,action)
 end
 if flow.screen=='title' then
  return '불가능 길드',nil,{
   centered(cy+35,'게임 시작',function() flow.screen='lobby' end)
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
    index==1 and function() flow.axeSelected=not flow.axeSelected end,
    index==1 and flow.axeSelected)
   card.detail=index==1 and (flow.axeSelected and '선택됨' or '격투 · 근접') or '준비 중'
   cards[#cards+1]=card
  end
  cards[#cards+1]=centered(cy+120,'대기실로 돌아가기',function() flow.screen='lobby' end)
  local count=flow.axeSelected and '1' or '0'
  return '캐릭터 선택','선택 '..count..' / 3 · 현재 출전 가능 1명',cards
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
 g.setColor(ink)
 g.setFont(fonts.heading)
 g.printf(heading,0,h/2-155,w,'center')
 g.setFont(fonts.body)
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
