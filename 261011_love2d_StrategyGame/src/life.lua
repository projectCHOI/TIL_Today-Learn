-- Death-triggered items are resolved before battle defeat checks.
local Items=require('src.items')
local Life={}
function Life.tryRevive(unit)
 if unit.health>0 or type(unit.bag)~='table' then return false end
 local maximum=unit.maxHealth or (unit.stats and unit.stats[1])
 if not maximum or maximum<=0 then return false end
 for index,item in ipairs(Items) do
  if item.revive and (unit.bag[index] or 0)>0 then
   unit.bag[index]=unit.bag[index]-1
   unit.health=maximum
   return true
  end
 end
 return false
end
return Life
