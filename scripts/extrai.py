import py7zr,sys,os,csv
mes=sys.argv[1]
d=f"caged/x{mes}"
os.makedirs(d,exist_ok=True)
with py7zr.SevenZipFile(f"caged/{mes}.7z") as z:
    nomes=z.getnames(); print("arquivos:",nomes)
    z.extractall(d)
f=[os.path.join(dp,n) for dp,_,fn in os.walk(d) for n in fn][0]
print("extraido:",f, os.path.getsize(f)//1024//1024,"MB")
out=f"caged/olimpia_{mes}.csv"; n=0
with open(f,encoding="latin-1") as fh, open(out,"w",encoding="utf-8") as o:
    head=fh.readline(); o.write(head)
    cols=head.strip().split(";"); print("colunas:",cols)
    im=cols.index("município") if "município" in cols else 3
    for line in fh:
        if line.split(";")[im]=="353390": o.write(line); n+=1
print(f"linhas Olímpia: {n} -> {out}")
os.remove(f)
