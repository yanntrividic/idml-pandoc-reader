# IDML Pandoc reader

Ce dépôt contient un programme en ligne de commande automatisant la lecture de fichiers IDML (InDesign Markup Language) pour [Pandoc](https://pandoc.org). Pandoc est un convertisseur universel pouvant convertir énormément de formats de fichiers d'entrée vers énormément de formats de fichiers de sortie, dont DOCX, ODT, HTML, Markdown, AsciiDoc, [etc.](https://pandoc.org/diagram.svgz)

Le développement de ce programme a été effectué dans le contexte du projet [Déborder Bolloré](https://deborderbollore.fr), où il était nécessaire de faire coexister les compétences expertes de graphistes utilisateurices d'Adobe InDesign et de développeureuses web, dans l'idée de produire une publication multiformat accessible quel que soit le contexte de lecture. 

À terme, une interface web viendra faciliter l'utilisation de ce programme. Cette interface s'appellera OutDesign.

## Contenus du dépôt

Les fichiers et dossiers les plus importants du dépôt sont :

* `idml2docbook` est un package Python permettant de faire le pont entre les formats IDML et DocBook, ce dernier étant compris par Pandoc ;
* `lua-filters` contient des filtres Lua permettant de modifier le comportement du lecteur DocBook afin de mieux correspondre aux attendus de la conversion de fichiers IDML ;
* `maps` et `map.json.sample` contiennent des fichiers JSON exemples montrant comment paramétrer la conversion en fonction des spécificités de chaque livre, voir _Correspondance des styles_ ;
* `.env.sample` est un fichier de configuration permettant de donner des valeurs par défaut au convertisseur ;
* `batch.sh` est le script utilisé pour faciliter la conversion de fichiers en lots via Pandoc ;
* `idml.lua` fait le lien entre `idml2docbook` et Pandoc, voir _Commandes de base_ ;

## Prérequis

### Dépendances

Le format IDML est complexe, et il est difficile d'en extraire les informations. Dans l'idéal, ce dépôt consisterait en un seul fichier Haskell, comme [les autres lecteurs de Pandoc](https://github.com/jgm/pandoc/tree/main/src/Text/Pandoc/Readers). Cependant, cela prendrait un temps fou à développer.

D'autres se sont penché·es sur la question de la lecture de fichiers IDML, en particulier le projet [`idml2xml-frontend`](https://github.com/transpect/idml2xml-frontend), distribué sous licence FreeBSD. Nous construisons notre convertisseur en continuant ce travail, en proposant un [_binding_](https://fr.wikipedia.org/wiki/Binding) entre `idml2xml-frontend` et Pandoc.

Les dépendances sont :

* Python 3.x ;
* Java 1.7+ ;
* les dépendances du package Python (avec la commande `pip install -r requirements.txt`)
* [`idml2xml-frontend`](https://github.com/transpect/idml2xml-frontend) (s'installe avec `git` via la commande `git clone https://github.com/transpect/idml2xml-frontend --recurse-submodules`) ;
* avoir précisé dans un fichier `.env` le chemin vers `idml2xml-frontend` (voir l'exemple fourni avec `.env.sample`).

Pandoc n'est pas une dépendance à proprement parler étant donné que `idml2docbook` n'en a pas besoin. Cependant, [une version un peu modifiée de Pandoc](https://github.com/yanntrividic/pandoc/) a été développée pour supporter la lecture des styles de paragraphes et de caractères. Pour l'utiliser, il faut [la compiler depuis la source](https://github.com/yanntrividic/pandoc/blob/main/INSTALL.md). Il est aussi possible d'utiliser la version principale de Pandoc, mais alors sans _Correspondance des styles_. Une [_pull request_](https://github.com/jgm/pandoc/pull/10665) est en cours pour intégrer ces nouvelles fonctionnalités dans la branche principale de Pandoc.

> **Note :** Pour les fichiers IDML les plus lourds, il peut être nécessaire d'[augmenter la taille du tas Java](https://github.com/transpect/idml2xml-frontend/blob/master/idml2xml.sh#L33), par exemple à `2048m` ou `4096m`.

### Configuration de l'environnement `.env`

Le fichier `.env.sample` montre l'exemple d'un fichier de fichier de configuration.

A minima, pour fonctionner, ce convertisseur nécessite d'exécuter `idml2xml-frontend`. Le fichier `.env` a donc pour seule ligne obligatoire le chemin absolu menant au dossier `idml2xml-frontend` présent sur votre machine, correspondant à l'entrée `IDML2HUBXML_SCRIPT_FOLDER`. Seule cette entrée est **obligatoire**.

Les autres valeurs du fichier `.env` permettent de remplacer les valeurs par défaut du package `idml2docbook`. Pour plus d'informations sur ces différentes variables, consultez l'aide du package :

```bash
python -m idml2docbook -h
```

### Test de la configuration

Pour vérifier que les dépendances ont bien été installées et le fichier `.env` bien paramétré, vous pouvez tester le convertisseur dans votre terminal avec la commande suivante :

```bash
pandoc hello_world.idml -f idml.lua -t markdown
```

Le résultat devrait alors être :

```
::: {wrapper="1" role="NormalParagraphStyle"}
Hello world!
:::
```

## Usage

### Correspondance des styles

Une fois la [version modifiée de Pandoc](https://github.com/yanntrividic/pandoc/) installée, Pandoc sera en mesure d'interpréter les attributs `role` des éléments des fichiers DocBook obtenus après conversion. Ces rôles sont ensuite considérés comme des classes par Pandoc grâce au filtre `roles-to-classes.lua`.

Ces attributs correspondent aux styles de paragraphes et de caractères précisés dans InDesign. Comme illustré dans le fichier `map.json.sample`, il est possible d'associer ces styles de paragraphes et de caractères à des traitements particuliers :

* `role` : remplace le rôle du fichier source par une ou plusieurs classes ;
* `type` : change le type d'élément (par défaut, `para` pour tous les éléments) vers un nouveau type ;
* `level` : si `type` est un titre DocBook (`title`), `level` spécifie le niveau du titre ;
* `delete` : supprime les éléments avec cet attribut `role` ;
* `unwrap` : déplie le contenu de ces éléments dans l'élément parent ;
* `cut` : crée un nouveau fichier à chaque élément ayant ce `role` ;
* `empty` : conserve les éléments vides portant ce `role` (tous les autres éléments vides sont supprimés, sauf si l'option `-e`/`--empty` est active).

Le script `idml2docbook/map.py` aide à constituer ces fichiers JSON. Ce script prend un fichier DocBook et un fichier JSON de correspondance, et détaille la correspondance de styles qui va être appliquée via par exemple la commande suivante :

```bash
python idml2docbook/map.py file.xml maps/db.json
```

### Commandes de base

Il est possible d'utiliser ce convertisseur de diverses manières :

1. Avec le package `idml2docbook`, puis en exécutant Pandoc sur les fichiers produits ;
1. Avec le lecteur Lua `idml.lua` ;
1. Avec le script `batch.sh`.

#### `idml2docbook`

Ce package Python est la contribution principale de ce dépôt. Il offre une API permettant de convertir un fichier fichier IDML en un ou plusieurs fichiers DocBook.

Convertir un fichier :

```bash
python -m idml2docbook hello_world.idml
```

Afficher l'aide à l'utilisation avec l'option `-h`/`--help` :

```bash
python -m idml2docbook -h 
```

#### `idml.lua`

Ce fichier fait le pont entre Pandoc et `idml2docbook`. Il permet de prendre le résultat de ce dernier pour l'insérer dans Pandoc. [Pandoc ne permet pas de spécifier d'arguments arbitraires en ligne de commande](https://github.com/jgm/pandoc/discussions/9689), ce qui implique que seul modifier le fichier `.env` peut influencer le comportement de `idml2docbook` quand exécuté au travers de `idml.lua`.

Convertir un fichier IDML vers Markdown, avec par exemple le filtre `roles-to-classes.lua` :

```
pandoc -f idml.lua -t markdown --lua-filter=lua-filters/roles-to-classes.lua hello_world.idml
```

#### `batch.sh`

Avant toute chose, il est nécessaire de donner les droits d'exécution à ce script :

```bash
chmod +x batch.sh
```

Ce petit script shell permet de faciliter la liaison entre Pandoc et `idml2docbook` lorsque ce dernier est utilisé avec l'option `-c`/`--cut` pour séparer le résultat de la conversion en plusieurs fichiers (ou chapitres).

Cette commande prend deux dossiers en arguments : un dossier d'entrée et un de sortie. Il est ainsi possible de chaîner les commandes, par exemple :

```bash
python -m idml2docbook file.idml --output xml_folder --cut ; ./batch.sh xml_folder md_folder
```

### Détail de la commande permettant de convertir le recueil _Déborder Bolloré_

La commande pour compiler les contributions du recueil _Déborder Bolloré_, dont on peut retrouver le résultat sur le dépôt [deborderbollore/articles](https://gitlab.com/deborderbollore/articles), est la suivante :

```bash
python -m idml2docbook db.idml \
  --output xml \
  --map maps/db.json \
  --cut \
  --names \
  --raster jpg \
  --vector svg \
  --media-folder images ;
./batch.sh xml articles
```

En détails :

* `-o`/`--output` : permet de préciser le dossier où seront contenus les fichiers DocBook produits ;
* `-m`/`--map` : spécifie les opérations à effectuer sur certains styles de caractères et de paragraphes, voir _Correspondance des styles_ ;
* `-c`/`--cut` : coupe le résultat en plusieurs fichiers DocBook autonomes ;
* `-n`/`--names` : génère les noms des fichiers finaux à partir des contenus des titres de niveau 1 ;
* `-r`/`--raster` : remplace les extensions des images matricielles par `jpg` dans les URL des fichiers de sortie ;
* `-v`/`--vector` : idem pour les images vectorielles ;
* `-f`/`--media-folder` : remplace l'URL absolue des médias dans les fichiers de sortie par `images/`.

D'autres paramétrages encore sont exposés via les options de ce package.

Enfin, le script `batch` convertit les fichiers DocBook obtenus en Markdown, en précisant la saveur `markdown_phpextra`, et avec les filtres Lua nécessaires.


<!------------------------------------------------------->

<!-- ## Vieilles notes à trier

### À propos du format IDML

IDML est le format "ouvert" d'InDesign, de retrocompabilitié. C'est celui que l'on peut lire et interpréter sans 

vers un fichier Markdown en conservant au maximum la structure sémantique du fichier originale, de sorte à automatiser une chaîne de publication en prenant un fichier INDD comme fichier pivot.

### HTML (hérité) comme format d'entrée

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

### IDML comme format d'entrée

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

#### idml2xml-frontend

En cherchant `idml docbook` dans GitHub, je suis tombé sur le travail de le-tex, leur framework Transpect et plus particulièrement leur projet[`idml2xml-frontend`](https://github.com/transpect/idml2xml-frontend), qui a développé un convertisseur de fichiers IDML vers DocBook 5.1. C'est exactement ce dont on a besoin, ça marche bien.

Ça ajoute pas mal de dépendances au projet, qui sont toutes plutôt bien bundled dans le dépôt `idml2xml-frontend`, mais il faut a minima avoir Java>=1.7 installé sur sa machine.

À partir de là, on peut réutiliser le travail effectué pour préparer le contenu des fichiers HTML (hérité) pour Pandoc, et on est bien. Il y a un tutoriel sur leur site web pour notamment [mapper des styles pour la conversion](https://transpect.github.io/tutorial.html) en configurant correctement leur convertisseur, mais je ne suis pas certain que ça s'applique vraiment à notre pipeline... En soi, ça n'est pas très important, étant donné qu'on peut reprendre ce qu'on veut ensuite dans BeautifulSoup, ce qui est un peu moins classique pour travailler du XML que XSLT ou xProc mais qui fait le boulot quand même. (Update : suite à diverses tentatives pour intégrer le mapping des classes, notamment via [`map-style-names`](https://github.com/transpect/map-style-names), il s'est révélé assez clairement que le gain qui serait obtenu en modifiant `idml2xml-frontend` serait assez minime par rapport au coût d'apprentissage des différentes technologies impliquées (xProc et Transpect), mieux vaut construire autour.)

### DocBook comme format d'entrée

Il y a des choses à savoir avant de pouvoir convertir du DocBook avec Pandoc. [Cet article un peu vieux (attention)](https://www.peterlavin.com/articles/pandoc.html) a l'air de soulever des questions intéressantes.

Aussi, il n'est pas ultra clair ce que Pandoc supporte quant à la spécification de DocBook v5.1. [Il semblerait qu'il y ait une partie du support pour la v4.5, et une autre pour la v5.x.](https://github.com/jgm/pandoc/issues/7747).

Pour obtenir de l'AsciiDoc depuis DocBook, on a notamment [ce convertisseur](https://github.com/asciidoctor/docbookrx), auquel Dan Allen, entre autres, a beaucoup contribué. Trouvé grâce à cette [note de blog](https://blogs.gnome.org/pmkovar/2015/10/27/converting-docbook-into-asciidoc/) qui est intéressante sur la question.

Code source du reader : https://github.com/jgm/pandoc/blob/main/src/Text/Pandoc/Readers/DocBook.hs.

Le problème avec cette approche, c'est que Pandoc ne supporte pas l'attribut `role` pour les blocs (voir [#9089](https://github.com/jgm/pandoc/issues/9089)), qui est un attribut un peu fourre-tout mais qui permet notamment d'attribuer des sortes de classes à DocBook.

Pour régler ce problème, plusieurs solutions :

* Forker Pandoc et y ajouter le support pour automatiquement ajouter l'attribut `role` à la liste d'attributs de tous les blocs pour le lecteur DocBook.
* Trouver une solution en formattant le fichier XML fourni en entrée en permettant de récupérer l'information dans l'AST, puis nettoyer l'AST avec des filtres. Ce qui a été essayé jusqu'à présent. Ajouter des `xml:id` sur tous les éléments ne fonctionne pas. Peut-être qu'on pourrait encapsuler le contenu de toutes les feuilles de type bloc dans des `phrase` qui auraient des `role` ?
* Convertir le fichier DocBook en un fichier HTML, qui lui comporterait des classes, au travers d'une transformation XSLT.


### Markdown comme format de sortie

Pour rendre les identifiants et les classes, Kirby utilise [`markdown.extra`](https://michelf.ca/projects/php-markdown/extra/). Concrètement, ça ne semble pas être la meilleure approche pour gérer ça.

### Pandoc

Pandoc utilise des filtres Lua pour manipuler l'AST **après** que le contenu du code source ait été parsé par ses _readers_. Cela veut dire que si le reader Pandoc pour DocBook ignore un élément ou un attribut, alors les filtres Lua ne pourront rien y faire, les données sont perdues.

En l'occurrence, les blocs imbriqués ne peuvent pas porter d'attributs ou de métadonnées, ce qui fait sauter les noms de classes et les `id` de la plupart de nos éléments.

Pour contourner ce problème, deux options : 

* Préprocesser le fichier HTML ;
* Écrire un reader Pandoc pour DocBook custom pour notre cas de figure, du genre `inherited_html`.

Il y a exactement ce qu'on veut dans la doc de Pandoc avec l'example [_Extracting the content from web pages_](https://pandoc.org/custom-readers.html#example-extracting-the-content-from-web-pages). Ce qui est intéressant dans ce cas est que le _preprocessing_ est géré par une application tierce, qui permet beaucoup plus de flexibilité en amont du parsing du fichier.

Le plus simple serait certainement de brancher un script de preprocessing ici, avec BeautifulSoup par exemple, pour nettoyer l'HTML et ensuite utiliser Pandoc pour générer le Markdown en sortie. C'est le plus simple car finalement, avant que le document soit parsé, avoir accès à des filtres Lua n'a pas un intérêt énorme... L'API de Pandoc est pour ainsi dire inutile. Aussi, Pandoc ne fournit pas d'outil pour exposer ses _readers_ internes, ce qui veut dire que surcharger un reader Pandoc pour DocBook spécifique (le reader `html`) est impossible.

### Licence

<a href="https://gitlab.com/deborderbollore/idml-pandoc-reader">IDML Pandoc Reader</a> © 2025 par <a href="https://yanntrividic.fr">Yann Trividic</a> est distribué sous licence <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a><img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/sa.svg" style="max-width: 1em;max-height:1em;margin-left: .2em;"> -->