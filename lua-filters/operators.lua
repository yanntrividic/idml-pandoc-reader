-- Mapping operators for map.lua

local utils = require "utils"

local operators = {}

function operators.applyClasses(el, classes)
    local new_classes = {}
    for class in string.gmatch(classes, "%S+") do
        -- print("matched class", class)
        table.insert(new_classes, class)
    end
    -- print("new_classes", utils.printTable(new_classes))
    el.classes = new_classes
end


-- THIS RELATES TO applyAttrs


-- Helper to merge key/value pairs into an existing attr
local function mergeKeyvals(old_attr, new_keyvals)
  local id = old_attr.identifier or ""
  local classes = old_attr.classes or {}
  local keyvals = old_attr.attributes or {}

  for k, v in pairs(new_keyvals) do
    local found = false
    for i, kv in ipairs(keyvals) do
      if kv[1] == k then
        kv[2] = v
        found = true
        break
      end
    end
    if not found then
      table.insert(keyvals, {k, v})
    end
  end

  return {id, classes, keyvals}
end

-- Determine if a block supports attributes
local function blockSupportsAttrs(el)
  return el.t == "Div" or el.t == "Header" or el.t == "CodeBlock"
end

-- Determine if an inline supports attributes
local function inlineSupportsAttrs(el)
  return el.t == "Span" or el.t == "Code" or el.t == "Link"
end

-- Apply key/value attributes to a block
local function applyAttrsBlock(el, keyvals)
  if blockSupportsAttrs(el) then
    el.attr = mergeKeyvals(el.attr or {"", {}, {}}, keyvals)
    return el
  else
    -- Wrap in Div
    return pandoc.Div({el}, {"", {}, keyvals})
  end
end

-- Apply key/value attributes to an inline
local function applyAttrsInline(el, keyvals)
  if inlineSupportsAttrs(el) then
    el.attr = mergeKeyvals(el.attr or {"", {}, {}}, keyvals)
    return el
  else
    -- Wrap in Span
    return pandoc.Span({el}, {"", {}, keyvals})
  end
end

-- Dispatcher
function operators.applyAttrs(el, keyvals)
  local blockTypes = {
    Div=true, Header=true, Para=true,
    BlockQuote=true, BulletList=true,
    OrderedList=true, CodeBlock=true
  }
  local inlineTypes = {
    Link=true, Code=true, Span=true,
    Superscript=true, Emph=true,
    SmallCaps=true, Strikeout=true,
    Strong=true, Subscript=true
  }

  if blockTypes[el.t] then
    return applyAttrsBlock(el, keyvals)
  elseif inlineTypes[el.t] then
    return applyAttrsInline(el, keyvals)
  else
    return el
  end
end


-- THIS RELATES TO applyType


-- Helper to get inlines from a block
local function toInlines(block)
  if block.t == "Para" or block.t == "Header" then
    return block.content
  elseif block.t == "CodeBlock" then
    return { pandoc.Str(block.text) }
  elseif block.t == "Div" or block.t == "BlockQuote" then
    return block.content[1] and toInlines(block.content[1]) or {}
  elseif block.t == "BulletList" or block.t == "OrderedList" then
    local result = {}
    for _, item in ipairs(block.content or {}) do
      for _, b in ipairs(item) do
        for _, inline in ipairs(toInlines(b)) do
          table.insert(result, inline)
        end
      end
    end
    return result
  else
    return {}
  end
end

-- Helper to get blocks from a block or inline
local function toBlocks(el)
  if el.t == "CodeBlock" then
    return { pandoc.Para({ pandoc.Str(el.text) }) }
  elseif el.t == "Para" or el.t == "Header" then
    return { el }
  elseif el.t == "Div" or el.t == "BlockQuote" then
    return el.content
  elseif el.t == "BulletList" or el.t == "OrderedList" then
    return el.content
  else
    return { pandoc.Para({ el }) }
  end
end

-- Smart block conversion
local function blockToBlock(el, newtype)
  local attr = el.attr or {"", {}, {}}
  local result

  if newtype == "Div" then
    result = pandoc.Div(toBlocks(el), attr)
  elseif newtype == "Para" then
    result = pandoc.Para(toInlines(el))
  elseif newtype == "Header" then
    result = pandoc.Header(1, toInlines(el), attr)
  elseif newtype == "BlockQuote" then
    result = pandoc.BlockQuote(toBlocks(el))
  elseif newtype == "BulletList" then
    result = pandoc.BulletList({ toBlocks(el) })
  elseif newtype == "OrderedList" then
    result = pandoc.OrderedList({ toBlocks(el) })
  elseif newtype == "CodeBlock" then
    result = pandoc.CodeBlock(pandoc.utils.stringify(toInlines(el)), attr)
  else
    result = el
  end

  -- Wrap in Div if new node doesn't support attributes but old node had them
  if el.attr and el.attr ~= {"", {}, {}} then
    local attr_supported = (newtype == "Div" or newtype == "Header" or newtype == "CodeBlock")
    if not attr_supported then
      result = pandoc.Div({result}, attr)
    end
  end

  return result
end

-- Smart inline conversion
local function inlineToInline(el, newtype)
  local attr = el.attr or {"", {}, {}}
  local inlines = el.content or (el.text and { pandoc.Str(el.text) }) or {}
  local text = el.text or pandoc.utils.stringify(inlines)
  local result

  if newtype == "Span" then
    result = pandoc.Span(inlines, attr)
  elseif newtype == "Code" then
    result = pandoc.Code(text, attr)
  elseif newtype == "Link" then
    result = pandoc.Link(inlines, el.target or "", el.title or "", attr)
  elseif newtype == "Emph" then
    result = pandoc.Emph(inlines)
  elseif newtype == "Strong" then
    result = pandoc.Strong(inlines)
  elseif newtype == "Strikeout" then
    result = pandoc.Strikeout(inlines)
  elseif newtype == "Superscript" then
    result = pandoc.Superscript(inlines)
  elseif newtype == "Subscript" then
    result = pandoc.Subscript(inlines)
  elseif newtype == "SmallCaps" then
    result = pandoc.SmallCaps(inlines)
  else
    result = el
  end

  -- Wrap in Span if new node doesn't support attributes but old node had them
  if el.attr and el.attr ~= {"", {}, {}} then
    local attr_supported = (newtype == "Span" or newtype == "Code" or newtype == "Link")
    if not attr_supported then
      result = pandoc.Span({result}, attr)
    end
  end

  return result
end

-- Dispatcher
function operators.applyType(el, newtype)
  local blockTypes = {
    Div=true, Header=true, Para=true,
    BlockQuote=true, BulletList=true,
    OrderedList=true, CodeBlock=true
  }
  local inlineTypes = {
    Link=true, Code=true, Span=true,
    Superscript=true, Emph=true,
    SmallCaps=true, Strikeout=true,
    Strong=true, Subscript=true
  }

  if blockTypes[el.t] and blockTypes[newtype] then
    return blockToBlock(el, newtype)
  elseif inlineTypes[el.t] and inlineTypes[newtype] then
    return inlineToInline(el, newtype)
  else
    return el
  end
end


return operators