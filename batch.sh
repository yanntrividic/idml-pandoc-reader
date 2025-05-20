#!/bin/bash

: '
@file Batch convert a source folder of DocBook files
      into markdown_phpextra flavored files through Pandoc,
      using a series of options and filters developed for
      Déborder Bolloré (https://deborderbollore.fr).
@author Yann Trividic
@license CC BY-SA
'

mkdir -p "$2"

for i in "$1"/*.xml; do
  filename=$(basename "$i" .xml)
  pandoc \
    -f docbook \
    -t markdown_phpextra \
    --wrap=none \
    --lua-filter=lua-filters/roles-to-classes.lua \
    --lua-filter=lua-filters/collapse-sections-into-headers.lua \
    -o "$2/$filename.md" \
    "$i"
done