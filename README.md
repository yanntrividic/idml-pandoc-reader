# IDML Pandoc reader

Ce dépôt contient un programme en ligne de commande automatisant la lecture de fichiers IDML (InDesign Markup Language) pour [Pandoc](https://pandoc.org). Pandoc est un convertisseur universel pouvant convertir énormément de formats de fichiers d'entrée vers énormément de formats de fichiers de sortie, dont DOCX, ODT, HTML, Markdown, AsciiDoc, [etc.](https://pandoc.org/diagram.svgz) **Seule la structure du document est convertie, la mise en forme est totalement ignorée.**

Le développement de ce programme a été effectué dans le contexte du projet [Déborder Bolloré](https://deborderbollore.fr), où il était nécessaire de faire coexister les compétences expertes de graphistes utilisateurices d'Adobe InDesign et de développeureuses web, dans l'idée de produire une publication multiformat accessible quel que soit le contexte de lecture. 

À terme, une interface web viendra faciliter l'utilisation de ce programme. Cette interface s'appellera **OutDesign**.

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

D'autres se sont penché·es sur la question de la lecture de fichiers IDML, en particulier le projet [`idml2xml-frontend`](https://github.com/transpect/idml2xml-frontend), distribué sous licence FreeBSD. Nous construisons notre convertisseur en continuant ce travail, en proposant un [_binding_](https://fr.wikipedia.org/wiki/Binding) entre `idml2xml-frontend` et Pandoc, c'est-à-dire en convertissant la sortie HubXML de `idml2xml-frontend` vers le format DocBook 5.1.

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

A minima, pour fonctionner, ce convertisseur nécessite d'exécuter `idml2xml-frontend`. La ligne `IDML2HUBXML_SCRIPT_FOLDER` du fichier `.env` correspond donc au chemin absolu menant au dossier `idml2xml-frontend` présent sur votre machine. Seule cette entrée est **obligatoire** pour le fonctionnement de `idml2docbook`.

Les autres valeurs du fichier `.env` permettent de remplacer les valeurs par défaut du package `idml2docbook`. Pour plus d'informations sur ces différentes variables, consultez l'aide du package avec l'option `-h`/`--help` :

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

### Préparation des fichiers IDML

Un [guide de formatage](https://gitlab.com/deborderbollore/idml-pandoc-reader/-/blob/main/FORMATING_GUIDE.md) indique comment préparer les fichiers InDesign. Même s'il n'est pas obligatoire de suivre ces recommandations pour utiliser le convertisseur, la qualité du résultat obtenu peut varier grandement selon la manière dont vous avez conçu votre document.

### Correspondance des styles

Une fois la [version modifiée de Pandoc](https://github.com/yanntrividic/pandoc/) installée, Pandoc sera en mesure d'interpréter les attributs `role` des éléments des fichiers DocBook obtenus après conversion. Ces rôles sont ensuite considérés comme des classes par Pandoc grâce au filtre `roles-to-classes.lua`.

Les attributs `role` correspondent aux styles de paragraphes et de caractères précisés dans InDesign. Comme illustré dans le fichier `map.json.sample`, il est possible d'associer ces styles de paragraphes et de caractères à des traitements particuliers :

* `role` : remplace le rôle du fichier source par une ou plusieurs classes ;
* `type` : change le type d'élément (par défaut, `para` pour tous les éléments) vers un nouveau type ;
* `level` : si `type` est un titre DocBook (`title`), `level` spécifie le niveau du titre ;
* `delete` : supprime les éléments avec cet attribut `role` ;
* `unwrap` : déplie le contenu de ces éléments dans l'élément parent ;
* `cut` : crée un nouveau fichier avant chaque élément ayant ce `role` ;
* `empty` : conserve les éléments vides portant ce `role` (tous les autres éléments vides sont supprimés, sauf si l'option `-e`/`--empty` est active).

Le script `idml2docbook/map.py` aide à constituer ces fichiers JSON. Ce script prend un fichier sorti de `idml2xml-frontend` et un fichier JSON de correspondance, et détaille la correspondance de styles qui va être appliquée via par exemple la commande suivante :

```bash
python idml2docbook/map.py file.xml maps/db.json
```

### Commandes de base

Il est possible d'utiliser ce convertisseur de diverses manières :

1. Avec le package `idml2docbook`, puis en exécutant Pandoc sur le résultat produit ;
1. Avec le lecteur Lua `idml.lua` ;
1. Avec le script `batch.sh`.

#### `idml2docbook`

Ce package Python est la contribution principale de ce dépôt. Il offre une API permettant de convertir un fichier fichier IDML en un ou plusieurs fichiers DocBook.

Convertir un fichier IDML et l'enregistrer dans un fichier DocBook :

```bash
python -m idml2docbook hello_world.idml -o hello_world.xml
```

Il est aussi possible de directement envoyer le résultat de la conversion dans l'entrée standard de Pandoc :

```bash
pandoc -f docbook -t markdown <(python -m idml2docbook hello_world.idml)
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

Avant toute chose, il est nécessaire de spécifier la version de Pandoc à utiliser dans le fichier `.env`. Il est aussi nécessaire de donner les droits d'exécution à ce script :

```bash
chmod +x batch.sh
```

Ce petit script shell permet de faciliter la liaison entre Pandoc et `idml2docbook` lorsque ce dernier est utilisé avec l'option `-c`/`--cut` pour séparer le résultat de la conversion en plusieurs fichiers (ou chapitres).

Cette commande prend deux dossiers en arguments : un dossier d'entrée et un de sortie. Il est ainsi possible de chaîner les commandes, par exemple :

```bash
python -m idml2docbook file.idml --output docbook_folder --cut ; ./batch.sh docbook_folder md_folder
```

### Détail de la commande permettant de convertir le recueil _Déborder Bolloré_

La commande pour compiler les contributions du recueil _Déborder Bolloré_, dont on peut retrouver le résultat sur le dépôt [deborderbollore/articles](https://gitlab.com/deborderbollore/articles), est la suivante :

```bash
python -m idml2docbook db.idml \
  --output docbook \
  --map maps/db.json \
  --cut \
  --names \
  --raster jpg \
  --vector svg \
  --media-folder images ;
./batch.sh docbook articles
```

En détails :

* `-o`/`--output` : permet de préciser le dossier où seront contenus les fichiers DocBook produits ;
* `-m`/`--map` : spécifie les opérations à effectuer sur certains styles de caractères et de paragraphes, voir _Correspondance des styles_ ;
* `-c`/`--cut` : coupe le résultat en plusieurs fichiers DocBook autonomes ;
* `-n`/`--names` : génère les noms des fichiers finaux à partir des contenus des titres de niveau 1 ;
* `-r`/`--raster` : remplace les extensions des images matricielles par `jpg` dans les URL des fichiers de sortie ;
* `-v`/`--vector` : idem pour les images vectorielles ;
* `-f`/`--media-folder` : remplace l'URL absolue des médias dans les fichiers de sortie par `images/`.

D'autres paramétrages encore sont exposés via les options de ce package (voir l'aide avec `-h`/`--help`).

Enfin, le script `batch.sh` convertit les fichiers DocBook obtenus en Markdown, en précisant la saveur `markdown_phpextra`, et avec les filtres Lua nécessaires.
guide de le·a contributeurice

## Contribuer

Pour contribuer au développement de ce convertisseur, se référer au [guide de le·a contributeurice](https://gitlab.com/deborderbollore/idml-pandoc-reader/-/blob/main/CONTRIBUTING.md).

## Licence

<a href="https://gitlab.com/deborderbollore/idml-pandoc-reader">IDML Pandoc Reader</a> © 2025 par <a href="https://yanntrividic.fr">Yann Trividic</a> est distribué sous licence <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a><img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/sa.svg" style="max-width: 1em;max-height:1em;margin-left: .2em;">