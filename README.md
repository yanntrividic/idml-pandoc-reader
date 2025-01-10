# INDD to Markdown

Ce dépôt vise à automatiser la conversion d'un fichier Adobe InDesign vers un fichier Markdown en conservant au maximum la structure sémantique du fichier originale, de sorte à automatiser une chaîne de publication en prenant un fichier INDD comme fichier pivot.

## Prérequis

* Pandoc
* Python
* Avoir installé les dépendances du script Python (avec la commande `pip install -r requirements.txt`)

## Usage

```bash
pandoc -f html_inherited.lua -t input.html -o output.md --lua-filter=filter.lua
```

## HTML (hérité) comme format d'entrée

Un fichier INDD est constitué d'un ensemble de fichiers XML zippés, mais il est possible depuis Adobe InDesign d'avoir accès à d'autres types d'exports, en particulier ce qu'iels appellent le [HTML (hérité)](https://helpx.adobe.com/fr/indesign/using/export-content-html-cc.html) :

> L'exportation au format HTML convertit facilement votre contenu InDesign en un format adapté au Web. Lorsque vous exportez du contenu au format HTML, vous pouvez contrôler la manière dont le texte et les images sont exportés. InDesign conserve les noms des paragraphes, caractères, objets, tableaux et styles de cellule appliqués aux contenus exportés en marquant les contenus HTML avec les classes de styles CSS du même nom.

Cela implique que pour que ce convertisseur fonctionne comme escompté, il est nécessaire que le fichier INDD présenté en entrée soit strictement formaté, en adoptant une structure de document rigoureuse où chaque unité sémantique est différenciée par un style de paragraphe ou un style de caractère dédié.

En contrepartie, ce format d'export ne retient pas :

* les paragraphes vides (soit les caractères de fin de paragraphes `¶`) ;
* les espaces en tête et en queue de ligne (mais cela fonctionne avec des espaces insécables) ;
* _n_ espaces les uns à la suite des autres (mais cela fonctionne avec des espaces insécables) ;

Et il conserve :

* les césures, en ajoutant un espace après le tiret de la césure et en supprimant le retour chariot.

Le problème avec cette approche est qu'il est nécessaire d'avoir accès à une licence Adobe pour exporter dans un premier temps le fichier INDD au format HTML (hérité). Idéalement, ce convertisseur prendrait en entrée un fichier INDD (ou IDML), et en ressortirait un fichier Markdown. Cette approche, bien que plus générique, nécessite plus de travail du fait de la complexité de la structuration des documents IDML.

## IDML comme format d'entrée

Quand on dézippe un fichier IDML, chaque section du document apparaît ensuite dans un dossier `Stories` qui contient un fichier XML par série de blocs liés.

Scribus peut importer des fichiers IDML, mais ne peut pas les réexporter dans des formats intéressants concernant la structuration sémantique.

## Markdown comme format de sortie

Pour rendre les identifiants et les classes, Kirby utilise [`markdown.extra`](https://michelf.ca/projects/php-markdown/extra/). Concrètement, ça ne semble pas être la meilleure approche pour gérer ça.

## Pandoc

Pandoc utilise des filtres Lua pour manipuler l'AST **après** que le contenu du code source ait été parsé par ses _readers_. Cela veut dire que si le _reader_ ignore un élément ou un attribut, alors les filtres Lua ne pourront rien y faire, les données sont perdues.

En l'occurrence, les blocs imbriqués ne peuvent pas porter d'attributs ou de métadonnées, ce qui fait sauter les noms de classes et les `id` de la plupart de nos éléments.

Pour contourner ce problème, deux options : 

* Préprocesser le fichier HTML ;
* Écrire un _reader_ custom pour notre cas de figure, du genre `inherited_html`.

Il y a exactement ce qu'on veut dans la doc de Pandoc avec l'example [_Extracting the content from web pages_](https://pandoc.org/custom-readers.html#example-extracting-the-content-from-web-pages). Ce qui est intéressant dans ce cas est que le _preprocessing_ est géré par une application tierce, qui permet beaucoup plus de flexibilité en amont du parsing du fichier.

Le plus simple serait certainement de brancher un script de preprocessing ici, avec BeautifulSoup par exemple, pour nettoyer l'HTML et ensuite utiliser Pandoc pour générer le Markdown en sortie. C'est le plus simple car finalement, avant que le document soit parsé, avoir accès à des filtres Lua n'a pas un intérêt énorme... L'API de Pandoc est pour ainsi dire inutile. Aussi, Pandoc ne fournit pas d'outil pour exposer ses _readers_ internes, ce qui veut dire que surcharger un _reader_ spécifique (le reader `html`) est impossible.
