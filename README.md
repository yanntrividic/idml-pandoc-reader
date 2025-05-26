# IDML Pandoc reader

Ce dépôt contient un programme en ligne de commande automatisant la lecture de fichiers IDML (InDesign Markup Language) pour [Pandoc](https://pandoc.org). Pandoc est un convertisseur universel pouvant convertir énormément de formats de fichiers d'entrée vers énormément de formats de fichiers de sortie, dont DOCX, ODT, HTML, Markdown, AsciiDoc, [etc.](https://pandoc.org/diagram.svgz) **Seule la structure du document est convertie, la mise en forme est totalement ignorée.**

Le développement de ce programme a été effectué dans le contexte du projet [Déborder Bolloré](https://deborderbollore.fr), où il était nécessaire de faire coexister les compétences expertes de graphistes utilisateurices d'Adobe InDesign et de développeureuses web, dans l'idée de produire une publication multiformat accessible quel que soit le contexte de lecture. 

🚨 À terme, une interface web viendra faciliter l'utilisation de ce programme. Cette interface s'appellera **OutDesign**, en réponse à la concentration dans les logiciels d'édition.

Une documentation de ce dépôt est déployée en ligne sur [outdesign.deborderbollore.fr](https://outdesign.deborderbollore.fr).

::include{file=./docs/source/contribute.md}

::include{file=./docs/source/licence.md}