-- This is work in progress. This is an attemp at pulling out the mapping logics
-- out of Python to turn it into lua scripts, so that the mapping can be applied
-- to the Pandoc AST instead of the DocBook file.
-- Thus making it format-agnostic, and making it so Pandoc is the only dependency.

-- To run a test:
-- pandoc -f markdown test.md -t native --lua-filter=map.lua -M map=test.json

-- Note: It would also be possible to design these filters with a Python framework
-- such as panflute (https://github.com/sergiocorreia/panflute), but then
-- it would add a Python dependency, while Pandoc embeds its own Lua interpretor...

local json = require 'pandoc.json' -- requires Pandoc>=3.1.1

map_file = nil
content = nil
data = nil -- {} to prevent the nil error

local function read_map(map_file)

    -- Open the file in read mode
    local file = io.open(map_file, "r")

    if not file then
        error("Could not open " .. map_file .. "!")
    end

    -- Read the entire file content
    local content = file:read("*all")

    -- Close the file
    file:close()
    return content
end


function printTable(tbl, indent)
    indent = indent or 0
    for k, v in pairs(tbl) do
        local formatting = string.rep("  ", indent) .. k .. ": "
        if type(v) == "table" then
            print(formatting)
            printTable(v, indent + 1)
        else
            print(formatting .. tostring(v))
        end
    end
end

function Meta(meta)
  if meta.map then
    map_file = pandoc.utils.stringify(meta.map)
    print(map_file)
    content = read_map(map_file)
    data = json.decode(content)[1] -- We want the first item of the table
    printTable(data)
  end
  return meta
end

-- Helper function to apply class changes to elements
local function applyClass(el, key, class)
  if el.classes then
    for i, c in ipairs(el.classes) do
      if c == key then
        el.classes[i] = class
      end
    end
  end
  return el
end

-- Filter function for Blocks
function Block(el)
  for key, value in pairs(data) do
    el = applyClass(el, key, value.class)
  end
  return el
end

-- Filter function for Inlines
function Inline(el)
  for key, value in pairs(data) do
    el = applyClass(el, key, value.class)
  end
  return el
end

-- Changing the traversal order, see:
-- https://pandoc.org/lua-filters.html#typewise-traversal
return {
  { Meta = Meta },     -- (1)
  { Inline = Inline }, -- (2)
  { Block = Block }    -- (3)
}