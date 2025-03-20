# Charte éditoriale : Préparer un fichier InDesign en vue de l'utilisation de ce convertisseur

## Pourquoi IDML et pas INDD

Pour que la lecture du fichier se fasse correctement, il faut que celui-ci soit bien structuré. La qualité de cette structuration peut énormément varier selon les habitudes de travail de le·a graphiste qui a réalisé le fichier INDD.

Dans notre cas de figure, principalement des bonnes pratiques d'utilisation d'InDesign

## Toujours utiliser des styles : éviter au maximum le formattage direct

En l'état, le logiciel ne supporte pas les surcharges de styles.

Ça crée des éléments "Override", qui font qu'on perd où on en est et que le traitement doit ensuite est refait "à la main". Il n'y a pas vraiment de solution pour contourner ça.

## Styles de paragraphes, styles de caractères : sémantiser correctement son document

À chaque unité sémantique son style.

Aller du plus général vers le plus spécifique.

## Nommage des fichiers et des styles

Les fichiers (IDML et images), ainsi que les styles de paragraphes et de caractères :

Idéalement, que des caractères alphadécimaux non-accentués :

Par exemple :

❌ `Mon super-étonnant fichier InDesign.indd`
✔️ `Mon_super_etonnant_fichier_InDesign.indd`

### Ancrage des images

Une image non ancrée va casser le bloc chaîné ?

## Notes de bas de page, listes

Les faire dans les règles de l'art

## Espaces (début de ligne, fin de ligne, plusieurs à la suite)

Utiliser des espaces insécables (à vérifier où ça en est)

## Sauts de ligne forcés

Pas utiliser le caractère fin de paragraphe, qui sont transformés en espaces simples

## Gestion des drapeaux et des césures

Ne pas utiliser le retour chariot pour équilibrer les drapeaux. Plusieurs options : utiliser le tiret conditionnel pour forcer la césure dans un mot ; utiliser des styles de paragraphes pour modifier l'espace intermots et l'interlettrage.