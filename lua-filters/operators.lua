-- Mapping operators for map.lua

local utils = require "utils"

local operators = {}

-- Supported types by this filter

blockTypes = {
  Div = true,
  Header = true,
  Para = true,
  BlockQuote = true,
  BulletList = true,
  OrderedList = true,
  CodeBlock = true,
  Note = true,
  RawBlock = true
}

inlineTypes = {
  Link = true,
  Code = true,
  Span = true,
  Superscript = true,
  Emph = true,
  SmallCaps = true,
  Strikeout = true,
  Strong = true,
  Subscript=true
}

-- Helper function to get every Attr value as a table
local function getAttr(attr)
  local id, classes, attrs

  if type(attr) == "table" then
    id = attr[1] or ""
    classes = attr[2] or {}
    attrs = attr[3] or {}
  else
    id = attr.identifier
    classes = attr.classes
    attrs = attr.attributes
  end

  return id, classes, attrs
end

-- Helper function that checks if an element is a wrapper
-- that is, if it is a Span or a Div with a wrapper=1 attribute.
local function isWrapper(el)
  if (el.t == "Div" or el.t == "Span") and el.attr and el.attr.attributes then
    return el.attr.attributes["wrapper"] == "1"
  end
  return false
end

-- Function that removes a useless wrapper
-- i.e. A Div with only a wrapper attribute
-- or a span with only a wrapper attribute
local function removeUselessWrapper(el)
  if not isWrapper(el) then
    return el
  end

  local id, classes, attrs = getAttr(el.attr)

  -- Check if the only attribute is wrapper="1", and no id/classes
  local only_wrapper = #attrs == 1 and attrs["wrapper"] == "1"
  local no_other_attrs = #classes == 0 and id == ""

  if only_wrapper and no_other_attrs then
    -- Unwrap: return content directly
    return el.content
  else
    return el
  end
end

function operators.applyClasses(el, classes)
    local new_classes = {}
    for class in string.gmatch(classes, "%S+") do
        -- print("matched class", class)
        table.insert(new_classes, class)
    end
    -- print("new_classes", utils.printTable(new_classes))
    el.classes = new_classes
    return removeUselessWrapper(el)
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
-- It covers more cases than necessary IMHO.
local function toBlocks(el)
  if el.t == "CodeBlock" then
    return { pandoc.Para({ pandoc.Str(el.text) }) }
  elseif el.t == "Para" or el.t == "Header" then
    return { el }
  -- In the case we have a wrapper
  -- elseif el.t == "Div" and el.attributes.wrapper then
  --   return toBlocks(el.content[1])
  elseif el.t == "Div" or el.t == "BlockQuote" then
    return el.content
  elseif el.t == "BulletList" or el.t == "OrderedList" then
    return el.content
  else
    return { pandoc.Para({ el }) }
  end
end

-- This returns a new Attr object with an updated
-- wrapper attribute value.
-- Some Pandoc types have tuples as attributes,
-- others have Attr. This function covers both cases.
local function getAttrWithWrapper(attr, value)
  local id, classes, attrs = getAttr(attr)
  attrs["wrapper"] = value
  return pandoc.Attr(id, classes, attrs)
end

-- Smart block conversion
local function blockToBlock(el, newtype)
  local attr = el.attr or {"", {}, {}}
  attr = getAttrWithWrapper(attr, nil)
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
      attr_with_wrapper = getAttrWithWrapper(el.attr, 1) -- adding a wrapper attribute to attrs
      result = pandoc.Div({result}, attr_with_wrapper)
    end
  end

  return result
end

-- Smart inline conversion
local function inlineToInline(el, newtype)
  local attr = el.attr or {"", {}, {}}
  attr = getAttrWithWrapper(attr, nil)
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
      attr_with_wrapper = getAttrWithWrapper(el.attr, 1) -- adding a wrapper attribute to attrs
      result = pandoc.Span({result}, attr_with_wrapper) 
    end
  end

  return result
