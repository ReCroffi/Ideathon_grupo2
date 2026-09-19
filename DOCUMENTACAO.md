# Sou+Olímpia — documentação do projeto

Grupo 4 · Ideathon OlimpiaLab 2026 · Desafio 2 (Olímpia Conecta / Mundo Lógico)

---

## 0. Decisões fechadas pelo grupo

**Nome: Sou+Olímpia.** Mantido. Não conflita com a plataforma municipal Conecta+ Olímpia, e toda a identidade já está pronta — logo, os dois aplicativos, o deck, os PDFs e o repositório.

**Escopo: restaurantes, como recorte de validação.** A rede é aberta a qualquer negócio da cidade por construção; começamos por restaurantes porque é onde a sazonalidade está comprovada — restaurante é serviço, e a série de ISS mede serviços. Validar num setor só reduz a variável e torna o piloto mensurável. Os quatro estabelecimentos do protótipo são restaurantes: Cantina da Praça, Tempero Caseiro, Beira-Rio Peixaria e Burger da Esquina.

**Foco: a rede.** A entrega é a camada de interoperabilidade — credenciais assinadas, verificação offline entre estabelecimentos, vale com QR assinado, resgate único e credencial revogável. O programa de cartela é o primeiro caso de uso rodando em cima dela, não o produto. Essa ordem importa: o Desafio 2 exige "uma rede ou sistema de interoperabilidade demonstrado em funcionamento", e um aplicativo de descontos sozinho não atenderia ao requisito obrigatório.

**Observação de verificação:** a Lei nº 5.275/2026 e o programa Olímpia+ Movimento vieram do texto do grupo e não foram verificados nesta documentação. As leis lidas diretamente, nos boletins do Observatório do Turismo, são a **5.060/2025** (cria o OTO) e a **5.343/2026** (institui o SMITS).

## 1. Canvas de Solução para Problema Complexo

### Problema

**Que problema complexo queremos enfrentar?**
A economia de serviços de Olímpia opera em dois regimes. Janeiro e julho concentram 26% da arrecadação anual de ISS; maio e junho marcam 0,77 e 0,78 num índice em que a média do ano é 1,00. Janeiro vale 1,96× maio. Oito dos doze meses ficam abaixo da média do próprio ano.

**Quem é mais afetado?**
Os 3.801 trabalhadores de alojamento, alimentação, arte, cultura e lazer — o setor que o CAGED mostra sendo montado de junho a novembro (+205 vagas) e desmontado de dezembro a maio (−134). Janeiro sozinho corta 88 vagas: é o mês de maior faturamento e de maior demissão ao mesmo tempo. Depois deles, os restaurantes e prestadores que carregam custo fixo o ano inteiro contra uma receita que some por seis meses.

**Duas ou três causas principais**
1. A demanda é turística e obedece ao calendário escolar. Feriado não compensa: o Carnaval tem a maior ocupação do ano, 80,6%, e cai em fevereiro, um mês que marca 0,81. A cidade responde a duração, não a intensidade.
2. A capacidade instalada foi dimensionada para o turista, não para o morador — 1.131 unidades de comércio para 55 mil habitantes, uma a cada 49.
3. Ação coletiva entre negócios, que seria a saída, hoje roda em grupo de WhatsApp e planilha compartilhada, onde ninguém consegue verificar o que o outro afirma.

**Várias áreas da cidade:** emprego e renda, arrecadação municipal, mercado imobiliário (54,8% de crescimento no estoque de domicílios entre 2010 e 2022, contra 10% de população) e capacidade de atendimento público em janeiro e julho.

### Nossa solução

**O que é, em poucas frases**
Sou+Olímpia é uma camada de confiança entre os negócios da cidade. A prefeitura assina uma credencial dizendo que o negócio existe, é de Olímpia e está na rede. A partir daí, qualquer estabelecimento emite registros assinados — carimbo, vale, oferta — e qualquer outro verifica esses registros sozinho, sem telefonar para o emissor e sem planilha central que alguém precise manter.

