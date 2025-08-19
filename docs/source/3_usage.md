# Usage

## Préparation des fichiers IDML

Un [guide de formatage](/4_formatting_guide) indique comment préparer les fichiers InDesign. Même s'il n'est pas obligatoire de suivre ces recommandations pour utiliser le convertisseur, la qualité du résultat obtenu peut varier grandement selon la manière dont vous avez conçu votre document.

## Correspondance des styles

Une fois la [version modifiée de Pandoc](https://github.com/yanntrividic/pandoc/) installée, Pandoc sera en mesure d'interpréter les attributs `role` des éléments des fichiers DocBook obtenus après conversion. Ces rôles sont ensuite considérés comme des classes par Pandoc grâce au filtre `roles-to-classes.lua`.

Les attributs `role` correspondent aux styles de paragraphes et de caractères précisés dans InDesign. Comme illustré dans le fichier `maps/sample.json`, il est possible d'associer ces styles de paragraphes et de caractères à des traitements particuliers :

* `classes` : remplace le style de paragraphe ou de caractère source par une ou plusieurs classes ;
* `type` : change le type d'élément (par défaut, tous les éléments sont des `Para` ou des `Span`) vers [un nouveau type](https://pandoc.org/lua-filters.html#type-pandoc) (un titre, une emphase, une citation...) ;
* `level` : si `type` est un titre (élément `Header`), `level` spécifie le niveau du titre ;
* `delete` : supprime les éléments avec ce style de paragraphe ou de caractère ;
* `simplify` : enlève tous les attributs et classes des éléments avec ce style de paragraphe ou de caractère ;
* `wrap` : enveloppe l'élément dans un autre ;
* `unwrap` : déplie le contenu de ces éléments dans l'élément parent ;
* `br` : ajoute un saut de ligne avant l'élément concerné ;
* `cut` : crée un nouveau fichier avant chaque élément ayant le style de paragraphe sélectionné ;
* `empty` : conserve les éléments vides portant ce style de paragraphe (tous les autres éléments vides sont supprimés par défaut) ;

Le script `idml2docbook/map.py` aide à constituer ces fichiers JSON. Ce script prend un fichier sorti de `idml2xml-frontend` et un fichier JSON de correspondance, et détaille la correspondance de styles qui va être appliquée via par exemple la commande suivante :

```bash
python idml2docbook/map.py file.xml maps/sample.json
```

## Commandes de base

Il est possible d'utiliser ce convertisseur de diverses manières :

1. Avec le package `idml2docbook`, puis en exécutant Pandoc sur le résultat produit ;
1. Avec le lecteur Lua `idml.lua` ;
1. Avec le script `batch.sh`.

### idml2docbook

Ce package Python est la contribution principale de ce dépôt. Il offre une API permettant de convertir un fichier fichier IDML en un ou plusieurs fichiers DocBook.

Convertir un fichier IDML et l'enregistrer dans un fichier DocBook :

```bash
python -m idml2docbook hello_world.idml -o hello_world.dbk
```

Il est aussi possible de directement envoyer le résultat de la conversion dans l'entrée standard de Pandoc :

```bash
pandoc -f docbook -t markdown <(python -m idml2docbook hello_world.idml)
```

Afficher l'aide à l'utilisation avec l'option `-h`/`--help` :

```bash
python -m idml2docbook -h 
```

### idml.lua

Ce fichier fait le pont entre Pandoc et `idml2docbook`. Il permet de prendre le résultat de ce dernier pour l'insérer dans Pandoc. [Pandoc ne permet pas de spécifier d'arguments arbitraires en ligne de commande](https://github.com/jgm/pandoc/discussions/9689), ce qui implique que seul modifier le fichier `.env` peut influencer le comportement de `idml2docbook` quand exécuté au travers de `idml.lua`.

Convertir un fichier IDML vers Markdown, avec par exemple le filtre `roles-to-classes.lua` :

```bash
pandoc -f idml.lua -t markdown --lua-filter=lua-filters/roles-to-classes.lua hello_world.idml
```

Spécifier un fichier JSON de correspondance et l'utiliser pour personnaliser votre commande de conversion avec le filtre `map.lua` : 

```bash
pandoc -f idml.lua -t markdown --lua-filter=lua-filters/map.lua -M map=maps/sample.json hello_world.idml
```

Découper un fichier d'entrée en plusieurs fichiers de sortie ayant pour nom de base `output` avec le filtre `cut.lua` :

```bash
pandoc -f idml.lua -t markdown --lua-filter=lua-filters/cut.lua -M map=maps/sample.json hello_world.idml -o output
```

### Temps de calcul de idml2xml-frontend

Le convertisseur `idml2xml-frontend` est l'étape du processus qui prend de loin le plus de temps de calcul. Celle-ci n'ayant pas besoin d'être personnalisée, il n'est généralement nécessaire de l'exécuter qu'une seule fois par fichier IDML. Le résultat obtenu en exécutant `idml2xml-frontend` sur un fichier `hello_world.idml` est sauvegardé dans le dossier `idml2hubxml`. 

L'option `-x`/`--idml2hubxml-file` permet de spécifier un fichier intermédiaire tel que `idml2hubxml/hello_world.xml` en tant que fichier d'entrée de la conversion. Afin de significativement gagner du temps de calcul, il est ainsi possible de reprendre la conversion à partir de ce résultat intermédiaire :

```bash
python -m idml2docbook -x idml2hubxml/hello_world.xml -o hello_world.dbk
```

## Liste des options de idml2docbook

Toutes les options détaillées ici sont aussi documentées dans le logiciel en ligne de commande (voir l'aide avec `-h`/`--help`).

* **`-x`, `--idml2hubxml-file`** \
  Considère le fichier en entrée comme un fichier Hub XML. \
  Utile pour gagner du temps de traitement si `idml2xml-frontend` a déjà été exécuté sur le fichier IDML source. 

* **`-o`, `--output <fichier>`** \
  Nom à attribuer au fichier de sortie. \
  Par défaut, la sortie est redirigée vers la sortie standard (*stdout*). 

* **`-t`, `--typography`** \
  Refonte de l’orthotypographie selon les règles françaises \
  (espaces fines, espaces insécables, etc.). 

* **`-l`, `--thin-spaces`** \
  N’utiliser que des espaces fines pour la refonte de l’orthotypographie. \
  À utiliser conjointement avec `--typography`. 

* **`-b`, `--linebreaks`** \
  Ne pas remplacer les balises `<br>` par des espaces. 

* **`-p`, `--prettify`** \
  Embellir la sortie DocBook. \
  ⚠️ Peut ajouter des espaces indésirables dans la sortie. 

* **`-f`, `--media <chemin>`** \
  Chemin vers le dossier contenant les fichiers médias. \
  Par défaut : `Links`. 

* **`-r`, `--raster <extension>`** \
  Extension à utiliser pour remplacer celles des images *matricielles*. \
  Exemple : `jpg`. \
  Par défaut : aucune. 

* **`-v`, `--vector <extension>`** \
  Extension à utiliser pour remplacer celles des images *vectorielles*. \
  Exemple : `svg`. \
  Par défaut : aucune. 

* **`-i`, `--idml2hubxml-output <chemin>`** \
  Chemin vers la sortie du convertisseur `idml2hubxml` de Transpect. \
  Par défaut : `idml2hubxml`. 

* **`-s`, `--idml2hubxml-script <chemin>`** \
  Chemin vers le script du convertisseur `idml2xml-frontend` de Transpect. \
  Par défaut : `idml2xml-frontend`. 

* **`--env <fichier>`** \
  Chemin vers un fichier d’environnement `.env` pour `idml2docbook`. \
  Par défaut, cherche un fichier `.env` dans le répertoire courant. \
  Toutes les paires clé/valeur spécifiées dans ce fichier `.env` remplacent les valeurs par défaut du programme. 

* **`--version`** \
  Affiche la version de `idml2docbook` et quitte le programme. 

## Exemple avec la commande de conversion du recueil _Déborder Bolloré_

La commande pour compiler les contributions du recueil _Déborder Bolloré_, dont on peut retrouver le résultat sur le dépôt [deborderbollore/articles](https://gitlab.com/deborderbollore/articles), est la suivante :

```bash
pandoc -f docbook \
       -t markdown_phpextra \
       --wrap=none \
       --lua-filter=lua-filters/roles-to-classes.lua \
       --lua-filter=lua-filters/map.lua \
       --lua-filter=lua-filters/cut.lua \
       -M map=maps/db.json \
       -o output/db.md \
       <(python -m idml2docbook db.idml \
                --typography \
                --thin-spaces \
                --raster jpg \
                --vector svg \
                --media images)
```

En détails, les options pour Pandoc :

* `-o`/`--output` : permet de préciser le dossier où seront contenus les fichiers DocBook produits ;
* `-m`/`--map` : spécifie les opérations à effectuer sur certains styles de caractères et de paragraphes, voir [Correspondance des styles](#correspondance-des-styles) ;

Et celles pour `idml2docbook` :

* `-t`/`--typography` : refait totalement l'orthotypographie (espaces autour des signes de ponctuation, etc.) ;
* `-l`/`--thin-spaces` : l'orthotypographie utilise seulement des espaces fines ;
* `-r`/`--raster` : remplace les extensions des images matricielles par `jpg` dans les URL des fichiers de sortie ;
* `-v`/`--vector` : idem pour les images vectorielles ;
* `-f`/`--media-folder` : remplace l'URL absolue des médias dans les fichiers de sortie par `images/`.