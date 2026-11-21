-- Headless callback smoke test. It does not verify real LÖVE rendering.
local noop=function() end
local printed={}
local capture=function(text) printed[#printed+1]=tostring(text) end
local asset={setFilter=noop,getWidth=function() return 600 end,getHeight=function() return 400 end,getDimensions=function() return 600,400 end}
local g=setmetatable({print=capture,printf=capture,getDimensions=function() return 1200,800 end,getWidth=function() return 1200 end,getHeight=function() return 800 end,newCanvas=function() return asset end,newFont=function() return asset end,newImage=function() return asset end}, {__index=function() return noop end})
love={graphics=g,filesystem={getInfo=function() return false end},mouse={getPosition=function() return 600,400 end},math={random=math.random}}
package.loaded['ImpossibilityGuildMain']=nil
require('ImpossibilityGuildMain')
love.load()
local flow=require('src.game_flow')
local chars=require('src.characters')
local p=require('src.progression')
for _,character in ipairs({chars[1],chars[2],chars[3]}) do
 for _,screen in ipairs({'title','lobby','roster','character_detail','result'}) do
  flow.screen=screen;flow.character=character;love.draw()
 end
end
for _,character in ipairs({chars[1],chars[2],chars[3]}) do
for rank=1,3 do
 p.get(character).rank=rank
 flow.screen='lobby';flow.selectedCharacter=character
 love.mousepressed(600,490,1)
 assert(flow.screen=='battle')
 printed={};love.update(.016);love.draw()
 assert(table.concat(printed,'|'):find(character.korean,1,true),'selected character shown')
 assert(table.concat(printed,'|'):find('체력 '..p.stats(character)[1]..'/'..p.stats(character)[1],1,true),'selected stats shown')
 love.keypressed('w');love.draw();love.keypressed('a');love.draw()
 love.keypressed('s');love.draw();love.keypressed('d');love.draw()
 love.keypressed('q');love.draw();love.keypressed('q')
 love.mousepressed(830,75,1);love.draw();love.keypressed('escape')
 for i=1,rank*2 do
  love.mousepressed(30+((i-1)%3)*320,110+math.floor((i-1)/3)*36,1)
  love.draw()
 end
 love.mousepressed(600,400,2)
end
end
assert(flow:selectCharacter(chars[4])==false)
flow.selectedCharacter=nil;assert(flow:selectCharacter(chars[1]));assert(flow:selectCharacter(chars[2]));assert(flow:getSelectedCharacter()==chars[2]);assert(flow:selectCharacter(chars[2]));assert(flow:getSelectedCharacter()==nil)
flow.screen='roster';love.mousepressed(250,350,1);assert(flow.screen=='character_detail' and flow.character==chars[2]);love.mousepressed(880,600,1);assert(flow:getSelectedCharacter()==chars[2]);flow.screen='lobby';love.mousepressed(600,490,1);assert(flow.screen=='battle')
print('UI callbacks passed: title/lobby/roster/details/result, all three ranks, six skills, camera/help/bag')
