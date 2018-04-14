# -*- coding: utf-8 -*-
import requests
import json
import base64
import csv
import datetime

AUTHOR = 1 # On ne peut pas publier des articles avec l'API pour un autre auteur que celui qui se connecte

FILE = "data/posts3.csv"

USER = 'ben'
PYTHONAPP = "od0B LIm2 HQUo wbMq n3R6 gwq6"
URL = "http://lacherez.info/maison/wp-json/wp/v2"

token = base64.standard_b64encode((USER + ':' + PYTHONAPP).encode("ascii"))
headers = {'Authorization': 'Basic ' + token.decode("utf-8")}

def create_post(date, title, slug, content, excerpt, status="publish"):
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
    date = row[4]
    date_pub = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    slug = row[11]
    title = row[13]
    content = row[16]
    excerpt = ""

    print(title)
    p = create_post(date_pub, title, slug, content, excerpt)
    #print(p)
    r = publier(p)
    return r
    #print(r)


nb = 0
with open(FILE) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        a = process(row)
        if a:
            nb += 1

print("%s posts créés" % nb)

#r = requests.post(url + '/posts', headers=headers, json=post)
#print('Your post is published on ' + json.loads(r.content)['link'])
