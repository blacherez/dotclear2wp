# -*- coding: utf-8 -*-
import fileinput
SEP = ","
for line in fileinput.input():
    champs = line.split(SEP)
    n = 0
    for c in champs:
        print("%s: %s" % (n, c))
        n+=1
