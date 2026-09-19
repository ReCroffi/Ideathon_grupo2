import json
d=json.load(open('dados.json'))
h=open('base.html',encoding='utf-8').read()
h=h.replace('__DADOS_JSON__', json.dumps(d,ensure_ascii=False,separators=(',',':')))
open('olimpia.html','w',encoding='utf-8').write(h)
print('olimpia.html', len(h),'bytes')
