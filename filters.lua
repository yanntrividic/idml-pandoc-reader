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