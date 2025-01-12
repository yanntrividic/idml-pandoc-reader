-- Remove leading and trailing SoftBreak
-- This part is useless if we have one block per line in 
-- the input file.
function remove_leading_and_trailing_softbreaks(elem)
  -- It would be easier to use elem.remove, but this function is highly inefficient.
  local content = elem.content
  local len = #content

  -- Skip processing if the content is empty or has only one element
  if len < 2 then
    return elem
  end

  -- Create a new table for the filtered content
  local new_content = {}
  for i, item in ipairs(content) do
    -- Skip the first element if it's a SoftBreak
    if i == 1 and item.t == "SoftBreak" then
      goto continue
    end
    -- Skip the last element if it's a SoftBreak
    if i == len and item.t == "SoftBreak" then
      goto continue
    end

    -- Add other elements to the new content table
    new_content[#new_content + 1] = item
    ::continue::
  end

  -- Update the Span content
  elem.content = new_content
  return elem
end

-- Turns Span elements with the footnote class into Note elements
function turn_span_into_footnote_if_necessary(el)
  if el.classes[1] == "footnote" then
    return pandoc.Note{pandoc.Para(el.content)}
  else
    return el
  end
end

function Span(el)
    -- This part is useless if we have one block per line in 
    -- the input file.
    -- el = remove_leading_and_trailing_softbreaks(el)

    el = turn_span_into_footnote_if_necessary(el)
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