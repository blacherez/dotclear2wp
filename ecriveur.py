# -*- coding: utf-8 -*-
import requests
import json
import base64
import csv
import datetime
import os

import lib
import vendor.recupimages.recupimages as ri

AUTHOR = 1 # On ne peut pas publier des articles avec l'API pour un autre auteur que celui qui se connecte

FILE = "data/30posts.csv"
JSON_CATEGORIES = "data/categories.json"

BLOG_ID = "blog" # Identifiant du blog à transférer

USER = 'ben'
PYTHONAPP = "od0B LIm2 HQUo wbMq n3R6 gwq6"
URL = "http://lacherez.info/maison/wp-json/wp/v2"

token = base64.standard_b64encode((USER + ':' + PYTHONAPP).encode("ascii"))
headers = {'Authorization': 'Basic ' + token.decode("utf-8")}

# On lit les catégories dans le fichier JSON_CATEGORIES
nouvelle_categorie = {}
if os.path.exists(JSON_CATEGORIES):
    with open(JSON_CATEGORIES) as f:
        cat = json.load(f)
        if  len(cat):
            for k in cat:
                categorie = cat[k]
                if "ancien_id" in categorie:
                    # La catégorie a une correspondance dans les anciennes catégories
                    nouvelle_categorie[categorie["ancien_id"]] = categorie["nouvel_id"]
else:
    print("Le fichier %s n'existe pas, les billets créés n'auront pas de catégorie" % JSON_CATEGORIES)

def create_post(date, title, slug, content, excerpt, categories, status="publish"):
    """Crée le dictionnaire correspondant au post.
    date: objet datetime
    """
    post = {}
    post['date'] = date.isoformat()
    post['title'] = title
    post['slug'] = slug
    post['content'] = ri.traite(content)
    post['status'] = status
    post['author'] = AUTHOR # On ne peut pas publier pour un autre auteur que celui qui est connecté
    post['excerpt'] = excerpt
    post['format'] = 'standard'
    post['categories'] = categories

    return post

def publier(post):
    r = requests.post(URL + '/posts', headers=headers, json=post)
    c = json.loads(r.content.decode("utf-8"))
    if r.ok:
        return c["link"]
    else:
        print(c)
        return False

def parse_csv(row):
    valeurs = {}
    valeurs["blog_id"] = row[1]
    valeurs["categorie"] = row[3]
    valeurs["date"] = row[4]
    valeurs["slug"] = row[11]
    valeurs["title"] = row[13]
    valeurs["content"] = row[16]
    valeurs["excerpt"] = ""
    valeurs["status"] = row[20]
    return valeurs

def process(valeurs, nouvelle_categorie, blog):
    """
    Traite un article.
    valeur est un dictionnaire comportant :
        categorie : ancien id de catégorie
        date : date telle qu'elle est dans la base de dc (ie AAAA-MM-JJ HH:MM:SS)
        slug
        title
        content
        excerpt
        status
        blog_id
    """
    if not valeurs["blog_id"] == blog:
        # Le billet n'est pas dans le blog à transférer
        return None
    if valeurs["categorie"] in nouvelle_categorie:
        categorie = [nouvelle_categorie[valeurs["categorie"]]]
    else:
        categorie = []
    date_pub = datetime.datetime.strptime(valeurs["date"], "%Y-%m-%d %H:%M:%S")
    #title = bytes(valeurs["title"], "utf-8").decode('unicode_escape').encode("utf-8")
    title = lib.decode_escapes(valeurs["title"])
    blog_id = valeurs["blog_id"]
    slug = valeurs["slug"]
    content = lib.decode_escapes(valeurs["content"])
    excerpt = lib.decode_escapes(valeurs["excerpt"])
    status = valeurs["status"]
    # print(title)
    # print(categorie)
    print("%s (cat: %s) : %s, %s" % (title, categorie, status, blog_id))
    #return title
    p = create_post(date_pub, title, slug, content, excerpt, categorie)
    #print(p)
    r = publier(p)
    return r
    #print(r)

if __name__ == '__main__':
    nb = 0
    with open(FILE) as csvfile:
        #spamreader = csv.reader(csvfile, "unix", delimiter=',', quotechar='"', escapechar='\\', doublequote=False, quoting=csv.QUOTE_ALL)
        spamreader = csv.reader(csvfile, "unix")
        for row in spamreader:
            valeurs = parse_csv(row)
            if valeurs:
                print(valeurs)
                a = process(valeurs, nouvelle_categorie, BLOG_ID)
                if a:
                    nb += 1
            else:
                print("Rien pour %s" % row[:4])

    print("%s posts créés" % nb)
