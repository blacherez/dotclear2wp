# -*- coding: utf-8 -*-
"""
Crée les catégories qui n'existent pas encore dans le nouveau blog et enregistre un fichier json des correspondances d'id
Le script principal fonctionne avec un fichier CSV des catégories de l'ancien blog, mais les fonctions peuvent être appelées depuis d'autres
scripts pour s'adapter à d'autres formats.
"""
import requests
import json
import base64
import csv
import datetime
import html
import sys

AUTHOR = 1 # On ne peut pas publier des articles avec l'API pour un autre auteur que celui qui se connecte

FILE = "data/categories.csv"
CATEGORY_FILE = "data/categories.json"

USER = 'ben'
PYTHONAPP = "od0B LIm2 HQUo wbMq n3R6 gwq6"
URL = "http://lacherez.info/maison/wp-json/wp/v2"

token = base64.standard_b64encode((USER + ':' + PYTHONAPP).encode("ascii"))
HEADERS = {'Authorization': 'Basic ' + token.decode("utf-8")}



def create_cat(name, slug, description, parent=0):
    """Crée le dictionnaire correspondant à la catégorie.
    """
    category = {}
    category["name"] = html.escape(name)
    category["slug"] = slug
    category["description"] = description
    category["parent"] = parent

    return category

def send(category):
    """Envoie un dictionnaire pour créer la catégorie sur le site distant"""
    r = requests.post(URL + '/categories', headers=HEADERS, json=category)
    c = json.loads(r.content.decode("utf-8"))
    if r.ok:
        return c["id"]
    else:
        print(c)
        return False

def parse_csv(row):
    val = {}
    val['old_id'] = row[0]
    val['name'] = row[2]
    val['slug'] = row[3].lower()
    #description = row[4]
    val['description'] = ""

    return val


def process(ancien, new_cats):
    """
    ancien est un dictionnaire contenant :
    old_id
    name
    slug
    description
    """
    old_id = ancien["old_id"]
    name = ancien["name"]
    slug = ancien["slug"].lower()
    #description = row[4]
    description = ancien["description"]

    if slug in new_cats.keys():
        print("%s existe déjà" % slug)
        new_cats[slug]["ancien_id"] = old_id
    else:
        print("%s n'existe pas" % slug)
        cat = create_cat(name, slug, description)
        r = send(cat)
        if r:
            new_cats[slug] = {
                "nouvel_id": r,
                "ancien_id": old_id
            }
        else:
            print(cat)
    return new_cats

def get_remote_cats():
    params = {"per_page": 100}
    r = requests.get(URL + '/categories', headers=HEADERS, params = params)
    if r.ok:
        remote_cats = json.loads(r.content.decode("utf-8"))
        #print("%s catégories trouvées" % len(remote_cats))
    else:
        print(json.loads(r.content.decode("utf-8")))
        return None

    new_cats = {}
    for cat in remote_cats:
        #print(cat["slug"])
        new_cats[cat["slug"]] = {"nouvel_id": str(cat["id"])}
    return new_cats

def save2json(new_cats, jsonfile=CATEGORY_FILE):
    with open(jsonfile, "w") as f:
        json.dump(new_cats, f)

if __name__ == "__main__":
    # On récupère les catégories sur le site pour éviter de les créer en doublon
    c = get_remote_cats()
    if c:
        new_cats = c
    else:
        sys.exit(3)

    with open(FILE) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            valeurs = parse_csv(row)
            print(valeurs)
            if valeurs:
                new_cats = process(valeurs, new_cats)

    save2json(new_cats, CATEGORY_FILE)
