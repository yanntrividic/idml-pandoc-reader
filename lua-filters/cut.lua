-- This Lua script aims at replacing the idml2docbook/cut.py file.
-- Its objectives are to take the Pandoc AST, and generate one output
-- file per cut. The cuts are specified in the JSON map file passed as
-- metadata. A call to this script then looks like:

-- pandoc -f markdown -t native --lua-filter=cut.lua -M map=test/test.json test/test.md

local utils = require 'utils'

function Meta(meta)
  return utils.readAndPreprocessMap(meta)
end

function Pandoc(doc)
  local current = {}
  local file_index = 1

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

      local slug = utils.firstHeading(current)
      if slug then
        slug = "_" .. utils.slugify(slug)
      else
        slug = ""
      end

      local filename = string.format("%s/%s_%03d%s.%s",
                                     outdir, basename, file_index, slug, extension)

      local fh = io.open(filename, "w")
      fh:write(pandoc.write(subdoc, FORMAT))
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

  return nil -- nothing to stdout
end