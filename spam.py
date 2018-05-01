import re, sys
#motif = re.compile(r"(?P<post_id>\d+), '(?P<blog_id>([^']*(\\'|'')?)*)', '(?P<user_id>([^']*(\\'|'')?)*)', (?P<cat_id>\d+), '(?P<post_dt>\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)', '(?P<post_tz>([^']*(\\'|'')?)*)', '(?P<post_creadt>\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)', '(?P<post_upddt>\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)', '?(?P<post_password>([^']*(\\'|'')?)*)'?, '(?P<post_type>([^']*(\\'|'')?)*)', '(?P<post_format>([^']*(\\'|'')?)*)', '(?P<post_url>([^']*(\\'|'')?)*)', '(?P<post_lang>([^']*(\\'|'')?)*)', '(?P<post_title>([^']*(\\'|'')?)*)', '(?P<post_excerpt>([^']*(\\'|'')?)*)', '(?P<post_excerpt_xhtml>([^']*(\\'|'')?)*)', '(?P<post_content>([^']*(\\'|'')?)*)', '(?P<post_content_xhtml>([^']*(\\'|'')?)*)', '(?P<post_notes>([^']*(\\'|'')?)*)', '(?P<post_words>([^']*(\\'|'')?)*)', (?P<post_status>\d), (?P<post_selected>\d), (?P<post_open_comment>\d), (?P<post_open_tb>\d), (?P<nb_comment>\d+), (?P<nb_trackback>\d+), '(?P<post_meta>([^']*(\\'|'')?)*)', (?P<post_position>\d+)\),")
motif = re.compile(r"(?P<cat_id>\d+), '(?P<blog_id>([^']*(\\'|'')?)*)', '(?P<cat_title>([^']*(\\'|'')?)*)', '(?P<cat_url>([^']*(\\'|'')?)*)', '(?P<cat_desc>([^']*(\\'|'')?)*)', (?P<cat_position>\d+), (?P<cat_lft>\d+), (?P<cat_rgt>\d+)")  
actif = re.compile(r", 1, \d, \d, \d, \d+, \d+, '([^']*(\\'|'')?)*', \d+\),$")

with open("test_cat.sql") as f:
    lignes = f.readlines()

for l in lignes:
    r = motif.search(l)
    if r:
        print(r.group("cat_title"), r.group("cat_desc"))

#INSERT INTO `dc2_category` (`cat_id`, `blog_id`, `cat_title`, `cat_url`, `cat_desc`, `cat_position`, `cat_lft`, `cat_rgt`) VALUES
#(1, 'blog', 'L\'ACTU CLUBS & ASSOS', 'Actualites-club-asso', '', 6, 18, 19),
#(3, 'blog', 'ESCALADE', 'Escalade', '', 4, 8, 9),
#(4, 'blog', 'ZOOM SUR LES BEAUX LIVRES', 'Litterature', '', 3, 6, 7),
#(5, 'blog', 'LES EXPOS À LA MM', 'Expos', '', 2, 4, 5),
#(6, 'blog', 'RANDOS & BALADES', 'Randonnees-Balades', '<p>Dans cette catégorie on trouvera pour les randonneurs peu entrainés des balades agréables, faciles à se mettre\r\nsous les pieds, histoire de se dégourdir les jambes... Quelques canyons ludiques ne nécessitant pas un long apprentissage technique.</p>\r\n<p>Pour celui qui ne maitrise pas toutes les subtilités de la randonnée en montagne, de la cartographie ou du canyoning, les professionnels (Guides, Amm, B.E escalade) sont là pour partager leur savoir-faire.</p>\r\n<p>Voilà quelques idées...</p>', 5, 10, 11),
