# IDML Pandoc reader

Le dépôt [deborderbollore/idml-pandoc-reader](https://gitlab.com/deborderbollore/idml-pandoc-reader) contient un programme en ligne de commande automatisant la lecture de fichiers IDML (InDesign Markup Language) pour [Pandoc](https://pandoc.org). Pandoc est un convertisseur universel pouvant convertir énormément de formats de fichiers d'entrée vers énormément de formats de fichiers de sortie, dont DOCX, ODT, HTML, Markdown, AsciiDoc, [etc.](https://pandoc.org/diagram.svgz) **Seule la structure du document est convertie, la mise en forme est totalement ignorée.**

Le développement de ce programme a été effectué dans le contexte du projet [Déborder Bolloré](https://deborderbollore.fr), où il était nécessaire de faire coexister les compétences expertes de graphistes utilisateurices d'Adobe InDesign et de développeureuses web, dans l'idée de produire une publication multiformat accessible quel que soit le contexte de lecture. 

<div style="color:orangered">

À terme, une interface web viendra faciliter l'utilisation de ce programme. Cette interface s'appellera **OutDesign**.

</div>

```{toctree}
---
maxdepth: 2
caption: Documentation
---
contents
prerequisites
usage
formatting_guide
conversion_graph
contribute
licence
```