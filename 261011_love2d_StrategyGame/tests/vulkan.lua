-- Run from the project root: lua tests/vulkan.lua
local G=require('src.grid')
local W=require('src.world')
local B=require('src.skirmish')
local C=require('src.combat')
local S=require('src.skills')
local P=require('src.progression')
local profiles=require('src.characters')
local count=0
local function check(value,label) assert(value,label);count=count+1 end
local serial=0
local function fixture()
 serial=serial+1
 local char={}
 for k,v in pairs(profiles[1]) do char[k]=v end
 char.name='test'..serial
 local map=G.rectangle(12,12);map.edges={};map.pulleys={}
 for _,t in ipairs(map.tiles) do t.height=0 end
 local b=B.new(map,char,{})
 b.chests={};b.warrior=G.get(map,5,5);b.tile=b.warrior
 b.rolled=6;b.remaining=99;b.random=function(lo,hi) return lo end
 for i,e in ipairs(b.enemies) do
  e.tile=G.get(map,6,5);e.health=10000;e.stats[1]=10000
 end
 return b,map,char
end
local function enemy(b,q,r,h)
 local e=b.enemies[1];e.tile=G.get(b.map,q,r);e.health=h or 10000
 b.enemies={e};return e
end
-- All cells in a 5x5 area are compared to the exact diagrams.
do
 local b=fixture();local e=enemy(b,6,5)
 local expected={axe_strike=4,rampage=8,wood_split=12,rage_axe=4,final_gambit=4}
 for id,n in pairs(expected) do
  local seen=0
  for dx=-2,2 do for dy=-2,2 do
   e.tile=G.get(b.map,5+dx,5+dy)
   if C.canTarget(b.map,b,e,S[id]) then seen=seen+1 end
  end end
  check(seen==n,id..' mask')
 end
 e.tile=G.get(b.map,5,6)
 check(C.canTarget(b.map,b,e,S.wood_split),'wood below center included')
 e.tile.height=3
 check(not C.canTarget(b.map,b,e,S.axe_strike),'height three rejected')
 e.tile.height=2
 check(C.canTarget(b.map,b,e,S.axe_strike),'height two allowed')
