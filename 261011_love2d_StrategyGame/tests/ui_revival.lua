-- Headless integration: select unit, open the fixed chest, take stone, inspect bag.
local printed={}
local noop=function() end
local asset={setFilter=noop,getWidth=function() return 600 end,getHeight=function() return 400 end,getDimensions=function() return 600,400 end}
local capture=function(text) printed[#printed+1]=tostring(text) end
local g=setmetatable({print=capture,printf=capture,getDimensions=function() return 1200,800 end,getWidth=function() return 1200 end,getHeight=function() return 800 end,newCanvas=function() return asset end,newFont=function() return asset end,newImage=function() error('no test artwork') end}, {__index=function() return noop end})
love={graphics=g,filesystem={getInfo=function() return false end},mouse={getPosition=function() return 600,400 end},math={random=function(a,z) return a end}}
package.loaded['ImpossibilityGuildMain']=nil
require('ImpossibilityGuildMain');love.load()
local flow=require('src.game_flow');flow.selectedCharacter=require('src.characters')[1];flow.screen='lobby'
love.mousepressed(600,490,1)
local camera=require('src.camera')
local ux,uy=camera.project(2,10,0)
love.mousepressed(ux,uy,1)
love.mousepressed(1050,260,1)
local cx,cy=camera.project(0,10,0)
love.mousepressed(cx,cy,1)
love.mousepressed(600,80,1)
printed={};love.draw()
assert(table.concat(printed,'|'):find('부활석',1,true),'stone popup visible')
love.mousepressed(750,380,1)
love.mousepressed(830,75,1)
printed={};love.draw()
assert(table.concat(printed,'|'):find('부활석 ×1 · 사망 시 자동 사용',1,true),'passive stone inventory row visible')
love.keypressed('escape');love.draw()
print('Revival UI passed: open chest -> popup -> take -> passive bag row; missing image fallback')
