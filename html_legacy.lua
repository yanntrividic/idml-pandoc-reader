-- Custom reader that preprocesses an HTML document that was exported
-- from Adobe InDesign with the HTML (Legacy) option.
-- It first cleans the HTML with a Python script and then pipes the
-- result in Pandoc's HTML reader.

-- Turns Span elements with the footnote class into Note elements
function Span(el)
  if el.classes[1] == "footnote" then
      return pandoc.Note{pandoc.Para(el.content)}
  end
  return el
end

function traverse_and_remove_softbreaks(blocks)
  local i = 1
  while i <= #blocks do
    -- If the current element is a Note and the next is a SoftBreak, remove the SoftBreak
    if blocks[i].t == "Note" and blocks[i + 1] and blocks[i + 1].t == "SoftBreak" then
      table.remove(blocks, i + 1)
    end
    i = i + 1
  end
end

-- Process inline elements to remove SoftBreak after Note
function Inlines(inlines)
  traverse_and_remove_softbreaks(inlines)
  return inlines
end

function preprocessing(source)
  local result
  if not pcall(function ()
    result = pandoc.pipe("python", {'preprocessing.py', source.name}, "")
  end) then
    io.stderr:write("Error running 'preprocessing.py'\n")
    os.exit(1)
  end
  return result
end

function Reader(input)
  local preprocessed_html = ''
  for _, source in ipairs(input) do
    preprocessed_html = preprocessed_html .. preprocessing(source)
  end
  return pandoc.read(preprocessed_html, "html")
end