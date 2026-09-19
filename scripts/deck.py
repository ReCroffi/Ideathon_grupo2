#!/usr/bin/env python
"""Gera o deck do pitch Sou+Olímpia (16:9, editável)."""
from pptx import Presentation
from pptx.util import Inches as In, Pt
from pptx.dml.color import RGBColor as C
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path

AZUL, AZUL_ESC = C(0x0E,0x6F,0xD8), C(0x0A,0x4C,0x96)
AMARELO, VERMELHO, VERDE, LARANJA = C(0xF5,0xC4,0x00), C(0xD6,0x27,0x18), C(0x12,0x80,0x40), C(0xE0,0x7A,0x00)
TINTA, CINZA, CINZA2 = C(0x10,0x15,0x1C), C(0x49,0x53,0x5F), C(0x8A,0x93,0x9E)
FUNDO, BRANCO, LINHA = C(0xF1,0xF4,0xF8), C(0xFF,0xFF,0xFF), C(0xD9,0xE0,0xE9)
AZUL_CLARO = C(0xE7,0xF1,0xFD)

TIT = "Trebuchet MS"
TXT = "Trebuchet MS"

LOGO = Path.home()/"Ideathon/mvp/logo.jpg"
SAIDA = Path.home()/"Ideathon/SouMaisOlimpia-pitch.pptx"

prs = Presentation()
prs.slide_width, prs.slide_height = In(13.333), In(7.5)
W, H = 13.333, 7.5


def slide(fundo=BRANCO):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, In(W), In(H))
    bg.fill.solid(); bg.fill.fore_color.rgb = fundo
    bg.line.fill.background(); bg.shadow.inherit = False
    return s


def caixa(s, x, y, w, h, txt, tam=18, cor=TINTA, negrito=False, fonte=TXT,
          align=PP_ALIGN.LEFT, espaco=1.15, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(In(x), In(y), In(w), In(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    linhas = txt.split("\n")
    for i, ln in enumerate(linhas):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = espaco
        r = p.add_run(); r.text = ln
        r.font.size = Pt(tam); r.font.bold = negrito
        r.font.color.rgb = cor; r.font.name = fonte
    return tb


def retangulo(s, x, y, w, h, preenche=None, borda=None, raio=0.04, esp=1.25):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, In(x), In(y), In(w), In(h))
    shp.adjustments[0] = raio
    if preenche is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = preenche
    if borda is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = borda; shp.line.width = Pt(esp)
    shp.shadow.inherit = False
    shp.text_frame.text = ""
    return shp


def faixa_titulo(s, eyebrow, titulo, sub=None):
    caixa(s, 0.85, 0.55, 11.6, 0.3, eyebrow.upper(), 11, AZUL, True, TIT, espaco=1)
    caixa(s, 0.85, 0.92, 11.6, 1.0, titulo, 34, TINTA, True, TIT, espaco=1.02)
    barra = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, In(0.85), In(1.88), In(1.1), In(0.06))
    barra.fill.solid(); barra.fill.fore_color.rgb = AZUL
    barra.line.fill.background(); barra.shadow.inherit = False
    if sub:
        caixa(s, 0.85, 2.12, 11.2, 0.8, sub, 16, CINZA, False, TXT, espaco=1.25)


_pag = [1]
def rodape(s, n=None):
    _pag[0] += 1
    caixa(s, 0.85, 6.92, 7, 0.28, "SOU+OLÍMPIA · GRUPO 4 · IDEATHON OLIMPIALAB 2026", 9, CINZA2, False, TIT, espaco=1)
    caixa(s, 11.0, 6.92, 1.5, 0.28, str(_pag[0]), 9, CINZA2, False, TIT, align=PP_ALIGN.RIGHT, espaco=1)


# ══════════════════════ 1 · CAPA ══════════════════════
s = slide(BRANCO)
faixa = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, In(W), In(0.22))
faixa.fill.solid(); faixa.fill.fore_color.rgb = AZUL; faixa.line.fill.background(); faixa.shadow.inherit = False
if LOGO.exists():
    s.shapes.add_picture(str(LOGO), In(1.0), In(1.15), height=In(1.9))
