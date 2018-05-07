# -*- coding: utf-8 -*-
"""
Fichier de config pour l'application. Le fichier config-sample.py doit être renommé en config.py
"""
AUTHOR = 1 # On ne peut pas publier des articles avec l'API pour un autre auteur que celui qui se connecte

CSVFILE = "data/30posts.csv"
#SQLFILE = "data/posts-cleaned.sql"
SQLFILE = "data/30posts.sql"

# Catégories
SQLCATEGORIES = "data/categories.sql"
JSON_CATEGORIES = "data/categories.json"

BLOG_ID = "blog" # Identifiant du blog à transférer

USER = 'ben' # Nom d'utilisateur sur le blog WP
PYTHONAPP = "" # Clé générée par l'extension Application Passwords
URL = "" # URL de la forme http://foo.com/wp-json/wp/v2
