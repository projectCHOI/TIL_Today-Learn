local Grid=require('src.grid')
local Movement=require('src.movement')
local World=require('src.world')
local Items=require('src.items')
local outpost=require('src.outpost')
local Combat=require('src.combat')
local Skills=require('src.skills')
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
  enemies=enemies, character=character, stats=character.stats,element=character.element,
  tile=assert(Grid.get(map,1,5)),attackers={},skillId=character.combatSkills[1],
  chests=chests, bag=bag or {}, maxHealth=character.stats[1], health=character.stats[1],
  baseElement=character.element,
  map=map, warrior=assert(Grid.get(map,1,5)),
  rolled=nil, remaining=0, won=false
 },Battle)
end

function Battle:roll(random)
 if self.rolled or self.won then return end
 self.random=random
 self.rolled=random(1,6)
 self.remaining=self.rolled
end

function Battle:endTurn()
 if self.won or self.lost then return end
 local messages={}
 for _,enemy in ipairs(self.enemies) do
  if self.health>0 and Combat.canTarget(self.map,enemy,self,Skills.test_strike) then
   local amount,hit=Combat.execute(enemy,self,Skills.test_strike,self.random or math.random)
   messages[#messages+1]=enemy.name..(hit and (' · 피해 '..amount) or ' · 빗나감')
  end
 end
 self.lost=self.health<=0
 self.rolled=nil
 self.remaining=0
 messages[#messages+1]=self.lost and '불칸이 쓰러졌습니다.' or '새 턴입니다. 주사위를 굴리세요.'
 return table.concat(messages,' / ')
end

function Battle:actionError()
 if self.won then return '승리했습니다.' end
 if self.lost then return '전투에서 패배했습니다.' end
 if not self.rolled then return '먼저 주사위를 굴리세요.' end
 if self.remaining==0 then return '남은 행동이 없습니다.' end
end

function Battle:canMove(tile,pulley)
 if self.chests[tile] then return nil,'상자가 이동을 막습니다.' end
 local occupied={}
 for _,enemy in ipairs(self.enemies) do occupied[enemy.tile]=enemy.health>0 end
 return Movement.step(self.map,self.warrior,tile,occupied,pulley)
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
 local item=Items[index]
 if not item or (self.bag[index] or 0)==0 then return end
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

function Battle:canAttack(target)
 if not target then return false end
 if target.kind then return target.hp>0 and self:touches(target) end
 local enemy=self:enemyAt(target)
 return enemy and Combat.canTarget(self.map,self,enemy,Skills[self.skillId]) or false
end

function Battle:attack(target)
 local problem=self:actionError()
 if problem then return problem end
 local skill=Skills[self.skillId]
 if self.remaining<skill.cost then return '행동 '..skill.cost..'회가 필요합니다.' end
 if not self:canAttack(target) then return '사거리·고도 차 또는 공격 경로를 확인하세요.' end
 self.remaining=self.remaining-skill.cost
 if target.kind then
  World.damage(target,10)
  return '시설물에 시험 피해 10을 입혔습니다.'
 end
 local enemy=self:enemyAt(target)
 local amount,hit=Combat.execute(self,enemy,skill,self.random or math.random)
 self.won=true
 for _,other in ipairs(self.enemies) do
  if other.health>0 then self.won=false end
 end
 if self.won then return '승리했습니다. 적을 모두 제거했습니다.' end
 return skill.name..(hit and (' · 피해 '..amount) or ' · 빗나감')
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
 if self:enemyAt(tile) and not pulley then return self:attack(tile) end
 local errorMessage=self:actionError()
 if errorMessage then return errorMessage end
 local cost,reason=self:canMove(tile,pulley)
 if not cost then return reason end
 self.warrior=tile
 self.tile=tile
 self.remaining=self.remaining-cost
 self.won=tile.flag==2
 return self.won and '승리했습니다. 적군 깃발에 도달했습니다.' or '이동했습니다.'
end

return Battle
