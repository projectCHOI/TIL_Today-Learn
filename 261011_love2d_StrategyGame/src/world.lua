local Hex=require('src.hexmap')
local W={}
local outpost=require('src.outpost')
local dirs={{1,0},{0,1},{-1,1},{-1,0},{0,-1},{1,-1}}
function W.new(a,e,preset)
 local map=Hex.new(a,e)
 map.edges={}; map.buildings={}; map.pulleys={}
 for i,t in ipairs(map.tiles) do
  t.id=i; t.height=0
  local col=t.q+math.floor(t.r/2)
  if col<=2 and t.r>=1 then t.height=1 end
  if col>=7 and t.r>=2 then t.height=-1 end
  if i%9==0 then t.object='tree' elseif i%11==0 then t.object='rock' elseif i%4==0 then t.object='grass' end
 end
 -- Two neighboring enemy tiles form a compact building at every supported map size.
 if preset then
  local function at(position)
   local col,row=position[1],position[2]
   return Hex.get(map,col-math.floor(row/2),row)
  end
  for _,tile in ipairs(map.tiles) do tile.height=0;tile.object=nil end
  for _,position in ipairs(outpost.heights) do at(position).height=position[3] end
  for _,position in ipairs(outpost.objects) do at(position).object=position[3] end
  local lower,upper=at(outpost.pulley[1]),at(outpost.pulley[2])
  map.pulleys[lower]=upper
  map.pulleys[upper]=lower
  map.start=at(outpost.start)
 end
 local start=a+1
 local inside={map.tiles[start],map.tiles[start+1]}
 for _,t in ipairs(inside) do t.building=1; t.object=nil; t.height=0 end
 map.buildings[1]={id=1,tiles=inside,indestructible=true}
 local door=false
 for _,t in ipairs(inside) do
  local vertices=Hex.vertices(t,1)
  for i,d in ipairs(dirs) do
   local n=Hex.get(map,t.q+d[1],t.r+d[2])
   if not n or n.building~=1 then
    local kind='wall'
    if not door and n and not n.building and (not preset or n.side==1) then kind='door'; door=true end
    local j=i==6 and 1 or i*2+1
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
