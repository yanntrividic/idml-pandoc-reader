-- This is work in progress. This is an attempt at pulling out the mapping logics
-- out of Python to turn it into lua scripts, so that the mapping can be applied
-- to the Pandoc AST instead of the DocBook file.
-- Thus making it format-agnostic, and making it so Pandoc is the only dependency.

-- Enables relative imports
local script_dir = debug.getinfo(1, "S").source:match("@?(.*)/") or "."
package.path = script_dir .. "/?.lua;" .. package.path

local utils = require 'utils'
local operators = require 'operators'

local pu = pandoc.utils

function Meta(meta)
  return utils.readAndPreprocessMap(meta)
end

-- Those Inline tags can be ignored as they are not considered in semantics
-- and add a tremendous computing time if applyMapping is applied to all of them.
filtered_inlines = {
  Str = true,
  Space = true,
  LineBreak = true,
  SoftBreak = true
}

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

local function walk_any(el)
  if filtered_inlines[el.t] then -- No need to apply it to all Inlines
    return el
  end

  local t = pu.type(el)

  -- Handle lists of elements (Blocks, Inlines, List)
  if t == "Blocks" or t == "Inlines" or t == "List" then
    local result = pandoc.List()
    for _, item in ipairs(el) do
      local walked = walk_any(item)
      if walked ~= nil then
        local wt = pu.type(walked)
        if wt == "Block" or wt == "Inline" then
          result:insert(walked)
        elseif wt == "Blocks" or wt == "Inlines" or wt == "List" then
          for _, c in ipairs(walked) do
            result:insert(c)
          end
        elseif type(walked) == "string" then
          result:insert(pandoc.Str(walked))
        elseif type(walked) == "table" then
          for _, c in ipairs(walked) do
            if type(c) == "string" then
              result:insert(pandoc.Str(c))
            else
              result:insert(c)
            end
          end
        end
      end
    end
    return result
  end

  -- Handle single element (Block or Inline)
  if t == "Block" or t == "Inline" then
    -- Recurse into content
    if el.content then
      el.content = walk_any(el.content)
    elseif el.c then
      el.c = walk_any(el.c)
    end

    local transformed = applyMapping(el)
    local tt = pu.type(transformed)

    if tt == "Block" or tt == "Inline" then
      return transformed
    elseif tt == "Blocks" or tt == "Inlines" or tt == "List" then
      return walk_any(transformed)
    elseif type(transformed) == "string" then
      return pandoc.Str(transformed)
    elseif type(transformed) == "table" and #transformed > 0 then
      return pandoc.List(transformed)
    elseif transformed == nil then
      return {}
    else
      return transformed
    end
  end

  -- Handle raw strings returned from unwrap or delete
  if type(el) == "string" then
    return pandoc.Str(el)
  end

  -- Handle plain Lua tables
  if type(el) == "table" and #el > 0 then
    local res = pandoc.List()
    for _, c in ipairs(el) do
      res:insert(walk_any(c))
    end
    return res
  end

  -- Fallback: return unchanged
  return el
end


function Pandoc(doc)
  local new_blocks = pandoc.List()

  -- Depth-first traversal of every block
  for _, blk in ipairs(doc.blocks) do
    local transformed = walk_any(blk)

    local tt = pu.type(transformed)
    if tt == "Block" then
      new_blocks:insert(transformed)
    elseif tt == "Blocks" or tt == "List" then
      for _, b in ipairs(transformed) do
        new_blocks:insert(b)
      end
    end
  end

  -- First we cleanup the OrderedLists and BulletLists
  doc.blocks = operators.mergeLists(new_blocks)

  -- Then we cut
  utils.updateMapWithNewClasses(map)
  if utils.isCutable() then
    -- And a value has to be returned in order to 
    -- at least apply the mergeList treatment
    return operators.cut(doc)
  else
    return doc
  end
end

-- Changing the traversal order, see:
-- https://pandoc.org/lua-filters.html#typewise-traversal
return {
  { Meta = Meta },     -- (1)
  { Pandoc = Pandoc }  -- (2)
}