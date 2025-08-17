-- Utility functions for map.lua

local utils = {}

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

function utils.readMap(map_file)
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

local function split(str, pat)
    local t = {}
    str:gsub("([^" .. pat .. "]+)", function(c) t[#t+1] = c end)
    return t
end

-- Parse one selector like "BlockQuote.class1.class2"
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

-- el: Pandoc element
-- tag: string or nil
-- classes: table of strings
function utils.isMatchingSelector(el, selector)
    local tag, classes = utils.parseSelector(selector)
    -- Check tag if provided
    if tag and el.t ~= tag then
        return false
    end

    -- Check classes if provided
    if classes then
        local el_classes = el.classes or {}
        for _, class in ipairs(classes) do
            local found = false
            for _, c in ipairs(el_classes) do
                if c == class then
                    found = true
                    break
                end
            end
            if not found then
                return false
            end
        end
    end

    return true
end

return utils