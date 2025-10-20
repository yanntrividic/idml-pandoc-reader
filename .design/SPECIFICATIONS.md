# Specifications

## A conversion editor, not a text editor

OutDesign is _not_ a text editor. It _could_ allow some basic text editing, but its purpose is to customise conversions; both _format conversions_ and _schema conversions_.

## Style preview

Elements have style. We are currently able to extract it, and I am pretty convinced it would help if we had a preview of those styles (even if support is not 100%). Also, it would be handy to have an idea of what are the styles applied.

## Interactive conversion operators

An IDML file is basically a zipped archive of XML files. The structure of IDML editorial content can be abstracted to a XML tree with a depth of one. From that, we want to be able to reconstruct a more complex tree structure to fit the needs of virtually any data schema, in any conversion workflow.

This is where we need **conversion operators**.

Conversion operators, applied on specific nodes, can change the nodes (i.e., their attributes or their name), or the tree structure itself (e.g., by grouping/ungrouping some nodes, or adding/deleting others).

OutDesign will be here to help composing those operations in order to turn one specific schema into another, by designing the conversion in an interactive, visual way, and each operator will require its own visual metaphor.

Operators will include (WIP):

* **wrap** – wrap an element in a new parent element
* **unwrap** – unwrap an element in its parent
* **delete** – delete an element
* **merge** – group sibling elements in one wrapper element
* **join** – join the content of a series of sibling elements inline 
* **simplify** – remove all attributes from an element
* **reassign** – change the value of an attribute
* etc.

## Flag toggles

In addition to conversion operators, a conversion command usually has flags. The IDML Pandoc Reader [has many](https://outdesign.deborderbollore.fr/en/3_usage.html#liste-des-options). Most of those options need to find a place in the interface.

## Conversion commands for reuse

Ideally, OutDesign will just be an interface that will help building a sort of complex Pandoc command + a [mapping file](https://outdesign.deborderbollore.fr/en/3_usage.html#correspondance-des-styles), so that once the conversion is nicely designed in OutDesign, it can just be exported and run on any machine that has Pandoc installed.

These command should also be stored in the local storage of the browser, so that each session can be reloaded based on the command that was stored, and that users can easily switch sessions and settings.

## An opening to the underlying model

OutDesign must represent an opening for the inner functionings of Pandoc and the IDML Pandoc Reader. If somebody starts using OutDesign and wants to go deeper, OutDesign must act as a stepladder to help people understand more easily what's happening behind the scenes.