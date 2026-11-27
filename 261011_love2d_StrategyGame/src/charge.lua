local Grid=require('src.grid')
local World=require('src.world')
local Combat=require('src.combat')
local Charge={}
local function contains(offsets,origin,tile)
 if not origin or not tile then return false end
 for _,d in ipairs(offsets or {}) do
  if tile.q-origin.q==d[1] and tile.r-origin.r==d[2] then return true end
 end
 return false
end
function Charge.canTarget(map,origin,landing,health,enemy,skill)
 return contains(skill.originOffsets,origin,enemy.tile)
  and Combat.canTarget(map,{tile=landing,health=health},enemy,skill)
end
function Charge.canLand(battle,tile,skill)
 if not skill.charge or battle.pendingCharge or not tile or battle.health<=0
  or (battle.moveLocks or 0)>0 then return false end
 local origin=battle.warrior
 if not contains(skill.landings,origin,tile) then return false end
 if skill.jumpHeight and math.abs(origin.height-tile.height)>skill.jumpHeight then return false end
 local occupied=battle.occupied and battle:occupied() or {}
 for _,enemy in ipairs(battle.enemies) do if enemy.health>0 then occupied[enemy.tile]=true end end
 for chest in pairs(battle.chests) do occupied[chest]=true end
 if occupied[tile] or tile.object=='rock' then return false end
 -- Never move through a closed door, wall, unit, chest or rock.
 -- Eagle Talon alone can traverse height gaps of up to three without a pulley.
 local maxSteps=Grid.distance(origin,tile)
 local queue={{origin,0}};local seen={[origin]=true};local index=1;local reached=false
 while queue[index] do
  local from,steps=queue[index][1],queue[index][2];index=index+1
  if from==tile then reached=true;break end
  if steps<maxSteps then
   for _,d in ipairs({{1,0},{-1,0},{0,1},{0,-1}}) do
    local nextTile=Grid.get(battle.map,from.q+d[1],from.r+d[2])
    if nextTile and not seen[nextTile] and not occupied[nextTile] and nextTile.object~='rock'
     and math.abs(from.height-nextTile.height)<=(skill.jumpHeight or 1)
     and (not skill.jumpHeight or math.abs(origin.height-nextTile.height)<=skill.jumpHeight)
     and not World.blocked(battle.map,from,nextTile) then
     seen[nextTile]=true;queue[#queue+1]={nextTile,steps+1}
    end
   end
  end
 end
 if not reached then return false end
 for _,enemy in ipairs(battle.enemies) do
  if Charge.canTarget(battle.map,origin,tile,battle.health,enemy,skill) then return true end
 end
 return false
end
return Charge