caixa(s, 1.0, 3.35, 10.5, 1.2, "Rede de confiança para os\nnegócios de Olímpia", 40, TINTA, True, TIT, espaco=1.02)
caixa(s, 1.0, 4.85, 9.6, 0.9,
      "Uma camada que permite pequenos negócios provarem quem são e\nverificarem uns aos outros — sem planilha e sem grupo de WhatsApp.",
      17, CINZA, False, TXT, espaco=1.3)
retangulo(s, 1.0, 5.95, 4.4, 0.62, AZUL_CLARO, None)
caixa(s, 1.25, 6.12, 4.0, 0.4, "Desafio 2 · Olímpia Conecta", 14, AZUL_ESC, True, TIT, espaco=1)
caixa(s, 5.9, 6.12, 6.0, 0.4, "Grupo 4  ·  Geise · Bruno · Alan · Naisa · Renan · Alan · Eduardo",
      12, CINZA2, False, TXT, espaco=1)

# ══════════════════════ 2 · O NÚMERO ══════════════════════
s = slide(BRANCO)
faixa_titulo(s, "O problema, medido", "Olímpia fatura 26% do seu ano\nde serviços em dois meses")
IDX = [("Jan",1.51),("Fev",0.81),("Mar",0.80),("Abr",0.92),("Mai",0.77),("Jun",0.78),
       ("Jul",1.46),("Ago",0.87),("Set",0.91),("Out",1.15),("Nov",0.93),("Dez",1.04)]
bx, by, bw, bh = 0.85, 2.45, 11.6, 2.9
larg = bw / 12
base = by + bh
# linha da média
lm = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, In(bx), In(base - bh*(1.0/1.7)), In(bw), In(0.015))
lm.fill.solid(); lm.fill.fore_color.rgb = CINZA2; lm.line.fill.background(); lm.shadow.inherit = False
caixa(s, bx+bw-1.6, base - bh*(1.0/1.7) - 0.3, 1.6, 0.25, "média do ano", 10, CINZA2, False, TIT,
      align=PP_ALIGN.RIGHT, espaco=1)
for i,(m,v) in enumerate(IDX):
    alt = bh * (v/1.7)
    cor = AZUL if v >= 1.10 else C(0x9E,0xC5,0xF4)
    r = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, In(bx+i*larg+0.07), In(base-alt), In(larg-0.14), In(alt))
    r.adjustments[0] = 0.08
    r.fill.solid(); r.fill.fore_color.rgb = cor
    r.line.fill.background(); r.shadow.inherit = False
    caixa(s, bx+i*larg, base-alt-0.32, larg, 0.28, f"{v:.2f}".replace(".",","), 11,
          TINTA if v>=1.10 else CINZA, True, TIT, align=PP_ALIGN.CENTER, espaco=1)
    caixa(s, bx+i*larg, base+0.08, larg, 0.28, m, 11, CINZA, False, TIT, align=PP_ALIGN.CENTER, espaco=1)
caixa(s, 0.85, 5.85, 11.6, 0.8,
      "Índice sazonal do ISS, 2023–2025, série que nós construímos a partir da API do Tesouro Nacional.\n"
      "Janeiro vale 1,96× maio. Oito dos doze meses ficam abaixo da média do próprio ano.",
      14, CINZA, False, TXT, espaco=1.3)
rodape(s)

