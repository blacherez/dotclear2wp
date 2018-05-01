import sys
import re

motif_ligne = re.compile(r"(?P<post_id>\d+), '(?P<blog_id>([^']*(\\'|'')?)*)', '(?P<user_id>([^']*(\\'|'')?)*)', (?P<cat_id>\d+), '(?P<post_dt>\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)', '(?P<post_tz>([^']*(\\'|'')?)*)', '(?P<post_creadt>\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)', '(?P<post_upddt>\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)', '?(?P<post_password>([^']*(\\'|'')?)*)'?, '(?P<post_type>([^']*(\\'|'')?)*)', '(?P<post_format>([^']*(\\'|'')?)*)', '(?P<post_url>([^']*(\\'|'')?)*)', '(?P<post_lang>([^']*(\\'|'')?)*)', '(?P<post_title>([^']*(\\'|'')?)*)', '(?P<post_excerpt>([^']*(\\'|'')?)*)', '(?P<post_excerpt_xhtml>([^']*(\\'|'')?)*)', '(?P<post_content>([^']*(\\'|'')?)*)', '(?P<post_content_xhtml>([^']*(\\'|'')?)*)', '(?P<post_notes>([^']*(\\'|'')?)*)', '(?P<post_words>([^']*(\\'|'')?)*)', (?P<post_status>-?\d), (?P<post_selected>\d), (?P<post_open_comment>\d), (?P<post_open_tb>\d), (?P<nb_comment>\d+), (?P<nb_trackback>\d+), '(?P<post_meta>([^']*(\\'|'')?)*)', (?P<post_position>\d+)\)")
actif = re.compile(r", 1, \d, \d, \d, \d+, \d+, '([^']*(\\'|'')?)*', \d+\)")

def parse(ligne):
    #print("Processing line %s" % ligne[:10])
    # On n'analyse la ligne que si elle correspond à un billet actif (càd que son état est 1)
    if actif.search(ligne):
        r = motif_ligne.search(ligne)
        if r:
            return r.groupdict()
    return None


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        for l in f.readlines():
            billet = parse(l)
            if billet:
                print(billet["post_title"])
