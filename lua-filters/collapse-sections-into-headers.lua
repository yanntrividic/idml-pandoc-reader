function Div(el)
  if el.classes:includes("section") then
    local first = el.content[1]
    if first and first.t == "Header" then
      local new_classes = {}
      local class_set = {}

      -- Add Header classes first
      for _, class in ipairs(first.attr.classes) do
        table.insert(new_classes, class)
        class_set[class] = true
      end

      -- Add Div classes (excluding "section") if not already present
      for _, class in ipairs(el.classes) do
        if class ~= "section" and not class_set[class] then
          table.insert(new_classes, class)
        end
      end

      -- Merge attributes from Div and Header
      local new_attributes = {}
      for k, v in pairs(el.attributes) do
        if k ~= "level" then
          new_attributes[k] = v
        end
      end
      for k, v in pairs(first.attr.attributes) do
        new_attributes[k] = v
      end

      first.attr = pandoc.Attr(first.attr.identifier, new_classes, new_attributes)

      return el.content
    end
  end
  return nil
end