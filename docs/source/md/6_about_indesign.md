# À propos d'InDesign

Adobe InDesign est un [jardin clos](https://en.wikipedia.org/w/index.php?title=Walled_garden_(technology)), soit une plateforme où le fournisseur contrôle les applications et les contenus, et dont l'accès et restraint. Cela pose problème dès lors que l'on ne souhaite pas tout faire dans leur écosystème.

Cela pose _particulièrement_ problème lorsque l'on veut publier un document multiformat sous des modalités choisies, car extraire des contenus d'InDesign est une tâche ardue.

## Les différents formats d'export

Exporter des documents d'InDesign pourrait suffire à réemployer les contenus travaillés dans InDesign. Seulement, ces exports ne sont pas faits pour être réemployés, et chacun présente ses inconvénients.

### PDF

Pour exporter un facsimilé de votre espace de travail, InDesign est sans conteste le meilleur candidat. Seulement, produire un PDF accessible peut s'avérer assez chronophage, et certains outils comme [WeasyPrint](https://weasyprint.org) ou [Paged.js](https://pagedjs.org) peuvent produire des documents accessibles d'une meilleure qualité et à moindre effort.

### HTML (hérité)

Pour réemployer vos contenus éditorialisés dans InDesign pour la conception d'un site web, l'export HTML (hérité) peut représenter un bon point d'entrée. Seulement, InDesign supprime certaines informations (les espaces de fin et de début de ligne, les sauts de ligne, etc.). Cela peut résulter en des problèmes totalement insolubles, étant donné qu'il n'existe aucun levier d'action pour personnaliser cette conversion de format.

### EPUB

Générer un livre numérique depuis InDesign est possible, mais cela nécessite de nombreuses opérations, et produit en sortie un fichier [difficile à dénoyauter](https://mastodon.ar.al/@aral/113760088265003444).

Dans le cadre du recueil _Déborder Bolloré_, les fichiers Markdown sortis du présent convertisseur ont nourri le [Gabarit Abrüpt](https://codeberg.org/abrupt/gabarit-abrupt/). Cela a permis de produire un EPUB léger et de qualité, dont le code est disponible sur le dépôt [deborderbollore/ebook](https://gitlab.com/deborderbollore/ebook).

## Le format IDML

IDML est le format "ouvert"[^cookbook] d'Adobe InDesign, son format de retrocompabilité (c'est-à-dire le format que la plupart des versions d'InDesign peuvent lire), _a contrario_ du format INDD qui est spécifique à chaque version. Par défaut, l'assemblage d'un projet InDesign génère un fichier IDML, ce qui fait que de nombreux projets, même anciens, existent sous la forme d'un fichier IDML. IDML est aussi le format que l'on peut lire et interpréter sans avoir besoin de lancer InDesign, car un fichier IDML est en fait une sorte d'[archive zippée](https://fr.wikipedia.org/wiki/ZIP_(format_de_fichier)) d'une arborescence de fichiers [XML](https://fr.wikipedia.org/wiki/Extensible_Markup_Language).

[^cookbook]: La spécification du format IDML n'est plus maintenue (publiquement du moins) depuis 2012. Elle est contenue dans la documentation du _InDesign SDK_ sous le nom de _InDesign Markup Language (IDML) Cookbook_. Il faut un compte Adobe pour pouvoir la [télécharger](https://developer.adobe.com/console/servicesandapis).

Même si ce format est théoriquement ouvert, il reste assez complexe, et le ramener à un format plus simple, plus largement utilisé et supporté, nécessite de nombreuses opérations, d'où la nécessité de ce convertisseur.

Par-delà cette complexité, le fait qu'InDesign soit un logiciel WYSIWYG[^wysiwyg] où l'on peut faire du formatage direct[^direct] rend extrêmement complexe la conversion vers des formats plus "structurés".

[^wysiwyg]: *What you see is what you get.*

[^direct]: Le formatage direct est le formatage appliqué sans structure, par exemple en identifiant un titre uniquement en gras avec un corps de texte important, ou placer un bloc dans la page (comme une image) sans l'ancrer dans le flux du texte.

Pour ces différentes raisons, **ce convertisseur fonctionne mieux lorsque certaines bonnes pratiques de formatage sont appliquées** (voir le [guide de formatage](/md/4_formatting_guide)). De manière générale, la plupart de ces recommandations sont aussi émises par Adobe pour structurer un fichier InDesign.


