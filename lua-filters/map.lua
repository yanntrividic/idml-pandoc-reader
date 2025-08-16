-- This is work in progress. This is an attemp at pulling out the mapping logics
-- out of Python to turn it into lua scripts, so that the mapping can be applied
-- to the Pandoc AST instead of the DocBook file.
-- Thus making it format-agnostic, and making it so Pandoc is the only dependency.

local json = require 'pandoc.json' -- requires Pandoc>=3.1.1
local utils = require 'utils'
local operators = require 'operators'

map = nil -- {} to prevent the nil error, but it will have to be handled differently

function Meta(meta)
  if meta.map then
    map_file = pandoc.utils.stringify(meta.map)
    -- print(map_file)
    content = utils.readMap(map_file)
    map = json.decode(content)[1] -- We want the first item of the table
    -- utils.printTable(map)
    utils.parseSelectors(map)
  end
  return meta
end

local function applyMapping(el)
  for selector, value in pairs(map) do
    if utils.isMatchingSelector(el, value.parsed) then
      if value.classes then
        operators.applyClass(el, value.classes)
      end
      if value.delete then
        print(el)
        return {}
      end
    end
  end
  return el
end

-- For all block elements
function Block(el)
  return applyMapping(el)
end

-- For all Inline elements
function Inline(el)
  return applyMapping(el)
end

-- Changing the traversal order, see:
-- https://pandoc.org/lua-filters.html#typewise-traversal
return {
  { Meta = Meta },     -- (1)
  { Inline = Inline }, -- (2)
  { Block = Block }    -- (3)
}