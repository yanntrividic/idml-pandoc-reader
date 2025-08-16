-- Mapping operators for map.lua

local utils = require "utils"

local operators = {}

function operators.applyClass(el, classes)
    local new_classes = {}
    for class in string.gmatch(classes, "%S+") do
        -- print("matched class", class)
        table.insert(new_classes, class)
    end
    -- print("new_classes", utils.printTable(new_classes))
    el.classes = new_classes
end

return operators