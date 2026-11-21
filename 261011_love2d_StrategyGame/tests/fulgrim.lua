-- Run from the project root: lua tests/fulgrim.lua
local G=require('src.grid')
local B=require('src.skirmish')
local C=require('src.combat')
local Charge=require('src.charge')
local S=require('src.skills')
local D=require('src.damage')
local P=require('src.progression')
local chars=require('src.characters')
local count,serial=0,0
local function check(value,label) assert(value,label);count=count+1 end
local function fixture()
 serial=serial+1
 local char={};for k,v in pairs(chars[2]) do char[k]=v end
 char.name='fulgrim_test_'..serial
 local map=G.rectangle(12,12);map.edges={};map.pulleys={}
 for _,t in ipairs(map.tiles) do t.height=0 end
 local b=B.new(map,char,{})
 b.chests={};b.warrior=G.get(map,5,5);b.tile=b.warrior
 b.rolled=6;b.remaining=99;b.random=function(lo,hi) return hi==99 and 0 or hi end
 local enemy=b.enemies[1];enemy.health=10000;enemy.tile=G.get(map,6,5);enemy.element='노말'
 b.enemies={enemy}
 return b,map,char,enemy
end
local function shifted(map,origin,d) return G.get(map,origin.q+d[1],origin.r+d[2]) end
-- Exhaustive masks, not just total cell counts.
do
 local b,map,char,e=fixture()
 local cases={spear_thrust=8,spear_throw=4,triple_thrust=8,brave_spear=24}
 for id,expectedCount in pairs(cases) do
  local cells=0
  for dx=-3,3 do for dy=-3,3 do
   e.tile=G.get(map,5+dx,5+dy)
   local expected
   if id=='brave_spear' then
    expected=(dx==0 or dy==0 or math.abs(dx)==math.abs(dy)) and (dx~=0 or dy~=0)
   elseif id=='spear_throw' then
    expected=math.abs(dx)+math.abs(dy)==2 and (dx==0 or dy==0)
   else expected=(dx==0 or dy==0) and math.abs(dx)+math.abs(dy)>=1 and math.abs(dx)+math.abs(dy)<=2 end
   local actual=C.canTarget(map,b,e,S[id])
   check(not not actual==not not expected,id..' exact cell '..dx..','..dy)
   if actual then cells=cells+1 end
  end end
  check(cells==expectedCount,id..' count')
 end
end
-- Terrain extensions and per-character attack gates.
do
 check(D.terrain(3,0)==1.8,'three down')
 check(D.terrain(0,3)==.2,'three up')
 check(not pcall(D.terrain,0,4),'unconfigured four rejected')
 local b,map,char,e=fixture()
 for _,id in ipairs({'spear_thrust','spear_throw','triple_thrust','eagle_talon','brave_spear','reckless_thrust'}) do
  e.tile=G.get(map,5,3)
  if id=='reckless_thrust' then e.tile=G.get(map,5,4) end
  for _,height in ipairs({-3,3}) do
   e.tile.height=height;check(C.canTarget(map,b,e,S[id]),id..' height three accepted')
  end
  for _,height in ipairs({-4,4}) do
   e.tile.height=height;check(not C.canTarget(map,b,e,S[id]),id..' height four rejected')
  end
  e.tile.height=0
 end
 e.tile=G.get(map,6,5);e.tile.height=3
 check(not C.canTarget(map,b,e,S.axe_strike),'Vulkan remains height two')
end
-- Throw doubles power before terrain, whereas triple multiplies final rounded damage once.
do
 local b,map,char,e=fixture();e.tile=G.get(map,7,5)
 local lo,hi=C.preview(b,e,S.spear_throw)
 check(lo==7 and hi==9,'throw same height power60')
 b.tile.height=3
 lo,hi=C.preview(b,e,S.spear_throw)
 check(lo==26 and hi==30,'throw downhill power120 then x1.8')
 b.tile.height=0;e.tile.height=3
 lo,hi=C.preview(b,e,S.spear_throw)
 check(lo==2 and hi==3,'throw uphill power120 then x0.2')
 e.tile.height=0
 local base={};for k,v in pairs(S.triple_thrust) do base[k]=v end;base.finalMultiplier=nil
 local baseLo,baseHi=C.preview(b,e,base)
 lo,hi=C.preview(b,e,S.triple_thrust)
 check(lo==baseLo*3 and hi==baseHi*3,'triple final range')
 local rolls=0
 local damage,hit=C.execute(b,e,S.triple_thrust,function(a,z) rolls=rolls+1;return a==0 and 0 or z end)
 check(hit and damage==baseHi*3 and e.health==10000-damage,'triple one application')
 check(rolls==2,'one accuracy and one damage RNG roll only')