Sobre essa camada roda o primeiro caso de uso: uma cartela de carimbos em que a recompensa cresce com o **número de estabelecimentos diferentes** visitados no mês.

**O que faz de diferente do que existe hoje**
Desconto linear redistribui o mesmo cliente entre concorrentes e é jogo de soma zero. Progressão por estabelecimentos distintos aumenta quantos lugares cada cliente visita — é motor de circulação, não guerra de margem. E é a única coisa que uma placa de 10% na porta não consegue fazer.

O segundo diferencial é a verificação: hoje, para saber se o estabelecimento ao lado realmente participa da campanha, alguém precisa abrir um arquivo que outra pessoa mantém. Na rede, a prova viaja junto com o dado e é conferível offline.

### Impactos esperados

**Se o teste der certo, o que melhora na vida das pessoas**
O trabalhador sazonal ganha um instrumento que move poder de compra do semestre em que ele ganha para o semestre em que ele falta. O morador passa a ter benefício organizado numa cidade onde hoje **não existe desconto permanente de morador** — o de 50% que circula foi promoção de um dia só, no aniversário da cidade em 2022. O estabelecimento ganha movimento nos meses em que a estrutura está ociosa.

**Números que a simulação projeta** (20 mil cenários, 30 restaurantes, cartela de 5, vale de R$ 20): receita incremental da rede de R$ 46.691 por mês na mediana, contra R$ 9.683 concedidos em vales — R$ 4,82 de receita para cada real de desconto. Lucro mediano de R$ 117 por restaurante, com 81% das simulações no positivo.

**Efeitos em cadeia**
*Economia:* menos demissão em janeiro, se o quadro puder ser sustentado por movimento local.
*Dados e gestão pública:* hoje não existe nenhuma base de transações do varejo de Olímpia — foi isso que travou o nosso próprio diagnóstico. A rede produz esse dado desde o primeiro dia, e ele serve à prefeitura, à associação comercial e ao próprio comerciante.
*Turismo:* a mesma camada serve para pacotes conjuntos entre hotel, restaurante e passeio, que hoje não existem porque ninguém consegue verificar o parceiro.
*Segurança da informação:* a cidade passa a ter um padrão de credencial verificável reaproveitável por outras políticas.

### Pessoas envolvidas

**Quem sofre mais:** trabalhadores sazonais do turismo (3.801 postos formais) e donos de restaurante e pequeno comércio de rua, que carregam custo fixo o ano todo.

**Quem decide ou influencia:** Prefeitura, pela Secretaria de Desenvolvimento Econômico; o Observatório do Turismo de Olímpia e o SMITS, que já têm competência legal para produzir e integrar informação estratégica; a Câmara Municipal, se houver necessidade de extensão legal; a associação comercial, que já organiza campanha coletiva há décadas.

**Quem pode ser parceiro:** Thermas dos Laranjais e Hot Beach — o Thermas já roda o contra-ciclo sozinho, com meia entrada para todos em maio, junho, agosto e setembro, de segunda a sexta, mediante doação de alimento. Sebrae, para mobilização dos estabelecimentos. As maquininhas e meios de pagamento, como trilho futuro em vez de concorrente.

### Como vamos testar

**O menor teste em até 30 dias**
De 3 a 5 restaurantes numa mesma rua, com 15% de desconto para morador durante duas semanas de um mês de vale. Comparação contra as duas semanas anteriores e contra o mesmo período do ano passado, com um grupo de controle de estabelecimentos parecidos que não participam. Hipótese e critério de sucesso registrados **antes** da coleta.

**Com quem e onde:** restaurantes de uma via de bairro, fora do eixo dos resorts, para medir o morador e não o turista.

**O que o teste responde:** se existe demanda adiável do morador que reage a desconto. É a premissa mais arriscada do projeto inteiro e custa perto de zero para testar.

### Apoios e recursos necessários

