-- Custom reader that preprocesses an IDML document that was exported
-- from Adobe InDesign with the DocBook reader.
-- It first converts the IDML with a Python script and then pipes the
-- result in Pandoc's DocBook reader.

function preprocessing(source)
    local result
    if not pcall(function ()
        result = pandoc.pipe("python", {'idml2docbook.py', source.name}, "")
    end) then
        io.stderr:write("Error running 'idml2docbook.py'\n")
        os.exit(1)
    end
    return result
end

function Reader(input)
    -- to add arguments from the command line, see (?)
    -- https://github.com/pandoc/lua-filters/blob/916ca389645940373d9a3c4beca3bd07d51b27aa/track-changes/track-changes.lua#L215
    -- arguments to add:
    -- * reflow-microtypography
    -- * map
    local preprocessed_html = ''
    for _, source in ipairs(input) do
        preprocessed_html = preprocessed_html .. preprocessing(source)
    end
    return pandoc.read(preprocessed_html, "docbook")
end