# ══════════════════════ 3 · CAUSA RAIZ ══════════════════════
s = slide(FUNDO)
faixa_titulo(s, "Cinco porquês", "O problema não é falta de cliente")
passos = [
    ("O faturamento de serviços cai pela metade na baixa", "índice 1,51 em janeiro contra 0,77 em maio"),
    ("A demanda é turística e só vem nas férias escolares", "feriado não resolve: Carnaval tem 80,6% de ocupação e cai num mês de 0,81"),
    ("O morador sozinho não cobre o buraco", "seria preciso R$ 3.278 a 8.195 a mais por domicílio por mês"),
    ("A saída é ação coletiva entre negócios", "campanha que manda o cliente de uma loja para outra"),
    ("Mas parceria hoje roda em planilha e WhatsApp", "ninguém consegue verificar o que o outro afirma"),
]
y = 2.35
for i,(t,d) in enumerate(passos):
    retangulo(s, 0.85, y, 11.6, 0.68, BRANCO, LINHA, 0.18, 0.75)
    n = s.shapes.add_shape(MSO_SHAPE.OVAL, In(1.05), In(y+0.17), In(0.34), In(0.34))
    n.fill.solid(); n.fill.fore_color.rgb = AZUL; n.line.fill.background(); n.shadow.inherit = False
    caixa(s, 1.05, y+0.22, 0.34, 0.25, str(i+1), 12, BRANCO, True, TIT, align=PP_ALIGN.CENTER, espaco=1)
    caixa(s, 1.55, y+0.12, 5.6, 0.3, t, 14.5, TINTA, True, TXT, espaco=1)
    caixa(s, 7.2, y+0.15, 5.05, 0.4, d, 12, CINZA, False, TXT, espaco=1.15)
    y += 0.78
retangulo(s, 0.85, y+0.12, 11.6, 0.78, AZUL, None, 0.16)
caixa(s, 1.15, y+0.3, 11.0, 0.42,
      "Causa raiz: falta uma camada de confiança entre os negócios locais. É exatamente o Desafio 2.",
      17, BRANCO, True, TXT, espaco=1)
rodape(s)

# ══════════════════════ 4 · A SOLUÇÃO ══════════════════════
s = slide(BRANCO)
faixa_titulo(s, "A solução", "Sou+Olímpia",
             "Uma camada de interoperabilidade entre os negócios da cidade. Cada negócio recebe uma credencial "
             "verificável; cada morador, a sua. Qualquer negócio emite um registro assinado — e qualquer outro verifica, "
             "sozinho, sem consultar ninguém.")
pilares = [
    ("Identidade", "A prefeitura assina a credencial que diz que o negócio existe, é de Olímpia e está na rede.", AZUL),
    ("Verificação", "Uma loja valida o registro de outra usando só a chave pública da rede. Offline.", VERDE),
    ("Circulação", "O primeiro caso de uso: cartela de carimbos que premia visitar lojas diferentes.", LARANJA),
]
for i,(t,d,cor) in enumerate(pilares):
    x = 0.85 + i*3.95
    retangulo(s, x, 3.5, 3.65, 2.35, BRANCO, LINHA, 0.06, 1.0)
    topo = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, In(x), In(3.5), In(3.65), In(0.1))
    topo.fill.solid(); topo.fill.fore_color.rgb = cor; topo.line.fill.background(); topo.shadow.inherit=False
    caixa(s, x+0.3, 3.85, 3.05, 0.4, t, 20, TINTA, True, TIT, espaco=1)
    caixa(s, x+0.3, 4.4, 3.05, 1.3, d, 13.5, CINZA, False, TXT, espaco=1.3)
rodape(s)

# ══════════════════════ 5 · COMO FUNCIONA ══════════════════════
s = slide(FUNDO)
faixa_titulo(s, "Como funciona", "A confiança viaja junto com o dado")
etapas = [
    ("LOJA A", "Emite um carimbo\nassinado com a\nprópria chave", VERMELHO),
    ("MORADOR", "Guarda o carimbo\nna carteira do\nseu aparelho", AZUL),
    ("LOJA B", "Verifica o carimbo\nda Loja A sozinha,\nsem consultar a Loja A", VERDE),
    ("REDE", "Fecha a cartela,\nemite o vale e\nimpede resgate duplo", LARANJA),
]
for i,(t,d,cor) in enumerate(etapas):
    x = 0.85 + i*2.98
    retangulo(s, x, 2.6, 2.6, 2.1, BRANCO, LINHA, 0.06, 1.0)
    caixa(s, x+0.25, 2.85, 2.1, 0.3, t, 11, cor, True, TIT, espaco=1)
    caixa(s, x+0.25, 3.25, 2.15, 1.3, d, 13.5, TINTA, False, TXT, espaco=1.25)
    if i < 3:
        caixa(s, x+2.62, 3.4, 0.35, 0.4, "→", 22, CINZA2, True, TIT, align=PP_ALIGN.CENTER, espaco=1)
