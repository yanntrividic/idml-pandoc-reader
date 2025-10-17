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
        if el.attributes then
            while el.attributes.role do
                -- Add the space-separated roles as classes
                for class in string.gmatch(el.attributes.role, "%S+") do
                    if not has_value(el.classes, class) then
                        el.classes:insert(class)
                    end
                end
                -- Remove the original "role" attribute
                el.attributes.role = nil
                
                -- In some very rare cases, such as:
                -- <para role="role1">
                -- 	<mediaobject role="role2">
                -- 		<imageobject>
                -- 			<imagedata fileref="image.jpg"/>
                -- 		</imageobject>
                -- 	</mediaobject>
                -- </para>

                -- Pandoc merge the wrappers and output:
                -- <div role="role1" markdown="1" wrapper="1" role="role2">
                -- 
                -- ![](image.jpg)
                -- 
                -- </div>

                -- This is a bug, I think.
                -- The while loop makes sure every role attribute is considered.
            end
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