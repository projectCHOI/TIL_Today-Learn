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

function Battle:act(tile,pulley)
 if self.won then return '승리했습니다.' end
 if not self.rolled then return '먼저 주사위를 굴리세요.' end
 if self.remaining==0 then return '남은 행동이 없습니다.' end
 if tile==self.target and self.hp>0 and not pulley then
  if Grid.distance(self.warrior,tile)~=1 then return '공격하려면 표적에 인접해야 합니다.' end
  if math.abs(self.warrior.height-tile.height)>1 or World.blocked(self.map,self.warrior,tile) then
   return '단차 또는 시설물이 공격을 막고 있습니다.'
  end
  self.hp=math.max(0,self.hp-10)
  self.remaining=self.remaining-1
  self.won=self.hp==0
  return self.won and '승리했습니다. 시험 표적을 제거했습니다.' or '도끼 공격으로 피해 10을 입혔습니다.'
 end
 local occupied={[self.target]=self.hp>0}
 local cost,reason=Movement.step(self.map,self.warrior,tile,occupied,pulley)
 if not cost then return reason end
 self.warrior=tile
 self.remaining=self.remaining-cost
 self.won=tile.flag==2
 return self.won and '승리했습니다. 적군 깃발에 도달했습니다.' or '이동했습니다.'
end

return Battle