retangulo(s, 0.85, 5.0, 11.6, 1.35, AZUL_CLARO, None, 0.08)
caixa(s, 1.2, 5.25, 11.0, 0.9,
      "O ponto está no terceiro quadro: a Loja B confia num registro emitido pela Loja A sem precisar confiar na Loja A,\n"
      "e sem que exista uma planilha central que alguém precise manter. É isso que substitui o grupo de WhatsApp.",
      15, AZUL_ESC, False, TXT, espaco=1.3)
rodape(s)

# ══════════════════════ 6 · O DIFERENCIAL ══════════════════════
s = slide(BRANCO)
faixa_titulo(s, "Por que não é mais um cashback", "A recompensa cresce com o número\nde lojas, não com o valor gasto")
retangulo(s, 0.85, 3.1, 5.6, 2.6, C(0xFB,0xEC,0xEC), C(0xE8,0xC6,0xC4), 0.06, 1.0)
caixa(s, 1.2, 3.35, 5.0, 0.35, "Desconto linear é soma zero", 18, VERMELHO, True, TIT, espaco=1)
caixa(s, 1.2, 3.85, 4.95, 1.7,
      "Se todas as lojas dão 10%, ninguém ganha participação. Redistribui o mesmo cliente entre concorrentes "
      "e a cidade inteira vende mais barato no mês em que já tem menos caixa.", 14, CINZA, False, TXT, espaco=1.35)
retangulo(s, 6.85, 3.1, 5.6, 2.6, C(0xED,0xF7,0xF0), C(0xB8,0xDD,0xC6), 0.06, 1.0)
caixa(s, 7.2, 3.35, 5.0, 0.35, "Progressão por lojas é circulação", 18, VERDE, True, TIT, espaco=1)
caixa(s, 7.2, 3.85, 4.95, 1.7,
      "Aumenta o número de estabelecimentos por cliente em vez de redistribuir o mesmo cliente. "
      "E é a única coisa que uma placa de 10% na porta não consegue fazer.", 14, CINZA, False, TXT, espaco=1.35)
caixa(s, 0.85, 6.05, 11.6, 0.6,
      "O vale é em reais, não em percentual: R$ 30 é legível para quem tem mediana de admissão de R$ 2.100.",
      14, CINZA, False, TXT, espaco=1.2)
rodape(s)

# ══════════════════════ 7 · SEGURANÇA ══════════════════════
s = slide(FUNDO)
faixa_titulo(s, "Segurança de dados", "A rede funciona sabendo\no mínimo sobre as pessoas")
linhas = [
    ("Nome do morador", "não guardamos", VERDE),
    ("CPF", "não guardamos", VERDE),
    ("Valor exato da compra", "não guardamos — só a faixa", VERDE),
    ("O que foi comprado", "não guardamos", VERDE),
    ("Loja, data e faixa de valor", "guardamos — é o que define o carimbo", CINZA),
    ("Identificador aleatório da carteira", "guardamos — descartável, o morador gera outro", CINZA),
]
y = 2.45
for t, d, cor in linhas:
    retangulo(s, 0.85, y, 11.6, 0.56, BRANCO, LINHA, 0.2, 0.75)
    caixa(s, 1.15, y+0.14, 4.6, 0.3, t, 14.5, TINTA, True, TXT, espaco=1)
    caixa(s, 5.9, y+0.14, 6.3, 0.3, d, 13.5, cor, False, TXT, espaco=1)
    y += 0.66
caixa(s, 0.85, y+0.1, 11.6, 0.9,
      "Assinatura ECDSA P-256 gerada no próprio navegador · verificação offline · credencial revogável a qualquer momento\n"
      "· vale com número de série que só pode ser resgatado uma vez.",
      14, CINZA, False, TXT, espaco=1.3)
