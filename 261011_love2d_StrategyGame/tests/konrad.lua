local G=require('src.grid')
local B=require('src.skirmish')
local C=require('src.combat')
local A=require('src.area')
local D=require('src.damage')
local P=require('src.progression')
local S=require('src.skills')
local chars=require('src.characters')
local count,serial=0,0
local function check(v,label) assert(v,label);count=count+1 end
local function fixture(rank)
 serial=serial+1
 local char={};for k,v in pairs(chars[3]) do char[k]=v end
 char.name='konrad_test_'..serial;P.get(char).rank=rank or 1
 local map=G.rectangle(12,12);map.edges={};map.pulleys={}
 for _,t in ipairs(map.tiles) do t.height=0 end
 local b=B.new(map,char,{})
 b.chests={};b.enemies={};b.tile=G.get(map,5,5);b.warrior=b.tile
 b.rolled=6;b.remaining=99;b.random=function(a,z) return a==0 and 0 or z end
 return b,map,char
end
local function add(b,q,r,health)
 local e={name='test enemy',health=health or 1000,stats={1000,30,35,20,20,45},element='노말',tile=G.get(b.map,q,r),attackers={}}
 b.enemies[#b.enemies+1]=e;return e
end
local function size(t) local n=0;for _ in pairs(t) do n=n+1 end;return n end
-- Validate the complete diagrams, including the gaps between the red groups.
do
 local b,map=fixture(3);local e=add(b,5,2)
 for _,id in ipairs({'aim','lockheed'}) do
  local n=0
  for dx=-4,4 do for dy=-4,4 do
   e.tile=G.get(map,5+dx,5+dy)
   local expected
   if id=='aim' then expected=(math.abs(dx)<=1 and math.abs(dy)==3) or (math.abs(dx)==3 and math.abs(dy)<=1)
   else expected=(dx==0 or dy==0) and math.abs(dx)+math.abs(dy)==4 end
   local actual=C.canTarget(map,b,e,S[id])
   check(not not actual==not not expected,id..' exact range '..dx..','..dy)
   if actual then n=n+1 end
  end end
  check(n==(id=='aim' and 12 or 4),id..' range size')
 end
 local counts={wind_burst=24,gale=48,shotgun=28,steel_rain=40}
 for id,n in pairs(counts) do
  check(size(A.cells(b,S[id]))==n,id..' all region cells')
 end
 for i=1,8 do check(size(A.cells(b,S.shotgun,i))==(i<=4 and 6 or 1),'shotgun selected group') end
 for i=1,4 do check(size(A.cells(b,S.steel_rain,i))==10,'steel rain selected group') end
 check(A.groupAt(b.tile,b.tile,S.wind_burst)==nil,'self excluded from wind')
 check(A.groupAt(b.tile,G.get(map,7,3),S.shotgun)==nil,'gap is not a group')
end
-- Independent accuracy rolls and one cost/use per multi-target cast.
do
 local b=fixture(2);b:selectSkill('shotgun')
 local a=add(b,4,1);local c=add(b,5,1);local d=add(b,6,1)
 local rolls={95,94,0};local accuracyRolls=0;local damageRolls=0
 b.random=function(lo,hi)
  if hi==99 then accuracyRolls=accuracyRolls+1;return rolls[accuracyRolls] end
  damageRolls=damageRolls+1;return hi
 end
 local before=b.remaining;local message=b:castArea(1)
 check(a.health==1000 and c.health<1000 and d.health<1000,'95 misses,94 and0 hit separately')
 check(accuracyRolls==3 and damageRolls==2,'accuracy independently consumed per enemy')
 check(b.remaining==before-2 and P.get(b.character).uses.shotgun==1,'one cost and use for three targets')
 check(message:find('대상 3') and message:find('명중 2'),'cast summary')
end
-- Only the selected region is attacked; a blocked portion remains undamaged.
do
 local b,map=fixture(2);b:selectSkill('steel_rain')
 local blocked=add(b,5,2);local clear=add(b,3,2);local otherGroup=add(b,1,5)
 map.edges={{kind='wall',hp=100,tile=G.get(map,5,4),neighbor=G.get(map,5,3)}}
 b:castArea(1)
 check(blocked.health==1000 and clear.health<1000,'partial wall blocking')
 check(otherGroup.health==1000,'unselected group untouched')
 map.edges[1].kind='door';map.edges[1].hp=60;map.edges[1].open=false
 local before=blocked.health;b:castArea(1)
 check(blocked.health==before,'closed door blocks steel rain')
 map.edges[1].open=true;b:castArea(1)
 check(blocked.health<before,'open door allows steel rain')
end
-- Rejected casts consume nothing; invalid heights never reach damage calculation.
do
 local b,map=fixture(2);b:selectSkill('shotgun');local e=add(b,5,2);local before=b.remaining
 b:castArea(8);check(b.remaining==before and not P.get(b.character).uses.shotgun,'empty region not executed')
 b:castArea(0);b:castArea(9);check(b.remaining==before,'invalid group rejected')
 b.remaining=1;b:castArea(1);check(b.remaining==1,'insufficient AP rejected')
 b.remaining=99;e.tile.height=4;b:castArea(1)
 check(b.remaining==99 and e.health==1000,'height4 excluded')
 for _,height in ipairs({-3,3}) do
  e.tile.height=height;b:castArea(1);check(e.health<1000,'height3 attacked')
 end
end
-- Wind uses special damage at the original position, then pushes survivors outside the blue box.
do
 local b,map=fixture();b:selectSkill('wind_burst');local e=add(b,6,5)
 e.stats[3]=1000;e.stats[5]=1;e.tile.height=1
 local _,expected=C.preview(b,e,S.wind_burst)
 local before=b.remaining;b:castArea(1)
 check(e.health==1000-expected,'special damage before displacement')
 check(e.tile==G.get(map,8,5),'pushed to first tile outside radius2')
 check(b.remaining==before-1,'wind AP cost1')
 local c,m=fixture(3);c:selectSkill('gale');local target=add(c,6,6)
 c:castArea(1)
 check(target.tile==G.get(m,9,9),'gale diagonal outside radius3')
 check(c.remaining==97 and target.health<1000,'gale special damage and cost2')
end
-- Knockback does not tunnel through obstacles or occupied tiles and never adds collision damage.
do
 local b,map=fixture();local e=add(b,7,5);local blocker=add(b,8,5)
 check(not A.push(b,e,2) and e.tile==G.get(map,7,5),'unit blocks push')
 blocker.health=0;map.edges={{kind='wall',hp=100,tile=e.tile,neighbor=G.get(map,8,5)}}
 check(not A.push(b,e,2),'wall blocks push')
 map.edges[1].kind='door';map.edges[1].hp=60;map.edges[1].open=false
 check(not A.push(b,e,2),'closed door blocks push')
 map.edges={};b.chests[G.get(map,8,5)]={item=1}
 check(not A.push(b,e,2),'chest blocks push');b.chests={}
 G.get(map,8,5).object='rock';check(not A.push(b,e,2),'rock blocks push');G.get(map,8,5).object=nil
 G.get(map,8,5).height=2;check(not A.push(b,e,2),'unsafe cliff blocks push');G.get(map,8,5).height=0
 check(A.push(b,e,2) and e.tile==G.get(map,8,5),'clear route pushes normally')
 b.tile=G.get(map,10,5);b.warrior=b.tile;e.tile=G.get(map,11,5)
 check(not A.push(b,e,2) and e.tile==G.get(map,11,5),'map edge blocks push')
end
-- Outer-first handling moves a line outward without duplicate target damage or overlapping units.
do
 local b,map=fixture();b:selectSkill('wind_burst');local near=add(b,6,5);local far=add(b,7,5)
 local _,damage=C.preview(b,near,S.wind_burst)
 b:castArea(1)
 check(far.tile==G.get(map,8,5) and near.tile==G.get(map,7,5),'outer enemy moves first, inner stops behind it')
 check(near.health==1000-damage and far.health==1000-damage,'each enemy hit exactly once')
 local c=fixture();c:selectSkill('wind_burst');local dead=add(c,6,5,1);local original=dead.tile
 c:castArea(1);check(dead.health==0 and dead.tile==original and c.won,'dead target not pushed; last enemy victory')
end
-- Lockheed immobilizes on hit; one future valid movement attempt is blocked.
do
 local b,map=fixture(3);b:selectSkill('lockheed');local e=add(b,9,5)
 b:attack(e.tile)
 check(e.moveLocks==1 and b.remaining==95,'lockheed hit and cost4')
 check(not b:moveEnemy(e,G.get(map,10,5),false) and e.moveLocks==0,'first move blocked')
 check(b:moveEnemy(e,G.get(map,10,5),false),'next movement allowed')
 e.tile=G.get(map,9,5);local before=e.health
 b.random=function(lo,hi) return hi end;b:attack(e.tile)
 check(e.health==before and e.moveLocks==0,'miss does not immobilize')
end
-- Progress survives battles, misses count, and a shotgun cast counts once even with multiple targets.
do
 local b,map,char=fixture();b.health=20;local e=add(b,5,2)
 for i=1,3 do b:attack(e.tile) end
 check(P.get(char).rank==2 and b.health==43 and b.maxHealth==63,'middle promotion on third aim')
 check(b.stats[2]==60 and b.stats[6]==71 and #b:skillIds()==4,'middle stats')
 b:selectSkill('shotgun');add(b,4,2);b.random=function(lo,hi) return hi end
 b:castArea(1)
 check(P.get(char).rank==2 and P.get(char).uses.shotgun==1,'one all-miss cast counts once')
 b:castArea(1)
 check(P.get(char).rank==3 and b.health==63 and b.maxHealth==83,'upper promotion on second all-miss cast')
 check(b.stats[2]==80 and b.stats[6]==101 and #b:skillIds()==6,'upper stats')
 check(B.new(map,char,{}).maxHealth==83,'next battle retains rank')
 local stone
 for i,item in ipairs(require('src.items')) do if item.revive then stone=i end end
 b.bag[stone]=1;b.health=0;require('src.life').tryRevive(b)
 check(b.health==83 and b.bag[stone]==0,'Konrad resurrection uses upper HP')
end
print('Konrad tests passed: '..count)
