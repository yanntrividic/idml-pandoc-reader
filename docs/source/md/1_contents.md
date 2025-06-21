# Contenus du dépôt

Les fichiers et dossiers les plus importants du dépôt sont :

* `idml2docbook` est un package Python permettant de faire le pont entre les formats IDML et DocBook, ce dernier pouvant être lu par Pandoc ;
* `lua-filters` contient des filtres Lua permettant de modifier le comportement du lecteur DocBook afin de mieux correspondre aux attendus de la conversion de fichiers IDML ;
* `maps` contient des fichiers JSON exemples montrant comment paramétrer la conversion en fonction des spécificités de chaque document, voir [Correspondance des styles](https://outdesign.deborderbollore.fr/fr/3_usage.html#correspondance-des-styles) ;
* `.env.sample` est un fichier de configuration permettant de donner des valeurs par défaut au convertisseur ;
* `batch.sh` est le script utilisé pour faciliter la conversion de fichiers en lots via Pandoc des fichiers source du recueil _Déborder Bolloré_ ;
* `idml.lua` fait le lien entre `idml2docbook` et Pandoc, voir [Commandes de base](https://outdesign.deborderbollore.fr/fr/3_usage.html#commandes-de-base) ;
