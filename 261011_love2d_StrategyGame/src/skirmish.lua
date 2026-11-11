local Grid=require('src.grid')
local Movement=require('src.movement')
local World=require('src.world')
local Battle={}
Battle.__index=Battle

function Battle.new(map)
 return setmetatable({
  map=map, warrior=assert(Grid.get(map,1,5)), target=assert(Grid.get(map,3,4)),
  hp=30, rolled=nil, remaining=0, won=false
 },Battle)
end

function Battle:roll(random)
 if self.rolled or self.won then return end
 self.rolled=random(1,6)
 self.remaining=self.rolled
end

function Battle:endTurn()
 if self.won then return end
 self.rolled=nil
 self.remaining=0
end

function Battle:actionError()
 if self.won then return '승리했습니다.' end
 if not self.rolled then return '먼저 주사위를 굴리세요.' end
 if self.remaining==0 then return '남은 행동이 없습니다.' end
end

function Battle:canMove(tile,pulley)
 return Movement.step(self.map,self.warrior,tile,{[self.target]=self.hp>0},pulley)
end

function Battle:touches(edge)
 return edge.tile==self.warrior or edge.neighbor==self.warrior
end

function Battle:canToggleDoor(edge)
 return edge.kind=='door' and edge.hp>0 and self:touches(edge)
end

function Battle:canAttack(target)
 if target.kind then
  return target.hp>0 and self:touches(target)
 end
 return target==self.target and self.hp>0 and Grid.distance(self.warrior,target)==1
  and math.abs(self.warrior.height-target.height)<=1
  and not World.blocked(self.map,self.warrior,target)
end

function Battle:attack(target)
 local errorMessage=self:actionError()
 if errorMessage then return errorMessage end
 if not self:canAttack(target) then return '공격 범위를 벗어났거나 공격 경로가 막혀 있습니다.' end
 self.remaining=self.remaining-1
 if target.kind then
  World.damage(target,10)
  return target.hp==0 and '시설물을 파괴했습니다.' or '시설물에 피해 10을 입혔습니다.'
 end
 self.hp=math.max(0,self.hp-10)
 self.won=self.hp==0
 return self.won and '승리했습니다. 시험 표적을 제거했습니다.' or '도끼 공격으로 피해 10을 입혔습니다.'
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
 if tile==self.target and self.hp>0 and not pulley then return self:attack(tile) end
 local errorMessage=self:actionError()
 if errorMessage then return errorMessage end
 local cost,reason=self:canMove(tile,pulley)
 if not cost then return reason end
 self.warrior=tile
 self.remaining=self.remaining-cost
 self.won=tile.flag==2
 return self.won and '승리했습니다. 적군 깃발에 도달했습니다.' or '이동했습니다.'
end

return Battle
