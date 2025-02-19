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
    local preprocessed_html = ''
    for _, source in ipairs(input) do
        preprocessed_html = preprocessed_html .. preprocessing(source)
    end
    return pandoc.read(preprocessed_html, "docbook")
end