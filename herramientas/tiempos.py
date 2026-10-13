import json,glob,os,collections,statistics
L=collections.defaultdict(list)
for d in glob.glob('/datos/trabajos/*'):
    try: e=json.load(open(d+'/estado.json'))
    except Exception: continue
    if e.get('partes') or not e.get('fin') or not e.get('inicio'): continue
    L[os.path.basename(d).split('-')[0]].append((float(e['inicio']),float(e['fin']),int(e.get('n_paginas') or 0)))
r=[]
for k,v in L.items():
    p=sum(x[2] for x in v); m=(max(x[1] for x in v)-min(x[0] for x in v))/60
    r.append((p,m))
r.sort()
for p,m in r: print(p, round(m,1))
big=[m for p,m in r if p>=1000]
print('n',len(r),'>=1000:',len(big),'mediana',round(statistics.median(big),1),'max',round(max(big),1))
