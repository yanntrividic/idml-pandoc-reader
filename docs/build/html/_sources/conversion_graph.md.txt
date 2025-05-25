# Graphe de conversions

La logique derrière ce projet est la suivante :

1. Prendre un fichier IDML en entrée, et le donner à [`idml2xml-frontend`](https://github.com/transpect/idml2xml-frontend) pour obtenir un fichier [Hub XML](https://github.com/le-tex/Hub) ;
2. À partir de ce fichier, le "nettoyer" pour obtenir un document dans la spécification DocBook 5.1, supportée par Pandoc ;

Ces deux premières étapes sont les objectifs du paquet `idml2docbook` développé pour ce projet.

3. Lire le fichier DocBook produit avec la [version modifiée de Pandoc](https://github.com/yanntrividic/pandoc/) ;
4. Appliquer des filtres Lua pour correctement structurer l'[arbre de syntaxe abstraite](https://fr.wikipedia.org/wiki/Arbre_de_la_syntaxe_abstraite) (AST) de Pandoc ;
5. Utiliser le _writer_ de Pandoc souhaité.

```{graphviz} conversions.dot
:caption: _Graphe des conversions à l'œuvre dans ce projet._
:align: center
```