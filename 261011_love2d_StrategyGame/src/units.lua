local Progress=require('src.progression')
local Units={}
Units.fields={character=true,stats=true,element=true,tile=true,warrior=true,attackers=true,skillId=true,
 equippedGem=true,bag=true,maxHealth=true,health=true,rageStacks=true,baseElement=true,extraElement=true,moveLocks=true,
 actionLocks=true,howlUsed=true,attackBonus=true,specialBonus=true,faction=true}
function Units.new(character,tile,bag)
 local stats=Progress.stats(character)
 return {character=character,name=character.korean,stats=stats,tile=tile,bag=bag or {},
  health=stats[1],maxHealth=stats[1],element=character.element,baseElement=character.element,
  equippedGem=bag and bag.equippedGem,extraElement=bag and bag.equippedGem and require('src.items')[bag.equippedGem].element,
  skillId=character.combatSkills[1],attackers={},rageStacks=0,faction='ally'}
end
function Units.occupied(battle,except)
 local occupied={}
 for _,list in ipairs({battle.units or {},battle.enemies,battle.spirits or {}}) do
  for _,unit in ipairs(list) do
   if unit~=except and unit.health>0 then occupied[unit.tile]=true end
  end
 end
 return occupied
end
function Units.at(battle,tile,includeDead)
 for _,list in ipairs({battle.units or {},battle.enemies,battle.spirits or {}}) do
  for _,unit in ipairs(list) do
   if unit.tile==tile and (includeDead or unit.health>0) then return unit end
  end
 end
end
return Units
