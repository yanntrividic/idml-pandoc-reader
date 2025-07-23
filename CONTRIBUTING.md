# CONTRIBUTING

This project is an ongoing work. Want to contribute? You can:

* Make an issue if you meet a bug (on [GitHub](https://github.com/yanntrividic/idml-pandoc-reader/issues) or on [Gitlab](https://gitlab.com/deborderbollore/idml-pandoc-reader/-/issues));
* Submit a pull request (ideally, on [GitLab](https://gitlab.com/deborderbollore/idml-pandoc-reader)) to improve something, to solve an issue, or else (feel free to explain what you want to do beforehand);
* Contact the maintainer of this projet at [bonjour@yanntrividic.fr](mailto:bonjour@yanntrividic.fr).

## TODO

### For this project

* [x] Make a wrapper that is able to pipe distinct sections into the reader so that several ouput files are produced
* [x] Write the ~~editorial chart~~ formatting guide
* [x] Make a nice JSON template that shows how to write down a `map.json`, and pass add an optional argument to `preprocessing.py` to specify a custom JSON file
* [x] Try out incorporating alt-text in InDesign, does it follow in HTML Legacy?
* [x] Handle the nested sections
* [x] Make a wrapper script so that it is possible to specify a map through the command line, expose other options...
* [x] Write the documentation
* [x] Write a `setup.py` file
* [x] Add every option to the `.env` file so that the `idml.lua` file is usable on its own
* [ ] Enable CSS selectors in map files
* [x] Translate the docs to english
* [ ] Publish the package on [PyPI](https://pypi.org/)
* [x] Mirror the repo on GitHub
* [ ] Add a `merge` operator to the map, that merge together consecutive elements with the same selector
* [ ] Add a "Motivations" documentation page that illustrates where this project can be useful
* [ ] Merge all PO files into one for easier maintainance
* [x] Add to the docs the alt-text of the images is to be done
* [x] Replace URLencoded strings in filenames
* [x] Add "InDesign files" to the formatting guide title
* [x] Add a note on the difficulty of the installation
* [x] Add a command documentation on the duration of idml2hubxml

### Issues to publish on jgm/pandoc

* [ ] Linebreaks in headers isn't supported with the AsciiDoc writer
* [ ] ID attributes are not supported in headers with the AsciiDoc writer
* [ ] brackets in asciidoc are broken

### idml2xml

* [ ] Make it so calls to le-tex.de are not needed
* [ ] Support accentuated characters in class names