local Hex=require('src.grid')
local W={}
local outpost=require('src.outpost')
local dirs={{1,0},{0,1},{-1,0},{0,-1}}
function W.new(a,e,preset)
 local map=preset and Hex.rectangle(outpost.width,outpost.height) or Hex.new(a,e)
 map.edges={}; map.buildings={}; map.pulleys={}
 for i,t in ipairs(map.tiles) do
  t.id=i; t.height=0
  if not preset then
   if t.q<=2 and t.r>=1 then t.height=1 end
   if t.q>=7 and t.r>=2 then t.height=-1 end
   if i%9==0 then t.object='tree' elseif i%11==0 then t.object='rock' elseif i%4==0 then t.object='grass' end
  end
 end
 local function at(position)
  return assert(Hex.get(map,position[1],position[2]),'Invalid outpost coordinate')
 end
 local inside={}
 local doorTargets={}
 if preset then
  for _,position in ipairs(outpost.high) do at(position).height=2 end
  for _,position in ipairs(outpost.steps) do at(position).height=1 end
  for _,position in ipairs(outpost.low) do at(position).height=-1 end
  for _,position in ipairs(outpost.objects) do at(position).object=position[3] end
  for _,position in ipairs(outpost.building) do inside[#inside+1]=at(position) end
  for _,door in ipairs(outpost.doors) do doorTargets[at(door[1])]=at(door[2]) end
  local lower,upper=at(outpost.pulley[1]),at(outpost.pulley[2])
  map.pulleys[lower]=upper
  map.pulleys[upper]=lower
  for side,position in ipairs(outpost.flags) do at(position).flag=side end
 else
  inside={map.tiles[a+1],map.tiles[a+2]}
 end
 for _,t in ipairs(inside) do t.building=1; t.object=nil; t.height=0 end
 map.buildings[1]={id=1,tiles=inside,indestructible=true}
 local door=false
 for _,t in ipairs(inside) do
  local vertices=Hex.vertices(t,1)
  for i,d in ipairs(dirs) do
   local n=Hex.get(map,t.q+d[1],t.r+d[2])
   if not n or n.building~=1 then
    local kind='wall'
    if n and (doorTargets[t]==n or (not preset and not door)) then kind='door'; door=true end
    local j=i==4 and 1 or i*2+1
    map.edges[#map.edges+1]={tile=t,neighbor=n,kind=kind,hp=kind=='door' and 60 or 100,maxhp=kind=='door' and 60 or 100,open=false,
      ax=vertices[i*2-1],ay=vertices[i*2],bx=vertices[j],by=vertices[j+1],height=1.45}
   end
  end
 end
 return map
end
function W.toggle(edge)
 if edge.kind=='door' and edge.hp>0 then edge.open=not edge.open; return true end
 return false
end
function W.damage(edge,amount)
 if amount<=0 then return end
 edge.hp=math.max(0,edge.hp-amount)
 if edge.hp==0 then edge.open=false end
end
function W.blocked(map,a,b)
 for _,edge in ipairs(map.edges) do
  if (edge.tile==a and edge.neighbor==b) or (edge.tile==b and edge.neighbor==a) then
   return edge.hp>0 and not edge.open
  end
 end
 return false
end
return W
