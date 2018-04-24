# -*- coding: utf-8 -*-
import requests
import json
import base64
import csv
import datetime
import os

AUTHOR = 1 # On ne peut pas publier des articles avec l'API pour un autre auteur que celui qui se connecte

FILE = "data/posts3.csv"
JSON_CATEGORIES = "data/categories.json"

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
print(nouvelle_categorie)

def create_post(date, title, slug, content, excerpt, categories, status="publish"):
    """Crée le dictionnaire correspondant au post.
    date: objet datetime
    """
    post = {}
    post['date'] = date.isoformat()
    post['title'] = title
    post['slug'] = slug
    post['content'] = content
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


def process(row):
    categorie = [nouvelle_categorie[row[3]]]
    date = row[4]
    date_pub = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    slug = row[11]
    title = row[13]
    content = row[16]
    excerpt = ""
    status = row[20]

    # print(title)
    # print(categorie)
    print("%s (cat: %s) : %s" % (title, categorie, status))
    return 0
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
            a = process(row)
            if a:
                nb += 1

    print("%s posts créés" % nb)

#r = requests.post(url + '/posts', headers=headers, json=post)
#print('Your post is published on ' + json.loads(r.content)['link'])
