# Notes on style mapping and conversion operators in Lua

In addition to storing some Lua filters for the IDML Pandoc Reader, this folder is an attempt at adapting some of the code from `idml2docbook` to a Lua filter, so that a part of the API only has Pandoc as a dependency. This file gathers notes about it.

**Disclaimer:** Many choices here are highly opinionated. 

## TODO

* [x] Make a pseudo CSS selector API in Lua, that could support queries such as `Div.class1.class2`
* [ ] Enable support for conversion operators:
    * [x] **wrap** – wrap an element in a new parent element
    * [x] **unwrap** – unwrap an element in its parent
    * [x] **delete** – delete an element
    * [ ] **merge** – group the content of sibling elements
    * [x] **simplify** – remove all attributes from an element
    * [x] **reassign** – change the value of an attribute
* [x] Enable support for other operators, currently found in the JSON map files (see https://outdesign.deborderbollore.fr/en/3_usage.html#correspondance-des-styles):
    * [x] **type**
    * [x] **role** [is now `classes`.]
    * [x] **cut** does it make sense here? Is it possible? It seems like it's doable. Also, removing --map from the Python module makes the cuts difficult to do from there.
    * [x] **level**
    * [x] **br**
    * [x] **empty**
* [x] Work on perfs. The `map.lua` filter currently multiplies by 2 the computing time of a file. _Déborder Bolloré_ takes a bit less than 3.6s, compared to 1.7s without the filter. Could [jog](https://github.com/tarleb/jog) be a solution for improving perfs? **Update:** Jog was made for small filters, which skip large parts of the document. The `map.lua` filter needs to apply on most elements of the AST to check whether the selector applies to them. Jog actually increases computing time by 3x to 5x.
* [ ] Add logging messages with the `pandoc.log` module.
* [ ] Add a `merge` operator, especially for CLV3
* [x] Make it so it is possible to turn an `Inline` in to a `Block` through the `type` operator. Especially useful for when character styles are used as paragraph styles. **Update:** It's been explored in the `custom-traversal-order-pandoc` branch. It is not so easy to pull out because `Inline` and `Block` functions are typed. For now, the new implementation increases by 7x the computing time. Maybe it could be optimised.
* [ ] Technically, now that the mapping is written in Lua, it would be possible to apply Lua filters on elements selected by `isMatchingSelector`... Wouldn't it?


## Run a test

To run a test.

```bash
diff test/test.output <(pandoc -f markdown test/test.md -t markdown --lua-filter=map.lua -M map=test/test.json)
```

To run the conversion command for _Déborder Bolloré_:

```bash
diff test/bollo.output <(pandoc -f docbook test/bollo.dbk -t markdown_phpextra --lua-filter=roles-to-classes.lua --lua-filter=collapse-sections-into-headers.lua --lua-filter=map.lua -M map=test/bollo.json --wrap=none)
```

## Panflute

It would also be possible to design these filters with a Python framework such as [Panflute](https://github.com/sergiocorreia/panflute), but then it would add a Python dependency, while Pandoc embeds its own Lua interpretor...

## List of Pandoc types

Pandoc's list of types available in Lua is quite short. It can be found [here](https://pandoc.org/lua-filters.html#lua-type-reference). Some types are more necessary than others for OutDesign. Checked entries are the one that are currently supported, and **bold** ones are the most important to implement for the style mapping.

Checked types are the types currently supported by the filter.

### Blocks

When the element can't hold classes or attributes, it must be wrapped in a `Div` that can, and this `Div` must be tagged with a `"wrapper"=1` attribute.

* [x] [class attrs] **Div**
* [x] [class attrs] **Figure**
* [x] [class attrs] **Header**
* [x] [no classes!] **Para**
* [x] [no classes!] **BlockQuote**
* [x] [no classes!] **BulletList**
* [x] [no classes!] **OrderedList**
* [x] [class attrs] CodeBlock
* [ ] [class attrs] Table
* [ ] [no classes!] DefinitionList
* [ ] [no classes!] HorizontalRule
* [ ] [no classes!] LineBlock
* [ ] [no classes!] Plain
* [x] [no classes!] RawBlock

### Inlines

When an Inline can't have classes or attributes, it must be wrapped in a `Span` that can, and this `Span` must be tagged with a `"wrapper"=1` attribute.

* [x] [class attrs] **Link**
* [x] [class attrs] **Code**
* [x] [class attrs] **Span**
* [x] [class attrs] **Image**
* [x] [no classes!] **LineBreak**
* [x] [no classes!] **Superscript**
* [x] [no classes!] **Emph**
* [x] [no classes!] **SmallCaps**
* [x] [no classes!] **Strikeout**
* [x] [no classes!] **Strong**
* [x] [no classes!] **Subscript**
* [ ] [no classes!] Cite
* [ ] [no classes!] Math
* [x] [no classes!] Note
* [ ] [no classes!] Quoted
* [ ] [no classes!] RawInline
* [ ] [no classes!] SoftBreak
* [x] [no classes!] Space
* [x] [no classes!] Str

## querySelectorAll

So basically, what we need is a `querySelectorAll` function that returns all the Pandoc Blocks and Inlines that match the selector, that kinda look like CSS selectors. For simplicity, we'll consider that `Div` and elements are always wrappers for _one_ single child element. That implies that when we talk about a class for a node that actually can't hold a class attribute, we are actually talking about the class of the wrapping `Div`.

Several scenarios have to be met:

* `.class1` returns all elements that have for parent a `Div` with `class1` as a class, and all Inline elements that have `class1` for a class
* `.class1.class2` returns all elements that have for parent a `Div` with both `class1` and `class2`, and all Inline elements that have `class1` and `class2`
* `.class1, .class2` returns all elements that have for parent a `Div` with `class1` or `class2`, and all Inline elements that have either `class1` or `class2`

And it should also work according to Pandoc types:

* `BlockQuote.class1` is actually refering to the elements that are `BlockQuote` elements wrapped with a `Div` that has a `class1` class.

**Note:** This has been implemented, though it was adapted to Pandoc Lua filters structure into a `isMatchingSelector` ffunction.