rodape(s)

# ══════════════════════ 8 · ACESSIBILIDADE ══════════════════════
s = slide(BRANCO)
faixa_titulo(s, "Acessibilidade", "Feito para ser usado no balcão,\npor qualquer pessoa")
itens = [
    "Navegação completa por teclado, com foco sempre visível",
    "Cada verificação é anunciada por leitor de tela",
    "Contraste WCAG AA — amarelo e laranja da marca nunca viram texto",
    "Alvos de toque de 46 pixels, para usar com uma mão só",
    "Nenhum estado é comunicado apenas por cor",
    "Animação desligada para quem pediu redução de movimento",
]
y = 2.9
for i, it in enumerate(itens):
    col = i % 2
    row = i // 2
    x = 0.85 + col*5.9
    yy = y + row*0.95
    mk = s.shapes.add_shape(MSO_SHAPE.OVAL, In(x), In(yy+0.05), In(0.28), In(0.28))
    mk.fill.solid(); mk.fill.fore_color.rgb = VERDE; mk.line.fill.background(); mk.shadow.inherit=False
    caixa(s, x, yy+0.09, 0.28, 0.25, "✓", 11, BRANCO, True, TIT, align=PP_ALIGN.CENTER, espaco=1)
    caixa(s, x+0.45, yy, 5.1, 0.8, it, 14.5, TINTA, False, TXT, espaco=1.3)
rodape(s)

# ══════════════════════ 9 · DEMONSTRAÇÃO ══════════════════════
s = slide(FUNDO)
faixa_titulo(s, "Entrega obrigatória", "O que vocês vão ver rodando",
             "Protótipo funcional, sem servidor e sem internet. Toda a criptografia acontece no navegador.")
demo = [
    "A prefeitura credencia os quatro negócios",
    "A Padaria carimba a carteira do morador",
    "A Farmácia verifica o carimbo da Padaria sozinha",
    "Três lojas distintas fecham a cartela e liberam o vale",
    "O vale é resgatado — e a segunda tentativa é recusada",
    "Um carimbo adulterado é rejeitado na hora",
]
y = 3.15
for i, d in enumerate(demo):
    n = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, In(0.85), In(y), In(0.42), In(0.42))
    n.adjustments[0] = 0.25
    n.fill.solid(); n.fill.fore_color.rgb = AZUL if i < 4 else VERMELHO
    n.line.fill.background(); n.shadow.inherit = False
    caixa(s, 0.85, y+0.08, 0.42, 0.3, str(i+1), 13, BRANCO, True, TIT, align=PP_ALIGN.CENTER, espaco=1)
    caixa(s, 1.45, y+0.06, 10.8, 0.36, d, 16, TINTA, False, TXT, espaco=1)
    y += 0.56
caixa(s, 0.85, y+0.15, 11.6, 0.5,
      "Os dois últimos passos são os que provam a tese: a rede recusa o que não deveria aceitar.",
      14, CINZA, False, TXT, espaco=1.2)
rodape(s)

# ══════════════════════ 10 · GOVERNANÇA ══════════════════════
s = slide(BRANCO)
faixa_titulo(s, "Governança", "A prefeitura coordena — e não paga")
retangulo(s, 0.85, 2.75, 5.6, 2.0, BRANCO, LINHA, 0.06, 1.0)
caixa(s, 1.2, 3.0, 5.0, 0.35, "O que a prefeitura faz", 17, AZUL_ESC, True, TIT, espaco=1)
caixa(s, 1.2, 3.45, 4.95, 1.2,
      "Assina credenciais, chancela o programa e recebe os indicadores de circulação. "
      "Nada mais que isso.", 14, CINZA, False, TXT, espaco=1.3)
retangulo(s, 6.85, 2.75, 5.6, 2.0, BRANCO, LINHA, 0.06, 1.0)
caixa(s, 7.2, 3.0, 5.0, 0.35, "O que ela não faz", 17, VERMELHO, True, TIT, espaco=1)
caixa(s, 7.2, 3.45, 4.95, 1.2,
      "Não custeia desconto. Se custeasse, viraria subsídio a consumo — exigindo lei, dotação, "
      "licitação e prestação de contas ao TCE.", 14, CINZA, False, TXT, espaco=1.3)
