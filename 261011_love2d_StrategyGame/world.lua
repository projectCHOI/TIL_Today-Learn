local Hex=require('hexmap')
local W={}
local dirs={{1,0},{0,1},{-1,1},{-1,0},{0,-1},{1,-1}}
function W.new(a,e)
 local map=Hex.new(a,e)
 map.edges={}; map.buildings={}
 for i,t in ipairs(map.tiles) do
  t.id=i; t.height=0
  local col=t.q+math.floor(t.r/2)
  if col<=2 and t.r>=1 then t.height=0.55 end
  if col>=7 and t.r>=2 then t.height=-0.4 end
  if i%9==0 then t.object='tree' elseif i%11==0 then t.object='rock' elseif i%4==0 then t.object='grass' end
 end
 -- Two neighboring enemy tiles form a compact building at every supported map size.
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
    if not door and n and not n.building then kind='door'; door=true end
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
