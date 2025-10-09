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
  RawBlock = true,
  List = true
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
  Subscript=true,
  Underline=true
}

-- Helper function to get every Attr value as a table
local function getAttr(attr)
  local id, classes, attrs

  if not attr then
    id = ""
    classes = {}
    attrs = {}
  elseif type(attr) == "table" then
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

-- Helper function to check if an Attr is empty
local function isEmptyAttr(attr)
  local id, classes, attrs = getAttr(attr)
  return id == "" and #classes == 0 and #attrs == 0
end

-- Helper function to remove useless Span and Div around
local function removeEmptyWrapper(el)
  if (el.t == "Div" or el.t == "Span") and isEmptyAttr(el.attr) then
    return el.content
  end
  return el
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
  return el
end

-- This is highly specific to the IDML Pandoc Reader specific.
-- It can be handy to keep empty elements. The idml2docbook
-- module sends the data of empty elements to the AST by
-- just filling it with a LineBreak. (Should it be a SoftBreak?)
function operators.isContentOneLineBreak(el)
  div_wrapper_with_one_linebreak = pandoc.Div(pandoc.Para(pandoc.LineBreak()), pandoc.Attr("", el.classes, { wrapper = 1 }))
  return el == div_wrapper_with_one_linebreak
end

function operators.applyClasses(el, classes)
    local new_classes = {}
    for class in string.gmatch(classes, "%S+") do
        table.insert(new_classes, class)
    end
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
  if blockTypes[el.t] then
    return applyAttrsBlock(el, keyvals)
  elseif inlineTypes[el.t] then
    return applyAttrsInline(el, keyvals)
  else
    return el
  end
end

-- THIS RELATES TO applyType

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
local function blockToBlock(el, newtype, wrapper_attr, is_list)
  local attr
  if wrapper_attr ~= nil then
    attr = wrapper_attr
  else
    attr = el.attr
  end

  local is_empty_attr = isEmptyAttr(attr)

  if is_empty_attr then
    attr = {"", {}, {}}
  end

  local content
  if is_list then
    content = el
  else
    content = el.content
  end

  if newtype == "Header" then
    result = pandoc.Header(1, pandoc.utils.blocks_to_inlines({el}), getAttrWithWrapper(attr, nil))
  elseif newtype == "Para" then
    result = pandoc.Para(content)
  elseif newtype == "BlockQuote" then
    result = pandoc.BlockQuote(el)
  elseif newtype == "Div" then
    result = pandoc.Div(content, getAttrWithWrapper(attr, nil))
  elseif newtype == "BulletList" then
    result = pandoc.BulletList({ el })
  elseif newtype == "OrderedList" then
    result = pandoc.OrderedList({ el })
  elseif newtype == "CodeBlock" then
    result = pandoc.CodeBlock(pandoc.utils.stringify(content), getAttrWithWrapper(attr, nil))
  else
    result = el
  end

  -- Wrap in Div if new node doesn't support attributes but old node had them
  if not is_empty_attr then
    local attr_supported = (newtype == "Div" or newtype == "Header" or newtype == "CodeBlock")
    if not attr_supported then
      attr_with_wrapper = getAttrWithWrapper(attr, 1) -- adding a wrapper attribute to attrs
      result = pandoc.Div({result}, attr_with_wrapper) 
    end
  end

  return result
end

-- Smart inline conversion
local function inlineToInline(el, newtype, wrapper_attr)
  local attr
  is_empty_attr = isEmptyAttr(el.attr)
  if is_empty_attr then
    attr = {"", {}, {}}
  else
    attr = el.attr
  end

  local inlines = el.content or ({ pandoc.Str(el.text)}) or {}
  local text = el.text or pandoc.utils.stringify(inlines)
  local result

  if newtype == "Span" then
    result = pandoc.Span(inlines, attr)
  elseif newtype == "Emph" then
    result = pandoc.Emph(inlines)
  elseif newtype == "Strong" then
    result = pandoc.Strong(inlines)
  elseif newtype == "Link" then
    result = pandoc.Link(inlines, el.target or "", el.title or "", attr)
  elseif newtype == "Superscript" then
    result = pandoc.Superscript(inlines)
  elseif newtype == "Subscript" then
    result = pandoc.Subscript(inlines)
  elseif newtype == "SmallCaps" then
    result = pandoc.SmallCaps(inlines)
  elseif newtype == "Code" then
    result = pandoc.Code(text, attr)
  elseif newtype == "Strikeout" then
    result = pandoc.Strikeout(inlines)
  elseif newtype == "Underline" then
    result = pandoc.Underline(inlines)
  else
    result = el
  end

  -- Wrap in Span if new node doesn't support attributes but old node had them
  if not is_empty_attr then
    local attr_supported = (newtype == "Span" or newtype == "Code" or newtype == "Link")
    if not attr_supported then
      attr_with_wrapper = getAttrWithWrapper(attr, 1) -- adding a wrapper attribute to attrs
      result = pandoc.Span({result}, attr_with_wrapper) 
    end
  end

  return result
end

