# Installation

## Dépendances

Le format IDML est complexe, et il est difficile d'en extraire les informations. Dans l'idéal, ce dépôt consisterait en un seul fichier Haskell, comme [les autres lecteurs de Pandoc](https://github.com/jgm/pandoc/tree/main/src/Text/Pandoc/Readers). Cependant, cela prendrait un temps fou à développer.

D'autres se sont penché·es sur la question de la lecture de fichiers IDML, en particulier le projet [`idml2xml-frontend`](https://github.com/transpect/idml2xml-frontend), distribué sous licence FreeBSD. Nous construisons notre convertisseur en continuant ce travail, en proposant un [_binding_](https://fr.wikipedia.org/wiki/Binding) entre `idml2xml-frontend` et Pandoc, c'est-à-dire en convertissant la sortie Hub XML de `idml2xml-frontend` vers le format DocBook 5.1.

Les principales dépendances sont :

* Python 3.x ;
* Java 1.7+ ;
* les dépendances du package Python `idml2docbook` ;
* [`idml2xml-frontend`](https://github.com/transpect/idml2xml-frontend).

Pour comprendre l'utilité de chacune des dépendances, voir le [graphe de conversions](/5_conversion_graph).

## Installation avec install\.sh

Premièrement, commencez par télécharger [la dernière version publiée](https://gitlab.com/deborderbollore/idml-pandoc-reader/-/releases/permalink/latest) du logiciel et décompressez l'archive ZIP obtenue.

Ensuite, un script d'installation `install.sh` pour Mac et Linux a été développé afin de faciliter la prise en main de ce logiciel. L'installation sur Windows est elle aussi possible en adaptant les étapes détaillées ci-dessous, mais celle-ci pas pu être encore testée. Ce script a principalement pour fonctions de :

* vérifier que Java (>= 7.0.0) est installé ;
* vérifier que Git est installé ;
* installer `idml2xml-frontend` ;
* vérifier que Python 3 et pip (>= 21.0) sont installés ;
* installer les dépendances Python à partir de `requirements.txt` ;
* génèrer un simple fichier d'environnement `.env` ;
* installer éventuellement le module `idml2docbook` via `pip install .` ;
* exécuter une commande de test pour vérifier la validité de l'installation.

Pour exécuter ce script, commencez par lui donner les droits d'exécution :

```bash
chmod +x ./install.sh
```

Vous pouvez ensuite lancer l'installation :

```bash
./install.sh
```

> **Note :** Pour les fichiers IDML les plus lourds, il peut être nécessaire d'[augmenter la taille du tas Java](https://github.com/transpect/idml2xml-frontend/blob/master/idml2xml.sh#L33), par exemple à `2048m` ou `4096m`.

## Configuration de l'environnement .env

Le fichier `.env.sample` montre l'exemple d'un fichier de fichier de configuration.

A minima, pour fonctionner, ce convertisseur nécessite d'exécuter `idml2xml-frontend`. La ligne `IDML2HUBXML_SCRIPT_FOLDER` du fichier `.env` correspond donc au chemin absolu menant au dossier `idml2xml-frontend` présent sur votre machine. Il s'agit sûrement de la ligne la plus utile de votre fichier `.env`. Cette ligne est normalement renseignée automatiquement avec le script d'installation.

Les paires clé/valeur du fichier `.env` permettent de remplacer les valeurs par défaut du package `idml2docbook`. Pour plus d'informations sur ces différentes variables, consultez [la liste des options](https://outdesign.deborderbollore.fr/fr/3_usage.html#liste-des-options).

## Pandoc

Pandoc n'est pas une dépendance à proprement parler étant donné que le convertisseur `idml2docbook` n'en a pas besoin pour fonctionner.

Cependant, [une version un peu modifiée de Pandoc](https://github.com/yanntrividic/pandoc/) a été développée pour supporter la lecture des styles de paragraphes et de caractères. Pour l'utiliser, il faut [la compiler depuis la source](https://github.com/yanntrividic/pandoc/blob/main/INSTALL.md).

Il est aussi possible d'utiliser la version principale de Pandoc, mais alors sans [Correspondance des styles](https://outdesign.deborderbollore.fr/fr/3_usage.html#correspondance-des-styles). Une [_pull request_](https://github.com/jgm/pandoc/pull/10932) est en bonne voix d'intégrer ces nouvelles fonctionnalités dans la branche principale de Pandoc.


## Test de la configuration avec la version modifiée de Pandoc

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
