/* Codificador QR mínimo — modo byte, nível de correção M, versões 1 a 10.
   Suficiente para o payload do vale e sem dependência externa. */
const QR = (function () {
  "use strict";

  // ---------- GF(256), polinômio primitivo 0x11D ----------
  const EXP = new Uint8Array(512), LOG = new Uint8Array(256);
  (function () {
    let x = 1;
    for (let i = 0; i < 255; i++) { EXP[i] = x; LOG[x] = i; x <<= 1; if (x & 0x100) x ^= 0x11D; }
    for (let i = 255; i < 512; i++) EXP[i] = EXP[i - 255];
  })();
  const mul = (a, b) => (a && b) ? EXP[LOG[a] + LOG[b]] : 0;

  function rsGen(n) {                       // coeficientes do menor para o maior grau
    let g = [1];
    for (let i = 0; i < n; i++) {
      const ng = new Array(g.length + 1).fill(0);
      for (let j = 0; j < g.length; j++) { ng[j] ^= mul(g[j], EXP[i]); ng[j + 1] ^= g[j]; }
      g = ng;
    }
    return g.reverse();                     // maior grau primeiro, líder = 1
  }
  function rsEcc(data, ecLen) {
    const gen = rsGen(ecLen);
    const buf = new Uint8Array(data.length + ecLen);
    buf.set(data);
    for (let i = 0; i < data.length; i++) {
      const f = buf[i];
      if (f) for (let j = 1; j < gen.length; j++) buf[i + j] ^= mul(gen[j], f);
    }
    return Array.from(buf.slice(data.length));
  }

  // ---------- tabelas para nível M, versões 1..10 ----------
  // [codewords de EC por bloco, blocos grupo 1, dados g1, blocos g2, dados g2]
  const BLOCOS_M = {
    1:[10,1,16,0,0], 2:[16,1,28,0,0], 3:[26,1,44,0,0], 4:[18,2,32,0,0], 5:[24,2,43,0,0],
    6:[16,4,27,0,0], 7:[18,4,31,0,0], 8:[22,2,38,2,39], 9:[22,3,36,2,37], 10:[26,4,43,1,44]
  };
  const CAP_M = {1:14,2:26,3:42,4:62,5:84,6:106,7:122,8:152,9:180,10:213};
  const ALINHA = {
    1:[], 2:[6,18], 3:[6,22], 4:[6,26], 5:[6,30],
    6:[6,34], 7:[6,22,38], 8:[6,24,42], 9:[6,26,46], 10:[6,28,50]
  };

  function bch15(fmt) {                     // informação de formato: BCH(15,5)
    let v = fmt << 10;
    for (let i = 4; i >= 0; i--) if (v & (1 << (i + 10))) v ^= 0x537 << i;
    return (((fmt << 10) | v) ^ 0x5412) & 0x7FFF;
  }
  function bch18(ver) {                     // informação de versão: BCH(18,6)
    let v = ver << 12;
    for (let i = 5; i >= 0; i--) if (v & (1 << (i + 12))) v ^= 0x1F25 << i;
    return ((ver << 12) | v) & 0x3FFFF;
  }

  // ---------- montagem ----------
  function reservado(tam, ver) {            // true onde não entram dados
    const r = Array.from({length: tam}, () => new Uint8Array(tam));
    const marca = (x, y, w, h) => {
      for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
        const yy = y + j, xx = x + i;
        if (yy >= 0 && yy < tam && xx >= 0 && xx < tam) r[yy][xx] = 1;
      }
    };
    marca(0, 0, 9, 9);                      // localizador + formato (canto superior esquerdo)
    marca(tam - 8, 0, 8, 9);                // superior direito
    marca(0, tam - 8, 9, 8);                // inferior esquerdo
    for (let i = 0; i < tam; i++) { r[6][i] = 1; r[i][6] = 1; }   // temporização
    const al = ALINHA[ver];
    for (const cy of al) for (const cx of al) {
      const perto = (a, b) => Math.abs(a - b) < 7;
      if ((perto(cx, 6) && perto(cy, 6)) ||
          (perto(cx, tam - 7) && perto(cy, 6)) ||
          (perto(cx, 6) && perto(cy, tam - 7))) continue;
      marca(cx - 2, cy - 2, 5, 5);
    }
    if (ver >= 7) { marca(tam - 11, 0, 3, 6); marca(0, tam - 11, 6, 3); }
    return r;
  }

  function desenhaFixos(m, tam, ver) {
    const localizador = (x, y) => {
      for (let j = -1; j <= 7; j++) for (let i = -1; i <= 7; i++) {
        const yy = y + j, xx = x + i;
        if (yy < 0 || yy >= tam || xx < 0 || xx >= tam) continue;
        const borda = (i >= 0 && i <= 6 && (j === 0 || j === 6)) || (j >= 0 && j <= 6 && (i === 0 || i === 6));
        const miolo = i >= 2 && i <= 4 && j >= 2 && j <= 4;
        m[yy][xx] = (borda || miolo) ? 1 : 0;
      }
    };
    localizador(0, 0); localizador(tam - 7, 0); localizador(0, tam - 7);
    for (let i = 8; i < tam - 8; i++) { const v = i % 2 === 0 ? 1 : 0; m[6][i] = v; m[i][6] = v; }
    const al = ALINHA[ver];
    for (const cy of al) for (const cx of al) {
      const perto = (a, b) => Math.abs(a - b) < 7;
      if ((perto(cx, 6) && perto(cy, 6)) ||
          (perto(cx, tam - 7) && perto(cy, 6)) ||
          (perto(cx, 6) && perto(cy, tam - 7))) continue;
      for (let j = -2; j <= 2; j++) for (let i = -2; i <= 2; i++)
        m[cy + j][cx + i] = (Math.max(Math.abs(i), Math.abs(j)) !== 1) ? 1 : 0;
    }
    m[tam - 8][8] = 1;                      // módulo escuro obrigatório
    if (ver >= 7) {
      const vi = bch18(ver);
      for (let i = 0; i < 18; i++) {
        const b = (vi >> i) & 1, r = Math.floor(i / 3), c = i % 3;
        m[tam - 11 + c][r] = b;
        m[r][tam - 11 + c] = b;
      }
    }
  }

  function gravaFormato(m, tam, mascara) {
    const f = bch15((0 << 3) | mascara);    // 00 = nível M
    for (let i = 0; i < 15; i++) {
      const b = (f >> i) & 1;
      if (i < 6) m[i][8] = b;
      else if (i < 8) m[i + 1][8] = b;
      else if (i === 8) m[8][7] = b;
      else m[8][14 - i] = b;
      if (i < 8) m[8][tam - 1 - i] = b;
      else m[tam - 15 + i][8] = b;
    }
  }

  const MASCARAS = [
    (r, c) => (r + c) % 2 === 0,
    (r, c) => r % 2 === 0,
    (r, c) => c % 3 === 0,
    (r, c) => (r + c) % 3 === 0,
    (r, c) => (Math.floor(r / 2) + Math.floor(c / 3)) % 2 === 0,
    (r, c) => ((r * c) % 2) + ((r * c) % 3) === 0,
    (r, c) => (((r * c) % 2) + ((r * c) % 3)) % 2 === 0,
    (r, c) => (((r + c) % 2) + ((r * c) % 3)) % 2 === 0
  ];

  function penalidade(m, tam) {
    let p = 0;
    // regra 1: sequências de 5+ iguais
    for (let dir = 0; dir < 2; dir++)
      for (let a = 0; a < tam; a++) {
        let run = 1;
        for (let b = 1; b < tam; b++) {
          const at = dir ? m[b][a] : m[a][b], ant = dir ? m[b - 1][a] : m[a][b - 1];
          if (at === ant) { run++; if (run === 5) p += 3; else if (run > 5) p += 1; }
          else run = 1;
        }
      }
    // regra 2: blocos 2x2
    for (let r = 0; r < tam - 1; r++) for (let c = 0; c < tam - 1; c++) {
      const v = m[r][c];
      if (v === m[r][c + 1] && v === m[r + 1][c] && v === m[r + 1][c + 1]) p += 3;
    }
    // regra 3: padrão 1:1:3:1:1 com 4 claros
    const A = [1,0,1,1,1,0,1,0,0,0,0], B = [0,0,0,0,1,0,1,1,1,0,1];
    const casa = (get, i, pat) => pat.every((v, k) => get(i + k) === v);
    for (let a = 0; a < tam; a++)
      for (let b = 0; b <= tam - 11; b++) {
        const gl = i => m[a][i], gc = i => m[i][a];
        if (casa(gl, b, A) || casa(gl, b, B)) p += 40;
        if (casa(gc, b, A) || casa(gc, b, B)) p += 40;
      }
    // regra 4: desequilíbrio claro/escuro
    let escuros = 0;
    for (let r = 0; r < tam; r++) for (let c = 0; c < tam; c++) escuros += m[r][c];
    const pct = (escuros * 100) / (tam * tam);
    p += Math.floor(Math.abs(pct - 50) / 5) * 10;
    return p;
  }

  /** Gera a matriz de módulos (0/1) para um texto. Retorna {tam, matriz, versao}. */
  function gerar(texto, versaoFixa, mascaraFixa) {
    const bytes = Array.from(new TextEncoder().encode(texto));
    let ver = versaoFixa || 0;
    if (!ver) {
      for (let v = 1; v <= 10; v++) if (bytes.length <= CAP_M[v]) { ver = v; break; }
      if (!ver) throw new Error("payload longo demais para versão 10 nível M");
    }
    if (bytes.length > CAP_M[ver]) throw new Error("payload não cabe na versão pedida");

    const [ecPorBloco, g1, d1, g2, d2] = BLOCOS_M[ver];
    const totalDados = g1 * d1 + g2 * d2;

    // fluxo de bits: modo 0100 + contagem (8 bits até v9) + dados
    const bits = [];
    const push = (val, n) => { for (let i = n - 1; i >= 0; i--) bits.push((val >> i) & 1); };
    push(0b0100, 4);
    push(bytes.length, ver <= 9 ? 8 : 16);
    for (const b of bytes) push(b, 8);
    const capBits = totalDados * 8;
    for (let i = 0; i < 4 && bits.length < capBits; i++) bits.push(0);   // terminador
    while (bits.length % 8) bits.push(0);
    const cw = [];
    for (let i = 0; i < bits.length; i += 8) cw.push(parseInt(bits.slice(i, i + 8).join(""), 2));
    const ENCHE = [0xEC, 0x11];
    for (let i = 0; cw.length < totalDados; i++) cw.push(ENCHE[i % 2]);

    // blocos
    const blocosD = [], blocosE = [];
    let p = 0;
    for (let i = 0; i < g1; i++) { const d = cw.slice(p, p + d1); p += d1; blocosD.push(d); blocosE.push(rsEcc(d, ecPorBloco)); }
    for (let i = 0; i < g2; i++) { const d = cw.slice(p, p + d2); p += d2; blocosD.push(d); blocosE.push(rsEcc(d, ecPorBloco)); }

    // intercalação
    const fluxo = [];
    const maxD = Math.max(d1, d2 || 0);
    for (let i = 0; i < maxD; i++) for (const b of blocosD) if (i < b.length) fluxo.push(b[i]);
    for (let i = 0; i < ecPorBloco; i++) for (const b of blocosE) fluxo.push(b[i]);

    const fluxoBits = [];
    for (const b of fluxo) for (let i = 7; i >= 0; i--) fluxoBits.push((b >> i) & 1);

    // matriz
    const tam = 17 + 4 * ver;
    const res = reservado(tam, ver);
    const base = Array.from({length: tam}, () => new Uint8Array(tam));
    desenhaFixos(base, tam, ver);

    // colocação em zigue-zague, da direita para a esquerda
    const posicoes = [];
    let subindo = true;
    for (let col = tam - 1; col > 0; col -= 2) {
      if (col === 6) col--;                 // pula a coluna de temporização
      for (let k = 0; k < tam; k++) {
        const row = subindo ? tam - 1 - k : k;
        for (const c of [col, col - 1]) if (!res[row][c]) posicoes.push([row, c]);
      }
      subindo = !subindo;
    }
    posicoes.forEach(([r, c], i) => { base[r][c] = i < fluxoBits.length ? fluxoBits[i] : 0; });

    // escolha da máscara
    const candidatas = mascaraFixa != null ? [mascaraFixa] : [0,1,2,3,4,5,6,7];
    let melhor = null, melhorP = Infinity, melhorM = 0;
    for (const mk of candidatas) {
      const m = base.map(l => Uint8Array.from(l));
      for (let r = 0; r < tam; r++) for (let c = 0; c < tam; c++)
        if (!res[r][c] && MASCARAS[mk](r, c)) m[r][c] ^= 1;
      gravaFormato(m, tam, mk);
      const pen = penalidade(m, tam);
      if (pen < melhorP) { melhorP = pen; melhor = m; melhorM = mk; }
    }
    return {tam, matriz: melhor, versao: ver, mascara: melhorM};
  }

  /** SVG pronto para embutir. */
  function svg(texto, opc) {
    const o = opc || {};
    const {tam, matriz} = gerar(texto, o.versao, o.mascara);
    const q = o.margem == null ? 4 : o.margem;
    const total = tam + q * 2;
    let d = "";
    for (let r = 0; r < tam; r++) for (let c = 0; c < tam; c++)
      if (matriz[r][c]) d += `M${c + q} ${r + q}h1v1h-1z`;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${total} ${total}" `
         + `shape-rendering="crispEdges" role="img" aria-label="${o.alt || "Código QR"}">`
         + `<rect width="${total}" height="${total}" fill="${o.fundo || "#fff"}"/>`
         + `<path d="${d}" fill="${o.cor || "#000"}"/></svg>`;
  }

  // ---- apoio de teste: lê os codewords de volta de uma matriz pronta ----
  function lerDeVolta(matriz, ver, mascara) {
    const tam = 17 + 4 * ver;
    const res = reservado(tam, ver);
    const m = matriz.map(l => Array.from(l));
    for (let r = 0; r < tam; r++) for (let c = 0; c < tam; c++)
      if (!res[r][c] && MASCARAS[mascara](r, c)) m[r][c] ^= 1;
    const pos = [];
    let subindo = true;
    for (let col = tam - 1; col > 0; col -= 2) {
      if (col === 6) col--;
      for (let k = 0; k < tam; k++) {
        const row = subindo ? tam - 1 - k : k;
        for (const c of [col, col - 1]) if (!res[row][c]) pos.push([row, c]);
      }
      subindo = !subindo;
    }
    const bits = pos.map(([r, c]) => m[r][c]);
    const cw = [];
    for (let i = 0; i + 8 <= bits.length; i += 8) cw.push(parseInt(bits.slice(i, i + 8).join(""), 2));
    return {cw, nbits: bits.length};
  }
  function fluxoDe(texto, ver) {
    const g = gerar(texto, ver, 0);
    return lerDeVolta(g.matriz, ver, 0).cw;
  }
  return {gerar, svg, lerDeVolta, fluxoDe};
})();