local function liftElement(el, targetDomain)
  if targetDomain == "Block" then
    return pandoc.Para({el})
  elseif targetDomain == "Inline" then
    return pandoc.Span(el.content or {el}, el.attr or {"", {}, {}})
  end
end

local function inlineToBlock(el, newtype)
  return blockToBlock(liftElement(el, "Block"), newtype, nil, false)
end

local function blockToInline(el, newtype)
  return inlineToInline(liftElement(el, "Inline"), newtype, nil)
end

-- This function replaces the type of the given element by a new type.
-- It works for both Inlines and Blocks, but it will only replace Block elements
-- with other Block elements, and only replace Inline elements with Inline elements.
-- This function keeps track of classes, attributes and ids. When necessary,
-- a wrapper Div or Span is created around the new element type to keep all
-- the data after conversion.
function operators.applyType(el, newtype)
  if isWrapper(el) then
    local wrapper_id, wrapper_classes, wrapper_attributes = getAttr(el)
    local wrapper_attr = pandoc.Attr(wrapper_id, wrapper_classes, wrapper_attributes)

    el = el.content[1]

    if blockTypes[el.t] and blockTypes[newtype] then
      return blockToBlock(el, newtype, wrapper_attr, false)
    elseif inlineTypes[el.t] and inlineTypes[newtype] then
      return inlineToInline(el, newtype, wrapper_attr)
    else
      return el
    end
  else
    if blockTypes[el.t] and blockTypes[newtype] then
      return blockToBlock(el, newtype, nil, false)
    elseif inlineTypes[el.t] and inlineTypes[newtype] then
      return inlineToInline(el, newtype, nil)
    elseif inlineTypes[el.t] and blockTypes[newtype] then
      return inlineToBlock(el, newtype)
    elseif blockTypes[el.t] and inlineTypes[newtype] then
      return blockToInline(el, newtype)
    else
      -- We are in the context where this is an unwrapped Div that
      -- contains only one element. It won't work for several elements.
      if blockTypes[el[1].t] and blockTypes[newtype] then
        return blockToBlock(el[1], newtype, wrapper_attr, true)
      end
    end
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
  elseif t == "Underline" then
    return pandoc.Underline(el.content)
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
          el.t == "CodeBlock" or el.t == "RawBlock" or 
          el.t == "Div" or el.t == "Header" or
          el.t == "BulletList" or el.t == "OrderedList" then
      return pandoc.Para(pandoc.utils.blocks_to_inlines({el}))

    elseif el.t == "Para" then
      return el  -- already Para
    end

    -- Fallback
    return el
  end
end

-- Function that wraps a Block element or an Inline element
-- in a wrapper element. Not all elements can be wrapper elements.
-- Many wraps possibilities are actually covered by applyType.
-- Here, we will consider that a wrapper element has to be a Div
-- or a Span, and that it can have classes.
-- The wrapper argument is actually a string that can hold classes,
-- Note: These wrappers are explicit, not explicit such as elements
-- with wrapper=1 atributes.
function operators.wrap(el, wrapper)
  local tag, classes = utils.parseSelector(wrapper)
  if blockTypes[el.t] then
    -- Wrap Blocks in a Div
    return pandoc.Div({el}, pandoc.Attr("", classes))
  elseif inlineTypes[el.t] then
    -- Wrap Inlines in a the corresponding tag
    if tag == "Superscript" then
      el = pandoc.Superscript({el})
    elseif tag == "Emph" then
      el = pandoc.Emph({el})
    elseif tag == "SmallCaps" then
      el = pandoc.SmallCaps({el})
    elseif tag == "Strikeout" then
      el = pandoc.Strikeout({el})
    elseif tag == "Strong" then
      el = pandoc.Strong({el})
    elseif tag == "Underline" then
      el = pandoc.Underline({el})
    elseif tag == "Subscript" then
      el = pandoc.Subscript({el})
    else -- Then it is wrapped only in a Span
      return pandoc.Span({el}, pandoc.Attr("", classes))
    end
    return pandoc.Span({el}, pandoc.Attr("", classes)) -- wrap in a Span
  else
    return el
  end
end

-- Cleans the final returned object.
function operators.clean(el)
  return removeEmptyWrapper(el)
end

-- Inserts a LineBreak element before the element given
-- as argument.
function operators.insertLineBreakBefore(el)
  -- We are in the context where this is an unwrapped Div that
  -- contains only one element. It won't work for several elements.
  if el.t == nil and type(el) ~= "string" then
    els = { pandoc.LineBreak() }
    for i, elem in pairs(el) do
      table.insert(els, elem)
    end
    return els
  else
    return { pandoc.LineBreak(), el }
  end
end