end
-- Promotions, HP recovery, per-character session data and misses.
do
 local b,map,char,e=fixture();b.health=17
 check(not b:selectSkill('eagle_talon'),'middle skill locked initially')
 for i=1,3 do b:attack(e.tile) end
 check(P.get(char).rank==2 and b.health==42 and b.maxHealth==55,'middle promotion and HP')
 check(b.stats[2]==75 and b.stats[6]==80 and #b:skillIds()==4,'middle stats and skills')
 check(P.get(chars[1]).rank==1,'Vulkan progress separate')
 b:selectSkill('eagle_talon')
 for i=1,2 do
  b.warrior=G.get(map,5,5);b.tile=b.warrior;e.tile=G.get(map,4,3)
  b:beginCharge(G.get(map,3,3));b:attack(e.tile)
 end
 check(P.get(char).rank==3 and b.health==72 and b.maxHealth==85,'upper promotion and HP')
 check(b.stats[2]==120 and b.stats[6]==100 and #b:skillIds()==6,'upper stats and skills')
 local nextBattle=B.new(map,char,{})
 check(nextBattle.maxHealth==85 and P.get(char).uses.eagle_talon==2,'next stage retains progress')
 local other=fixture()
 other.random=function(a,z) return z end -- force miss, despite production accuracy100
 local original=S.spear_thrust.accuracy;S.spear_thrust.accuracy=80
 for i=1,3 do other:attack(other.enemies[1].tile) end
 S.spear_thrust.accuracy=original
 check(P.get(other.character).rank==2 and other.enemies[1].health==10000,'misses still count without damage')
end
-- All blue/red move-then-attack masks exactly match both diagrams.
for _,id in ipairs({'eagle_talon','reckless_thrust'}) do
 local b,map,char,e=fixture();P.get(char).rank=3;b:selectSkill(id)
 local skill=S[id];local origin=b.tile;local union={}
 for _,d in ipairs(skill.landings) do
  local landing=shifted(map,origin,d)
  for _,r in ipairs(skill.originOffsets) do
   e.tile=shifted(map,origin,r)
   local dx,dy=math.abs(e.tile.q-landing.q),math.abs(e.tile.r-landing.r)
   local expected
   if id=='eagle_talon' then expected=(dx==0 or dy==0) and dx+dy>=1 and dx+dy<=2
   else expected=math.max(dx,dy)==1 end
   local actual=Charge.canTarget(map,origin,landing,b.health,e,skill)
   check(not not actual==not not expected,id..' corresponding red cell')
   if actual then union[e.tile]=true end
  end
  local candidate
  for _,r in ipairs(skill.originOffsets) do
   e.tile=shifted(map,origin,r)
   if Charge.canTarget(map,origin,landing,b.health,e,skill) then candidate=e.tile;break end
  end
  check(candidate and b:canCharge(landing),id..' each blue landing')
  e.tile=candidate
  local before=b.remaining
  b:beginCharge(landing)
  check(b.tile==landing and b.remaining==before-skill.cost,id..' payment on move')
  b:attack(e.tile)
  check(not b.pendingCharge and b.remaining==before-skill.cost,id..' attack has no extra payment')
  b.warrior=origin;b.tile=origin
 end
 local n=0;for _ in pairs(union) do n=n+1 end
 check(n==(id=='eagle_talon' and 20 or 12),id..' union of red cells')
end
-- Eagle climbs three without a pulley; normal movement and other charges do not.
do
 local b,map,char,e=fixture();P.get(char).rank=2;b:selectSkill('eagle_talon')
 local origin=b.tile;local landing=G.get(map,3,3);landing.height=3;e.tile=G.get(map,4,3)
 check(b:canCharge(landing),'eagle height3 without pulley')
 landing.height=4;check(not b:canCharge(landing),'eagle height4 rejected');landing.height=3
 local before=b.remaining
 b:beginCharge(landing);check(b.tile==landing,'eagle executes climb')
 b:cancelCharge();check(b.tile==origin and b.remaining==before,'cancel refunds eagle cost2')
 b.remaining=1;b:beginCharge(landing)
 check(not b.pendingCharge and b.tile==origin and b.remaining==1,'insufficient charge actions do nothing')
 b.remaining=99;landing.object='rock';check(not b:canCharge(landing),'rock landing rejected');landing.object=nil
 b.chests[landing]={item=1};check(not b:canCharge(landing),'chest landing rejected');b.chests[landing]=nil
 local other={health=5,tile=landing};b.enemies[2]=other
 check(not b:canCharge(landing),'occupied landing rejected');b.enemies[2]=nil
 map.edges={{kind='wall',hp=100,tile=origin,neighbor=G.get(map,4,5)},
 {kind='door',hp=60,open=false,tile=origin,neighbor=G.get(map,5,4)}}
 check(not b:canCharge(landing),'closed walls block departure routes')
 map.edges={};landing.height=0
 local to=e.tile
 map.edges={{kind='wall',hp=100,tile=landing,neighbor=to}}
 check(not b:canCharge(landing),'wall blocks landing-to-enemy attack')
end
-- Reckless direction selection, cost3 cancellation, ordinary movement unchanged.
do
 local b,map,char,e=fixture();P.get(char).rank=3;b:selectSkill('reckless_thrust')
 local origin=b.tile;local landing=G.get(map,5,3);e.tile=G.get(map,6,2)
 check(b:canCharge(landing),'reckless blue forward')
 b:beginCharge(landing);e.tile=G.get(map,8,5)
 check(not b:canAttack(e.tile),'cannot attack another direction red group')
 local before=b.remaining;b:cancelCharge()
 check(b.remaining==before+3 and b.tile==origin,'reckless cancel refunds three')
 e.tile=G.get(map,6,2);landing.height=3
 check(not b:canCharge(landing),'reckless does not acquire eagle jump')
 b:selectSkill('spear_thrust');local nextTile=G.get(map,5,4);nextTile.height=2
 check(not b:canMove(nextTile,false),'ordinary walk still limited to one height')
end
print('Fulgrim tests passed: '..count)
