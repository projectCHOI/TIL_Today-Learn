local Grid=require('src.grid')
local World=require('src.world')
local Damage=require('src.damage')
local Life=require('src.life')
local Rules=require('src.rules')
local Combat={}

-- Traverse crossed tile boundaries. At a diagonal corner, all four edges must be clear.
function Combat.pathClear(map,from,to)
 local dx,dy=to.q-from.q,to.r-from.r
 local sx=dx>=0 and 1 or -1
 local sy=dy>=0 and 1 or -1
 local tx=dx==0 and math.huge or .5/math.abs(dx)
 local ty=dy==0 and math.huge or .5/math.abs(dy)
 local stepX=dx==0 and math.huge or 1/math.abs(dx)
 local stepY=dy==0 and math.huge or 1/math.abs(dy)
 local tile=from
 while tile~=to do
  if math.abs(tx-ty)<1e-9 then
   local x=Grid.get(map,tile.q+sx,tile.r)
   local y=Grid.get(map,tile.q,tile.r+sy)
   local nextTile=Grid.get(map,tile.q+sx,tile.r+sy)
   if not x or not y or not nextTile or World.blocked(map,tile,x)
    or World.blocked(map,tile,y) or World.blocked(map,x,nextTile)
    or World.blocked(map,y,nextTile) then return false end
   tile=nextTile
   tx=tx+stepX
   ty=ty+stepY
  elseif tx<ty then
   local nextTile=Grid.get(map,tile.q+sx,tile.r)
   if not nextTile or World.blocked(map,tile,nextTile) then return false end
   tile=nextTile
   tx=tx+stepX
  else
   local nextTile=Grid.get(map,tile.q,tile.r+sy)
   if not nextTile or World.blocked(map,tile,nextTile) then return false end
   tile=nextTile
   ty=ty+stepY
  end
 end
 return true
end

function Combat.canTarget(map,attacker,defender,skill)
 if attacker.health<=0 or defender.health<=0 then return false end
 local a,b=attacker.tile,defender.tile
 local dx,dy=math.abs(a.q-b.q),math.abs(a.r-b.r)
 local distance=skill.metric=='chebyshev' and math.max(dx,dy) or dx+dy
 local inRange=false
 if skill.area=='center' then
  inRange=math.max(dx,dy)<=skill.radius and dx+dy>0
 elseif skill.area=='groups' or skill.area=='all' then
  local q,r=b.q-a.q,b.r-a.r
  for _,region in ipairs(skill.regions) do
   if q>=region[1] and q<=region[3] and r>=region[2] and r<=region[4] then inRange=true;break end
  end
 elseif skill.offsets then
  for _,offset in ipairs(skill.offsets) do
   if b.q-a.q==offset[1] and b.r-a.r==offset[2] then inRange=true end
  end
 else inRange=distance>=skill.minRange and distance<=skill.maxRange end
 if skill.straight and dx~=0 and dy~=0 then return false end
 return inRange
  and math.abs(a.height-b.height)<=(skill.maxHeight or 3) and (skill.ignoreWalls or Combat.pathClear(map,a,b))
end

function Combat.input(attacker,defender,skill,random)
 local power=skill.power
 if skill.heightPower and attacker.tile.height~=defender.tile.height then power=power*2 end
 if skill.rage then power=power+30*math.min(9,attacker.rageStacks or 0) end
 if skill.retaliation and attacker.attackers[defender] then power=power*2 end
 local types={defender.element}
 if defender.extraElement then types[2]=defender.extraElement end
 return {
  attacker=attacker,defender=defender,category=skill.category,power=power,
  attackType=skill.element,defenderTypes=types,
  attackerHeight=attacker.tile.height,defenderHeight=defender.tile.height,random=random,ignoreTerrain=skill.ignoreTerrain
 }
end

function Combat.preview(attacker,defender,skill)
 if skill.sacrifice then return defender.health,defender.health end
 local low,high=Damage.range(Combat.input(attacker,defender,skill))
 return low*(skill.finalMultiplier or 1),high*(skill.finalMultiplier or 1)
end

function Combat.execute(attacker,defender,skill,random)
 -- Record an executed attack before its accuracy roll, including misses.
 defender.attackers=defender.attackers or {}
 attacker.attackers=attacker.attackers or {}
 defender.attackers[attacker]=true
 if attacker.faction=='ally' and defender.hypnotized and Rules.hypnosisWakeOnMiss then defender.hypnotized=nil end
 if random(0,99)>=skill.accuracy then return 0,false end
 if attacker.faction=='ally' then defender.hypnotized=nil end
 local amount=skill.sacrifice and defender.health or Damage.calculate(Combat.input(attacker,defender,skill,random))
 amount=amount*(skill.finalMultiplier or 1)
 if skill.root then defender.moveLocks=skill.rootCount or 1 end
 if skill.stun then defender.actionLocks=skill.stun end
 if skill.sacrifice then attacker.health=0 end
 defender.health=math.max(0,defender.health-amount)
 local revived={}
 if Life.tryRevive(defender) then revived[#revived+1]=defender end
 if skill.sacrifice and Life.tryRevive(attacker) then revived[#revived+1]=attacker end
 if defender.health==0 then
  for source in pairs(defender.attackers) do if source.attackers then source.attackers[defender]=nil end end
  attacker.attackers[defender]=nil
  defender.attackers={}
 end
 return amount,true,revived
end

return Combat
