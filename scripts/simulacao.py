"""Sou+Olímpia — modelo econômico do programa de cartela (v2, corrigido).

Correção sobre a v1: o resgate do vale não é custo cheio. O cliente que resgata
faz uma compra, e a loja ganha margem sobre ela. O custo líquido do resgate é
  ticket_resgate * margem - vale
quando a visita de resgate é incremental, e -vale quando não é.
"""
import json, random

random.seed(42)
def tri(a, m, b): return random.triangular(a, b, m)

def por_cartela(p):
    """Resultado de UMA cartela completada, para a rede inteira (em R$ de margem)."""
    mg_carimbos = p["carimbos"] * p["inc"] * p["ticket"] * p["margem"]
    mg_resgate  = p["inc_resgate"] * p["ticket_resgate"] * p["margem"] - p["vale"]
    return mg_carimbos + mg_resgate

def breakeven(carimbos, ticket, margem, vale, ticket_resgate=None):
    """Incrementalidade mínima (mesma nas duas pontas) para não haver perda."""
    tr = ticket_resgate if ticket_resgate else ticket
    return vale / ((carimbos * ticket + tr) * margem)

CEN = {
    "3 carimbos · vale R$ 30": (3, 30),
    "3 carimbos · vale R$ 15": (3, 15),
    "5 carimbos · vale R$ 30": (5, 30),
    "5 carimbos · vale R$ 20": (5, 20),
    "5 carimbos · vale R$ 15": (5, 15),
}
print("PONTO DE EQUILÍBRIO — incrementalidade mínima, margem bruta 28%")
print(f"{'cenário':<26}{'ticket 40':>11}{'ticket 60':>11}{'ticket 90':>11}")
be_tab = {}
for nome,(nc,vl) in CEN.items():
    be_tab[nome] = {}
    linha = f"{nome:<26}"
    for tk in (40,60,90):
        be = breakeven(nc, tk, 0.28, vl, max(tk, 2*vl))
        be_tab[nome][tk] = be
        linha += f"{be*100:>10.0f}%"
    print(linha)

N = 20000
LOJAS = 30
DOMICILIOS = 20418
res = []
for _ in range(N):
    p = dict(carimbos=5, vale=20, margem=tri(0.20,0.28,0.38))
    p["ticket"]         = tri(35, 60, 110)
    p["ticket_resgate"] = max(p["ticket"], 2*p["vale"])
    p["inc"]            = tri(0.05, 0.18, 0.40)   # visita de carimbo incremental
    p["inc_resgate"]    = tri(0.20, 0.45, 0.75)   # resgate puxa mais que carimbo
    adesao    = tri(0.02, 0.06, 0.15)
    conclusao = tri(0.15, 0.30, 0.55)
    cartelas  = DOMICILIOS * adesao * conclusao
    lucro_rede = cartelas * por_cartela(p)
    res.append({
        "cartelas": cartelas,
        "visitas": cartelas * (p["carimbos"]+1),
        "receita_incr": cartelas * (p["carimbos"]*p["inc"] + p["inc_resgate"]) * p["ticket"],
        "vales": cartelas * p["vale"],
        "lucro_rede": lucro_rede,
        "lucro_loja": lucro_rede / LOJAS,
    })

def pct(c,q):
    v = sorted(r[c] for r in res); return v[int(q*(len(v)-1))]

fmt = lambda x: f"{x:,.0f}".replace(",",".")
print(f"\nMONTE CARLO — 20.000 cenários · {LOJAS} lojas · cartela de 5 · vale R$ 20")
print(f"{'métrica (por mês)':<38}{'P10':>12}{'mediana':>12}{'P90':>12}")
for c,rot in [("cartelas","Cartelas fechadas na cidade"),
              ("visitas","Visitas geradas pelo programa"),
              ("receita_incr","Receita incremental da rede (R$)"),
              ("vales","Valor concedido em vales (R$)"),
              ("lucro_rede","Lucro líquido da rede (R$)"),
              ("lucro_loja","Lucro líquido por loja (R$)")]:
    print(f"{rot:<38}"+"".join(fmt(pct(c,q)).rjust(12) for q in (.10,.50,.90)))

prob = sum(1 for r in res if r["lucro_loja"]>0)/N
print(f"\nProbabilidade de a loja ter lucro: {prob*100:.0f}%")
print(f"Retorno por real concedido em vale (mediana): R$ {pct('receita_incr',.5)/pct('vales',.5):.2f} de receita incremental")

curva=[]
for inc in [i/100 for i in range(0,41,2)]:
    p=dict(carimbos=5,vale=20,margem=0.28,ticket=60,ticket_resgate=60,inc=inc,inc_resgate=min(1,inc*2.5))
    cart=DOMICILIOS*0.06*0.30
    curva.append({"inc":inc,"lucro_loja":cart*por_cartela(p)/LOJAS})

json.dump({"breakeven":be_tab,
  "percentis":{c:{str(q):pct(c,q) for q in (.1,.5,.9)} for c in
     ("cartelas","visitas","receita_incr","vales","lucro_rede","lucro_loja")},
  "prob_lucro":prob,"curva":curva,"lojas":LOJAS,"domicilios":DOMICILIOS},
  open("simulacao.json","w"),indent=1)
print("\n-> simulacao.json")
