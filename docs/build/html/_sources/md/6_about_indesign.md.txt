# À propos d'InDesign

Adobe InDesign fait partie de ce qu'on pourrait appeler un [jardin clos](https://en.wikipedia.org/w/index.php?title=Walled_garden_(technology)), soit une plateforme où le fournisseur contrôle les applications et les contenus, et dont l'accès et restraint. Cela pose problème dès lors que l'on ne souhaite pas tout faire dans leur écosystème.

Cela pose particulièrement problème lorsque l'on veut publier un document multiformat sous ses propres conditions, car extraire des contenus d'InDesign est une tâche ardue.

## Les différents formats d'export

Exporter des documents d'InDesign pourrait suffire à réemployer les contenus travaillés dans InDesign. Seulement, ces exports ne sont pas faits pour être réemployés, et chacun présente ses inconvénients.

### PDF

Pour exporter un facsimile de votre espace de travail InDesign, InDesign est sans conteste le meilleur candidat. Seulement, produire un PDF accessible peut s'avérer assez énergivore, et certains outils comme [WeasyPrint](https://weasyprint.org) ou [Paged.js](https://pagedjs.org).

### HTML (hérité)

### EPUB 

## Le format IDML

IDML est le format "ouvert"[^cookbook] d'Adobe InDesign, le format de retrocompabilité d'InDesign (c'est-à-dire le format que toutes les versions d'InDesign peuvent lire), a contrario du format INDD qui est spécifique à chaque version. IDML est aussi le format que l'on peut lire et interpréter sans avoir besoin de lancer InDesign, car un fichier IDML est en fait une sorte d'[archive zippée](https://fr.wikipedia.org/wiki/ZIP_(format_de_fichier)) d'une arborescence de fichiers [XML](https://fr.wikipedia.org/wiki/Extensible_Markup_Language).

[^cookbook]: La spécification du format IDML n'est plus maintenue (publiquement du moins) depuis 2012. Elle est contenue dans la documentation du _InDesign SDK_ sous le nom de _InDesign Markup Language (IDML) Cookbook_, et il faut un compte Adobe pour pouvoir la [télécharger](https://developer.adobe.com/console/servicesandapis).

Même si ce format est théoriquement ouvert, il reste assez complexe, et le ramener à un format plus simple, plus largement utilisé et supporté, nécessite de nombreuses opérations, d'où la nécessité de ce convertisseur.

Par-delà cette complexité, le fait qu'InDesign soit un logiciel WYSIWYG[^wysiwyg] où l'on peut faire du formatage direct[^direct] rend extrêmement complexe la conversion vers des formats plus "structurés".

[^wysiwyg]: *What you see is what you get.*

[^direct]: Le formatage direct est le formatage appliqué sans structure, par exemple en identifiant un titre uniquement en gras avec un corps de texte important, ou placer un bloc dans la page (comme une image) sans l'ancrer dans le flux du texte.

Pour ces différentes raisons, **ce convertisseur fonctionne mieux lorsque certaines bonnes pratiques de formatage sont appliquées.** De manière générale, la plupart de ces recommandations sont aussi émises par Adobe pour structurer un fichier InDesign.


