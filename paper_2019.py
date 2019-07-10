#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:45:19 2019

@author: dan
"""

from bs4 import BeautifulSoup as BS

doc = BS(open('/tmp/in.fodt').read(), features='xml')

to_insert = doc.find('text:p', place='here')

p = doc.new_tag('text:p')
p.string = 'sdfdfs'
to_insert.insert_after(p)

P = []
L = ''
for l in [ x.strip('\n') for x in open('paper-2019').readlines() ]:
    if not l:
        P += [L]
        L = ''
    else:
        L += ' %s' % l

for p in P:
    ins = doc.new_tag('text:p')
    ins['text:style-name'] = 'P2'
    ins.string = p
    to_insert.insert_after(ins)
    to_insert = ins

print(doc.prettify())    