**Pessoas:** um articulador para recrutar os restaurantes, e alguém do OTO ou da Secretaria para assinar as credenciais.
**Tempo:** duas semanas de preparação e duas de coleta.
**Espaços:** uma rua comercial; nada de infraestrutura física.
**Dados:** já temos — série mensal de ISS via API do Tesouro, microdados do CAGED, Censo e CEMPRE do IBGE, boletins do OTO. Tudo no repositório, com os scripts que reproduzem.
**Materiais:** o protótipo já está pronto e roda offline no navegador. Para o piloto de campo bastam cartelas impressas e um formulário de coleta.
**Parcerias:** chancela da Prefeitura ou da associação comercial, que é o que dá legitimidade à credencial.

---

## 2. O que os dados comprovam, e o que não

### Comprovado

Os serviços de Olímpia têm sazonalidade forte e estável: índice 1,51 em janeiro e 1,46 em julho, contra 0,77 em maio e 0,78 em junho, com o mesmo desenho em três anos independentes. O emprego do turismo segue o mesmo calendário, montado antes da alta e desmontado depois dela.

### Não comprovado

Não existe dado público que mostre queda do varejo na baixa. O emprego formal do comércio, descontada a abertura de um hipermercado que sozinha responde por +107 vagas em maio, fechou 2025 com saldo de **−14 vagas**, sem padrão sazonal. Loja paga ICMS, que é estadual e não tem série mensal por município.

Também não há evidência de que o morador deixa de consumir na baixa. O morador está na cidade o ano todo — quem some é o visitante.

### Correção de um número que circulou

O texto do grupo diz "mais de um milhão de visitantes por ano". O dado é mais forte que isso: o OTO projeta **1,1 milhão só entre dezembro e janeiro**, e o Thermas dos Laranjais sozinho recebeu 1,85 milhão de visitantes em 2024, segundo o Theme Index da TEA/AECOM. Usar "por ano" subestima e enfraquece o argumento.

---

## 3. Solução construída

### 3.1 Camada de confiança

Credenciais de negócio e registros assinados com **ECDSA P-256**, gerados pela Web Crypto API no próprio navegador. A verificação é local: uma loja valida o carimbo de outra usando apenas a chave pública da prefeitura, sem internet e sem servidor. Credencial revogável — a prefeitura tira um negócio da rede e os carimbos e ofertas dele param de valer na hora.

### 3.2 Aplicativo do morador

Cartela do mês, lista de estabelecimentos credenciados e a página de descontos. Quando a cartela fecha, o vale aparece com **QR assinado** que carrega o vale inteiro, não só o número de série — o estabelecimento confere a assinatura no próprio aparelho.

### 3.3 Aplicativo do lojista

Carimba a cartela do cliente, verifica os carimbos das outras lojas, lê o QR e resgata o vale. Resgate duplo é recusado pela série. Tem também a tela de ofertas próprias e o console que mostra cada operação criptográfica acontecendo.

### 3.4 Privacidade por construção

A rede **não guarda** nome, CPF, valor exato da compra nem o que foi comprado. Guarda a loja, a data, a faixa de valor e um código aleatório de carteira que o morador pode descartar e gerar outro.

### 3.5 Acessibilidade

Navegação por teclado com foco visível, cada verificação anunciada por leitor de tela, contraste WCAG AA, alvos de toque de no mínimo 46 pixels, nenhum estado comunicado só por cor e animação desligada para quem configurou redução de movimento.

---

## 4. Modelo de financiamento do desconto

O desconto é custeado pelo estabelecimento onde o vale é resgatado, não pela prefeitura. Se o poder público custear, vira subsídio a consumo e passa a exigir lei, dotação orçamentária, licitação de plataforma e prestação de contas ao Tribunal de Contas. Mantendo o custo no comerciante, a prefeitura entra como operadora da camada de confiança — coordena, chancela e mede.

