local function roles_to_classes(els)
    for _, el in ipairs(els) do
        if el.attributes and el.attributes.role then
            -- Add the single role as a class
            el.classes:insert(el.attributes.role)
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