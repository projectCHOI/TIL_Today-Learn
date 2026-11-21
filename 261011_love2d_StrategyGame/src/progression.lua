-- Session-only character progress. No disk persistence.
local P={}
local sessions={}
local labels={'하급','중급','상급'}
function P.get(character)
 local id=character.name
 if not sessions[id] then sessions[id]={rank=1,uses={}} end
 return sessions[id]
end
function P.label(character) return labels[P.get(character).rank] end
function P.stats(character)
 local rank=P.get(character).rank
 return character.ranks and character.ranks[rank] or character.stats
end
function P.skills(character)
 local result={}
 local rank=P.get(character).rank
 for i,id in ipairs(character.combatSkills or {}) do
  if i<=rank*2 then result[#result+1]=id end
 end
 return result
end
function P.record(unit,id)
 local state=P.get(unit.character)
 state.uses[id]=(state.uses[id] or 0)+1
 local rule=unit.character.promotions and unit.character.promotions[state.rank]
 if not rule or (state.uses[rule.skill] or 0)<rule.count then return end
 local oldMax=unit.maxHealth
 state.rank=state.rank+1
 unit.stats=P.stats(unit.character)
 unit.maxHealth=unit.stats[1]
 if unit.health>0 then unit.health=math.min(unit.maxHealth,unit.health+unit.maxHealth-oldMax) end
 return labels[state.rank]..' 승급 · 최대 체력 증가분 회복'
end
return P
