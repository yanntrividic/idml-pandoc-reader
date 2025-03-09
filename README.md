# IDML Pandoc reader

Ce dépôt vise à automatiser la conversion d'un fichier Adobe InDesign vers un fichier Markdown en conservant au maximum la structure sémantique du fichier originale, de sorte à automatiser une chaîne de publication en prenant un fichier INDD comme fichier pivot.

## Prérequis

* Pandoc
* Python
* les dépendances du script Python (avec la commande `pip install -r requirements.txt`)
* `idml2xml-frontend` (s'installe avec `git` via la commande `git clone https://github.com/transpect/idml2xml-frontend --recurse-submodules`)
* avoir précisé dans un fichier `.env` le chemin vers idml2xml-frontend (voir l'exemple fourni avec `.env.sample`)

## Usage

```bash
pandoc -f idml.lua -t input.idml -o output.md --lua-filter=roles-to-classes.lua
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

Si on regarde [la spécification du format IDML](https://www.jetsetcom.net/images/downloads/IDML-File-Format-Specification-CS5-2010.pdf) (qui est opensource mais difficile à trouver), et qu'on arpente un peu le contenu d'un fichier IDML, on se rend compte qu'il y a quand même matière à faire quelque chose.

Ça aurait au moins deux avantages :

* IDML est plus proche d'INDD que le format d'exportation HTML (hérité), en cela, certaines informations importantes sont présentes dans IDML mais pas dans l'export HTML.
* Il n'est pas rare que les utilisateurices d'InDesign garde par sécurité des fichiers IDML comme format de stockage, celui-ci étant plus pérenne qu'INDD. Personne n'exporte ses projets InDesign pour du stockage.

En prenant IDML comme format d'entrée, ce qui aurait le plus de sens serait de convertir ce format vers DocBook, qui est plus largement répandu. Il existe aussi un reader Pandoc pour DocBook.

Plusieurs problèmes/désavantages sont cependant présents :

* La structure d'IDML, bien que linéaire et facilement parcourable, reste tout de même assez différente de la structure de DocBook, écrire un convertisseur représenterait un certain investissement en temps (en comparaison de développer un reader pour HTML (hérité)).
* Le format HTML (hérité) est directement généré depuis le fichier INDD, et contient en particulier des informations sur les surcharges de styles qui ne sont pas triviales à recalculer. On perdrait ça dans un premier temps.

### idml2xml-frontend

En cherchant `idml docbook` dans GitHub, je suis tombé sur le travail de le-tex, leur framework Transpect et plus particulièrement leur projet[`idml2xml-frontend`](https://github.com/transpect/idml2xml-frontend), qui a développé un convertisseur de fichiers IDML vers DocBook 5.1. C'est exactement ce dont on a besoin, ça marche bien.

Ça ajoute pas mal de dépendances au projet, qui sont toutes plutôt bien bundled dans le dépôt `idml2xml-frontend`, mais il faut a minima avoir Java>=1.7 installé sur sa machine.

À partir de là, on peut réutiliser le travail effectué pour préparer le contenu des fichiers HTML (hérité) pour Pandoc, et on est bien. Il y a un tutoriel sur leur site web pour notamment [mapper des styles pour la conversion](https://transpect.github.io/tutorial.html) en configurant correctement leur convertisseur, mais je ne suis pas certain que ça s'applique vraiment à notre pipeline... En soi, ça n'est pas très important, étant donné qu'on peut reprendre ce qu'on veut ensuite dans BeautifulSoup, ce qui est un peu moins classique pour travailler du XML que XSLT ou xProc mais qui fait le boulot quand même. (Update : suite à diverses tentatives pour intégrer le mapping des classes, notamment via [`map-style-names`](https://github.com/transpect/map-style-names), il s'est révélé assez clairement que le gain qui serait obtenu en modifiant `idml2xml-frontend` serait assez minime par rapport au coût d'apprentissage des différentes technologies impliquées (xProc et Transpect), mieux vaut construire autour.)

## DocBook comme format d'entrée

Il y a des choses à savoir avant de pouvoir convertir du DocBook avec Pandoc. [Cet article un peu vieux (attention)](https://www.peterlavin.com/articles/pandoc.html) a l'air de soulever des questions intéressantes.

Aussi, il n'est pas ultra clair ce que Pandoc supporte quant à la spécification de DocBook v5.1. [Il semblerait qu'il y ait une partie du support pour la v4.5, et une autre pour la v5.x.](https://github.com/jgm/pandoc/issues/7747).

Pour obtenir de l'AsciiDoc depuis DocBook, on a notamment [ce convertisseur](https://github.com/asciidoctor/docbookrx), auquel Dan Allen, entre autres, a beaucoup contribué. Trouvé grâce à cette [note de blog](https://blogs.gnome.org/pmkovar/2015/10/27/converting-docbook-into-asciidoc/) qui est intéressante sur la question.

Code source du reader : https://github.com/jgm/pandoc/blob/main/src/Text/Pandoc/Readers/DocBook.hs.

Le problème avec cette approche, c'est que Pandoc ne supporte pas l'attribut `role` pour les blocs (voir [#9089](https://github.com/jgm/pandoc/issues/9089)), qui est un attribut un peu fourre-tout mais qui permet notamment d'attribuer des sortes de classes à DocBook.

Pour régler ce problème, plusieurs solutions :

* Forker Pandoc et y ajouter le support pour automatiquement ajouter l'attribut `role` à la liste d'attributs de tous les blocs pour le lecteur DocBook.
* Trouver une solution en formattant le fichier XML fourni en entrée en permettant de récupérer l'information dans l'AST, puis nettoyer l'AST avec des filtres. Ce qui a été essayé jusqu'à présent. Ajouter des `xml:id` sur tous les éléments ne fonctionne pas. Peut-être qu'on pourrait encapsuler le contenu de toutes les feuilles de type bloc dans des `phrase` qui auraient des `role` ?
* Convertir le fichier DocBook en un fichier HTML, qui lui comporterait des classes, au travers d'une transformation XSLT.


## Markdown comme format de sortie

Pour rendre les identifiants et les classes, Kirby utilise [`markdown.extra`](https://michelf.ca/projects/php-markdown/extra/). Concrètement, ça ne semble pas être la meilleure approche pour gérer ça.

## Pandoc

Pandoc utilise des filtres Lua pour manipuler l'AST **après** que le contenu du code source ait été parsé par ses _readers_. Cela veut dire que si le reader Pandoc pour DocBook ignore un élément ou un attribut, alors les filtres Lua ne pourront rien y faire, les données sont perdues.

En l'occurrence, les blocs imbriqués ne peuvent pas porter d'attributs ou de métadonnées, ce qui fait sauter les noms de classes et les `id` de la plupart de nos éléments.

Pour contourner ce problème, deux options : 

* Préprocesser le fichier HTML ;
* Écrire un reader Pandoc pour DocBook custom pour notre cas de figure, du genre `inherited_html`.

Il y a exactement ce qu'on veut dans la doc de Pandoc avec l'example [_Extracting the content from web pages_](https://pandoc.org/custom-readers.html#example-extracting-the-content-from-web-pages). Ce qui est intéressant dans ce cas est que le _preprocessing_ est géré par une application tierce, qui permet beaucoup plus de flexibilité en amont du parsing du fichier.

Le plus simple serait certainement de brancher un script de preprocessing ici, avec BeautifulSoup par exemple, pour nettoyer l'HTML et ensuite utiliser Pandoc pour générer le Markdown en sortie. C'est le plus simple car finalement, avant que le document soit parsé, avoir accès à des filtres Lua n'a pas un intérêt énorme... L'API de Pandoc est pour ainsi dire inutile. Aussi, Pandoc ne fournit pas d'outil pour exposer ses _readers_ internes, ce qui veut dire que surcharger un reader Pandoc pour DocBook spécifique (le reader `html`) est impossible.
