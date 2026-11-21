local Grid=require('src.grid')
local Movement=require('src.movement')
local World=require('src.world')
local Items=require('src.items')
local outpost=require('src.outpost')
local Combat=require('src.combat')
local Skills=require('src.skills')
local Progress=require('src.progression')
local Charge=require('src.charge')
local Area=require('src.area')
local Battle={}
Battle.__index=Battle

function Battle.new(map,character,bag)
 local chests={}
 for index,position in ipairs(outpost.chests) do
  local tile=assert(Grid.get(map,position[1],position[2]))
  chests[tile]={item=index,open=false}
 end
 local enemies={}
 local positions={{2,5},{3,4},{3,6}}
 for i,element in ipairs({'노말','독','고스트'}) do
  enemies[i]={name=element..' 시험 적',element=element,stats={45,30,35,20,20,45},
   health=45,tile=assert(Grid.get(map,positions[i][1],positions[i][2])),attackers={}}
 end
 return setmetatable({
  enemies=enemies, character=character, stats=Progress.stats(character),element=character.element,
  tile=assert(Grid.get(map,1,5)),attackers={},skillId=character.combatSkills[1],
  chests=chests, bag=bag or {}, maxHealth=Progress.stats(character)[1], health=Progress.stats(character)[1], rageStacks=0,
  baseElement=character.element,
  map=map, warrior=assert(Grid.get(map,1,5)),
  rolled=nil, remaining=0, won=false
 },Battle)
end

function Battle:roll(random)
 if self.rolled or self.won or self.lost or self.pendingCharge then return end
 self.random=random
 self.rolled=random(1,6)
 self.remaining=self.rolled
end

