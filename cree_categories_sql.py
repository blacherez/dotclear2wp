# -*- coding: utf-8 -*-
"""
Crée les catégories qui n'existent pas encore dans le nouveau blog et enregistre un fichier json des correspondances d'id
On utilise un fichier SQL pour les catégories de l'ancien blog et on utilise les fonctions du module cree_categories.py
"""
import re
import cree_categories as cc
FILE = "data/categories.sql"
CATEGORY_FILE = "data/categories.json"

BLOG_ID = "blog" # ID du blog qu'on veut transférer

MOTIF_LIGNE = re.compile(r"(?P<cat_id>\d+), '(?P<blog_id>([^']*(\\'|'')?)*)', '(?P<cat_title>([^']*(\\'|'')?)*)', '(?P<cat_url>([^']*(\\'|'')?)*)', '?(?P<cat_desc>([^']*(\\'|'')?)*)'?, (?P<cat_position>\d+), (?P<cat_lft>\d+), (?P<cat_rgt>\d+)")

def parse_sql(line):
    valeurs = {}
    print(line[:12])
    r = MOTIF_LIGNE.search(line)
    if r:
        valeurs["old_id"] = r.group("cat_id")
        valeurs["name"] = r.group("cat_title")
        valeurs["slug"] = r.group("cat_url")
        valeurs["description"] = r.group("cat_desc")
        valeurs["blog_id"] = r.group("blog_id")
        return valeurs
    return None

if __name__ == "__main__":
    # On récupère les catégories sur le site pour éviter de les créer en doublon
    c = cc.get_remote_cats()
    if c:
        new_cats = c
    else:
        sys.exit(3)

    with open(FILE) as f:
        lines = f.readlines()

    for line in lines:
        valeurs = parse_sql(line)
        if valeurs:
            print(valeurs["name"])
            new_cats = cc.process(valeurs, new_cats, BLOG_ID)


    cc.save2json(new_cats, CATEGORY_FILE)
