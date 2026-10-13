import json,glob,os,time,collections
M=collections.defaultdict(lambda: collections.Counter())
for d in sorted(glob.glob('/datos/trabajos/*')):
    try: e=json.load(open(d+'/estado.json'))
    except Exception: continue
    j=os.path.basename(d)
    ini=float(e.get('inicio') or os.path.getmtime(d)); mes=time.strftime('%Y-%m',time.localtime(ini))
    c=M[mes]
    if '-' not in j:
        c['lotes']+=1; c['paginas']+=int(e.get('n_paginas') or 0); c['mb']+=float(e.get('tam_mb') or 0)
        c['estado_'+str(e.get('estado'))]+=1
    if e.get('partes'): continue
    s=d+'/salida'
    if os.path.isdir(s):
        per=[p for p in os.listdir(s) if os.path.isdir(os.path.join(s,p))]
        c['personas']+=len(per)
        for p in per:
            cs=[x for x in os.listdir(os.path.join(s,p)) if x.startswith('corte_')]
            c['cortes']+=len(cs)
            for x in cs:
                dd=os.path.join(s,p,x,'documentos')
                if os.path.isdir(dd): c['documentos']+=len([f for f in os.listdir(dd) if f.endswith('.pdf')])
    r=d+'/revision.jsonl'
    if os.path.exists(r): c['correcciones']+=sum(1 for _ in open(r))
    if os.path.exists(d+'/propuestas.json'): c['con_propuestas']+=1
for m in sorted(M): print(m, dict(M[m]))
