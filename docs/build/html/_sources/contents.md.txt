# Contenus du dépôt

Les fichiers et dossiers les plus importants du dépôt sont :

* `idml2docbook` est un package Python permettant de faire le pont entre les formats IDML et DocBook, ce dernier étant compris par Pandoc ;
* `lua-filters` contient des filtres Lua permettant de modifier le comportement du lecteur DocBook afin de mieux correspondre aux attendus de la conversion de fichiers IDML ;
* `maps` et `map.json.sample` contiennent des fichiers JSON exemples montrant comment paramétrer la conversion en fonction des spécificités de chaque livre, voir [Correspondance des styles](https://outdesign.deborderbollore.fr/usage.html/#correspondance_des_styles) ;
* `.env.sample` est un fichier de configuration permettant de donner des valeurs par défaut au convertisseur ;
* `batch.sh` est le script utilisé pour faciliter la conversion de fichiers en lots via Pandoc ;
* `idml.lua` fait le lien entre `idml2docbook` et Pandoc, voir [Commandes de base](https://outdesign.deborderbollore.fr/usage.html/#commandes_de_base) ;
