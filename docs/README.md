# Documentation

Cette documentation est compilée avec [Sphinx](https://www.sphinx-doc.org) et déployée sur [outdesign.deborderbollore.fr](https://outdesign.deborderbollore.fr).

Pour installer les dépendances nécessaires pour compiler cette documentation, rendez-vous dans ce répertoire et exécutez la commande suivante :

```bash
pip install -r requirements.txt
```

Pour compiler la documentation :

```bash
make all
```

Pour mettre à jour les fichiers d'internationalisation (pour traduire la documentation vers l'anglais) :

```bash
make gettext ; sphinx-intl update -p build/gettext -l en
```

La customisation de cette documentation Sphinx est librement inspirée de celle de [Club1](https://club1.fr/docs/).