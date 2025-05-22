# TODO

## For this project

* [x] Make a wrapper that is able to pipe distinct sections into the reader so that several ouput files are produced
* [ ] Write the editorial chart
* [x] Make a nice JSON template that shows how to write down a `map.json`, and pass add an optional argument to `preprocessing.py` to specify a custom JSON file
* [x] Try out incorporating alt-text in InDesign, does it follow in HTML Legacy?
* [x] Handle the nested sections
* [x] Make a wrapper script so that it is possible to specify a map through the command line, expose other options...
* [ ] Write the documentation
* [ ] Write a `setup.py` file
* [ ] Add every option to the `.env` file so that the `idml.lua` file is usable on its own.

## Issues to publish on jgm/pandoc

* [ ] Linebreaks in headers isn't supported with the AsciiDoc writer
* [ ] ID attributes are not supported in headers with the AsciiDoc writer

## idml2xml

* [ ] Make it so calls to le-tex.de are not needed
* [ ] Support accentuated characters in class names