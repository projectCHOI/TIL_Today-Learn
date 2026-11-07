local Hex=require('src.grid')
local World=require('src.world')
local M={}

function M.step(map,from,to,occupied,pulley)
 if not to then return nil,'이동할 타일을 선택하세요.' end
 if pulley then
  if map.pulleys[from]~=to then return nil,'연결된 도르래가 없습니다.' end
 elseif Hex.distance(from,to)~=1 then
  return nil,'인접한 칸을 선택하세요.'
 elseif math.abs(from.height-to.height)>1 then
  return nil,'단차가 큽니다. 도르래나 우회로를 이용하세요.'
 end
 if occupied[to] then return nil,'도착 칸이 점유되어 있습니다.' end
 if to.object=='rock' then return nil,'바위가 이동을 막습니다.' end
 if World.blocked(map,from,to) then return nil,'벽이나 닫힌 문이 이동을 막습니다.' end
 return 1
end

return M
