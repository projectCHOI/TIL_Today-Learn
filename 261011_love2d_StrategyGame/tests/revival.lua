local G=require('src.grid')
local W=require('src.world')
local B=require('src.skirmish')
local C=require('src.combat')
local S=require('src.skills')
local P=require('src.progression')
local L=require('src.life')
local Items=require('src.items')
local chars=require('src.characters')
local count,serial=0,0
local function check(v,label) assert(v,label);count=count+1 end
local stone
for i,item in ipairs(Items) do if item.id=='reawaken_stone' then stone=i end end
check(stone==18,'append item without renumbering existing inventory')
check(Items[stone].image=='mob_reawaken stone.png','exact image name including space')
local function fixture(profile,rank,stones)
 serial=serial+1
 local char={};for k,v in pairs(chars[profile or 1]) do char[k]=v end
 char.name='revival_test_'..serial
 P.get(char).rank=rank or 1
 local map=G.rectangle(12,12);map.edges={};map.pulleys={}
 for _,t in ipairs(map.tiles) do t.height=0 end
 local b=B.new(map,char,{[stone]=stones or 0})
 local e=b.enemies[1];e.tile=G.get(map,2,5);b.enemies={e}
 b.random=function(a,z) return a==0 and 0 or z end
 b.rolled=6;b.remaining=6
 return b,e,map
end
local lethal={category='physical',power=9999,accuracy=100,element='노말'}
do
 local b,e=fixture(1,1,2);local tile=b.tile;local before=b.remaining
 local amount,hit,revived=C.execute(e,b,lethal,b.random)
 check(hit and amount>=b.maxHealth,'lethal hit')
 check(b.health==40 and b.bag[stone]==1,'first death revives full consumes one')
 check(#revived==1 and revived[1]==b,'revival event returned')
 check(b.tile==tile and b.remaining==before,'same tile and no AP cost')
 check(not L.tryRevive(b) and b.bag[stone]==1,'healthy unit cannot consume twice')
 C.execute(e,b,lethal,b.random)
 check(b.health==40 and b.bag[stone]==0,'second death uses second stone')
 C.execute(e,b,lethal,b.random)
 check(b.health==0 and b.bag[stone]==0,'third death without stones stays dead')
end
for _,profile in ipairs({1,2}) do
 for rank=1,3 do
  local b,e=fixture(profile,rank,1)
  C.execute(e,b,lethal,b.random)
  check(b.health==P.stats(b.character)[1] and b.maxHealth==b.health,'current rank full HP')
  check(P.get(b.character).rank==rank,'rank unchanged')
 end
end
do
 local b,e=fixture(1,1,1);b.health=20
 C.execute(e,b,S.test_strike,b.random)
 check(b.health>0 and b.health<20 and b.bag[stone]==1,'nonlethal does not consume')
 local health=b.health
 C.execute(e,b,S.test_strike,function(a,z) return z end)
 check(b.health==health and b.bag[stone]==1,'miss does not consume')
 local result=b:useItem(stone)
 check(result:find('자동') and b.remaining==6 and b.bag[stone]==1,'manual use prohibited without consumption')
end
do
 local b,e=fixture(2,1,1);b.health=1
 local message=b:endTurn()
 check(not b.lost and b.health==30,'revive before defeat decision')
 check(message:find('부활석') and message:find('펄그림'),'revival announced using correct character')
 check(b.remaining==0 and not b.rolled,'revival grants no extra turn')
 b.health=1;b:endTurn()
 check(b.lost and b.health==0,'defeat when no stones remain')
end
do
 local b,e=fixture(1,1,1);b.health=1
 local other={name='second',element='노말',health=45,stats={45,30,35,20,20,45},attackers={},tile=G.get(b.map,1,4)}
 b.enemies[2]=other
 b:endTurn()
 check(b.health>0 and b.health<40 and b.bag[stone]==0,'later enemies still act after full HP revival')
end
do
 local b,e=fixture(1,3,1);b:selectSkill('final_gambit')
 local other={health=45,tile=G.get(b.map,3,5)};b.enemies[2]=other
 local message=b:attack(e.tile)
 check(e.health==0 and b.health==110 and b.bag[stone]==0,'sacrifice also triggers resurrection')
 check(not b.won and not b.lost,'battle continues if other enemies survive')
 check(b.remaining==2 and message:find('부활석'),'only skill action cost paid')
 local c,enemy=fixture(1,3,1);c:selectSkill('final_gambit');c:attack(enemy.tile)
 check(c.won and not c.lost and c.health==110,'last enemy victory with resurrection')
 local d,last=fixture(1,3,0);d:selectSkill('final_gambit');d:attack(last.tile)
 check(d.won and not d.lost and d.health==0,'existing simultaneous death victory retained')
end
do
 local a,e=fixture(1,1,0);local other=fixture(2,1,1)
 C.execute(e,a,lethal,a.random)
 check(a.health==0 and other.bag[stone]==1,'cannot consume another characters stone')
 check(not L.tryRevive({health=0,stats={45}}),'no bag does not revive')
end
do
 local map=W.new(nil,nil,true);local b=B.new(map,chars[1],{})
 local tile=G.get(map,0,5)
 check(b.chests[tile] and b.chests[tile].item==stone,'fixed test chest beside spawn')
 b.rolled=6;b.remaining=6
 local chest=b:inspect(tile)
 check(chest and chest.open and b.remaining==5,'opening costs one as before')
 check(not b.bag[stone] and b.chests[tile],'decline leaves item in open chest')
 b:inspect(tile);check(b.remaining==5,'reopening is free')
 b:takeItem(tile)
 check(b.bag[stone]==1 and not b.chests[tile],'take removes chest and adds own inventory')
 local nextBattle=B.new(map,chars[1],b.bag)
 check(nextBattle.bag[stone]==1,'unused stone survives next battle in session')
end
print('Revival tests passed: '..count)
