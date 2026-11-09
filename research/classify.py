import json, csv, re
rows = {}
for f in ['ideas-raw.json','ideas-suburbs.json','ideas-problems.json']:
    d = json.load(open(f, encoding='utf-8'))
    for r in d['tasks'][0].get('result') or []:
        k = r['keyword'].strip().lower()
        if k not in rows or (r.get('search_volume') or 0) > (rows[k].get('search_volume') or 0):
            rows[k] = r

SUBS = 'cape town|capetown|durbanville|bellville|parow|milnerton|table view|brackenfell|goodwood|somerset west|century city|edgemead|bothasig|kuils|kraaifontein|montague|vasco|richwood|pinelands|observatory|woodstock'
LOC = re.compile(SUBS)
SERV = [('waterproofing','waterproof'),('damp','damp-proofing'),('paint','painting'),('kitchen','kitchen-renovations'),('bathroom','bathroom-renovations'),('extension','home-extensions'),('plaster','plastering'),('tiling','tiling'),('roof','roofing'),('renovat','home-renovations')]

MONEY = re.compile(r'company|companies|contractor|specialist|near me|service|services|cost|price|quote|installer|expert|professional')
PROBLEM = re.compile(r'leak|rising damp|mould|mold|ceiling|crack|effloresc|seepage|wet wall')
INFO = re.compile(r'how to|what is|diy|meaning|difference|vs |average cost of')

def buck(k):
    if INFO.search(k): return 'info'
    if PROBLEM.search(k): return 'problem'
    if MONEY.search(k) or LOC.search(k): return 'money'
    return 'other'

def service(k):
    for pat, slug in SERV:
        if pat in k: return slug
    return ''

out = []
for k, r in rows.items():
    v = r.get('search_volume') or 0
    out.append([k, v, round(r.get('cpc') or 0, 2), (r.get('competition') or ''), buck(k), service(k)])
out.sort(key=lambda x: (-x[1], -x[2]))
with open('keyword-master.csv','w',newline='',encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(['keyword','volume','cpc','competition','bucket','service'])
    w.writerows(out)
from collections import Counter
print('unique:', len(out), Counter(o[4] for o in out))
print('money with volume:', sum(1 for o in out if o[4]=='money' and o[1]>0))
