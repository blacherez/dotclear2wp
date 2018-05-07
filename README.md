Scripts pour transférer les billets d'un blog Dotclear vers un Wordpress

# Etapes à suivre

## Installation des composants nécessaires sur le WP

## Récupération des catégories
Script cree_categories_sql.py

## Récupération des billets
Script ecriveur_sql.py

Ce script récupère les billets de l'ancien blog dans le fichier SQL de dump de la base de données du Dotclear (la version CSV ne fonctionne pas) et les crée dans le blog Wordpress, en modifiant à la volée les chemins des images.

Les images sont copiées localement, d'où l'étape suivante.

## Copie du répertoire des images à l'emplacement correct sur le serveur du WP
