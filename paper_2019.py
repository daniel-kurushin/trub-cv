#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:45:19 2019

@author: dan
"""

from bs4 import BeautifulSoup as BS

def image(soup, name):
    """
    <text:p text:style-name="P3">
     <draw:frame
       draw:style-name="fr1"
       draw:name="Изображение1"
       text:anchor-type="as-char"
       svg:width="16cm"
       svg:height="7cm"
       draw:z-index="0">
       <draw:image xlink:href="Спиралеобразный%20робот.jpeg"
         xlink:type="simple"
         xlink:show="embed"
         xlink:actuate="onLoad"
         draw:filter-name="&lt;Все форматы&gt;"
         loext:mime-type="image/jpeg"/>
     </draw:frame>
     <text:line-break/>gfhghf
   </text:p>
    """
    height = "%scm" % 7
    draw_props = {
        'draw:style-name':"fr1",
        'draw:name':name,
        'text:anchor-type':"as-char",
        'svg:width':"16cm",
        'svg:height':height,
        'draw:z-index':"0"
    }
    p = soup.new_tag('text:p')
    p['text:style-name'] = 'P3'
    draw = soup.new_tag('draw:frame')
    

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