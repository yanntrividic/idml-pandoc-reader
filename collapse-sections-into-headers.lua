function Div(el)
    if el.classes:includes("section") then
      local first = el.content[1]
      if first and first.t == "Header" then
        local new_classes = {}
        for _, class in ipairs(el.classes) do
          if class ~= "section" then
            table.insert(new_classes, class)
          end
        end

        el.attributes["level"] = nil
        first.attr = pandoc.Attr(el.identifier, new_classes, el.attributes)
  
        -- Return all contents of the Div directly (unwrap)
        return el.content
      end
    end
    return nil
  end