local TypeChart=require('src.type_chart')
local Damage={}
-- Adjust combat tempo here. Larger values reduce damage.
Damage.divisor=12

local function number(value,name,minimum)
 assert(type(value)=='number' and value==value and value<math.huge
  and value>=minimum,name..' must be a finite number >= '..minimum)
 return value
end

local function typeName(name)
 local aliases={['불']='불꽃',['드레곤']='드래곤',['벌래']='벌레'}
 name=aliases[name] or name
 assert(TypeChart[name],'Unknown type: '..tostring(name))
 return name
end

function Damage.terrain(attackerHeight,defenderHeight)
 number(attackerHeight,'attackerHeight',-math.huge)
 number(defenderHeight,'defenderHeight',-math.huge)
 local difference=attackerHeight-defenderHeight
 assert(difference%1==0 and math.abs(difference)<=3,
  'Height difference must be an integer from -3 to 3')
 local multipliers={[-3]=0.2,[-2]=0.4,[-1]=0.6,[0]=1,[1]=1.4,[2]=1.6,[3]=1.8}
 return multipliers[difference]
end

function Damage.effectiveness(attackType,defenderTypes)
 local row=TypeChart[typeName(attackType)]
 assert(type(defenderTypes)=='table' and #defenderTypes>=1 and #defenderTypes<=2,
  'Defender needs one or two types')
 local multiplier=1
 local seen={}
 for _,element in ipairs(defenderTypes) do
  element=typeName(element)
  -- A gem matching the base type does not square its weaknesses.
  if not seen[element] then
   multiplier=multiplier*row[element]
   seen[element]=true
  end
 end
 return multiplier
end

function Damage.gemEffectiveness(attackType,gemType,defenderTypes)
 local multiplier=1
 local seen={}
 for _,element in ipairs(defenderTypes) do
  element=typeName(element)
  if not seen[element] then
   for _,offense in ipairs({attackType,gemType}) do
    multiplier=multiplier*math.max(1,TypeChart[typeName(offense)][element])
   end
   seen[element]=true
  end
 end
 return multiplier
end

local function parameters(input)
 assert(type(input)=='table','Damage input must be a table')
 assert(input.category=='physical' or input.category=='special',
  'Skill category must be physical or special')
 local attackIndex=input.category=='physical' and 2 or 4
 local defenseIndex=input.category=='physical' and 3 or 5
 local bonus=attackIndex==2 and (input.attacker.attackBonus or 0) or (input.attacker.specialBonus or 0)
 local attack=number(input.attacker.stats[attackIndex]+bonus,'attack',0)
 local defense=number(input.defender.stats[defenseIndex],'defense',0)
 assert(defense>0,'Defense must be greater than zero')
 local power=number(input.power,'power',0)
 local divisor=number(Damage.divisor,'divisor',0)
 assert(divisor>0,'Divisor must be greater than zero')
 local base=math.floor(power*attack/defense/divisor+2)
 local terrain=input.ignoreTerrain and 1 or Damage.terrain(input.attackerHeight,input.defenderHeight)
 local effectiveness=input.gemType and Damage.gemEffectiveness(input.attackType,input.gemType,input.defenderTypes)
  or Damage.effectiveness(input.attackType,input.defenderTypes)
 return base,terrain,effectiveness
end

local function final(base,terrain,effectiveness,randomFactor)
 -- Follow the supplied formula literally, including its minimum of 1 at x0.
 return math.max(1,math.floor(base*terrain*effectiveness*randomFactor))
end

-- Pure calculation. Passing randomFactor makes test/replay results deterministic.
-- A supplied RNG follows Lua/LÖVE's random(min,max) API.
function Damage.calculate(input)
 local base,terrain,effectiveness=parameters(input)
 local randomFactor=input.randomFactor
 if randomFactor==nil then randomFactor=(input.random or math.random)(85,100)/100 end
 number(randomFactor,'randomFactor',0.85)
 assert(randomFactor<=1,'randomFactor must be <= 1')
 return final(base,terrain,effectiveness,randomFactor),{
  base=base,terrain=terrain,effectiveness=effectiveness,randomFactor=randomFactor
 }
end

-- UI preview without consuming random numbers or changing unit state.
function Damage.range(input)
 local base,terrain,effectiveness=parameters(input)
 return final(base,terrain,effectiveness,0.85),final(base,terrain,effectiveness,1)
end

return Damage
