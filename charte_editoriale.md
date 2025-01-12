# Charte éditoriale : Préparer un fichier InDesign en vue de l'utilisation de ce convertisseur

Pour que la lecture du fichier se fasse correctement, il faut que celui-ci soit bien structuré. La qualité de cette structuration peut énormément varier selon les habitudes de travail de le·a graphiste qui a réalisé le fichier INDD.

Dans notre cas de figure, principalement des bonnes pratiques.

## Nommage des fichiers et des styles

Les fichiers (INDD, HTML et images), ainsi que les styles de paragraphes et de caractères :

Idéalement, que des caractères alphadécimaux non-accentués :

Par exemple :

❌ `Mon super-étonnant fichier InDesign.indd`
✔️ `Mon_super_etonnant_fichier_InDesign.indd`

## Styles de paragraphes, styles de caractères

À chaque unité sémantique son style.

### Éviter au maximum le formattage direct

Ça crée des éléments "Override", qui font qu'on perd où on en est et que le traitement doit ensuite est refait "à la main". Il n'y a pas vraiment de solution pour contourner ça.

### Correspondance des styles et fichier map.py

#### Faire correspondre un style InDesign à une classe CSS

```python
"nomdustyle": { "name": "i", "classes": ["rouge"] }
```

#### Supprimer tous les éléments ayant un certain style

```python
"delete": True
```

#### Supprimer un style en conservant les éléments qui y font référence

```python
"unwrap": True
```

## Blocs chaînés

Un bloc, une section, un fichier

### Ancrage des images

Une image non ancrée va casser le bloc chaîné ?

## Notes de bas de page

Les faire dans les règles de l'art, ou alors !
Faire un style de caractère pour les notes de bas de pages, un style de caractère pour l'appel de notes.
Avoir systématiquement le même contenu dans l'appel de note et dans la référence dans la note elle même.

## Espaces (début de ligne, fin de ligne, plusieurs à la suite)

Utiliser des espaces insécables

## Sauts de ligne forcés

Pas utiliser le caractère fin de paragraphe

## Gestion des drapeaux et des césures

Ne pas utiliser le retour chariot pour équilibrer les drapeaux. Plusieurs options : utiliser le tiret conditionnel pour forcer la césure dans un mot ; utiliser des styles de paragraphes pour modifier l'espace intermots et l'interlettrage.