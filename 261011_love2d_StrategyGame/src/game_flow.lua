local roster=require('src.characters')
local Progress=require('src.progression')
local typeColors=require('src.type_colors')
local Flow={screen='title',selectedCharacter=nil,selectedParty={}}
function Flow:getParty()
 if #self.selectedParty>0 then return self.selectedParty end
 return self.selectedCharacter and {self.selectedCharacter} or {}
end
function Flow:getSelectedCharacter() return self:getParty()[1] end
function Flow:isSelected(character)
 for _,c in ipairs(self:getParty()) do if c==character then return true end end
 return false
end
function Flow:selectCharacter(character)
 if not character or not character.deployable then return false end
 if #self.selectedParty==0 and self.selectedCharacter then self.selectedParty={self.selectedCharacter} end
 for i,c in ipairs(self.selectedParty) do
  if c==character then table.remove(self.selectedParty,i);self.selectedCharacter=self.selectedParty[1];self.selectionError=nil;return true end
 end
 if #self.selectedParty>=3 then self.selectionError='최대 3명까지 출전할 수 있습니다.';return false end
 self.selectedParty[#self.selectedParty+1]=character;self.selectedCharacter=self.selectedParty[1];self.selectionError=nil;return true
end
local statNames={'체력','공격력','방어력','특수공격','특수방어','스피드'}
local skillLabels={'하급 기술','하급 기술','중급 기술','중급 기술','상급 기술','상급 기술'}
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

local portraits={}

local function getPortrait(character)
 local file=character.portrait
 if not file then return getTitleImage() end
 if portraits[file]==nil then
  local path='assets/images/characters/'..file
  portraits[file]=love.filesystem.getInfo(path,'file') and love.graphics.newImage(path) or false
 end
 return portraits[file] or getTitleImage()
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
 local art=getPortrait(character)
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
 g.print('현재 능력치 · '..Progress.label(character),rx,line)
 g.printf('현재 속성',rx,line,rw-64,'right')
 g.rectangle('fill',rx+rw-56,line-2,56,21,4,4)
 typeText(g,character.element,rx+rw-56,line,56,color)
 g.setColor(ink)
 local total=0
 for i,value in ipairs(Progress.stats(character)) do
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
  local locked=character.ranks and math.ceil(i/2)>Progress.get(character).rank
  g.print(skill..(locked and ' (잠김)' or ''),rx+80,line+131+(i-1)*20)
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
  local names={}
  for _,c in ipairs(flow:getParty()) do names[#names+1]=c.korean end
  local party=#names>0 and ('출전 캐릭터 · '..table.concat(names,' / ')) or '출전 캐릭터를 선택하세요.'
  return '게임 대기실',party,{
   centered(cy+18,'캐릭터 선택',function() flow.screen='roster' end),
   centered(cy+78,'게임 실행',flow.selectedCharacter and function()
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
    end,flow:isSelected(character))
   card.detail=character.korean..(flow:isSelected(character) and ' · 선택됨' or '')
   cards[#cards+1]=card
  end
  cards[#cards+1]=centered(cy+120,'대기실로 돌아가기',function() flow.screen='lobby' end)
  local count=tostring(#flow:getParty())
  return '캐릭터 선택','선택 '..count..' / 3 · '..(flow.selectionError or '일곱 캐릭터 중 1~3명 선택'),cards
 elseif flow.screen=='character_detail' then
  local x,y,width,height=detailBounds(w,h)
  local actionY=y+height-52
  return nil,nil,{
   button(x+width-254,actionY,112,38,'카드 목록',function() flow.screen='roster' end),
   button(x+width-132,actionY,118,38,
    flow.character.deployable and (flow:isSelected(flow.character) and '선택 해제' or '출전 선택') or '출전 준비 중',
    flow.character.deployable and function()
    flow:selectCharacter(flow.character)
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
   flow.selectedCharacter=nil;flow.selectedParty={}
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