A lógica é a mesma que o Thermas já pratica: tarifa cheia o ano todo, desconto concentrado nos meses de vale e nos dias úteis. A margem da alta paga o desconto da baixa.

### O desenho do vale decide se fecha

Incrementalidade mínima para o restaurante não perder dinheiro, com margem bruta de 28%:

| Desenho da cartela | Ticket R$ 40 | R$ 60 | R$ 90 |
|---|---|---|---|
| 3 carimbos · vale R$ 30 | 60% | **45%** | 30% |
| 5 carimbos · vale R$ 30 | 41% | 30% | 20% |
| **5 carimbos · vale R$ 20** | 30% | **20%** | 13% |
| 5 carimbos · vale R$ 15 | 22% | 15% | 10% |

Programa de fidelidade costuma entregar de 10% a 30% de incrementalidade. O desenho de 3 carimbos com vale de R$ 30 precisaria de 45% e **não fecha**. Cartela de 5 com vale de R$ 20 precisa de 20%, que está dentro do plausível. No piloto de 3 restaurantes, manter 3 carimbos mas **baixar o vale para R$ 15**, que exige 22%.

---

## 5. Riscos

**Subsídio ao que já aconteceria.** O desconto pode premiar compra que ocorreria de qualquer forma. Mitigação: medir incrementalidade contra grupo de controle desde o piloto.

**Guerra de margem.** Se virar desconto linear, todos dão desconto e ninguém ganha participação — e a cidade vende mais barato no mês de menos caixa. Mitigação: a progressão é por estabelecimentos distintos, não por valor gasto.

**Indiferença.** Oito por cento sobre um ticket de R$ 40 valem R$ 3,20; ninguém abre aplicativo por isso. Mitigação: vale em reais, valor fixo e legível, e a progressão como mecânica de jogo.

**Incumbentes.** Nubank, PicPay, Mercado Pago e as maquininhas já fazem cashback com base maior. Mitigação: a defesa é a camada local, a regra municipal e o comerciante de rua que não está em nenhuma dessas bases — e o fato de que nenhum deles resolve o problema do enunciado, que é um negócio verificar o outro.

**Jurídico.** Qualquer desenho que envolva dinheiro público exige lei, licitação e prestação de contas. Mitigação: a prefeitura não toca no dinheiro.

---

## 6. Fontes

Tesouro Nacional (SICONFI, RREO Anexo 03, ente 3533908) · IBGE (Censo 2022, CEMPRE 2024, PIB dos Municípios 2023) · Ministério do Trabalho e Emprego (microdados do Novo CAGED, 12 meses de 2025) · Observatório do Turismo de Olímpia (boletins de expectativa, 2026) · Thermas dos Laranjais (tarifário oficial e calendário de promoções) · TEA/AECOM (Theme Index 2024).

Dados, scripts e protótipos no repositório. O diagnóstico completo está em `diagnostico/Olimpia-diagnostico-ideathon.pdf`.

---

## 7. Material produzido

| Arquivo | O que é |
|---|---|
| `mvp/mobile.html` | Os dois aplicativos — morador e restaurante — lado a lado no projetor, alternáveis no celular |
| `mvp/index.html` | Versão de mesa, com o painel da prefeitura e o console de confiança |
| `mvp/Sou+Olimpia-demo.mp4` | Demonstração de 60 segundos, sem áudio, para narrar por cima |
| `mvp/qr.js` | Codificador de QR próprio, validado contra implementação de referência e decodificado com OpenCV |
| `SouMaisOlimpia-pitch.pptx` | Deck de 17 slides, editável, com o vídeo embutido |
| `SouMaisOlimpia-roteiro-pitch.pdf` | Roteiro de 5 minutos, os 90 segundos da demo e 10 perguntas de jurado com resposta |
| `SouMaisOlimpia-decisoes.pdf` | Histórico das decisões do grupo |
| `diagnostico/` | Diagnóstico completo e painel interativo |
| `dados/` e `scripts/` | Séries usadas e os scripts que reproduzem tudo |
