local Grid=require('src.grid')
local World=require('src.world')
local Damage=require('src.damage')
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
 return distance>=skill.minRange and distance<=skill.maxRange
  and math.abs(a.height-b.height)<=skill.maxHeight and Combat.pathClear(map,a,b)
end

local function damageInput(attacker,defender,skill,random)
 local power=skill.power
 if skill.retaliation and attacker.attackers[defender] then power=power*2 end
 local types={defender.element}
 if defender.extraElement then types[2]=defender.extraElement end
 return {
  attacker=attacker,defender=defender,category=skill.category,power=power,
  attackType=skill.element,defenderTypes=types,
  attackerHeight=attacker.tile.height,defenderHeight=defender.tile.height,random=random
 }
end

function Combat.preview(attacker,defender,skill)
 return Damage.range(damageInput(attacker,defender,skill))
end

function Combat.execute(attacker,defender,skill,random)
 -- Record an executed attack before its accuracy roll, including misses.
 defender.attackers[attacker]=true
 if random(0,99)>=skill.accuracy then return 0,false end
 local amount=Damage.calculate(damageInput(attacker,defender,skill,random))
 defender.health=math.max(0,defender.health-amount)
 if defender.health==0 then
  for source in pairs(defender.attackers) do source.attackers[defender]=nil end
  attacker.attackers[defender]=nil
  defender.attackers={}
 end
 return amount,true
end

return Combat