retangulo(s, 0.85, 5.05, 11.6, 1.35, AZUL_CLARO, None, 0.08)
caixa(s, 1.2, 5.28, 11.0, 0.95,
      "Encaixe legal: Olímpia já tem o Observatório do Turismo (Lei 5.060/2025) e o SMITS (Lei 5.343/2026), "
      "cuja finalidade é produzir e integrar informação estratégica.\nO programa entra como módulo de varejo — "
      "estender uma lei que existe, em vez de aprovar uma nova. A confirmar com a procuradoria.",
      14.5, AZUL_ESC, False, TXT, espaco=1.3)
rodape(s)

# ══════════════════════ 11 · HONESTIDADE ══════════════════════
s = slide(FUNDO)
faixa_titulo(s, "O que ainda não sabemos", "Os limites, ditos por nós\nantes de alguém perguntar")
lim = [
    ("Não temos evidência de que o varejo caia na baixa",
     "A sazonalidade medida é de serviços. Fomos verificar o varejo e o emprego formal é plano o ano todo."),
    ("O programa não fecha o vale, e nenhuma tática fecha",
     "Olímpia tem uma loja para cada 49 habitantes, capacidade dimensionada para o turista. Dá para reduzir a amplitude."),
    ("A premissa mais arriscada ainda não foi testada",
     "Se existe demanda adiável do morador que responda a desconto. Testável com 3 a 5 lojas e um grupo de controle."),
]
y = 2.65
for t, d in lim:
    retangulo(s, 0.85, y, 11.6, 1.15, BRANCO, C(0xE8,0xC6,0xC4), 0.08, 1.0)
    barra = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, In(0.85), In(y), In(0.08), In(1.15))
    barra.fill.solid(); barra.fill.fore_color.rgb = LARANJA
    barra.line.fill.background(); barra.shadow.inherit = False
    caixa(s, 1.25, y+0.18, 10.9, 0.32, t, 16, TINTA, True, TXT, espaco=1)
    caixa(s, 1.25, y+0.58, 10.9, 0.45, d, 13.5, CINZA, False, TXT, espaco=1.2)
    y += 1.3
caixa(s, 0.85, y+0.1, 11.6, 0.5,
      "Dizer isso pontua mais do que fingir certeza — e é o que separa diagnóstico de chute.",
      14, CINZA, False, TXT, espaco=1.2)
rodape(s)

# ══════════════════════ ECONOMIA 1 · PONTO DE EQUILÍBRIO ══════════════════════
s = slide(BRANCO)
faixa_titulo(s, "Quanto isso rende", "O desenho do vale decide\nse o comerciante ganha")
caixa(s, 0.85, 2.25, 11.6, 0.6,
      "Incrementalidade mínima para a loja não perder dinheiro — quanto das visitas precisa ser movimento que não existiria sem o programa.",
      15, CINZA, False, TXT, espaco=1.25)
cols = ["Desenho da cartela", "Ticket R$ 40", "Ticket R$ 60", "Ticket R$ 90"]
larguras = [4.6, 2.33, 2.33, 2.34]
linhas_be = [
    ("3 carimbos · vale R$ 30", "60%", "45%", "30%", VERMELHO),
    ("3 carimbos · vale R$ 15", "33%", "22%", "15%", CINZA),
    ("5 carimbos · vale R$ 30", "41%", "30%", "20%", CINZA),
    ("5 carimbos · vale R$ 20", "30%", "20%", "13%", VERDE),
    ("5 carimbos · vale R$ 15", "22%", "15%", "10%", CINZA),
]
y = 2.92
x = 0.85
for i, c in enumerate(cols):
    caixa(s, x, y, larguras[i], 0.3, c.upper(), 9.5, CINZA2, True, TIT,
          align=PP_ALIGN.LEFT if i == 0 else PP_ALIGN.CENTER, espaco=1)
    x += larguras[i]
