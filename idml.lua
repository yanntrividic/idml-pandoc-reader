-- Custom reader that preprocesses an IDML document that was exported
-- from Adobe InDesign with the DocBook reader.
-- It first converts the IDML with a Python script and then pipes the
-- result in Pandoc's DocBook reader.

function preprocessing(source)
    local result
    if not pcall(function ()
        result = pandoc.pipe("python", {'-m', 'idml2docbook', source.name}, "")
    end) then
        io.stderr:write("Error running 'idml2docbook'\nRefer to idml2docbook.log")
        os.exit(1)
    end
    return result
end

function Reader(input)
    local preprocessed_docbook = ''
    for _, source in ipairs(input) do
        preprocessed_docbook = preprocessed_docbook .. preprocessing(source)
    end
    return pandoc.read(preprocessed_docbook, "docbook")
end