-- Merge consecutive OrderedList and BulletList elements together.
-- For now, it only considers top-level elements.
-- It works for both "simple" series of Lists, and also with
-- Div-wrapped lists (and ignores it if the Div is not a wrapper.)
function operators.mergeLists(blocks)
  local result = {}
  local i = 1

  while i <= #blocks do
    local blk = blocks[i]

    -- Case 1: plain BulletList
    if blk.t == "BulletList" then
      local items = pandoc.List(blk.content)
      i = i + 1
      while i <= #blocks and blocks[i].t == "BulletList" do
        items:extend(blocks[i].content)
        i = i + 1
      end
      table.insert(result, pandoc.BulletList(items))

    -- Case 2: plain OrderedList
    elseif blk.t == "OrderedList" then
      local attr = blk.content[1]
      local items = pandoc.List(blk.content)
      i = i + 1
      while i <= #blocks and blocks[i].t == "OrderedList" do
        local other_attr = blocks[i].content[1]
        local other_items = pandoc.List(blocks[i].content)
        if other_attr.style == attr.style and other_attr.delimiter == attr.delimiter then
          items:extend(other_items)
          i = i + 1
        else
          break
        end
      end
      local listattr = pandoc.ListAttributes(attr.start, attr.style, attr.delimiter)
      table.insert(result, pandoc.OrderedList(items, listattr))

    -- Case 3: Div-wrapped list
    elseif blk.t == "Div" and isWrapper(blk)
      and #blk.content == 1
      and (blk.content[1].t == "BulletList" or blk.content[1].t == "OrderedList")
    then
      local div_id, div_classes, div_attrs = getAttr(blk.attr)
      local inner = blk.content[1]

      if inner.t == "BulletList" then
        local items = pandoc.List(inner.content)
        i = i + 1
        while i <= #blocks do
          local nxt = blocks[i]
          if nxt.t == "Div" and isWrapper(nxt)
            and pandoc.utils.equals(nxt.classes, div_classes)
            and #nxt.content == 1
            and nxt.content[1].t == "BulletList"
          then
            items:extend(nxt.content[1].content)
            i = i + 1
          else
            break
          end
        end
        table.insert(result, pandoc.Div({ pandoc.BulletList(items) }, pandoc.Attr(div_id, div_classes, div_attrs)))

      elseif inner.t == "OrderedList" then
        local attr = inner.content[1]
        local items = pandoc.List(inner.content)
        i = i + 1
        while i <= #blocks do
          local nxt = blocks[i]
          if nxt.t == "Div" and isWrapper(nxt)
            and pandoc.utils.equals(nxt.classes, div_classes)
            and #nxt.content == 1
            and nxt.content[1].t == "OrderedList"
          then
            local other_attr = nxt.content[1].content
            local other_items = pandoc.List(nxt.content[1].content)
            if other_attr.style == attr.style and other_attr.delimiter == attr.delimiter then
              items:extend(other_items)
              i = i + 1
            else
              break
            end
          else
            break
          end
        end
        local listattr = pandoc.ListAttributes(attr.start, attr.style, attr.delimiter)
        table.insert(result, pandoc.Div({ pandoc.OrderedList(items, listattr) }, pandoc.Attr(div_id, div_classes, div_attrs)))
      end

    else
      -- default: leave block unchanged
      table.insert(result, blk)
      i = i + 1
    end
  end

  return result
end

function operators.cut(doc)
  local current = {}
  local file_index = 1

  if not PANDOC_STATE.output_file then
    -- We only apply the cuts if an output file is specified
    -- as the stdout is for the uncut file.
    return doc
  end

  local outdir, basename
  if PANDOC_STATE.output_file and #PANDOC_STATE.output_file > 0 then
    outdir = PANDOC_STATE.output_file:match("(.+)/[^/]+$") or "."
    basename = PANDOC_STATE.output_file:match(".*/([^/]+)$") or PANDOC_STATE.output_file
    local name = basename:match("^(.*)%.([^%.]+)$")
    if name then
      basename = name
    end
  else
    outdir = "."
    basename = "cut"
  end

  local extension = utils.ext[FORMAT] or "txt"

  local function flush()
    if #current > 0 then
      local subdoc = pandoc.Pandoc(current, doc.meta)

      local slug = utils.firstNonEmptyHeader(current)
      if slug then
        slug = "_" .. utils.slugify(slug)
      else
        slug = ""
      end

      local filename = string.format("%s/%s_%03d%s.%s",
                                     outdir, basename, file_index, slug, extension)

      -- Follow this recommendation:
      -- https://fosstodon.org/@pandoc/114578758417418208
      local encoded_filename = pandoc.text.toencoding(filename)
      local encoded_outdir = pandoc.text.toencoding(outdir)

      utils.mkdir(outdir) -- creates the output directory if necessary
      local fh = io.open(encoded_filename, "w")

      
      fh:write(pandoc.write(subdoc, FORMAT, PANDOC_WRITER_OPTIONS))
      fh:close()

      file_index = file_index + 1
      current = {}
    end
  end

  for _, blk in ipairs(doc.blocks) do
    local is_cut = false
    for _, entry in ipairs(map) do
      if utils.isMatchingSelector(blk, entry._tag, entry._classes)
         and entry.operation.cut then
        is_cut = true
        break
      end
    end

    if is_cut then
      flush()
    end
    table.insert(current, blk)
  end

  flush()

  return doc
end

return operators