reg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, In(0.85), In(y+0.36), In(11.6), In(0.02))
reg.fill.solid(); reg.fill.fore_color.rgb = TINTA; reg.line.fill.background(); reg.shadow.inherit = False
y += 0.5
for nome, a, b, c, cor in linhas_be:
    destaque = cor in (VERDE, VERMELHO)
    if destaque:
        retangulo(s, 0.8, y-0.07, 11.7, 0.5,
                  C(0xED,0xF7,0xF0) if cor == VERDE else C(0xFB,0xEC,0xEC), None, 0.16)
    x = 0.85
    caixa(s, x, y, larguras[0], 0.34, nome, 14.5, TINTA, destaque, TXT, espaco=1)
    x += larguras[0]
    for j, v in enumerate((a, b, c)):
        caixa(s, x, y, larguras[j+1], 0.34, v, 15, cor if destaque else TINTA, True, TIT,
              align=PP_ALIGN.CENTER, espaco=1)
        x += larguras[j+1]
    y += 0.52
retangulo(s, 0.85, y+0.1, 11.6, 0.88, AZUL_CLARO, None, 0.1)
caixa(s, 1.2, y+0.26, 11.0, 0.6,
      "Programa de fidelidade costuma entregar de 10% a 30% de incrementalidade. O desenho de 3 carimbos com vale de R$ 30\n"
      "precisaria de 45% — não fecha. Cartela de 5 com vale de R$ 20 precisa de 20%, que está dentro do plausível.",
      14.5, AZUL_ESC, False, TXT, espaco=1.3)
rodape(s)

# ══════════════════════ ECONOMIA 2 · MONTE CARLO ══════════════════════
s = slide(FUNDO)
faixa_titulo(s, "Simulação", "20 mil cenários: 30 lojas,\ncartela de 5 e vale de R$ 20")
for i, (n, t) in enumerate([("81%", "das simulações dão lucro\npara a loja participante"),
                            ("R$ 4,82", "de receita incremental para\ncada real concedido em vale"),
                            ("20%", "de incrementalidade é\no ponto de virada")]):
    x = 0.85 + i*3.95
    retangulo(s, x, 2.2, 3.65, 1.25, BRANCO, LINHA, 0.08, 1.0)
    caixa(s, x+0.3, 2.38, 3.05, 0.45, n, 26, AZUL_ESC, True, TIT, espaco=1)
    caixa(s, x+0.3, 2.88, 3.15, 0.5, t, 12, CINZA, False, TXT, espaco=1.2)

caixa(s, 0.85, 3.72, 11.6, 0.3, "Faixas de resultado por mês — P10 é o cenário pessimista, P90 o otimista.",
      13.5, CINZA, False, TXT, espaco=1)
mc = [
    ("Cartelas fechadas na cidade", "256", "484", "838"),
    ("Visitas geradas pelo programa", "1.533", "2.905", "5.031"),
    ("Receita incremental da rede", "R$ 21.638", "R$ 46.691", "R$ 94.997"),
    ("Valor concedido em vales", "R$ 5.111", "R$ 9.683", "R$ 16.769"),
    ("Lucro líquido da rede", "R$ -1.361", "R$ 3.509", "R$ 13.382"),
    ("Lucro líquido por loja", "R$ -45", "R$ 117", "R$ 446"),
]
caixa(s, 0.85, 4.15, 5.3, 0.28, "MÉTRICA", 9.5, CINZA2, True, TIT, espaco=1)
for i, c in enumerate(("P10", "MEDIANA", "P90")):
    caixa(s, 6.15 + i*2.1, 4.15, 2.1, 0.28, c, 9.5, CINZA2, True, TIT, align=PP_ALIGN.CENTER, espaco=1)
