# Revision history for idml-pandoc-reader

## idml-pandoc-reader 0.4.1 (2025-08-25)

* Removed a few comments in the code.
* Wrote better docs.

## idml-pandoc-reader 0.4.0 (2025-08-20)

* Mapping functionalities are now written in Lua. That means that they are now format-agnostic, and can work with Pandoc as their only dependency, see `lua-filters/map.lua`.
* `idml2docbook` was updated to reflect those changes, and is now closer to a simple IDML-to-DocBook converter.
* JSON mapping structure has changed to comply to the new architecture, operators changed as well.
* `cut.py` was removed and integrated as well as a Lua filter automatically called when a `cut` operation is specified in a mapping JSON file.
* `batch.sh` was removed, as it was mostly making a bridge between `idml2docbook`, `cut.py` and Pandoc. This is not necessary anymore.

## idml-pandoc-reader 0.3.0 (2025-08-18)

* A `.design` folder and its content now exist to document the design of OutDesign.
* Started working on new Lua filters to apply mapping through Pandoc, and not Python.
* Fixed a bug where paragraph and style names extraction was raising an error if there was an extra IDML layer.

## idml-pandoc-reader 0.2.0 (2025-08-01)

* Role names are now using the same `custom_slugify` method as filenames.

## idml-pandoc-reader 0.1.0 (2025-07-31)

Initial release.