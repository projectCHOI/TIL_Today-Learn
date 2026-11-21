-- Optional: run with a standalone Lua interpreter from the project root.
for _,file in ipairs({'vulkan','fulgrim','revival','konrad','ui_smoke','ui_revival','ui_konrad'}) do
 dofile('tests/'..file..'.lua')
end
print('All rule and headless UI checks passed.')
