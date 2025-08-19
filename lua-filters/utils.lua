-- Utility functions for map.lua

local json = require 'pandoc.json' -- requires Pandoc>=3.1.1

local utils = {}

utils.ext = {
  -- Markdown family
  markdown          = "md",
  commonmark        = "md",
  gfm               = "md",
  markdown_mmd      = "md",
  markdown_phpextra = "md",
  markdown_strict   = "md",

  -- HTML
  html   = "html",
  html4  = "html",
  html5  = "html",

  -- DocBook
  docbook      = "xml",
  docbook4     = "xml",
  docbook5     = "xml",

  -- LaTeX / TeX
  latex  = "tex",
  beamer = "tex",
  context= "tex",

  -- MS Office
  docx = "docx",
  pptx = "pptx",
  xlsx = "xlsx",

  -- OpenDocument
  odt = "odt",
  odp = "odp",
  ods = "ods",

  -- RTF / TXT
  rtf = "rtf",
  plain = "txt",

  -- OPML
  opml = "opml",

  -- EPUB
  epub  = "epub",
  epub2 = "epub",
  epub3 = "epub",

  -- JSON (Pandoc AST)
  json = "json",

  -- ICML (Adobe InCopy)
  icml = "icml",

  -- Man page / roff
  man  = "1",
  ms   = "ms",

  -- Textile
  textile = "textile",

  -- Org
  org = "org",

  -- AsciiDoc
  asciidoc  = "adoc",
  asciidoctor = "adoc",

  -- Other special ones
  native = "native",
  pdf    = "pdf"
}

-- Helper function to slugify Header contents for filenames.
-- There might be some problems with accentuated chars...
function utils.slugify(str)
  str = pandoc.text.lower(str)
  str = str:gsub("[^%w%s-]", "")    -- drop non-word chars
  str = str:gsub("%s+", "_")        -- spaces to underscores
  str = str:gsub("_+", "_")         -- collapse multiple _
  str = str:gsub("^_*(.-)_*$", "%1")-- trim leading/trailing _
  return str
end

-- extract first heading text from a block list
function utils.firstHeading(blocks)
  for _, blk in ipairs(blocks) do
    if blk.t == "Header" then
      return pandoc.utils.stringify(blk.content)
    end
  end
  return nil
end

-- Helper function for timing performances
-- example call: el = utils.timeit("simplify", operators.simplify, el)
function utils.timeit(message, func, ...)
    local info = debug.getinfo(func, "S")
    local location = string.format("%s:%d", info.short_src, info.linedefined)

    local start_time = os.clock()
    local results = {func(...)}
    local end_time = os.clock()

    print(string.format(message .. ": Function defined at %s took %.6f seconds",
        location, end_time - start_time))

    return table.unpack(results)
end

function utils.printTable(tbl, indent)
    indent = indent or 0
    for k, v in pairs(tbl) do
        local formatting = string.rep("  ", indent) .. k .. ": "
        if type(v) == "table" then
            print(formatting)
            utils.printTable(v, indent + 1)
        else
            print(formatting .. tostring(v))
        end
    end
end

local function readMap(map_file)
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

-- Parse one selector like "BlockQuote.class1.class2"
local function split(str, pat)
  local t = {}
  str:gsub("([^" .. pat .. "]+)", function(c) t[#t+1] = c end)
  return t
end

function utils.parseSelector(sel)
  local parts = split(sel, "%.")
  local tag, classes

  if #parts == 0 then
    return nil, {}
  elseif #parts == 1 then
    if sel:sub(1,1) == "." then
      tag = nil
      classes = { sel:sub(2) }
    else
      tag = sel
      classes = {}
    end
  else
    if sel:sub(1,1) == "." then
      tag = nil
      classes = parts
      classes[1] = sel:sub(2, #parts[1]+1)
    else
      tag = parts[1]
      classes = { table.unpack(parts, 2) }
    end
  end

  return tag, classes
end

-- Cache for memoization: element+selector -> match result
local matchCache = {}

-- Precompute parsed selectors for map entries
local function preprocessMap(map)
  for _, entry in ipairs(map) do
    local tag, classes = utils.parseSelector(entry.selector)
    entry._tag = tag
    entry._classes = classes
  end
end

function utils.readAndPreprocessMap(meta)
  if meta.map then
    map_file = pandoc.utils.stringify(meta.map)
    content = readMap(map_file)
    map = json.decode(content)
    preprocessMap(map)
  end
  return meta
end

-- Memoized matching function
function utils.isMatchingSelector(el, tag, classes)
  -- Build a unique key per element + selector
  local el_tag = el.t or ""
  local el_classes = el.classes or {}
  local key = el_tag .. ":" .. table.concat(el_classes, ",") ..
              "|" .. (tag or "") .. ":" .. table.concat(classes or {}, ",")

  if matchCache[key] ~= nil then
    return matchCache[key]
  end

  -- Check tag
  if tag and el.t ~= tag then
    matchCache[key] = false
    return false
  end

  -- Check classes
  if classes then
    local el_class_set = {}
    for _, c in ipairs(el_classes) do el_class_set[c] = true end
    for _, class in ipairs(classes) do
      if not el_class_set[class] then
        matchCache[key] = false
        return false
      end
    end
  end

  matchCache[key] = true
  return true
end

return utils