# -*- coding: utf-8 -*-
"""
Crée les billets depuis un fichier SQL
"""
import ecriveur as e
import line_parser
import sys

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

import re
import codecs

ESCAPE_SEQUENCE_RE = re.compile(r'''
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )''', re.UNICODE | re.VERBOSE)

def decode_escapes(s):
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)

if __name__ == '__main__':
    nb = 0
    with open(FILE) as f:
        for l in f.readlines():
            billet = parse_sql(l)
            if billet:
                print(decode_escapes(billet["title"]))
                a = e.process(billet, e.nouvelle_categorie, BLOG_ID)
                if a:
                    nb += 1

    print("%s posts créés" % nb)
