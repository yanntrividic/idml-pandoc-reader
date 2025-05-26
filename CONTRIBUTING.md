# CONTRIBUTING

This project is an ongoing work. Want to contribute? You can:

* Make an issue if you meet a bug;
* Submit a pull request to improve something;
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
* [ ] Write a `setup.py` file
* [x] Add every option to the `.env` file so that the `idml.lua` file is usable on its own
* [ ] Enable CSS selectors in map files
* [ ] Translate the docs to english
* [ ] Publish the package on [PyPI](https://pypi.org/)
* [ ] Mirror the repo on GitHub

### Issues to publish on jgm/pandoc

* [ ] Linebreaks in headers isn't supported with the AsciiDoc writer
* [ ] ID attributes are not supported in headers with the AsciiDoc writer

### idml2xml

* [ ] Make it so calls to le-tex.de are not needed
* [ ] Support accentuated characters in class names