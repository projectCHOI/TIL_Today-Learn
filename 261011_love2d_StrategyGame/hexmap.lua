local M = {}
local directions = {{1,0},{1,-1},{0,-1},{-1,0},{-1,1},{0,1}}
local function key(q,r) return q .. ',' .. r end
function M.new(allied, enemy)
    assert(allied >= 10 and allied <= 50 and allied % 1 == 0)
    assert(enemy >= 10 and enemy <= 50 and enemy % 1 == 0)
    local map = {tiles={}, lookup={}}
    for side, count in ipairs({allied, enemy}) do
        for i=0,count-1 do
            local row = math.floor(i/5)
            local col = i%5
            -- Fill outward from the border so partial rows remain connected.
            local offset = side == 1 and 4-col or 5+col
            local q = offset-math.floor(row/2)
            local tile = {q=q, r=row, side=side}
            table.insert(map.tiles,tile)
            map.lookup[key(q,row)] = tile
        end
    end
    return map
end
function M.get(map,q,r) return map.lookup[key(q,r)] end
function M.neighbors(map,tile)
    local out={}
    for _,d in ipairs(directions) do
        local t=M.get(map,tile.q+d[1],tile.r+d[2])
        if t then table.insert(out,t) end
    end
    return out
end
function M.distance(a,b)
    local dq,dr=a.q-b.q,a.r-b.r
    return (math.abs(dq)+math.abs(dr)+math.abs(dq+dr))/2
end
function M.center(tile,size)
    return math.sqrt(3)*size*(tile.q+tile.r/2),1.5*size*tile.r
end
function M.vertices(tile,size)
    local x,y=M.center(tile,size)
    local out={}
    for i=0,5 do
        local a=math.rad(60*i-30)
        out[#out+1]=x+size*math.cos(a)
        out[#out+1]=y+size*math.sin(a)
    end
    return out
end
return M
