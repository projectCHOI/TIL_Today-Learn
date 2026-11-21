-- Region selection and knockback shared by area skills.
local Grid=require('src.grid')
local Combat=require('src.combat')
local Area={}
function Area.groupAt(origin,tile,skill)
 if not tile or tile.kind then return nil end
 local dx,dy=tile.q-origin.q,tile.r-origin.r
 if skill.area=='center' then
  if math.max(math.abs(dx),math.abs(dy))<=skill.radius and (dx~=0 or dy~=0) then return 1 end
 else
  for i,r in ipairs(skill.regions or {}) do
   if dx>=r[1] and dx<=r[3] and dy>=r[2] and dy<=r[4] then return i end
  end
 end
end
function Area.canReach(map,unit,tile,skill)
 return Area.groupAt(unit.tile,tile,skill)~=nil
  and math.abs(unit.tile.height-tile.height)<=skill.maxHeight
  and Combat.pathClear(map,unit.tile,tile)
end
function Area.cells(battle,skill,group)
 local cells={}
 for _,tile in ipairs(battle.map.tiles) do
  local id=Area.groupAt(battle.tile,tile,skill)
  if id and (not group or group==id) and Area.canReach(battle.map,battle,tile,skill) then cells[tile]=true end
 end
 return cells
end
function Area.targets(battle,skill,group)
 local targets={}
 for _,enemy in ipairs(battle.enemies) do
  if enemy.health>0 and Area.groupAt(battle.tile,enemy.tile,skill)==group
   and Area.canReach(battle.map,battle,enemy.tile,skill) then targets[#targets+1]=enemy end
 end
 return targets
end
local function sign(n) return n==0 and 0 or (n>0 and 1 or -1) end
function Area.push(battle,enemy,radius)
 local origin=battle.tile
 local dx,dy=sign(enemy.tile.q-origin.q),sign(enemy.tile.r-origin.r)
 if dx==0 and dy==0 then return false end
 local moved=false
 while math.max(math.abs(enemy.tile.q-origin.q),math.abs(enemy.tile.r-origin.r))<=radius do
  local tile=Grid.get(battle.map,enemy.tile.q+dx,enemy.tile.r+dy)
  if not tile or tile==battle.tile or tile.object=='rock' or battle.chests[tile]
   or math.abs(tile.height-enemy.tile.height)>1 or not Combat.pathClear(battle.map,enemy.tile,tile) then break end
  local occupied=false
  for _,other in ipairs(battle.enemies) do
   if other~=enemy and other.health>0 and other.tile==tile then occupied=true;break end
  end
  if occupied then break end
  enemy.tile=tile;moved=true
 end
 return moved
end
function Area.execute(battle,skill,targets)
 local result={count=#targets,hits=0,damage=0,moved=0,revivals=0}
 local hitUnits={}
 -- Snapshot targets once: moving one enemy must not change who gets hit.
 for _,enemy in ipairs(targets) do
  local amount,hit,revived=Combat.execute(battle,enemy,skill,battle.random or math.random)
  if hit then
   result.hits=result.hits+1;result.damage=result.damage+amount
   result.revivals=result.revivals+#(revived or {})
   if enemy.health>0 then hitUnits[#hitUnits+1]=enemy end
  end
 end
 if skill.push then
  -- Outer units move first so a column can move outward without swapping or overlap.
  table.sort(hitUnits,function(a,b)
   local da=math.max(math.abs(a.tile.q-battle.tile.q),math.abs(a.tile.r-battle.tile.r))
   local db=math.max(math.abs(b.tile.q-battle.tile.q),math.abs(b.tile.r-battle.tile.r))
   if da~=db then return da>db end
   if a.tile.q~=b.tile.q then return a.tile.q<b.tile.q end
   return a.tile.r<b.tile.r
  end)
  for _,enemy in ipairs(hitUnits) do
   if Area.push(battle,enemy,skill.radius) then result.moved=result.moved+1 end
  end
 end
 return result
end
return Area
