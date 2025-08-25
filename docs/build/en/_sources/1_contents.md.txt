# Contenus du dépôt

Ce projet adopte pour l'instant une structure "monodépôt", c'est-à-dire que plusieurs sous-projets sont contenus dans ce dépôt, qui sera sûrement découpé à termes en plusieurs dépôts distincts. Les fichiers et dossiers les plus importants du dépôt sont :

* `.design` est un dossier appliquant la structure du projet [contribute.design](https://contribute.design) et qui rassemble le travail de design d'interface qui aboutira à termes sur OutDesign ;
* `docs` contient le code source de la présente documentation ;
* `idml2docbook` est un package Python permettant de faire le pont entre les formats IDML et DocBook, ce dernier pouvant être lu par Pandoc ;
* `lua-filters` contient une série de filtres Lua permettant de manipuler la structure des fichiers fournis en entrée à Pandoc, indépendemment de leur format ;
* `maps` contient des fichiers JSON exemples montrant comment paramétrer la conversion en fonction des spécificités de chaque document, voir [Correspondance des styles](https://outdesign.deborderbollore.fr/fr/3_usage.html#correspondance-des-styles) ;
* `.env.sample` est un fichier de configuration permettant de donner des valeurs par défaut au convertisseur ;
* `idml.lua` est un lecteur de fichiers personnalisés pour Pandoc pour faire le lien avec `idml2docbook`, voir [Commandes de base](https://outdesign.deborderbollore.fr/fr/3_usage.html#commandes-de-base) ;
* `install.sh` est le script d'installation du projet.