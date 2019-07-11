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

def image(soup, number, name):
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
        {'text:style-name':'PCentered'},
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
    img.insert(2,"Рис. %s — %s" % (number, name))
    return img

doc = BS(open('in.fodt').read(), features='xml')

to_insert = doc.find('text:p', place='here')

P = []
L = ''
C = {}

x = open('paper-2019').read()
for bib in [ x.strip('\n') for x in open('paper-2019.bib').readlines() ]:
    try:
        idx, paper = re.findall('(\d+)\.\s(.*)', bib )[0]
        try:
            ref = ' '.join(re.findall('(.{10}).*?\..*?(\d{4}).*', paper)[0])
        except IndexError:
            ref = re.findall('.*(http.*)', paper)[0]
        while ref in C.keys():
            ref += 'a'
        C.update({ref:{'idx':idx,'paper':paper}})
    except Exception as e:
        print(bib)
        raise e
        
RT = []
nidx = 0
C1 = []
for cite in re.findall('(\[a.*?\])', x):
    n = re.findall('.*?(\d+).*', cite)[0]
    ref = [ (k, v) for k, v in C.items() if v['idx'] == n]
    try:
        nidx += 1
        C1 += [(nidx, ref[0][1]['paper'])]
        RT += [(cite, ('[%s]' % ref[0][0], '[%s]' % nidx))]
    except IndexError:
        print(ref)

for _from, _to in RT:
    x = x.replace(_from, _to[0])
for _from, _to in RT:
    x = x.replace(_to[0], _to[1])
    

for l in [ v.strip('\n') for v in x.split('\n') ]:
    if not l:
        P += [L]
        L = ''
    else:
        L += ' %s' % l

picnumber = 0
headnumber = 0
pictures = {}
headers = {}
cites = {}

for p in [ x.strip() for x in P]:
    if p.startswith('Рис.'):
        picnumber += 1
        name = re.findall(string=p, pattern='Рис. (.*)')[0]
        ins = image(doc, picnumber, name)
        pictures.update({name:picnumber})
    elif p.startswith('='):
        headnumber += 1
        header = "%s. %s" % (headnumber, p.strip('='))
        ins = _new_tag(doc, 'text:p', {'text:style-name':'Pheader'}, header)
        headers.update({header:headnumber})
    else:
        ins = _new_tag(doc, 'text:p', {'text:style-name':'Pnormal'}, p)
    to_insert.insert_after(ins)
    to_insert = ins

for k, v in C1:
    p = "%s. %s" % (k, v)
    ins = _new_tag(doc, 'text:p', {'text:style-name':'Pnormal'}, p)
    to_insert.insert_after(ins)
    to_insert = ins
    
citeno = 0
for p in doc('text:p'):
    text = str(p.string)
    if text:
        for picref in re.findall('/p (.*?)/', text):
            n = pictures[picref]
            text = re.sub('/p %s/' % picref, str(n), text)
    if str(p.string) != text:
        p.string = text
        
print(doc.prettify())    