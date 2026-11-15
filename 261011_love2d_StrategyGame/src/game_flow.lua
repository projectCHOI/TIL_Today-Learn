local Flow={screen='title',axeSelected=false}
local roster={
 {name='Vulkan', korean='불칸', job='도끼전사', equipment='도끼(Axe)', element='격투', deployable=true,
  stats={40,80,35,35,45,70},
  skills={'도끼치기','난동부리기','장작패기','인파이트','분노의 도끼','목숨걸기'}},
 {name='Fulgrim', korean='펄그림', job='창 전사', equipment='창(Spear)', element='노말',
  stats={30,55,30,30,30,60},
  skills={'찌르기','정광석화 찌르기','삼단 찌르기','독수리 발톱','브레이브(Brave) 스피어','이판사판 찌르기'}},
 {name='Konrad', korean='콘라드', job='궁수', equipment='활(Bow)', element='노말',
  stats={40,45,40,35,35,56},
  skills={'명중','바람 일으키기','이중공격','강철비','돌풍','록 히드(Lockheed)'}},
 {name='Angron', korean='앙그론', job='마법사', equipment='지팡이(Staff)', element='노말',
  stats={28,25,25,45,35,40},
  skills={'명상','사이코키네시스 (Psychic)','정신집중','하이퍼보이스 (Hyper Voice)','매지컬리프','사이코쇼크'}},
 {name='Mortarion', korean='모리타운', job='소환사', equipment='책(book)', element='악',
  stats={25,20,15,105,55,90},
  skills={'순간이동 (Teleport)','정령소환(Elementals)','최면술','중급 정령소환(Elementals)','정령 폭탄 (Elementals Bomb)','길동무 (Destiny Bond)'}},
 {name='Magnus', korean='마그누스', job='샤먼', equipment='쌍방울(Double Bell)', element='페어리',
  stats={30,35,30,100,35,80},
  skills={'HP회복 (Recover)','정보수집','찬송가','기합구슬','이스게레의 노래','부활'}},
 {name='Lorgar', korean='로가', job='늑대인간', equipment='방패(Shield)', element='고스트',
  stats={45,55,65,45,45,45},
  skills={'할퀴기','스카이업퍼컷 (Sky Uppercut)','하늘 걷기','참격','난동부리기','늑대 변신(berserker)'}}
}
local typeColors={
 ['노말']={148/255,148/255,149/255}, ['격투']={224/255,156/255,48/255},
 ['독']={115/255,81/255,152/255}, ['벌레']={159/255,162/255,68/255},
 ['불꽃']={229/255,108/255,62/255}, ['물']={81/255,133/255,197/255},
 ['전기']={251/255,185/255,23/255}, ['얼음']={109/255,200/255,235/255},
 ['고스트']={104/255,72/255,112/255}, ['페어리']={218/255,180/255,212/255},
 ['악']={76/255,73/255,72/255}, ['드래곤']={83/255,92/255,168/255}
}
local statNames={'체력','공격력','방어력','특수공격','특수방어','스피드'}
local skillLabels={'하급 기본','하급 특수','중급 기본','중급 특수','상급 기본','상급 특수'}
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

local function typeText(g,text,x,y,width,color)
 g.setColor(1,1,1)
 g.printf(text,x-1,y,width,'center')
 g.printf(text,x+1,y,width,'center')
 g.printf(text,x,y-1,width,'center')
 g.printf(text,x,y+1,width,'center')
 g.setColor(color)
 g.printf(text,x,y,width,'center')
end

local function drawCharacterDetail(g,w,h,character)
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
 local color=typeColors[character.element]
 typeText(g,character.korean..' · '..character.name,px,py+portraitHeight-70,portraitWidth,color)
 typeText(g,character.job,px,py+portraitHeight-44,portraitWidth,color)

 local rx=x+left+10
 local rw=width-left-24
 local line=y+14
 g.setColor(ink)
 g.print('현재 능력치',rx,line)
 g.printf('현재 속성',rx,line,rw-64,'right')
 g.rectangle('fill',rx+rw-56,line-2,56,21,4,4)
 typeText(g,character.element,rx+rw-56,line,56,color)
 g.setColor(ink)
 local total=0
 for i,value in ipairs(character.stats) do
  local col=(i-1)%2
  local row=math.floor((i-1)/2)
  local sx=rx+col*rw/2
  local sy=line+25+row*20
  g.print(statNames[i],sx,sy)
  g.printf(tostring(value),sx,sy,rw/2-12,'right')
  total=total+value
 end
 g.print('총합',rx,line+85)
 g.printf(tostring(total),rx,line+85,rw-12,'right')
 g.print('공격기',rx,line+110)
 for i,skill in ipairs(character.skills) do
  g.print(skillLabels[i],rx,line+131+(i-1)*20)
  g.print(skill,rx+80,line+131+(i-1)*20)
 end

 local inventoryY=y+height-115
 g.setColor(.89,.91,.94)
 g.rectangle('fill',rx,inventoryY,rw,56,5,5)
 g.setColor(ink)
 g.print('주무기 · '..character.equipment,rx+10,inventoryY+8)
 g.print('획득 장비 · 없음    회복 아이템 · 없음',rx+10,inventoryY+30)
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
  for index,character in ipairs(roster) do
   local card=button(left+(index-1)*(width+gap),cy-64,width,160,character.job,function()
     flow.character=character
     flow.screen='character_detail'
    end,character.deployable and flow.axeSelected)
   card.detail=character.korean..(character.deployable and flow.axeSelected and ' · 선택됨' or '')
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
   button(x+width-132,actionY,118,38,
    flow.character.deployable and (flow.axeSelected and '선택 해제' or '출전 선택') or '출전 준비 중',
    flow.character.deployable and function()
    flow.axeSelected=not flow.axeSelected
    flow.screen='roster'
   end,flow.character.deployable)
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
 if self.screen=='character_detail' then drawCharacterDetail(g,w,h,self.character) end
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
