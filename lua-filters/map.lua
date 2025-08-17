-- This is work in progress. This is an attempt at pulling out the mapping logics
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
    map = json.decode(content)
  end
  return meta
end

local function applyMapping(el)
  for _, entry in pairs(map) do
    -- We check if the element matches the selector
    if utils.isMatchingSelector(el, entry.selector) then
      local o = entry.operation
      -- and apply the various operations
      if o.delete then
        return {}
      end
      if o.simplify then
        el = operators.simplify(el)
      end
      if o.classes then
        el = operators.applyClasses(el, o.classes)
      end
      if o.attrs then
        operators.applyAttrs(el, o.attrs)
      end
      if o.type then
        el = operators.applyType(el, o.type)
      end
      if o.level then
        el = operators.applyLevel(el, o.level)
      end
      if o.unwrap then
        el = operators.unwrap(el)
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