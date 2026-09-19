import json,subprocess
from datetime import date
BASE="https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo"
def fetch(ano,per):
    u=f"{BASE}?an_exercicio={ano}&nr_periodo={per}&co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2003&id_ente=3533908"
    try: return json.loads(subprocess.run(["curl","-s","--max-time","90",u],capture_output=True,text=True).stdout).get("items",[])
    except Exception as e: return []
def mes_ref(ano,per,coluna):
    # MR = ultimo mes do bimestre `per`
    mr = per*2
    off = 0 if coluna=="<MR>" else int(coluna.replace("<MR-","").replace(">",""))
    m = mr - off; a = ano
    while m<1: m+=12; a-=1
    return a,m
series={}
for ano,per in [(2023,6),(2024,6),(2025,6),(2026,4)]:
    items=fetch(ano,per)
    if not items: print(f"! {ano}/p{per} sem dados"); continue
    for r in items:
        if r["cod_conta"] not in ("ISSLiquidoExcetoTransferenciasEFUNDEB","IPTULiquidoExcetoTransferenciasEFUNDEB","ReceitaTributariaLiquidaExcetoTransferenciasEFUNDEB","RREO3CotaParteDoICMS"): continue
        c=r["coluna"]
        if not c.startswith("<MR"): continue
        a,m=mes_ref(ano,per,c)
        series.setdefault(r["cod_conta"],{})[(a,m)]=r["valor"]
    print(f"ok {ano}/p{per}")
json.dump({k:{f"{a}-{m:02d}":v for (a,m),v in sorted(d.items())} for k,d in series.items()},open("iss_series.json","w"),indent=1)
iss=series.get("ISSLiquidoExcetoTransferenciasEFUNDEB",{})
print("\n=== ISS mensal (R$) ===")
anos=sorted({a for a,_ in iss})
print("mês  " + "".join(f"{a:>12}" for a in anos))
for m in range(1,13):
    row=f"{m:>3}  "
    for a in anos:
        v=iss.get((a,m))
        row += f"{v/1000:>11,.0f}k" if v else f"{'-':>12}"
    print(row)
