local function has_value (tab, val)
    for index, value in ipairs(tab) do
        if value == val then
            return true
        end
    end
    return false
end

local function roles_to_classes(els)
    for _, el in ipairs(els) do
        if el.attributes and el.attributes.role then
            -- Add the single role as a class
            if not has_value(el.classes, el.attributes.role) then
                el.classes:insert(el.attributes.role)
            end
            -- Remove the original "role" attribute
            el.attributes.role = nil
        end
    end
end

function Inlines(inlines)
    roles_to_classes(inlines)
    return inlines
end

function Blocks(blocks)
    roles_to_classes(blocks)
    return blocks
end