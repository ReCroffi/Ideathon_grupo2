# Ideathon - OlimpiaLab - 2026

# Sou+Olímpia

## Grupo 4

Integrantes

- Geise
- Bruno
- Alan
- Naisa
- Renan
- Alan
- Eduardo

## Desafio 2 — Olímpia Conecta (Mundo Lógico)

> **A pergunta:** como conectar pequenos negócios, pessoas e dados com segurança?
>
> **A dor:** dependência de planilhas e mensagens soltas para formar parcerias.
>
> **A entrega obrigatória:** uma rede ou sistema de interoperabilidade demonstrado em funcionamento.
>
> **Aviso:** não precisa ser blockchain. O objetivo é resolver a confiança. Pode usar APIs, bancos de dados integrados ou credenciais verificáveis.

### O Problema

Como diminuir os impactos da sazonalidade nos negócios da cidade.

### Os cinco porquês

1. **Por que os negócios de Olímpia sofrem?**
   Porque o faturamento de serviços cai quase pela metade entre o pico e o vale. Índice sazonal do ISS: 1,51 em janeiro contra 0,77 em maio.

2. **Por que cai pela metade?**
   Porque a demanda é turística e o turista só vem nas férias escolares. Janeiro e julho concentram 26% do ISS do ano em 17% do calendário. Feriado não resolve: o Carnaval tem a maior ocupação do ano, 80,6%, e cai em fevereiro, um mês que marca 0,81. A cidade responde a duração, não a intensidade.

3. **Por que o negócio não compensa com o morador?**
   Porque a capacidade instalada foi dimensionada para mais de um milhão de visitantes no verão, não para 55 mil moradores. São 1.131 unidades de comércio, uma a cada 49 habitantes. Fechar o vale só com o morador exigiria de R$ 3.278 a R$ 8.195 a mais por domicílio por mês, contra uma mediana de admissão de R$ 2.100.

4. **Por que os negócios não atacam isso de forma coletiva?**
   Porque ação coletiva exige parceria entre negócios — campanha que manda o cliente de uma loja para outra, pacote que junta hotel, restaurante e passeio. Hoje isso se organiza em grupo de WhatsApp e planilha compartilhada, que quebra assim que passa de uma dúzia de participantes.

5. **Por que a planilha quebra?**
   Porque ninguém consegue verificar o que o outro afirma. Não existe camada comum de identidade e registro entre os negócios da cidade: cada um tem o seu caderno, e confiar no caderno do vizinho é um ato de fé.

**Causa raiz:** falta uma camada de confiança interoperável entre os negócios locais. Sem ela, nenhuma ação coletiva contra a sazonalidade escala além do grupo de WhatsApp.

É exatamente o que o Desafio 2 pede.

---

## O diagnóstico

Antes de propor solução, medimos o problema. Não existia nenhum estudo sobre sazonalidade do comércio de Olímpia, então construímos a série a partir de dado público.

| Indicador | Valor |
|---|---|
| Pico ÷ vale (serviços) | 1,96× |
| Janeiro + julho | 26% do ISS do ano |
| Mês mediano | 0,92 — abaixo da própria média do ano |
| Meses abaixo da média | 8 de 12 |
| Vale | maio (0,77) e junho (0,78) |
| Saldo de emprego no turismo | +205 vagas de jun a nov, −134 de dez a mai |
| Mediana de admissão | R$ 2.100 |
| Empregos de renda estável | 11.062 de 25.756 ocupados formais |

Três achados que mudaram o rumo do projeto:

**O emprego antecipa o turista.** Janeiro é o mês de maior faturamento e de maior demissão ao mesmo tempo: corta 88 vagas no turismo, porque o contrato temporário vence quando as férias acabam.

**O varejo pode não ser sazonal.** Toda a sazonalidade medida é de serviços — loja paga ICMS, não ISS. O único indicador de varejo disponível, o emprego formal, é plano o ano todo: saldo de −14 vagas em 2025 depois de descontar a abertura de um hipermercado que sozinha responde por +107 em maio. Não afirmamos o que não medimos.

**O maior player da cidade já roda o contra-ciclo.** O Thermas mantém tarifa única o ano inteiro, R$ 189 online, e concede meia entrada para todos em maio, junho, agosto e setembro, de segunda a sexta, mediante doação de alimento. O preço de tabela não sobe na alta: o preço efetivo cai na baixa, e o desconto vem disfarçado de ação social.

Detalhes, ressalvas e método completo: [`diagnostico/Olimpia-diagnostico-ideathon.pdf`](diagnostico/Olimpia-diagnostico-ideathon.pdf).

---

## A proposta

> Esta seção é a proposta em discussão pelo grupo, não uma decisão fechada.