function Battle:endTurn()
 if self.won or self.lost then return end
 if self.pendingCharge then return '이동 기술의 공격을 완료하거나 우클릭으로 취소하세요.' end
 local messages={}
 for _,enemy in ipairs(self.enemies) do
  if self.health>0 and Combat.canTarget(self.map,enemy,self,Skills.test_strike) then
   local amount,hit,revived=Combat.execute(enemy,self,Skills.test_strike,self.random or math.random)
   messages[#messages+1]=enemy.name..(hit and (' · 피해 '..amount) or ' · 빗나감')
   if revived and #revived>0 then messages[#messages+1]=self.character.korean..' · 부활석 사용, 체력 전부 회복' end
  end
 end
 self.lost=self.health<=0
 self.rolled=nil
 self.remaining=0
 messages[#messages+1]=self.lost and (self.character.korean..'이 쓰러졌습니다.') or '새 턴입니다. 주사위를 굴리세요.'
 return table.concat(messages,' / ')
end

function Battle:actionError()
 if self.won then return '승리했습니다.' end
 if self.lost then return '전투에서 패배했습니다.' end
 if self.pendingCharge then return '이동 기술의 공격을 완료하거나 우클릭으로 취소하세요.' end
 if not self.rolled then return '먼저 주사위를 굴리세요.' end
 if self.remaining==0 then return '남은 행동이 없습니다.' end
end

function Battle:canMove(tile,pulley)
 if self.pendingCharge or (self.moveLocks or 0)>0 then return nil,'이동할 수 없습니다.' end
 if self.chests[tile] then return nil,'상자가 이동을 막습니다.' end
 local occupied={}
 for _,enemy in ipairs(self.enemies) do occupied[enemy.tile]=enemy.health>0 end
 return Movement.step(self.map,self.warrior,tile,occupied,pulley)
end

-- Shared enemy movement entry point for future AI path selection.
function Battle:moveEnemy(enemy,tile,pulley)
 if self.won or self.lost or self.pendingCharge or enemy.health<=0 then return nil,'이동할 수 없습니다.' end
 local occupied={[self.tile]=self.health>0}
 for _,other in ipairs(self.enemies) do
  if other~=enemy and other.health>0 then occupied[other.tile]=true end
 end
 for chest in pairs(self.chests) do occupied[chest]=true end
 local cost,reason=Movement.step(self.map,enemy.tile,tile,occupied,pulley)
 if not cost then return nil,reason end
 if (enemy.moveLocks or 0)>0 then
  enemy.moveLocks=enemy.moveLocks-1
  return nil,'장작패기 효과로 이번 이동을 할 수 없습니다.'
 end
 enemy.tile=tile
 return cost
end

function Battle:canInspect(tile)
 return tile and self.chests[tile] and Grid.distance(self.warrior,tile)==1
  and math.abs(self.warrior.height-tile.height)<=1 and not World.blocked(self.map,self.warrior,tile)
end

function Battle:inspect(tile)
 if not self:canInspect(tile) then return nil,'상자에 인접해야 합니다.' end
 local chest=self.chests[tile]
 if not chest.open then
  local problem=self:actionError()
  if problem then return nil,problem end
  self.remaining=self.remaining-1
  chest.open=true
 end
 return chest
end

function Battle:takeItem(tile)
 local chest=self:canInspect(tile) and self.chests[tile]
 if not chest or not chest.open then return end
 local index=chest.item
 self.bag[index]=(self.bag[index] or 0)+1
 self.chests[tile]=nil
 local item=Items[index]
 if item.element then self.extraElement=item.element end
 return item.name..' 획득'
end

function Battle:useItem(index)
 if self.pendingCharge then return '이동 기술을 완료하거나 취소하세요.' end
 local item=Items[index]
 if not item or (self.bag[index] or 0)==0 then return end
 if item.revive then return '부활석은 가방에 보유하면 사망 시 자동으로 사용됩니다.' end
 if item.element then
  self.extraElement=item.element
  return item.element..' 속성을 적용했습니다.'
 end
 local problem=self:actionError()
 if problem then return problem end
 local amount=math.min(item.heal,self.maxHealth-self.health)
 if amount==0 then return '이미 체력이 가득 찼습니다.' end
 self.health=self.health+amount
 self.remaining=self.remaining-1
 self.bag[index]=self.bag[index]-1
 return item.name..' 사용 · 체력 '..amount..' 회복'
end

function Battle:touches(edge)
 return edge.tile==self.warrior or edge.neighbor==self.warrior
end

function Battle:canToggleDoor(edge)
 return edge.kind=='door' and edge.hp>0 and self:touches(edge)
end

function Battle:enemyAt(tile)
 for _,enemy in ipairs(self.enemies) do
  if enemy.tile==tile and enemy.health>0 then return enemy end
 end
end

function Battle:skillIds() return Progress.skills(self.character) end
function Battle:selectSkill(id)
 for _,available in ipairs(self:skillIds()) do
  if id==available then self:cancelCharge(); self.skillId=id; return true end
 end
 return false
end
function Battle:cancelCharge()
 if not self.pendingCharge then return end
 self.warrior=self.pendingCharge.origin
 self.tile=self.warrior
 self.remaining=self.remaining+self.pendingCharge.cost
 self.pendingCharge=nil
end

function Battle:canCharge(tile)
 return Charge.canLand(self,tile,Skills[self.skillId])
end
function Battle:beginCharge(tile)
 local problem=self:actionError()
 if problem then return problem end
 local skill=Skills[self.skillId]
 if self.remaining<skill.cost then return '행동 '..skill.cost..'회가 필요합니다.' end
 if not self:canCharge(tile) then return '이동 경로 또는 이동 후 공격할 대상을 확인하세요.' end
 self.pendingCharge={origin=self.warrior,cost=skill.cost,skillId=self.skillId}
 self.warrior=tile;self.tile=tile;self.remaining=self.remaining-skill.cost
 if tile.flag==2 then
  self.pendingCharge=nil;self.won=true
  return '전투 성공 · 적군 깃발에 도달했습니다.'
 end
 return skill.name..' · 빨간 칸의 적을 선택하세요. 우클릭으로 취소할 수 있습니다.'
end

function Battle:canAttack(target)
 if not target then return false end
 local skill=Skills[self.skillId]
 if target.kind then
  return not self.pendingCharge and not skill.charge and not skill.area and not skill.sacrifice and target.hp>0 and self:touches(target)
 end
 local enemy=self:enemyAt(target)
 if not enemy then return false end
 if skill.charge then
  return self.pendingCharge and self.pendingCharge.skillId==self.skillId
   and Charge.canTarget(self.map,self.pendingCharge.origin,self.warrior,self.health,enemy,skill) or false
 end
 return Combat.canTarget(self.map,self,enemy,skill)
end

function Battle:resolveOutcome()
 self.won=true
 for _,enemy in ipairs(self.enemies) do if enemy.health>0 then self.won=false end end
 self.won=self.won or (self.health>0 and self.warrior.flag==2)
 self.lost=not self.won and self.health<=0
end

function Battle:areaGroupAt(tile)
 return Area.groupAt(self.tile,tile,Skills[self.skillId])
end
function Battle:areaCells(group)
 return Area.cells(self,Skills[self.skillId],group)
end
function Battle:castArea(group)
 local problem=self:actionError()
 if problem then return problem end
 local skill=Skills[self.skillId]
 if not skill.area then return '범위 기술을 선택하세요.' end
 if self.remaining<skill.cost then return '행동 '..skill.cost..'회가 필요합니다.' end
 if not group or group%1~=0 or group<1 or group>(skill.area=='center' and 1 or #skill.regions) then
  return '빨간 공격 구역을 선택하세요.'
 end
 local targets=Area.targets(self,skill,group)
 if #targets==0 then return '선택 구역에 공격 가능한 적이 없습니다.' end
 self.remaining=self.remaining-skill.cost
 local result=Area.execute(self,skill,targets)
 local text=skill.name..' · 대상 '..result.count..' · 명중 '..result.hits..' · 총 피해 '..result.damage
 if skill.push then text=text..' · 밀침 '..result.moved end
 if result.revivals>0 then text=text..' · 부활석 발동 '..result.revivals end
 -- One skill cast counts once, independently of its target count or misses.
 local promotion=Progress.record(self,self.skillId)
 if promotion then text=text..' / '..promotion end
 self:resolveOutcome()
 if self.won then text=text..' / 전투 성공' end
 return text
end

function Battle:attack(target)
 if Skills[self.skillId].area then return self:castArea(self:areaGroupAt(target)) end
 local pending=self.pendingCharge
 if not pending then
  local problem=self:actionError()
  if problem then return problem end
 elseif self.won or self.lost then return '전투가 종료되었습니다.' end
 local skill=Skills[self.skillId]
 if not pending and self.remaining<skill.cost then return '행동 '..skill.cost..'회가 필요합니다.' end
 if not self:canAttack(target) then return '사거리·고도 차 또는 공격 경로를 확인하세요.' end
 if not pending then self.remaining=self.remaining-skill.cost end
 local result
 if target.kind then
  World.damage(target,10)
  result='시설물에 시험 피해 10을 입혔습니다.'
 else
  local enemy=self:enemyAt(target)
  local amount,hit,revived=Combat.execute(self,enemy,skill,self.random or math.random)
  result=skill.name..(hit and (' · 피해 '..amount) or ' · 빗나감')
  for _,unit in ipairs(revived or {}) do
   local name=unit.character and unit.character.korean or unit.name
   result=result..' / '..name..' · 부활석 사용, 체력 전부 회복'
  end
 end
 -- Uses and rage count executed attacks even on a miss; rejected actions do not count.
 if skill.rage then self.rageStacks=math.min(9,self.rageStacks+1) end
 local promotion=Progress.record(self,self.skillId)
 if promotion then result=result..' / '..promotion end
 self.pendingCharge=nil
 self:resolveOutcome()
 if self.won then return result..' / 전투 성공' end
 if self.lost then return result..' / '..self.character.korean..'이 쓰러졌습니다.' end
 return result
end

function Battle:toggleDoor(edge)
 local errorMessage=self:actionError()
 if errorMessage then return errorMessage end
 if not self:canToggleDoor(edge) then return '문에 인접해야 열거나 닫을 수 있습니다.' end
 World.toggle(edge)
 self.remaining=self.remaining-1
 return edge.open and '문을 열었습니다.' or '문을 닫았습니다.'
end

function Battle:act(tile,pulley)
 if Skills[self.skillId].area and not pulley and self:areaGroupAt(tile) then
  return self:castArea(self:areaGroupAt(tile))
 end
 if self.pendingCharge then return self:attack(tile) end
 if Skills[self.skillId].charge and not pulley and not self:enemyAt(tile) then return self:beginCharge(tile) end
 if self:enemyAt(tile) and not pulley then return self:attack(tile) end
 local errorMessage=self:actionError()
 if errorMessage then return errorMessage end
 if (self.moveLocks or 0)>0 then
  self.moveLocks=self.moveLocks-1
  return '장작패기 효과로 이번 이동을 할 수 없습니다.'
 end
 local cost,reason=self:canMove(tile,pulley)
 if not cost then return reason end
 self.warrior=tile
 self.tile=tile
 self.remaining=self.remaining-cost
 self.won=tile.flag==2
 return self.won and '승리했습니다. 적군 깃발에 도달했습니다.' or '이동했습니다.'
end

return Battle