end

-- This function replaces the type of the given element by a new type.
-- It works for both Inlines and Blocks, but it will only replace Block elements
-- with other Block elements, and only replace Inline elements with Inline elements.
-- This function keeps track of classes, attributes and ids. When necessary,
-- a wrapper Div or Span is created around the new element type to keep all
-- the data after conversion.
function operators.applyType(el, newtype)
  if blockTypes[el.t] and blockTypes[newtype] then
    return blockToBlock(el, newtype)
  elseif inlineTypes[el.t] and inlineTypes[newtype] then
    return inlineToInline(el, newtype)
  else
    return el
  end
end

function operators.applyLevel(el, level)
  if el.t == "Header" then
    -- Preserve attributes and content
    return pandoc.Header(level, el.content, el.attr)
  end
  -- If it's not a Header, just return it unchanged
  return el
end

-- Function that simplifies an element.
-- If the element is a wrapper, it unwraps its content.
-- If it is not a wrapper, it only deleted its Attr.
function operators.simplify(el)

  id, classes, attrs = getAttr(el.attr)
  
  if attrs["wrapper"] == "1" then
    return el.content  -- unwrap wrapper: return content directly
  end

  -- Rebuild element without attributes
  local t = el.t
  if t == "Div" then
    return pandoc.Div(el.content) -- remove Attr
  elseif t == "Para" then
    return pandoc.Para(el.content)
  elseif t == "Header" then
    -- I have no idea why the id is not being returned, it really
    -- seems like a bug here...
    return pandoc.Header(el.level, el.content, pandoc.Attr(id, {}, {}))
  elseif t == "BlockQuote" then
    return pandoc.BlockQuote(el.content)
  elseif t == "BulletList" then
    return pandoc.BulletList(el.content)
  elseif t == "OrderedList" then
    return pandoc.OrderedList(el.content, el.listAttributes or {0, ""})
  elseif t == "CodeBlock" then
    return pandoc.CodeBlock(el.text)
  elseif t == "Span" then
    return pandoc.Span(el.content)
  elseif t == "Code" then
    return pandoc.Code(el.text)
  elseif t == "Link" then
    return pandoc.Link(el.content, el.target)
  elseif t == "Emph" then
    return pandoc.Emph(el.content)
  elseif t == "Strong" then
    return pandoc.Strong(el.content)
  elseif t == "Strikeout" then
    return pandoc.Strikeout(el.content)
  elseif t == "Superscript" then
    return pandoc.Superscript(el.content)
  elseif t == "Subscript" then
    return pandoc.Subscript(el.content)
  elseif t == "SmallCaps" then
    return pandoc.SmallCaps(el.content)
  else
    return el  -- fallback: unknown element, return as-is
  end
end

-- Function that unwraps the content of an element in its parent.
-- For Inlines, that means replacing the Inline object with its content.
-- For Blocks, that means (opinionated):
-- 1) With a Div that is not a wrapper, that means replacing the Div
--    with its content. 
-- 2) With a Div that is a wrapper, that means replacing the Div and its
--    content element with a Para element without Attr.
-- 3) With any other Block, that means replacing the tag with a Para.
function operators.unwrap(el)
  if inlineTypes[el.t] then -- We check if we handle this element
    -- Code is an exception as it contains text and not content
    if el.t == "Code" then
      return el.text
    end
    return el.content
  end

  if blockTypes[el.t] then
    if isWrapper(el) then
      return pandoc.Para(el.content[1].content)
    else
      return el.content
    end

    -- Handle other Block elements
    if el.t == "Plain" then
      return pandoc.Para(el.content)

    elseif el.t == "BlockQuote" or el.t == "Note" or
          el.t == "CodeBlock" or el.t == "RawBlock" then
      return pandoc.Para(pandoc.utils.blocks_to_inlines({el}))

    elseif el.t == "Para" then
      return el  -- already Para
    end

    -- Fallback
    return el
  end
end

return operators