import json,csv,glob,os,collections,statistics
SEC={'A':'Agropecuária','B':'Ind. extrativa','C':'Indústria de transformação','D':'Eletricidade e gás','E':'Água e esgoto','F':'Construção','G':'Comércio','H':'Transporte','I':'Alojamento e alimentação','J':'Informação e comunicação','K':'Financeiro','L':'Imobiliárias','M':'Prof. científicas e técnicas','N':'Adm. e serviços complementares','O':'Administração pública','P':'Educação','Q':'Saúde','R':'Arte, cultura, esporte e lazer','S':'Outros serviços','T':'Serviços domésticos','U':'Organismos internacionais'}
TUR=set('IR')  # alojamento/alimentacao + arte/cultura/lazer
d={}
# --- ISS
iss=json.load(open('iss_series.json'))['ISSLiquidoExcetoTransferenciasEFUNDEB']
d['iss_arrecadacao']=iss
ativ={}
for k,v in iss.items():
    a,m=int(k[:4]),int(k[-2:]); am,aa=(m-1,a) if m>1 else (12,a-1)
    ativ.setdefault(aa,{})[am]=v
d['iss_por_mes_movimento']={str(a):{str(m):v for m,v in sorted(x.items())} for a,x in sorted(ativ.items())}
idx={}
for a in (2023,2024,2025):
    vals={m:v for m,v in ativ.get(a,{}).items() if not (a==2025 and m==3)}
    if len(vals)<10: continue
    base=statistics.mean(vals.values()); idx[a]={m:round(v/base,3) for m,v in vals.items()}
d['iss_indice_sazonal']={str(a):{str(m):v for m,v in sorted(x.items())} for a,x in idx.items()}
d['iss_indice_medio']={str(m):round(statistics.mean([idx[a][m] for a in idx if m in idx[a]]),3) for m in range(1,13)}
# --- CAGED
caged={}
for f in sorted(glob.glob('caged/olimpia_*.csv')):
    mes=os.path.basename(f).split('_')[1][:6]
    rows=list(csv.DictReader(open(f,encoding='utf-8'),delimiter=';'))
    if not rows: continue
    k=list(rows[0].keys())
    sec=[c for c in k if 'seÃ' in c][0]; sal=[c for c in k if c.startswith('saldo')][0]
    wc=[c for c in k if 'rio' in c and c.startswith('sal')][0]
    agg=collections.defaultdict(lambda:[0,0]); sal_adm=[]
    for r in rows:
        v=int(r[sal]); agg[r[sec]][0 if v>0 else 1]+=1
        if v>0:
            try:
                w=float(r[wc].replace(',','.'))
                if 0<w<100000: sal_adm.append(w)
            except: pass
    caged[mes]={'setores':{SEC.get(s,s):{'adm':a,'desl':dd,'saldo':a-dd} for s,(a,dd) in agg.items()},
                'total':{'adm':sum(a for a,_ in agg.values()),'desl':sum(x for _,x in agg.values())},
                'saldo':sum(a-x for a,x in agg.values()),
                'saldo_turismo':sum(a-x for s,(a,x) in agg.items() if s in TUR),
                'saldo_comercio':sum(a-x for s,(a,x) in agg.items() if s=='G'),
                'salario_mediano_admissao':round(statistics.median(sal_adm),2) if sal_adm else None}