reg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, In(0.85), In(4.48), In(11.6), In(0.02))
reg.fill.solid(); reg.fill.fore_color.rgb = TINTA; reg.line.fill.background(); reg.shadow.inherit = False
y = 4.6
for i, (rot, a, b, c) in enumerate(mc):
    if i == len(mc)-1:
        retangulo(s, 0.8, y-0.06, 11.7, 0.46, C(0xED,0xF7,0xF0), None, 0.16)
    caixa(s, 0.85, y, 5.3, 0.3, rot, 13.5, TINTA, i == len(mc)-1, TXT, espaco=1)
    for j, v in enumerate((a, b, c)):
        caixa(s, 6.15 + j*2.1, y, 2.1, 0.3, v, 13.5,
              VERDE if (i == len(mc)-1 and j > 0) else TINTA, j == 1, TIT,
              align=PP_ALIGN.CENTER, espaco=1)
    y += 0.38
rodape(s)

# ══════════════════════ 12 · CAPTURA PRINCIPAL ══════════════════════
CAP = Path.home()/"Ideathon/mvp/capturas"
s = slide(FUNDO)
faixa_titulo(s, "O protótipo", "A Loja B verificando o carimbo\nda Loja A, sozinha")
if (CAP/"mvp-verifica.png").exists():
    s.shapes.add_picture(str(CAP/"mvp-verifica.png"), In(2.55), In(2.35), height=In(3.9))
caixa(s, 0.85, 6.45, 11.6, 0.5,
      "Sem servidor, sem internet e sem planilha: a validação usa só a chave pública da prefeitura, no próprio aparelho.",
      14, CINZA, False, TXT, align=PP_ALIGN.CENTER, espaco=1.2)
rodape(s)

# ══════════════════════ 13 · PLANO B ══════════════════════
s = slide(BRANCO)
faixa_titulo(s, "Plano B", "Capturas da demonstração")
if (CAP/"mvp-rede.png").exists():
    s.shapes.add_picture(str(CAP/"mvp-rede.png"), In(0.85), In(2.45), width=In(5.6))
if (CAP/"mvp-carteira.png").exists():
    s.shapes.add_picture(str(CAP/"mvp-carteira.png"), In(6.85), In(2.45), width=In(5.6))
caixa(s, 0.85, 6.25, 5.6, 0.4, "Credenciamento dos negócios pela prefeitura", 13, CINZA, False, TXT, align=PP_ALIGN.CENTER, espaco=1)
caixa(s, 6.85, 6.25, 5.6, 0.4, "Carteira do morador, sem nome e sem CPF", 13, CINZA, False, TXT, align=PP_ALIGN.CENTER, espaco=1)
rodape(s)

# ══════════════════════ 14 · FECHAMENTO ══════════════════════
s = slide(BRANCO)
faixa = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, In(W), In(0.22))
faixa.fill.solid(); faixa.fill.fore_color.rgb = AZUL; faixa.line.fill.background(); faixa.shadow.inherit = False
if LOGO.exists():
    s.shapes.add_picture(str(LOGO), In(1.0), In(0.95), height=In(1.5))
caixa(s, 1.0, 2.9, 11.0, 1.9,
      "“Olímpia fatura 26% do seu ano de serviços em dois meses.\n"
      "Medimos isso com o ISS mensal do Tesouro Nacional — e descobrimos\n"
      "que o problema não é falta de cliente. É falta de uma camada que\n"
      "permita os negócios da cidade agirem juntos.”",
      26, TINTA, True, TIT, espaco=1.25)
retangulo(s, 1.0, 5.15, 11.3, 1.05, AZUL_CLARO, None, 0.08)
caixa(s, 1.35, 5.42, 10.7, 0.6,
      "Sou+Olímpia · a rede de confiança que a cidade ainda não tem — e o programa de circulação que roda em cima dela.",
      16, AZUL_ESC, True, TXT, espaco=1.2)
caixa(s, 1.0, 6.5, 11.3, 0.3,
      "Grupo 4 · Geise · Bruno · Alan · Naisa · Renan · Alan · Eduardo", 12, CINZA2, False, TXT, espaco=1)

prs.save(str(SAIDA))
print("salvo:", SAIDA, SAIDA.stat().st_size, "bytes,", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
