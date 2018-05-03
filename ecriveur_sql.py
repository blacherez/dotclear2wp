# -*- coding: utf-8 -*-
"""
Crée les billets depuis un fichier SQL
"""
import ecriveur as e
import line_parser

import sys
import datetime

FILE = "data/30posts.sql"
BLOG_ID = "blog"

def parse_sql(line):
    val = line_parser.parse(line)
    if val:
        valeurs = {}
        valeurs["categorie"] = val["cat_id"]
        valeurs["date"] = val["post_dt"]
        valeurs["slug"] = val["post_url"]
        valeurs["title"] = val["post_title"]
        valeurs["content"] = val["post_content"]
        valeurs["excerpt"] = val["post_excerpt"]
        valeurs["status"] = 1 # Notre parser ne garde que les billets actifs
        valeurs["blog_id"] = val["blog_id"]
        return valeurs

if __name__ == '__main__':
    debut = datetime.datetime.utcnow()
    nb = 0
    with open(FILE) as f:
        for l in f.readlines():
            billet = parse_sql(l)
            if billet:
                print(billet["title"])
                a = e.process(billet, e.nouvelle_categorie, BLOG_ID)
                if a:
                    nb += 1
    fin = datetime.datetime.utcnow()
    duree = fin - debut
    print("%s posts créés en %s" % (nb, duree))
