import re,sys
s=open(sys.argv[1],encoding='utf-8').read()
i=s.index('</style>')+len('</style>')
head,body=s[:i],s[i:]
head=head.replace('<style>','<style>\nbody{margin:0}\nimg{max-width:100%}\n[hidden]{display:none!important}\n',1)
out=('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
     '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
     '<meta name="robots" content="noindex, nofollow">\n'+head+'\n</head>\n<body>'+body+'\n</body>\n</html>\n')
open(sys.argv[2],'w',encoding='utf-8',newline='\n').write(out)