d['caged_2025']=caged
# --- OTO visitantes
d['oto_boletins']=[
 {'periodo':'Carnaval','mes':2,'ocupacao':80.64,'hospedados':75213,'rhc':11661,'dayuse':15511,'total':102386,'por_dia':20477},
 {'periodo':'Páscoa','mes':4,'ocupacao':75.07,'hospedados':42224,'rhc':6472,'dayuse':8695,'total':57391,'por_dia':19130},
 {'periodo':'Tiradentes','mes':4,'ocupacao':73.53,'hospedados':55035,'rhc':8382,'dayuse':11323,'total':74741,'por_dia':18685},
 {'periodo':'Dia do Trabalhador','mes':5,'ocupacao':65.38,'hospedados':36550,'rhc':5590,'dayuse':7524,'total':49664,'por_dia':16555},
 {'periodo':'Festa do Peão','mes':6,'ocupacao':41.74,'hospedados':23288,'rhc':3569,'dayuse':4795,'total':31651,'por_dia':10550},
 {'periodo':'Corpus Christi','mes':6,'ocupacao':67.78,'hospedados':49095,'rhc':7727,'dayuse':10146,'total':66968,'por_dia':16742},
 {'periodo':'Férias de julho','mes':7,'ocupacao':73.17,'hospedados':438214,'rhc':64375,'dayuse':89737,'total':592326,'por_dia':19107},
 {'periodo':'FEFOL (Folclore)','mes':8,'ocupacao':35.78,'hospedados':62962,'rhc':9140,'dayuse':12874,'total':84975,'por_dia':9442},
 {'periodo':'7 de Setembro','mes':9,'ocupacao':73.14,'hospedados':42408,'rhc':6227,'dayuse':8684,'total':57319,'por_dia':19106},
]
d['alta_temporada_verao']={'periodo':'dez/2025–jan/2026','total':1100000,'hospedados':815000,'rhc':127000,'dayuse':168000,'ocupacao':70.79,'por_dia':18000}
# --- socioeconomico IBGE
d['ibge']={'pop_censo2022':55074,'pop_est2026':57028,'area_km2':802.393,'densidade':68.62,
 'pib_2023':3569675501,'pib_per_capita_2023':64815.98,'idhm_2010':0.773,'escolarizacao':97.62,
 'salario_medio_sm_2024':2.6,'pessoal_ocupado_2024':25756,'assalariados_2024':18998,'empresas_2024':5858,
 'folha_2024':913398000,'esgoto':96.56,'agua':95.58,'idade_mediana':37,'envelhecimento':103.60,
 'dom_ocupados':20418,'dom_uso_ocasional':4380,'dom_vagos':2916,'dom_recenseados':27756,
 'cresc_domicilios_pct':54.77,'cresc_pop_aa':0.80,'transferencias_pct_2025':60.71,'receita_2025':472444065.23,
 'mortalidade_infantil_2025':10.29}
d['pib_per_capita']={'2010':23816.40,'2013':28279.83,'2016':35176.68,'2019':38588.17,'2020':38531.11,'2021':45985.63,'2022':56768.78,'2023':64815.98}
d['vab_2021']={'Serviços':1232950.114,'Indústria':648285.981,'Administração pública':265224.635,'Agropecuária':117750.639}
d['pessoal_ocupado_setor_2024']={'Indústria de transformação':5757,'Comércio':4973,'Alojamento e alimentação':2641,'Adm. e serviços complementares':2315,'Agropecuária':2002,'Administração pública':1694,'Arte, cultura, esporte e lazer':1160,'Saúde':1055,'Prof. científicas e técnicas':891,'Construção':740,'Educação':554,'Outros':1974}
d['base_renda']=[
 {'k':'Renda estável','v':11062,'det':'Indústria de transformação, administração pública, saúde, educação e agropecuária'},
 {'k':'Intermediário','v':10893,'det':'Comércio, serviços administrativos, construção e profissionais — atende morador e turista'},
 {'k':'Exposto ao turista','v':3801,'det':'Hospedagem, alimentação, arte, cultura e lazer — o quadro que encolhe na baixa'},
]
d['parques']={'Thermas dos Laranjais':{'visitantes_2024':1850000,'ranking_mundo':4},'Hot Beach':{'visitantes_2023':1035000,'ranking_mundo':5}}
json.dump(d,open('dados.json','w'),ensure_ascii=False,indent=1)
print('meses CAGED:',sorted(caged)); print('ok -> dados.json', os.path.getsize('dados.json'),'bytes')
for m in sorted(caged): print(m, 'saldo total',caged[m]['saldo'],'| turismo',caged[m]['saldo_turismo'],'| comercio',caged[m]['saldo_comercio'],'| sal.mediano adm R$',caged[m]['salario_mediano_admissao'])
