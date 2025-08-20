-- This is work in progress. This is an attempt at pulling out the mapping logics
-- out of Python to turn it into lua scripts, so that the mapping can be applied
-- to the Pandoc AST instead of the DocBook file.
-- Thus making it format-agnostic, and making it so Pandoc is the only dependency.

-- Enables relative imports
local script_dir = debug.getinfo(1, "S").source:match("@?(.*)/") or "."
package.path = script_dir .. "/?.lua;" .. package.path

local utils = require 'utils'
local operators = require 'operators'

function Meta(meta)
  return utils.readAndPreprocessMap(meta)
end

local function applyMapping(el)
  for _, entry in ipairs(map) do
    if utils.isMatchingSelector(el, entry._tag, entry._classes) then
      local o = entry.operation
      -- and apply the various operations
      if o.delete then
        return {}
      end
      if not o.empty then
        if operators.isContentOneLineBreak(el) then
          return {}
        end
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
      if o.wrap then
        el = operators.wrap(el, o.wrap)
      end
      el = operators.clean(el)
      if o.br then
        el = operators.insertLineBreakBefore(el)
      end
    end
  end
  return el
end

-- For all block elements
function Block(el)
  return applyMapping(el)
end

-- Those Inline tags can be ignored as they are not considered in semantics
-- and add a tremendous computing time if applyMapping is applied to all of them.
filtered_inlines = {
  Str = true,
  Space = true,
  Linebreak = true,
  SoftBreak = true
}

-- For all Inline elements
function Inline(el)
  if filtered_inlines[el.t] then -- No need to apply it to all Inlines
    return el
  else
    return applyMapping(el)
  end
end

function Pandoc(doc)
  doc.blocks = operators.mergeLists(doc.blocks)
  utils.updateMapWithNewClasses(map)
  if utils.isCutable() then
    return operators.cut(doc)
  else
    return doc
  end
end

-- Changing the traversal order, see:
-- https://pandoc.org/lua-filters.html#typewise-traversal
return {
  { Meta = Meta },     -- (1)
  { Inline = Inline }, -- (2)
  { Block = Block },   -- (3)
  { Pandoc = Pandoc }  -- (4)
}