end
-- Misses count; promotion heals exactly the increased maximum; per-session state survives a new battle.
do
 local b,map,char=fixture();local e=enemy(b,6,5)
 b.health=20;b.random=function(lo,hi) return hi end
 check(not b:selectSkill('rage_axe'),'locked skill')
 for i=1,4 do b:attack(e.tile) end
 check(P.get(char).rank==2,'middle promotion on fourth miss')
 check(b.health==45 and b.maxHealth==65,'promotion health delta')
 check(b.stats[2]==105 and #b:skillIds()==4,'middle stats and skills')
 local nextBattle=B.new(map,char,{})
 check(nextBattle.maxHealth==65 and P.get(char).uses.axe_strike==4,'session retention')
 b:selectSkill('rage_axe')
 for i=1,4 do b:attack(e.tile) end
 check(P.get(char).rank==3 and b.maxHealth==110 and b.health==90,'upper promotion')
 check(b.stats[4]==50 and #b:skillIds()==6,'upper stats and six skills')
 for i=1,10 do b:attack(e.tile) end
 check(b.rageStacks==9,'rage capped at nine increases')
 check(P.get(char).uses.rage_axe==14,'misses counted')
 check(B.new(map,char,{}).rageStacks==0,'rage resets each stage')
 local another=fixture()
 check(P.get(another.character).rank==1,'new identity starts lower')
end
-- Rage preview follows power 30,60,...300; misses still advance it.
do
 local b=fixture();local e=enemy(b,6,5);P.get(b.character).rank=2;b:selectSkill('rage_axe')
 local lo,hi=C.preview(b,e,S.rage_axe)
 check(lo==11 and hi==14,'rage initial power30')
 b:attack(e.tile)
 lo,hi=C.preview(b,e,S.rage_axe)
 check(lo==22 and hi==26,'rage next power60')
end
-- Retaliation is per attacking enemy, including misses.
do
 local b=fixture();local e=enemy(b,6,5)
 C.execute(e,b,S.test_strike,function(lo,hi) return hi end)
 check(b.attackers[e] and b.health==40,'miss records retaliation')
 local lo,hi=C.preview(b,e,S.rampage)
 check(lo==35 and hi==42,'retaliation doubles skill power')
end
-- Root applies only on a hit and does not kill a high-HP target.
do
 local b=fixture();local e=enemy(b,6,5)
 C.execute(b,e,S.wood_split,function(lo,hi) return lo end)
 check(e.moveLocks==1 and e.health>0,'one movement lock')
 local destination=G.get(b.map,7,5)
 check(not b:moveEnemy(e,destination,false) and e.moveLocks==0,'root blocks and consumes one valid move')
 check(b:moveEnemy(e,destination,false) and e.tile==destination,'next move allowed')
end
-- Four blue landings; only eight red original offsets; no wall teleport.
do
 local b,map,char=fixture();P.get(char).rank=3;b:selectSkill('close_combat')
 local e=enemy(b,4,3)
 check(b:canCharge(G.get(map,3,3)),'blue landing reachable')
 check(not b:canCharge(G.get(map,3,5)),'nonblue rejected')
 local origin=b.tile
 local before=b.remaining
 b:beginCharge(G.get(map,3,3))
 check(b.tile==G.get(map,3,3) and b.remaining==before-2,'charge moves and pays two')
 check(b:canAttack(e.tile),'red attack available')
 check(not b:canAttack(G.get(map,2,3)),'outward cardinal rejected')
 check(not b:canMove(G.get(map,3,4),false),'no ordinary move while charging')
 local held=b.tile;b:endTurn();check(b.tile==held and b.pendingCharge,'cannot end turn midcharge')
 b:cancelCharge()
 check(b.tile==origin and b.remaining==before,'cancel refunds and restores')
 b:beginCharge(G.get(map,3,3));b:attack(e.tile)
 check(not b.pendingCharge and b.remaining==before-2,'attack adds no movement or attack cost')
 b.tile=origin;b.warrior=origin;b.remaining=99
 G.get(map,4,5).object='rock';G.get(map,5,4).object='rock'
 check(not b:canCharge(G.get(map,3,3)),'blocked route rejected')
end
-- Every blue corner matches its inward red attack and preserves instant flag victory.
do
 for _,d in ipairs({{-2,-2},{2,-2},{-2,2},{2,2}}) do
  local b,map,char=fixture();P.get(char).rank=3;b:selectSkill('close_combat')
  enemy(b,5+math.floor(d[1]/2),5+d[2])
  local landing=G.get(map,5+d[1],5+d[2])
  check(b:canCharge(landing),'each blue corner has a valid inward red target')
 end
 local b,map,char=fixture();P.get(char).rank=3;b:selectSkill('close_combat')
 enemy(b,4,3);local landing=G.get(map,3,3);landing.flag=2
 b:beginCharge(landing)
 check(b.won and not b.pendingCharge,'blue landing on flag wins immediately')
end
-- Sacrifice ignores ghost immunity/HP, win takes precedence over own death.
do
 local b,map,char=fixture();P.get(char).rank=3;b:selectSkill('final_gambit')
 local e=enemy(b,6,5,9999);e.element='고스트'
 b:attack(e.tile)
 check(e.health==0 and b.health==0,'sacrifice kills both')
 check(b.won and not b.lost,'last enemy sacrifice wins')
 local c=fixture();P.get(c.character).rank=3;c:selectSkill('final_gambit')
 c:attack(c.enemies[1].tile)
 check(c.lost and not c.won,'surviving enemies mean failure')
end
-- Closed wall blocks targeting, including the sacrifice.
do
 local b,map=fixture();local e=enemy(b,6,5)
 map.edges={{tile=b.tile,neighbor=e.tile,hp=100,kind='wall'}}
 check(not C.canTarget(map,b,e,S.final_gambit),'wall blocks final gambit')
 local uses=P.get(b.character).uses.axe_strike or 0
 b:attack(e.tile)
 check((P.get(b.character).uses.axe_strike or 0)==uses,'invalid attack not counted')
end
print('Vulkan tests passed: '..count)
