# Prérequis

Pour comprendre l'utilité de chacune des dépendances, voir le [graphe de conversions](/conversion_graph).

## Dépendances

Le format IDML est complexe, et il est difficile d'en extraire les informations. Dans l'idéal, ce dépôt consisterait en un seul fichier Haskell, comme [les autres lecteurs de Pandoc](https://github.com/jgm/pandoc/tree/main/src/Text/Pandoc/Readers). Cependant, cela prendrait un temps fou à développer.

D'autres se sont penché·es sur la question de la lecture de fichiers IDML, en particulier le projet [`idml2xml-frontend`](https://github.com/transpect/idml2xml-frontend), distribué sous licence FreeBSD. Nous construisons notre convertisseur en continuant ce travail, en proposant un [_binding_](https://fr.wikipedia.org/wiki/Binding) entre `idml2xml-frontend` et Pandoc, c'est-à-dire en convertissant la sortie HubXML de `idml2xml-frontend` vers le format DocBook 5.1.

Les dépendances sont :

* Python 3.x ;
* Java 1.7+ ;
* les dépendances du package Python (avec la commande `pip install -r requirements.txt`)
* [`idml2xml-frontend`](https://github.com/transpect/idml2xml-frontend) (s'installe avec `git` via la commande `git clone https://github.com/transpect/idml2xml-frontend --recurse-submodules`) ;
* avoir précisé dans un fichier `.env` le chemin vers `idml2xml-frontend` (voir l'exemple fourni avec `.env.sample`).

Pandoc n'est pas une dépendance à proprement parler étant donné que `idml2docbook` n'en a pas besoin. Cependant, [une version un peu modifiée de Pandoc](https://github.com/yanntrividic/pandoc/) a été développée pour supporter la lecture des styles de paragraphes et de caractères. Pour l'utiliser, il faut [la compiler depuis la source](https://github.com/yanntrividic/pandoc/blob/main/INSTALL.md). Il est aussi possible d'utiliser la version principale de Pandoc, mais alors sans [Correspondance des styles](https://outdesign.deborderbollore.fr/usage.html#correspondance-des-styles). Une [_pull request_](https://github.com/jgm/pandoc/pull/10665) est en cours pour intégrer ces nouvelles fonctionnalités dans la branche principale de Pandoc.

> **Note :** Pour les fichiers IDML les plus lourds, il peut être nécessaire d'[augmenter la taille du tas Java](https://github.com/transpect/idml2xml-frontend/blob/master/idml2xml.sh#L33), par exemple à `2048m` ou `4096m`.

## Configuration de l'environnement .env

Le fichier `.env.sample` montre l'exemple d'un fichier de fichier de configuration.

A minima, pour fonctionner, ce convertisseur nécessite d'exécuter `idml2xml-frontend`. La ligne `IDML2HUBXML_SCRIPT_FOLDER` du fichier `.env` correspond donc au chemin absolu menant au dossier `idml2xml-frontend` présent sur votre machine. Seule cette entrée est **obligatoire** pour le fonctionnement de `idml2docbook`.

Les autres valeurs du fichier `.env` permettent de remplacer les valeurs par défaut du package `idml2docbook`. Pour plus d'informations sur ces différentes variables, consultez l'aide du package avec l'option `-h`/`--help` :

```bash
python -m idml2docbook -h
```

## Test de la configuration

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
