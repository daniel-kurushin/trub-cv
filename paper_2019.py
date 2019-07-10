#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:45:19 2019

@author: dan
"""

from bs4 import BeautifulSoup as BS
from PIL import Image
from urllib.parse import quote
import re

def _new_tag(soup, name, attrs, content):
    tag = soup.new_tag(name)
    for k, v in attrs.items():
        tag[k] = v
    if content is not None:
        if type(content) == str:
            tag.string = content
        else:
            tag.insert(0, content)
    return tag

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
       <draw:image 
         xlink:href="Спиралеобразный%20робот.jpeg"
         xlink:type="simple"
         xlink:show="embed"
         xlink:actuate="onLoad"
         draw:filter-name="&lt;Все форматы&gt;"
         loext:mime-type="image/jpeg"/>
     </draw:frame>
     <text:line-break/>gfhghf
   </text:p>
    """
    for suff in ['jpeg','png','jpg']:
        imname = '/home/dan/Yandex.Disk/Src/trub-cv/paper-img/%s.%s' % (name, suff)
        try:
            img = Image.open(imname)
            break
        except FileNotFoundError:
            pass
    w, h = img.size
    img = _new_tag(soup, 
        'text:p', 
        {'text:style-name':'P3'},
        _new_tag(soup,
            'draw:frame',
            {
                'draw:style-name':"fr1",
                'draw:name':name,
                'text:anchor-type':"as-char",
                'svg:width':"16cm",
                'svg:height':"%scm" % round(h * 16 / w, 2),
                'draw:z-index':"0"
            },
            _new_tag(soup,
                'draw:image',
                {
                    'xlink:href':quote(imname),
                    'xlink:type':"simple",
                    'xlink:show':"embed",
                    'xlink:actuate':"onLoad",
                    'draw:filter-name':"&lt;Все форматы&gt;",
                    'loext:mime-type':"image/%s" % img.format.lower()
                },
                None
            )
        )
    )
    img.insert(1, _new_tag(soup,'text:line-break',{},None))
    img.insert(2,name)
    return img

doc = BS(open('in.fodt').read(), features='xml')

to_insert = doc.find('text:p', place='here')

P = []
L = ''
for l in [ x.strip('\n') for x in open('paper-2019').readlines() ]:
    if not l:
        P += [L]
        L = ''
    else:
        L += ' %s' % l

for p in [ x.strip() for x in P]:
    if p.startswith('Рис.'):
        name = re.findall(string=p, pattern='Рис. (.*)')[0]
        ins = image(doc, name)
    else:
        ins = _new_tag(doc, 'text:p', {'text:style-name':'P2'}, p)
    to_insert.insert_after(ins)
    to_insert = ins

print(doc.prettify())    