**Sou+Olímpia** é uma camada de interoperabilidade entre os negócios da cidade. Cada negócio recebe uma credencial verificável; cada morador recebe a sua. Qualquer negócio pode emitir um registro assinado — um carimbo, um voucher, uma indicação, um item de pacote conjunto — e qualquer outro negócio pode verificar esse registro sem telefonar para o emissor e sem depender de uma planilha central que alguém precise manter.

A primeira aplicação rodando sobre essa camada é o **desconto progressivo por lojas visitadas**, que é por definição uma parceria multi-negócio:

- O morador junta carimbos de **lojas diferentes** dentro do mês, um por loja, em compras acima de um valor mínimo.
- Cartela completa vira um vale em reais, resgatável em qualquer loja da rede no mês seguinte — que na baixa temporada também é mês de vale.
- Quem paga o vale é a loja onde ele for resgatado. Em agregado se compensa: cada loja concede uns poucos vales e recebe várias visitas que não teria.

A diferença em relação a um desconto comum é o que ele faz com o cliente: desconto linear redistribui o mesmo cliente entre concorrentes, e é jogo de soma zero. Progressão por lojas distintas **aumenta o número de estabelecimentos por cliente**. É um motor de circulação, não uma guerra de margem. E é a única coisa que uma placa de 10% na porta não consegue fazer.

**Papel da prefeitura:** coordenar, chancelar e medir — nunca custear. Se o poder público paga o desconto, vira subsídio a consumo e exige lei, dotação, licitação e prestação de contas ao TCE. Mantendo o custo no comerciante, a prefeitura entra como operadora da camada de confiança. E há um encaixe pronto: o **SMITS**, Sistema Municipal de Inteligência Turística Sustentável, instituído pela Lei Municipal 5.343/2026, junto ao Observatório do Turismo criado pela Lei 5.060/2025. A finalidade declarada do SMITS é produção, integração e disseminação de informações estratégicas. O programa entra como módulo de varejo dele — estender uma lei que existe, em vez de aprovar uma nova.

**O ativo escondido:** hoje não existe nenhum dado de transação do varejo de Olímpia. Foi isso que travou o nosso diagnóstico. A rede produz esse dado desde o primeiro dia. Mesmo que o efeito de estímulo seja pequeno, o dataset tem valor para a prefeitura, para a associação comercial e para o próprio comerciante.

### O que ainda não sabemos

Honestidade sobre os limites, porque isso vale mais que otimismo:

- Não temos evidência de que o varejo caia na baixa. Temos evidência de que os **serviços** caem.
- O programa não fecha o vale, e nenhuma tática de varejo fecha. Dá para reduzir a amplitude.
- A premissa mais arriscada é existir demanda adiável do morador que responda a desconto. Isso é testável antes de escrever código: 3 a 5 lojas, 15% para morador, duas semanas de um mês de vale, contra um grupo de controle de lojas parecidas, com hipótese e critério de sucesso registrados antes da coleta.

---

## O que tem neste repositório

```
diagnostico/
  Olimpia-diagnostico-ideathon.pdf   diagnóstico completo, 5 páginas, com colinha de pitch
  diagnostico-fonte.html             fonte do PDF
  painel-olimpia.html                painel interativo, abre em qualquer navegador
dados/
  dados.json                         todos os indicadores consolidados
  iss_series.json                    série mensal de ISS, 2023-2025
  caged-olimpia-2025/                microdados do CAGED filtrados para Olímpia, 12 meses
scripts/
  iss.py                             baixa a série de ISS da API do SICONFI
  extrai.py                          extrai Olímpia dos microdados do CAGED
  consolida.py                       consolida tudo em dados.json
  build.py                           gera o painel
```

### Como reproduzir

```bash
python3 -m venv .venv && .venv/bin/pip install py7zr
.venv/bin/python scripts/iss.py         # série de ISS via API do Tesouro
.venv/bin/python scripts/consolida.py   # consolida os indicadores
.venv/bin/python scripts/build.py       # gera o painel
```

Os microdados do CAGED vêm do FTP do Ministério do Trabalho, um arquivo de ~55 MB por mês, em `ftp://ftp.mtps.gov.br/pdet/microdados/NOVO CAGED/2025/`. O FTP roda a cerca de 80 KB/s e derruba a conexão antes do fim, então o download precisa de retry com `curl -C -` até bater o tamanho exato do arquivo.

## Fontes

- **Tesouro Nacional / SICONFI** — API do RREO Anexo 03, ente 3533908. Série mensal de ISS, 2023-2025.
- **IBGE** — Censo 2022, CEMPRE 2024, PIB dos Municípios 2023, Panorama municipal.
- **Ministério do Trabalho e Emprego** — microdados do Novo CAGED, 12 meses de 2025.
- **Observatório do Turismo de Olímpia** — boletins de expectativa de ocupação e fluxo, 9 períodos de 2026.
- **Thermas dos Laranjais** — tarifário oficial e calendário de promoções 2026.
- **TEA / AECOM** — Theme Index 2024.
