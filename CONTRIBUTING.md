# CONTRIBUTING

This project is an ongoing work. Want to contribute? You can:

* Make an issue if you meet a bug (on [GitHub](https://github.com/yanntrividic/idml-pandoc-reader/issues) or on [Gitlab](https://gitlab.com/deborderbollore/idml-pandoc-reader/-/issues), and please embed the content of the logfile associated with your buggy execution);
* Submit a pull request (ideally, on [GitLab](https://gitlab.com/deborderbollore/idml-pandoc-reader)) to improve something, to solve an issue, or else (feel free to explain what you want to do beforehand);
* Contact the maintainer of this projet at [bonjour@yanntrividic.fr](mailto:bonjour@yanntrividic.fr).

Every contribution to the code must be published under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license.

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
* [x] Enable CSS selectors in map files (maybe by temporarily converting `role` attributes into `class`?)
* [x] Translate the docs to english
* [ ] Publish the package on [PyPI](https://pypi.org/)
* [x] Mirror the repo on GitHub
* [x] Add a `merge` operator to the map, that merge together consecutive elements with the same selector
* [ ] Add a "Motivations" documentation page that illustrates where this project can be useful
* [x] ~~Merge all PO files into one for easier maintainance~~ seems like a pain!
* [x] Add to the docs the alt-text of the images is to be done
* [x] Replace URLencoded strings in filenames
* [x] Add "InDesign files" to the formatting guide title
* [x] Add a note on the difficulty of the installation
* [x] Add a command documentation on the duration of idml2hubxml
* [ ] Add docs on how to use `slugs.py`
* [ ] Design OutDesign, an interface for the IDML Pandoc Reader (see the [design notes](https://github.com/yanntrividic/idml-pandoc-reader/tree/main/.design)!)
* [ ] Write tests... Many tests...
* [ ] Add a "Similar approaches section" in the docs somewhere, with IDML2JSON and such
* [ ] Add in the docs a reference to the logfile that is generated
* [ ] Write better docs for the `--typography` option
* [ ] Enhance customisation options of the `--typography` option (specify regex, presets? en/fr?)
* [x] Rewrite the correspondance mapping code as a Lua filter so that it is format agnostic for Pandoc, and allows this to be a true API for conversion personalization. (It mainly concerns the files `cut.py`, `map.py`, and `core.py`. Basically, what it would enable is easy schema mapping for going to a particular schema in any format (e.g. IDML) to any format (e.g. DOCX) for any person aware of semantic structuring.)
* [ ] Add support for endnotes.


### Issues to investigate and publish on @jgm/pandoc

* [ ] Linebreaks in headers isn't supported with the AsciiDoc writer
* [ ] ID attributes are not supported in headers with the AsciiDoc writer
* [ ] Brackets in asciidoc are broken

### idml2xml

* [x] ~~Make it so calls to le-tex.de are not needed anymore and gain autonomy~~ Did I dream that?
* [x] Support accentuated characters in class names
* [ ] There is a bug regarding fonts' direct formatting handling. I think the following snippet is not taking into account the fact that the first `phrase` is in italics, because the font is badly handled.

```
   <para role="NormalParagraphStyle">
      <phrase css:font-size="9pt" css:font-family="Latitude">Sarahland</phrase>
      <phrase css:font-size="9pt" css:font-family="Latitude">, Grand Central Publishing, 2021</phrase>
   </para>
```