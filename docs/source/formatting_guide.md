# Guide de formatage

## En guise d'introduction : à propos du format IDML

IDML est le format "ouvert"[^cookbook] d'Adobe InDesign, le format de retrocompabilité d'InDesign (c'est-à-dire le format que toutes les versions d'InDesign peuvent lire), a contrario du format INDD qui est spécifique à chaque version. IDML est aussi le format que l'on peut lire et interpréter sans avoir besoin de lancer InDesign, car un fichier IDML est en fait une sorte d'[archive zippée](https://fr.wikipedia.org/wiki/ZIP_(format_de_fichier)) d'une arborescence de fichiers [XML](https://fr.wikipedia.org/wiki/Extensible_Markup_Language).

[^cookbook]: La spécification du format IDML n'est plus maintenue (publiquement du moins) depuis 2012. Elle est contenue dans la documentation du _InDesign SDK_ sous le nom de _InDesign Markup Language (IDML) Cookbook_, et il faut un compte Adobe pour pouvoir la [télécharger](https://developer.adobe.com/console/servicesandapis).

Même si ce format est théoriquement ouvert, il reste assez complexe, et le ramener à un format plus simple, plus largement utilisé et supporté, nécessite de nombreuses opérations, d'où la nécessité de ce convertisseur.

Par-delà cette complexité, le fait qu'InDesign soit un logiciel WYSIWYG[^wysiwyg] où l'on peut faire du formatage direct[^direct] rend extrêmement complexe la conversion vers des formats plus "structurés".

[^wysiwyg]: *What you see is what you get.*

[^direct]: Le formatage direct est le formatage appliqué sans structure, par exemple en identifiant un titre uniquement en gras avec un corps de texte important, ou placer un bloc dans la page (comme une image) sans l'ancrer dans le flux du texte.

Pour ces différentes raisons, **ce convertisseur fonctionne mieux lorsque certaines bonnes pratiques de formatage sont appliquées.** De manière générale, la plupart de ces recommandations sont aussi émises par Adobe pour structurer un fichier InDesign.

## Recommandations

Cette liste est non exhaustive, et sera complétée au fur et à mesure que des cas singuliers apparaîtront.

### Éviter les surcharges de style

En l'état, le convertisseur ignore les surcharges de styles (lorsque un élément a un style de paragraphe avec un `+`). Il existe des manières de [facilement enlever ces surcharges](https://www.rockymountaintraining.com/adobe-indesign-quickly-recognizing-and-removing-overrides/).

### Une unité sémantique = un style de paragraphe ou de caractère

InDesign permet une certaine forme de sémantisation via les styles de paragraphes et les styles de caractères. Dans InDesign, les notions que l'on retrouve habituellement dans les langages de balisages (titres, citations, emphases, etc.) n'existent pas. Il faut donc préciser ce à quoi chaque style de paragraphe et de caractère correspond sémantiquement.

Les fichiers JSON chargés dans le convertisseur permettent de faire correspondre les styles de paragraphes et de caractères à des types d'éléments, mais il faut pour cela que chaque unité stylistique puisse être associée à une unité sémantique. En d'autres termes, que chaque style puisse être associé à un type d'élément en sortie.

### Chaînage des contenus

Pour assurer que les contenus apparaîssent dans le bon ordre dans dans le résultat de la conversion, le mieux est de correctement chaîner les blocs entre eux, et d'ancrer les images dans les blocs.

### Nommage des fichiers et des styles

Pour éviter tout problème, mieux vaut utiliser seulement des caractères alphadécimaux non-accentués dans vos noms de fichiers et noms de styles, par exemple :

❌ `Mon super-étonnant fichier InDesign.indd` \
✔️ `Mon_super_etonnant_fichier_InDesign.indd`

### Notes de bas de page, listes, textes alternatifs

Le convertisseur supporte entre autres les notes de bas de page, les listes et les textes alternatifs. Cependant, pour que cela soit bien reconnu, il faut en premier lieu les formater correctement dans InDesign.

### Hyperliens

Dans le cas d'un PDF pour l'impression, il est souvent nécessaire de faire figurer l'URL au complet. Si l'URL est correctement renseignée dans InDesign (c'est-à-dire, en spécifiant que l'URL et son texte de remplacement sont les mêmes), alors cela fonctionnera sans problème.

Cependant, cette tâche peut-être laborieuse. Pour permettre de plus simplement travailler les URL (par exemple dans des paragraphes en drapeaux), nous reconstituons automatiquement les URL contenant des sauts de ligne à condition que celle-ci commence par `http://` ou `https://`. Par exemple :

```
https://www.example
.org
```

Sera converti en [https://www.example.org](https://www.example.org), mais pas `https://www.example .org` si le `https://` n'était pas présent.

### Retour à la ligne et saut de paragraphe

Les retours à la ligne sont automatiquement convertis en caractères espace ` `.

Les sauts de paragraphes, soit deux blocs séparés par **un bloc vide**, sont supprimés, sauf si l'option `--empty` est active, ou que le bloc porte un style de parapraphe portant l'attribut `empty` dans le fichier JSON de correspondance. Voir [Correspondance des styles](https://outdesign.deborderbollore.fr/usage.html#correspondance_des_styles).

## Limitations

Les tabulations sont actuellement ignorées par le convertisseur.