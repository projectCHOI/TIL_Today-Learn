local C={index=0,scale=35,ox=600,oy=450}
function C.turn(delta) C.index=math.max(-1,math.min(1,C.index+delta)) end
function C.project(x,y,z)
 local a=math.rad(-90+C.index*45)
 local xx=x*math.cos(a)-y*math.sin(a)
 local depth=x*math.sin(a)+y*math.cos(a)
 return C.ox+xx*C.scale,C.oy+depth*C.scale*0.58-(z or 0)*C.scale,depth
end
function C.fit(map,w,h)
 local points={}
 for _,t in ipairs(map.tiles) do
  local H=require('hexmap'); local v=H.vertices(t,1)
  for i=1,12,2 do points[#points+1]={v[i],v[i+1],t.height}; points[#points+1]={v[i],v[i+1],t.height+2.6} end
 end
 C.scale=1;C.ox=0;C.oy=0
 local minx,maxx,miny,maxy=math.huge,-math.huge,math.huge,-math.huge
 for _,p in ipairs(points) do
  local x,y=C.project(p[1],p[2],p[3]);minx=math.min(minx,x);maxx=math.max(maxx,x);miny=math.min(miny,y);maxy=math.max(maxy,y)
 end
 C.scale=math.min((w-240)/(maxx-minx),(h-260)/(maxy-miny),58)
 C.ox=w/2-(minx+maxx)/2*C.scale
 C.oy=190+(h-260)/2-(miny+maxy)/2*C.scale
end
return C
