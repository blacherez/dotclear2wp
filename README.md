Scripts pour transférer les billets d'un blog Dotclear vers un Wordpress

# Etapes à suivre

## Modules python nécessaires
- requests
- bs4
- html5lib


## Installation des composants nécessaires sur le WP
Extension Application passwords

### Creating a New Application Password
Go the User Profile page of the user that you want to generate a new application password for. To do so, click Users on the left side of the WordPress admin, then click on the user that you want to manage.

Scroll down until you see the Application Passwords section. This is typically at the bottom of the page.

Within the input field, type in a name for your new application password, then click Add New.

Note: The application password name is only used to describe your password for easy management later. It will not affect your password in any way. Be descriptive, as it will lead to easier management if you ever need to change it later.

Once the Add New button is clicked, your new application password will appear. Be sure to keep this somewhere safe, as it will not be displayed to you again. If you lose this password, it cannot be obtained again.

Modifier le fichier .htaccess selon indications https://github.com/georgestephanis/application-passwords/wiki/Basic-Authorization-Header----Missing

Soit :

```apacheconf
# BEGIN WordPress
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule .* - [E=REMOTE_USER:%{HTTP:Authorization}]
RewriteBase /maison/
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /maison/index.php [L]
</IfModule>

# END WordPress
```

## Récupération des catégories
Script cree_categories_sql.py

## Récupération des billets
Script ecriveur_sql.py

Ce script récupère les billets de l'ancien blog dans le fichier SQL de dump de la base de données du Dotclear (la version CSV ne fonctionne pas) et les crée dans le blog Wordpress, en modifiant à la volée les chemins des images.

Les images sont copiées localement, d'où l'étape suivante.

## Copie du répertoire des images à l'emplacement correct sur le serveur du WP
