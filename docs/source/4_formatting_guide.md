# Guide de formatage pour InDesign

Pour que la qualité de la conversion d'un fichier IDML soit au rendez-vous, il est nécessaire que ce denier soit formaté correctement. Autrement, la qualité de la conversion sera moindre, et cela entraînera nécessairement un travail supplémentaire à effectuer sur les fichiers produits. **Pour minimiser la quantité de travail suite à la conversion, il est recommandé de suivre quelques bonnes pratiques lorsque vous travaillez dans InDesign.**

## Recommandations

Cette liste est non exhaustive, et sera complétée au fur et à mesure que des cas singuliers apparaîtront.

### Appliquer des styles de paragraphe aux paragraphes, et des styles de caractère aux caractères

La principale limitation des fonctionnalités de [correspondance des styles](https://outdesign.deborderbollore.fr/en/3_usage.html#correspondance-des-styles) de ce convertisseur est qu'il est actuellement impossible de convertir un style de paragraphe (élément de bloc) en un style de caractère (élément en ligne), et vice-versa. Pour que la correspondance puisse s'effectuer, il est nécessaire que l'on trouve dans le document InDesign [un usage correct des styles de paragraphe et de caractère](https://helpx.adobe.com/fr/indesign/using/paragraph-character-styles.html).

### Éviter les remplacements de style

Les remplacements de style correspondent à des modifications ponctuelles apportées aux styles de paragraphe ou de caractère définis dans un document InDesign. Ils apparaissent sous la forme d’un signe `+` à côté du nom du style appliqué, et peuvent être facilement repérés à l’aide du ["Surligneur de remplacements de styles"](https://helpx.adobe.com/fr/indesign/using/paragraph-character-styles.html#style-overrides).

Le convertisseur est capable de détecter ces remplacements et de les traiter automatiquement. Par exemple, le premier remplacement appliqué au style `NormalParagraphStyle` sera nommé `NormalParagraphStyle-override-1`. Tous les paragraphes partageant les mêmes attributs recevront ce nom, tandis que les remplacements suivants seront désignés `NormalParagraphStyle-override-2`, et ainsi de suite.

Même si ces remplacements sont correctement identifiés et la [correspondance des styles](https://outdesign.deborderbollore.fr/fr/3_usage.html#correspondance-des-styles) peut être appliquée comme n’importe quel autre style, ils compliquent le travail de post-traitement après conversion. Il est donc conseillé de les éviter autant que possible, en "effaçant les remplacements" ou en "redéfinissant le style" directement dans InDesign.

### Une unité sémantique = un style de paragraphe ou de caractère

InDesign permet une certaine forme de sémantisation via les styles de paragraphe et les styles de caractère. Dans InDesign, les notions que l'on retrouve habituellement dans les langages de balisages (titres, citations, emphases, etc.) n'existent pas. Il faut donc préciser ce à quoi chaque style de paragraphe et de caractère correspond sémantiquement.

Les [fichiers JSON](https://outdesign.deborderbollore.fr/fr/3_usage.html#correspondance-des-styles) chargés dans le convertisseur permettent de faire correspondre les styles de paragraphe et de caractère à des types d'éléments, mais il faut pour cela que chaque unité stylistique puisse être associée à une unité sémantique. En d'autres termes, que chaque style soit uniquement associé à un seul type d'élément en sortie.

### Chaînage des contenus

Pour garantir que les contenus apparaissent dans le bon ordre lors de la conversion, il est recommandé de [chaîner les blocs](https://helpx.adobe.com/indesign/using/threading-text.html?x-product=Helpx%2F1.0.0&x-product-location=Search%3AForums%3Alink%2F3.7.2-dev.2) et d'[ancrer les images dans ces blocs](https://helpx.adobe.com/indesign/using/anchored-objects.html).

Le convertisseur lit chaque bloc jusqu’à la fin avant de passer au suivant. Il est donc possible de chaîner plusieurs blocs qui se suivent, par exemple un chaînage par section. En revanche, avec les gros ouvrages, mieux vaut éviter de chaîner l’ensemble du document : des chaînages trop longs peuvent ralentir InDesign.

### Nommage des fichiers et des styles

Pour éviter les problèmes, mieux vaut utiliser seulement des caractères alphadécimaux non-accentués dans vos noms de fichiers IDML, d'images (les liens cassant facilement), et de noms de styles, un exemple :

❌ `Mon super-étonnant fichier InDesign d'la mort.idml` \
✔️ `Mon_super_etonnant_fichier_InDesign_dla_mort.idml`

### Ne pas incorporer les images

InDesign permet de gérer les images de deux manières : soit en les liant avec un fichier externe (pour ensuite faire un assemblage), soit en les incorporant. Incorporer les images augmente considérablement la taille du fichier IDML, et en l'état, ce mode de gestion des images n'est pas supporté par le convertisseur. Il est possible d'[annuler l'incorporation d'un fichier lié](https://helpx.adobe.com/fr/indesign/using/graphics-links.html) pour rendre un fichier IDML convertissable.

### Notes, listes, textes alternatifs

Le convertisseur supporte entre autres les notes de bas de page, les notes de fin, les listes et les textes alternatifs pour les images. Cependant, pour que cela soit bien reconnu, il faut en premier lieu les formater correctement dans InDesign.

### Hyperliens

Dans le cas d'un PDF pour l'impression, il est souvent nécessaire de faire figurer l'URL au complet. Si l'URL est correctement renseignée dans InDesign (c'est-à-dire, en spécifiant que l'URL et son texte de remplacement sont les mêmes), alors cela fonctionnera sans problème.

Cependant, cette tâche peut-être laborieuse. Pour permettre de plus simplement travailler les URL (par exemple dans des paragraphes en drapeaux), nous reconstituons automatiquement les URL contenant des sauts de ligne à condition que celle-ci commence par `http://` ou `https://`. Par exemple :

```
https://www.example
.org
```

Sera converti en [https://www.example.org](https://www.example.org), mais pas `https://www.example .org`, ou si le lien ne commençait pas par `https://`.

### Retour à la ligne et saut de paragraphe

Les retours à la ligne sont automatiquement convertis en caractères espace ` `.

Les sauts de paragraphes, soit deux blocs séparés par **un bloc vide**, sont supprimés, sauf si l'option `--empty` est active, ou que le bloc porte un style de parapraphe portant l'attribut `empty` dans le fichier JSON de correspondance. Voir [Correspondance des styles](https://outdesign.deborderbollore.fr/fr/3_usage.html#correspondance-des-styles).

## Limitations

Les [tabulations](https://helpx.adobe.com/fr/indesign/using/tabs-indents.html) et les métadonnées du fichier IDML sont actuellement ignorées par le convertisseur.