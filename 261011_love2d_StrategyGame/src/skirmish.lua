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
local Units=require('src.units')
local Rules=require('src.rules')
local Battle={}
Battle.__index=function(self,key)
 if Units.fields[key] and rawget(self,'active') then
  return self.active[key=='warrior' and 'tile' or key]
 end
 return Battle[key]
end
Battle.__newindex=function(self,key,value)
 if Units.fields[key] and rawget(self,'active') then self.active[key=='warrior' and 'tile' or key]=value
 else rawset(self,key,value) end
end

function Battle.new(map,character,bag)
 local party=character.name and {character} or character
 local allBags
 if not character.name then allBags=bag end
 character=assert(party[1],'출전 캐릭터가 없습니다.')
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
 local units={}
 local spawns={{1,5},{0,4},{0,6}}
 for i,profile in ipairs(party) do
  assert(i<=3,'최대 3명 출전')
  local ownBag
  if allBags then ownBag=allBags[profile.name] or {};allBags[profile.name]=ownBag else ownBag=i==1 and bag or {} end
  units[i]=Units.new(profile,assert(Grid.get(map,spawns[i][1],spawns[i][2])),ownBag)
 end
 for _,enemy in ipairs(enemies) do enemy.faction='enemy' end
 return setmetatable({map=map,enemies=enemies,chests=chests,units=units,active=units[1],
  spirits={},rolled=nil,remaining=0,won=false,lost=false,turn=1},Battle)
end

