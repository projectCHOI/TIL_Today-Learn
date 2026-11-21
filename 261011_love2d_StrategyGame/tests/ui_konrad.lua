-- Headless end-to-end inputs for Konrad's self-cast and selected-region UI.
local output={}
local noop=function() end
local art={setFilter=noop,getWidth=function() return 600 end,getHeight=function() return 400 end,getDimensions=function() return 600,400 end}
local capture=function(s) output[#output+1]=tostring(s) end
local g=setmetatable({print=capture,printf=capture,getDimensions=function() return 1200,800 end,getWidth=function() return 1200 end,getHeight=function() return 800 end,newCanvas=function() return art end,newFont=function() return art end,newImage=function() return art end}, {__index=function() return noop end})
love={graphics=g,filesystem={getInfo=function() return false end},mouse={getPosition=function() return 600,400 end},math={random=function(a,z) return a==0 and 0 or z end}}
local B=require('src.skirmish');local original=B.new;local current
B.new=function(...)
 current=original(...)
 local e=current.enemies[1];e.health=1000;e.tile=require('src.grid').get(current.map,4,4)
 current.enemies={e}
 return current
end
package.loaded['ImpossibilityGuildMain']=nil
require('ImpossibilityGuildMain');love.load()
local flow=require('src.game_flow');local char=require('src.characters')[3]
local camera=require('src.camera');local grid=require('src.grid');local progress=require('src.progression')
local function start(rank)
 progress.get(char).rank=rank;flow.screen='lobby';flow.selectedCharacter=char
 love.mousepressed(600,490,1)
 local x,y=camera.project(2,10,0);love.mousepressed(x,y,1)
 love.mousepressed(1050,260,1)
 assert(current.remaining==6)
end
-- Temporarily place the enemy within wind range, then activate using the explicit button.
start(1);current.enemies[1].tile=grid.get(current.map,2,5)
love.mousepressed(350,110,1);assert(current.skillId=='wind_burst')
love.mousepressed(600,80,1)
assert(current.remaining==5 and current.enemies[1].health<1000)
output={};love.draw();assert(table.concat(output,'|'):find('바람 일으키기 · 대상',1,true))
-- Click a red tile of the right-side shotgun rectangle.
start(2);love.mousepressed(670,110,1);assert(current.skillId=='shotgun')
local x,y=camera.project(8,8,0);love.mousepressed(x,y,1)
assert(current.remaining==4 and current.enemies[1].health<1000)
assert(progress.get(char).uses.shotgun==1)
-- Steel Rain is slot four and uses its own selected region.
start(2);love.mousepressed(30,150,1);assert(current.skillId=='steel_rain')
x,y=camera.project(8,8,0);love.mousepressed(x,y,1)
assert(current.remaining==3 and current.enemies[1].health<1000)
love.draw()
B.new=original
print('Konrad UI passed: select -> roll -> self-cast wind / region shotgun / region steel rain')
