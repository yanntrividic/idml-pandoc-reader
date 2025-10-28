# Specifications

## A conversion editor, not a text editor

OutDesign is _not_ a text editor. It _could_ allow some basic text editing, but its purpose is to customise conversions; both _format conversions_ and _schema conversions_.

## Style preview

Elements have style. We are currently able to extract it, and I am pretty convinced it would help if we had a preview of those styles (even if support is not 100%). Also, it would be handy to have an idea of what are the styles applied.

## Interactive conversion operators

One big chunk of work concerning interaction design in this project is related to interactive conversion operators. [A dedicated file](https://gitlab.com/deborderbollore/idml-pandoc-reader/-/blob/main/.design/OPERATORS.md) details where we are at the moment.

## Selector builder

The first step to applying a transformation operation is to select the elements or group of elements to apply it to. It necessarily comes down to designing a selector (CSS-like) to specify what are the elements we want.

Selectors can be:

* All elements of a type, such as `Para` (but I don't see how it would be relevent)
* A single element with an id `#my-id`
* Elements that share the same class `.my-class`
* Elements that share the same classes `.my-class1.my-class2`
* A combination of selectors `Para.my-class1, #my-id.my-class2`
* A nested structure: `Para.my-class Strong`

From there on, given a single-flow HTML document, what can we imagine to effectively build those selectors using direct manipulation raises some questions and problems in terms of interaction.

## Flag toggles

In addition to conversion operators, a conversion command usually has flags. The IDML Pandoc Reader [has many](https://outdesign.deborderbollore.fr/en/3_usage.html#liste-des-options). Most of those options need to find a place in the interface.

## Command builder, conversion commands for reuse

Ideally, OutDesign will just be an interface that will help building a sort of complex Pandoc command + a [mapping file](https://outdesign.deborderbollore.fr/en/3_usage.html#correspondance-des-styles), so that once the conversion is nicely designed in OutDesign, it can just be exported and run on any machine that has Pandoc installed.

These command should also be stored in the local storage of the browser, so that each session can be reloaded based on the command that was stored, and that users can easily switch sessions and settings.

## An opening to the underlying model

OutDesign must represent an opening for the inner functionings of Pandoc and the IDML Pandoc Reader. If somebody starts using OutDesign and wants to go deeper, OutDesign must act as a stepladder to help people understand more easily what's happening behind the scenes.