function Battle:roll(random)
 if self.rolled or self.won or self.lost or self.pendingCharge or self.pendingAction then return end
 self.random=random
 self.dice={}
 local total=0
 for i=1,(#self.units>=2 and 2 or 1) do self.dice[i]=random(1,6);total=total+self.dice[i] end
 self.rolled=total
 self.remaining=total
end

function Battle:selectUnit(unit)
 for _,ally in ipairs(self.units) do
  if ally==unit and ally.health>0 then self:cancelCharge();self.pendingAction=nil;self.moveMode=false;self.active=ally;return true end
 end
 return false
end
function Battle:unitAt(tile,includeDead) return Units.at(self,tile,includeDead) end
function Battle:occupied(except) return Units.occupied(self,except or self.active) end
function Battle:endTurn()
 if self.won or self.lost then return end
 if self.pendingCharge or self.pendingAction then return '진행 중인 기술을 완료하거나 취소하세요.' end
 local text=require('src.summoning').endTurn(self)
 if not self.won and not self.lost then
  for _,enemy in ipairs(self.enemies) do
   if enemy.health>0 then
    if enemy.hypnotized then
     require('src.summoning').wander(self,enemy)
    elseif (enemy.actionLocks or 0)>0 then enemy.actionLocks=enemy.actionLocks-1
    else
     local candidates={}
     for _,ally in ipairs(self.units) do candidates[#candidates+1]=ally end
     if Rules.spiritTargetable then for _,spirit in ipairs(self.spirits) do candidates[#candidates+1]=spirit end end
     table.sort(candidates,function(a,b) return Grid.distance(enemy.tile,a.tile)<Grid.distance(enemy.tile,b.tile) end)
     for _,ally in ipairs(candidates) do
      if Combat.canTarget(self.map,enemy,ally,Skills.test_strike) then
       local damage,hit,revived=Combat.execute(enemy,ally,Skills.test_strike,self.random or math.random)
       text[#text+1]=enemy.name..(hit and (' · 피해 '..damage) or ' · 빗나감')
       if revived and #revived>0 then text[#text+1]=(ally.name or '아군')..' · 부활석 발동' end
       break
      end
     end
    end
   end
  end
 end
 require('src.special').refreshAuras(self)
 self:resolveOutcome()
 self.rolled=nil;self.dice=nil;self.remaining=0;self.turn=self.turn+1
 text[#text+1]=self.lost and '아군이 모두 쓰러졌습니다.' or '새 턴입니다. 주사위를 굴리세요.'
 return table.concat(text,' / ')
end

function Battle:actionError()
 if self.won then return '승리했습니다.' end
 if self.lost then return '전투에서 패배했습니다.' end
 if self.pendingCharge or self.pendingAction then return '진행 중인 기술을 완료하거나 취소하세요.' end
 if self.health<=0 then return '생존한 아군을 선택하세요.' end
 if not self.rolled then return '먼저 주사위를 굴리세요.' end
 if self.remaining==0 then return '남은 행동이 없습니다.' end
 if (self.actionLocks or 0)>0 then return '행동 불능 상태입니다.' end
end

function Battle:canMove(tile,pulley)
 if self.pendingCharge or (self.moveLocks or 0)>0 then return nil,'이동할 수 없습니다.' end
 if self.chests[tile] then return nil,'상자가 이동을 막습니다.' end
 local occupied=self:occupied()
 return Movement.step(self.map,self.warrior,tile,occupied,pulley)
end

-- Shared enemy movement entry point for future AI path selection.
function Battle:moveEnemy(enemy,tile,pulley)
 if self.won or self.lost or self.pendingCharge or enemy.health<=0 then return nil,'이동할 수 없습니다.' end
 if (enemy.actionLocks or 0)>0 then enemy.actionLocks=enemy.actionLocks-1;return nil,'행동 불능으로 이동 취소' end
 local occupied=self:occupied(enemy)
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
 return not self.pendingCharge and not self.pendingAction and tile and self.chests[tile] and Grid.distance(self.warrior,tile)==1
  and math.abs(self.warrior.height-tile.height)<=1 and not World.blocked(self.map,self.warrior,tile)
end

function Battle:inspect(tile)
 if tile and self.chests[tile] and not self.chests[tile].open then
  local locked=self:consumeActionLock();if locked then return nil,locked end
 end
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
 local locked=self:consumeActionLock();if locked then return locked end
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
  if id==available then self:cancelCharge(); self.moveMode=false;self.skillId=id; return true end
 end
 return false
end
function Battle:cancelCharge()
 self.pendingAction=nil
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
 if Skills[self.skillId].effect then return require('src.special').canTarget(self,target) end
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
 require('src.special').refreshAuras(self)
 local enemyAlive=false;local allyAlive=false;local flag=false
 for _,enemy in ipairs(self.enemies) do if enemy.health>0 then enemyAlive=true end end
 for _,ally in ipairs(self.units) do
  if ally.health>0 then allyAlive=true;if ally.tile.flag==2 then flag=true end end
 end
 self.won=flag or (not enemyAlive and (allyAlive or Rules.simultaneousElimination=='victory'))
 self.lost=not self.won and not allyAlive
 -- Retain the active corpse until the next explicit selection; party members remain available.
end

function Battle:consumeActionLock()
 if (self.actionLocks or 0)>0 and self.rolled and self.remaining>0 and not self.won and not self.lost then
  self.actionLocks=self.actionLocks-1;self.remaining=self.remaining-1
  return '행동 불능으로 이번 행동이 취소되었습니다.'
 end
end
function Battle:finishSkill(id,text)
 local promotion=Progress.record(self,id)
 if promotion then text=text..' / '..promotion end
 self:resolveOutcome()
 if self.won then text=text..' / 전투 성공' elseif self.lost then text=text..' / 전투 실패' end
 return text
end
function Battle:cast(target)
 return require('src.special').cast(self,target)
end
function Battle:areaGroupAt(tile)
 return Area.groupAt(self.tile,tile,Skills[self.skillId])
end
function Battle:areaCells(group)
 return Area.cells(self,Skills[self.skillId],group)
end
function Battle:castArea(group)
 local locked=self:consumeActionLock();if locked then return locked end
 local problem=self:actionError()
 if problem then return problem end
 local skill=Skills[self.skillId]
 if not skill.area then return '범위 기술을 선택하세요.' end
 if self.remaining<skill.cost then return '행동 '..skill.cost..'회가 필요합니다.' end
 if skill.area=='all' then group=0 end
 if not group or group%1~=0 or group<0 or (group==0 and skill.area~='all') or group>(skill.area=='center' and 1 or #(skill.regions or {})) then
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
 local locked=self:consumeActionLock();if locked then return locked end
 if Skills[self.skillId].effect then return self:cast(target) end
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
  local amount,hit,revived=Combat.execute(self.active,enemy,skill,self.random or math.random)
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
 local locked=self:consumeActionLock();if locked then return locked end
 local errorMessage=self:actionError()
 if errorMessage then return errorMessage end
 if not self:canToggleDoor(edge) then return '문에 인접해야 열거나 닫을 수 있습니다.' end
 World.toggle(edge)
 self.remaining=self.remaining-1
 return edge.open and '문을 열었습니다.' or '문을 닫았습니다.'
end

function Battle:act(tile,pulley)
 if Skills[self.skillId].effect and not self.moveMode then
  if ({meditate=true,detonate=true,howl=true,berserk=true})[Skills[self.skillId].effect] then return '위쪽 기술 사용 버튼을 클릭하세요.' end
  return self:cast(tile)
 end
 local locked=self:consumeActionLock();if locked then return locked end
 if not self.moveMode and Skills[self.skillId].area and not pulley and self:areaGroupAt(tile) then
  return self:castArea(self:areaGroupAt(tile))
 end
 if self.pendingCharge then return self:attack(tile) end
 if not self.moveMode and Skills[self.skillId].charge and not pulley and not self:enemyAt(tile) then return self:beginCharge(tile) end
 if self.moveMode and self:enemyAt(tile) then return '도착 칸이 점유되어 있습니다.' end
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
 self:resolveOutcome()
 return self.won and '승리했습니다. 적군 깃발에 도달했습니다.' or '이동했습니다.'
end

return Battle