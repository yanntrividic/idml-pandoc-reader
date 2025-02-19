function roles_to_classes(blocks)
  local i = 1
  while i <= #blocks do
    if blocks[i].t == "Note" and blocks[i + 1] and blocks[i + 1].t == "SoftBreak" then
      table.remove(blocks, i + 1)
    end
    i = i + 1
  end
end

function Blocks(blocks)
  roles_to_classes(blocks)
  return blocks
end