import math, random, os, textwrap
from xml.sax.saxutils import escape as esc
ROOT = os.environ.get('OUT', './')
A = ROOT + 'assets/'
os.makedirs(A, exist_ok=True)

HEAD = "Impact,'Haettenschweiler','Arial Narrow Bold','Franklin Gothic Condensed','Arial Black',sans-serif"
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'SF Mono',Menlo,Consolas,'Liberation Mono','Courier New',monospace"
K, W_, G1, G2, G3 = '#000', '#fff', '#2b2b2b', '#777', '#d6d6d6'

COMMON = f'''<pattern id="dots" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="3.5" cy="3.5" r="1.45" fill="{K}"/></pattern>
<pattern id="dotsW" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="3.5" cy="3.5" r="1.45" fill="{W_}"/></pattern>
<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="{K}" stroke-width="1.3"/></pattern>
<pattern id="hatchW" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="{W_}" stroke-width="1.3"/></pattern>
<pattern id="gridK" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" stroke="#e2e2e2" stroke-width=".8"/></pattern>
<pattern id="gridW" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" stroke="#2a2a2a" stroke-width=".8"/></pattern>
<linearGradient id="fadeH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
<linearGradient id="fadeV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
<radialGradient id="fadeR"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<mask id="mH"><rect width="100%" height="100%" fill="url(#fadeH)"/></mask>
<mask id="mV"><rect width="100%" height="100%" fill="url(#fadeV)"/></mask>
<mask id="mR" maskContentUnits="objectBoundingBox"><rect width="1" height="1" fill="url(#fadeR)"/></mask>
<marker id="ahK" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10Z" fill="{K}"/></marker>
<marker id="ahW" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10Z" fill="{W_}"/></marker>'''

def svg(w, h, body, title, desc, defs=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" fill="none">
<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>
<defs>{COMMON}{defs}</defs>
{body}
</svg>'''

def save(n, s): open(A + n, 'w', encoding='utf-8').write(s)
def T(x, y, s, size=14, fam=None, fill=K, anchor='start', weight='400', ls=0, extra=''):
    fam = fam or SANS
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{esc(s)}</text>'
def mono(x, y, s, size=11, fill=K, anchor='start', ls=1): return T(x, y, s, size, MONO, fill, anchor, '400', ls)
def head(x, y, s, size, fill=K, tl=None, stroke=None):
    ex = (f'textLength="{tl}" lengthAdjust="spacingAndGlyphs" ' if tl else '') + (f'stroke="{stroke}" stroke-width="4" paint-order="stroke" stroke-linejoin="round"' if stroke else '')
    return T(x, y, s, size, HEAD, fill, 'start', '400', 0, ex)
def R(x, y, w, h, fill='none', stroke=K, sw=2, rx=0, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def L(x1, y1, x2, y2, c=K, sw=2, extra=''): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}" {extra}/>'
def C(x, y, r, fill='none', stroke=K, sw=2, extra=''): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def arrow(x1, y1, x2, y2, ink=K, sw=2, dash=''):
    d = f'stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ink}" stroke-width="{sw}" {d} marker-end="url(#ah{"W" if ink==W_ else "K"})"/>'
def dots(x, y, w, h, mask='mH', ink=K):
    return f'<g mask="url(#{mask})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#dots{"W" if ink==W_ else ""})"/></g>'
_mid = 0
def maskwrap(x, y, w, h, mask, ink):
    # mask in user space: define per-use mask
    global _mid
    _mid += 1; mid = f'm{_mid}'
    grad = {'mH': f'<linearGradient id="g{mid}" gradientUnits="userSpaceOnUse" x1="{x}" y1="0" x2="{x+w}" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>',
            'mHr': f'<linearGradient id="g{mid}" gradientUnits="userSpaceOnUse" x1="{x}" y1="0" x2="{x+w}" y2="0"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient>',
            'mV': f'<linearGradient id="g{mid}" gradientUnits="userSpaceOnUse" x1="0" y1="{y}" x2="0" y2="{y+h}"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>',
            'mVr': f'<linearGradient id="g{mid}" gradientUnits="userSpaceOnUse" x1="0" y1="{y}" x2="0" y2="{y+h}"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient>'}[mask]
    return f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}">{grad}<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#g{mid})"/></mask>', \
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#dots{"W" if ink==W_ else ""})" mask="url(#{mid})"/>'
def halftone(x, y, w, h, mask='mH', ink=K, op=1):
    m, r = maskwrap(x, y, w, h, mask, ink)
    return f'<defs>{m}</defs>' + r.replace('<rect', f'<rect opacity="{op}"', 1)
def corners(x, y, w, h, ink=K, n=14, sw=2):
    s = ''
    for cx, cy, dx, dy in [(x,y,1,1),(x+w,y,-1,1),(x,y+h,1,-1),(x+w,y+h,-1,-1)]:
        s += f'<path d="M{cx} {cy+dy*n}V{cy}H{cx+dx*n}" stroke="{ink}" stroke-width="{sw}"/>'
    return s

# ============================================================ HERO
def hero():
    W, H = 1200, 600
    random.seed(11)
    Lp = "M14,14 L772,14 L662,466 L14,466 Z"; Rp = "M796,14 L1186,14 L1186,466 L686,466 Z"
    b = R(0, 0, W, H, W_, W_, 0)
    b += f'<path d="{Lp}" fill="{W_}" stroke="{K}" stroke-width="5"/>'
    b += f'<path d="M744,14 L772,14 L662,466 L634,466 Z" fill="url(#hatch)"/>'
    b += f'<defs><clipPath id="cl"><path d="{Rp}"/></clipPath></defs>'
    b += f'<path d="{Rp}" fill="{K}"/><g clip-path="url(#cl)">'
    cx, cy = 946, 240
    for i in range(96):
        a = random.random() * 2 * math.pi; w0 = random.uniform(.002, .006); r0 = random.uniform(120, 190)
        x1, y1, x2, y2 = cx+r0*math.cos(a-w0), cy+r0*math.sin(a-w0), cx+r0*math.cos(a+w0), cy+r0*math.sin(a+w0)
        w1 = w0 * random.uniform(5, 14); x3, y3, x4, y4 = cx+800*math.cos(a+w1), cy+800*math.sin(a+w1), cx+800*math.cos(a-w1), cy+800*math.sin(a-w1)
        b += f'<polygon points="{x1:.0f},{y1:.0f} {x2:.0f},{y2:.0f} {x3:.0f},{y3:.0f} {x4:.0f},{y4:.0f}" fill="{W_}" opacity="{random.choice([.35,.6,.9])}"/>'
    xs = [840, 920, 1000, 1080]; cnt = [3, 5, 5, 3]; top, bot = 92, 388
    lay = [[(x, top+(bot-top)*(i+.5)/c) for i in range(c)] for x, c in zip(xs, cnt)]
    edges = [(p, q) for a_, b_ in zip(lay, lay[1:]) for p in a_ for q in b_]
    for p, q in edges: b += L(p[0], f'{p[1]:.0f}', q[0], f'{q[1]:.0f}', W_, 1, 'opacity=".75"')
    for k, (p, q) in enumerate(random.sample(edges, 9)):
        d = 2.4 + k * .3
        b += f'<circle r="3.6" fill="{W_}"><animateMotion dur="{d:.1f}s" begin="{k*.5:.1f}s" repeatCount="indefinite" path="M{p[0]} {p[1]:.0f} L{q[0]} {q[1]:.0f}"/></circle>'
    for l_ in lay:
        for x, y in l_: b += C(x, f'{y:.0f}', 11, K, W_, 2.5)
    b += C(1000, 240, 22, W_, K, 3) + C(1000, 240, 30, 'none', W_, 1.5, 'stroke-dasharray="3 5"')
    b += '</g>'
    b += f'<path d="{Rp}" fill="none" stroke="{K}" stroke-width="5"/>'
    b += mono(1160, 44, 'FIG. 01 — INFERENCE GRAPH', 11, W_, 'end', 2)
    for x, l in zip(xs, ['IN', 'L1', 'L2', 'OUT']): b += mono(x, 432, l, 11, W_, 'middle', 2)
    # left text
    b += mono(46, 52, 'DOSSIER Nº 01  /  AI-ML ENGINEERING', 12, K, 'start', 2)
    b += L(46, 64, 330, 64, K, 2)
    b += head(53, 197, 'SHLOK', 150, G3, 560, K) + head(48, 192, 'SHLOK', 150, K, 560)
    b += head(53, 331, 'MISHRA', 150, K, 600) .replace(f'fill="{K}"', f'fill="{G3}"', 1)
    b += head(48, 326, 'MISHRA', 150, W_, 600, K)
    b += f'<polygon points="48,350 572,350 548,398 48,398" fill="{K}"/>' + head(66, 387, 'AI / ML DEVELOPER', 40, W_, 340) + mono(540, 380, '// 2027', 12, W_, 'end', 2)
    b += T(48, 428, 'Building intelligent systems across ML, GenAI, RAG,', 17, SANS, K, 'start', '600') + T(48, 452, 'automation and applied AI.', 17, SANS, K, 'start', '600')
    # pipeline strip
    b += R(14, 482, 1172, 104, K, K, 0)
    st = [('INPUT', 'raw signals'), ('DATA', 'clean · structure'), ('MODEL', 'learn · evaluate'), ('INFERENCE', 'serve · explain'), ('OUTPUT', 'decisions')]
    for i, (a_, s_) in enumerate(st):
        x = 44 + i * 226
        b += R(x, 510, 176, 56, K, W_, 2.5) + mono(x + 10, 504, f'0{i+1}', 10, W_, 'start', 2)
        b += T(x + 88, 541, a_, 27, HEAD, W_, 'middle') + mono(x + 88, 558, s_, 10, '#a8a8a8', 'middle', 1)
        if i < 4: b += f'<line x1="{x+176}" y1="538" x2="{x+222}" y2="538" stroke="{W_}" stroke-width="2.5" stroke-dasharray="7 5" marker-end="url(#ahW)"><animate attributeName="stroke-dashoffset" from="24" to="0" dur="1.4s" repeatCount="indefinite"/></line>'
    b += R(2.5, 2.5, W-5, H-5, 'none', K, 5)
    save('hero.svg', svg(W, H, b, 'Shlok Mishra — AI / ML Developer', 'Monochrome manga-style hero panel with an inference graph and an input to output pipeline.'))

# ============================================================ BUTTONS
def button(fn, label, sub, glyph, invert=False):
    W, H = 250, 60
    bg, fg = (K, W_) if invert else (W_, K)
    b = R(6, 6, 240, 50, K, K, 0) + R(2, 2, 240, 50, bg, K, 3)
    b += R(12, 9, 36, 36, fg, fg, 0) + T(30, 33, glyph, 15, MONO, bg, 'middle', '700')
    b += T(60, 28, label, 22, HEAD, fg, 'start', '400', 1) + mono(60, 43, sub, 9, fg, 'start', 1)
    b += f'<path d="M214 22H228V36M228 22L214 36" stroke="{fg}" stroke-width="2.5"/>'
    save(fn, svg(W, H, b, label, f'{label} button'))

# ============================================================ HEADER
def header(fn, num, title, note):
    W, H = 1200, 84
    tl = len(title) * 23; tw = 96 + tl + 20
    b = R(0, 0, W, H, W_, W_, 0) + f'<polygon points="0,6 {tw+30},6 {tw},78 0,78" fill="{K}"/>'
    b += head(22, 58, num, 54, '#666') + head(96, 58, title, 50, W_, tl)
    b += L(tw + 50, 42, W - 4, 42, K, 2)
    for x in range(tw + 70, W - 4, 40): b += L(x, 34, x, 50, K, 1.5)
    b += f'<rect x="{W-300}" y="12" width="296" height="22" fill="{W_}"/>' + mono(W - 6, 28, note, 11, K, 'end', 2)
    b += f'<rect x="{tw+40}" y="62" width="{W-tw-44}" height="12" fill="url(#hatch)"/>'
    save(fn, svg(W, H, b, title, f'Section header {num} {title}'))

# ============================================================ ABOUT
def chip(x, y, t, ink=K, filled=False):
    w = len(t) * 8.2 + 34
    bg, fg = (K, W_) if filled else (W_, K)
    return R(x, y, w, 32, bg, ink, 2) + R(x + 9, y + 12, 8, 8, fg, fg, 0) + T(x + 24, y + 21, t, 13, SANS, fg, 'start', '600') , w
def about():
    W, H = 1200, 450
    b = R(0, 0, W, H, W_, W_, 0) + R(3, 3, W - 6, H - 6, W_, K, 5)
    b += f'<polygon points="3,3 372,3 332,{H-3} 3,{H-3}" fill="{K}"/>'
    b += halftone(3, 3, 360, H - 6, 'mHr', W_)
    b += head(30, 270, 'SM', 230, W_, 290)
    b += corners(26, 26, 296, 396, W_, 20, 3)
    b += mono(40, 56, 'PROFILE / 01', 12, W_, 'start', 3) + mono(40, 414, 'AI / ML DEVELOPER', 11, W_, 'start', 3)
    rows = [('NAME', 'Shlok Mishra'), ('FOCUS', 'AI / ML Engineering'), ('EDUCATION', 'BTech — Computer Science & Artificial Intelligence'),
            ('INSTITUTION', 'G H Raisoni College of Engineering, Nagpur'), ('BATCH', '2027')]
    for i, (k, v) in enumerate(rows):
        y = 54 + i * 54
        b += mono(410, y + 14, k, 11, G2, 'start', 3) + T(410, y + 40, v, 22, SANS, K, 'start', '700')
        b += L(410, y + 52, 1160, y + 52, K, 1.5 if i else 3)
    b += mono(410, 346, 'FOCUS AREAS', 11, G2, 'start', 3)
    items = ['Machine Learning', 'Generative AI', 'RAG', 'Agentic AI', 'AI Automation', 'Computer Vision', 'Data / ML Systems']
    x, y = 410, 360
    for i, t in enumerate(items):
        s, w = chip(x, y, t, K, i % 3 == 0)
        if x + w > 1160: x, y = 410, y + 40; s, w = chip(x, y, t, K, i % 3 == 0)
        b += s; x += w + 10
    save('about.svg', svg(W, H, b, 'Profile', 'Technical profile sheet: name, focus, education, institution, batch and focus areas.'))

# ============================================================ PIPELINE
def icon(kind, cx, cy, ink, bg):
    s = ''
    if kind == 'data':
        s += f'<ellipse cx="{cx}" cy="{cy-16}" rx="22" ry="8" fill="{bg}" stroke="{ink}" stroke-width="2.5"/><path d="M{cx-22} {cy-16}V{cy+14}A22 8 0 0 0 {cx+22} {cy+14}V{cy-16}" stroke="{ink}" stroke-width="2.5"/><path d="M{cx-22} {cy-1}A22 8 0 0 0 {cx+22} {cy-1}" stroke="{ink}" stroke-width="2"/>'
    elif kind == 'proc':
        s += C(cx, cy, 14, bg, ink, 3) + C(cx, cy, 5, ink, ink, 1) + ''.join(f'<rect x="{cx-4}" y="{cy-24}" width="8" height="9" fill="{ink}" transform="rotate({a} {cx} {cy})"/>' for a in range(0, 360, 60))
    elif kind == 'model':
        pts = [(cx-22, cy-14), (cx-22, cy+14), (cx, cy-20), (cx, cy), (cx, cy+20), (cx+22, cy-8), (cx+22, cy+8)]
        for p in pts[:2]:
            for q in pts[2:5]: s += L(p[0], p[1], q[0], q[1], ink, 1.2)
        for p in pts[2:5]:
            for q in pts[5:]: s += L(p[0], p[1], q[0], q[1], ink, 1.2)
        for p in pts: s += C(p[0], p[1], 4.5, bg, ink, 2)
    elif kind == 'ret':
        s += C(cx-4, cy-4, 15, bg, ink, 3) + L(cx+7, cy+7, cx+22, cy+22, ink, 5) + L(cx-12, cy-4, cx+4, cy-4, ink, 2) + L(cx-12, cy+3, cx+2, cy+3, ink, 2)
    elif kind == 'reason':
        s += C(cx, cy-16, 6, ink, ink, 1) + C(cx-18, cy+16, 6, bg, ink, 2.5) + C(cx+18, cy+16, 6, bg, ink, 2.5) + f'<path d="M{cx} {cy-10}V{cy}M{cx} {cy}H{cx-18}V{cy+10}M{cx} {cy}H{cx+18}V{cy+10}" stroke="{ink}" stroke-width="2.5"/>'
    elif kind == 'api':
        s += f'<path d="M{cx-8} {cy-18}L{cx-24} {cy}L{cx-8} {cy+18}M{cx+8} {cy-18}L{cx+24} {cy}L{cx+8} {cy+18}" stroke="{ink}" stroke-width="4"/>' + L(cx+4, cy-14, cx-4, cy+14, ink, 3)
    else:
        s += f'<path d="M{cx} {cy-22}L{cx+20} {cy-11}V{cy+11}L{cx} {cy+22}L{cx-20} {cy+11}V{cy-11}Z" fill="{bg}" stroke="{ink}" stroke-width="3"/><path d="M{cx} {cy}L{cx+20} {cy-11}M{cx} {cy}L{cx-20} {cy-11}M{cx} {cy}V{cy+22}" stroke="{ink}" stroke-width="2"/>'
    return s
def pipeline():
    W, H = 1200, 500
    st = [('DATA', 'Pandas · NumPy · SQL', 'data'), ('PROCESS', 'clean · transform', 'proc'), ('MODEL', 'ML · DL · CV · NLP', 'model'), ('RETRIEVAL', 'RAG · GraphRAG · Neo4j', 'ret'),
          ('REASONING', 'LLMs · LangChain · LangGraph', 'reason'), ('API', 'FastAPI · REST', 'api'), ('DEPLOYMENT', 'Git · GitHub · AWS', 'dep')]
    b = R(0, 0, W, H, W_, K, 0) + R(0, 0, W, H, 'url(#gridK)', 'none', 0) + R(3, 3, W - 6, H - 6, 'none', K, 5)
    bw, gap = 140, 28; x0 = 30
    ys = [250, 222, 194, 166, 138, 110, 82]
    pts = []
    for i, (n, s, k) in enumerate(st):
        x = x0 + i * (bw + gap); y = ys[i]; inv = i in (2, 4, 6)
        bg, fg = (K, W_) if inv else (W_, K)
        b += R(x + 6, y + 6, bw, 150, K, K, 0) + R(x, y, bw, 150, bg, K, 3)
        b += mono(x + 10, y + 20, f'STAGE {i+1:02d}', 10, fg, 'start', 2) + icon(k, x + bw // 2, y + 66, fg, bg)
        b += T(x + bw / 2, y + 116, n, 22, HEAD, fg, 'middle', '400', 1)
        b += T(x + bw / 2, y + 136, s, 9.5, MONO, fg, 'middle')
        b += L(x + bw / 2, y + 158, x + bw / 2, 440, K, 1, 'stroke-dasharray="2 4"')
        pts.append((x, y))
    for i in range(6):
        x1 = pts[i][0] + bw; y1 = pts[i][1] + 75; x2 = pts[i+1][0]; y2 = pts[i+1][1] + 75
        b += f'<path d="M{x1+6} {y1}H{x1+14}V{y2}H{x2}" stroke="{K}" stroke-width="2.5" stroke-dasharray="7 5" marker-end="url(#ahK)"><animate attributeName="stroke-dashoffset" from="24" to="0" dur="1.6s" repeatCount="indefinite"/></path>'
    b += L(30, 440, 1170, 440, K, 3)
    for x in range(30, 1171, 20): b += L(x, 440, x, 448 if (x - 30) % 100 else 456, K, 1.5)
    b += mono(30, 30, 'ENGINEERING MANUAL / SYSTEM FLOW', 12, K, 'start', 3) + mono(1170, 30, 'FIG. 02 — ABSTRACTION RISES →', 11, K, 'end', 2)
    b += mono(30, 484, 'raw data', 10, G2, 'start', 2) + mono(1170, 484, 'deployed system', 10, G2, 'end', 2)
    save('pipeline.svg', svg(W, H, b, 'Engineering pipeline', 'Seven stage flow: data, process, model, retrieval, reasoning, API, deployment.'))

# ============================================================ STACK
def panel(x, y, w, h, title, items, inv, idx, cols=1):
    bg, fg = (K, W_) if inv else (W_, K)
    s = R(x + 6, y + 6, w, h, K, K, 0) + R(x, y, w, h, bg, K, 3)
    s += R(x, y, w, 46, fg, K, 3) + T(x + 16, y + 34, title.upper(), 26, HEAD, bg, 'start', '400', 1) + mono(x + w - 14, y + 29, idx, 11, bg, 'end', 2)
    n = len(items); per = math.ceil(n / cols)
    for i, t in enumerate(items):
        c = i // per; r = i % per
        ix = x + 18 + c * (w // cols); iy = y + 78 + r * 34
        s += R(ix, iy - 11, 10, 10, fg, fg, 0) + T(ix + 22, iy, t, 17, SANS, fg, 'start', '600')
    return s
def stack():
    W, H = 1200, 560
    b = R(0, 0, W, H, W_, W_, 0)
    b += panel(6, 6, 330, 230, 'Languages', ['Python', 'SQL'], False, 'L1')
    b += panel(360, 6, 440, 230, 'AI / ML', ['Machine Learning', 'Deep Learning', 'Computer Vision', 'NLP'], True, 'L2', 2)
    b += panel(824, 6, 364, 230, 'Generative AI', ['LLMs', 'RAG', 'Agentic AI', 'LangChain', 'LangGraph'], False, 'L3', 2)
    b += panel(6, 276, 330, 270, 'Backend', ['FastAPI', 'REST APIs'], True, 'L4')
    b += panel(360, 276, 440, 270, 'Data', ['Pandas', 'NumPy', 'Neo4j'], False, 'L5')
    b += panel(824, 276, 364, 270, 'Engineering', ['Git', 'GitHub', 'AWS'], True, 'L6')
    b += halftone(380, 440, 400, 100, 'mVr', K) + halftone(26, 440, 290, 96, 'mVr', W_) + halftone(844, 440, 324, 96, 'mVr', W_)
    b += halftone(380, 150, 400, 80, 'mVr', W_) + halftone(844, 150, 324, 80, 'mVr', K) + halftone(26, 150, 290, 80, 'mVr', K)
    save('stack.svg', svg(W, H, b, 'System stack', 'Six layer technical stack: languages, AI/ML, generative AI, backend, data and engineering.'))

# ============================================================ EXPERIENCE
def experience():
    W, H = 1200, 400
    b = R(0, 0, W, H, W_, K, 0) + R(3, 3, W - 6, H - 6, W_, K, 5)
    b += f'<polygon points="3,3 520,3 470,{H-3} 3,{H-3}" fill="{K}"/>' + halftone(3, 250, 440, 147, 'mV', W_)
    b += mono(34, 44, 'FIELD LOG / ENGINEERING RECORD', 11, W_, 'start', 3)
    b += head(34, 142, 'WORKMATES', 100, W_, 400)
    b += R(34, 166, 430, 2, W_, W_, 0) + T(34, 204, 'Software Development Intern', 22, SANS, W_, 'start', '700')
    b += R(34, 224, 250, 30, W_, W_, 0) + mono(46, 244, 'MAY 2026 — AUGUST 2026', 12, K, 'start', 1)
    b += mono(34, 296, 'AFFILIATED WITH', 10, '#aaa', 'start', 3) + T(34, 320, 'Pragatishil Bahuuddeshiya Sanstha,', 16, SANS, W_, 'start', '600') + T(34, 342, 'Washim', 16, SANS, W_, 'start', '600')
    b += L(600, 60, 600, 350, K, 3)
    logs = [('LOG 01', 'Production deployments', ['sunitanursingschool.in', 'nsuryawanshicop.com'], 'Institutional web platforms for Sunita Nursing School and Narendra Suryawanshi College of Pharmacy.'),
            ('LOG 02', 'Live product', ['find-your-niche-01.vercel.app'], 'Find Your Niche — AI-powered taste discovery platform.')]
    y = 64
    for i, (a_, t, urls, d) in enumerate(logs):
        b += R(590, y - 4, 20, 20, K if i == 0 else W_, K, 3) + mono(630, y + 12, a_, 11, G2, 'start', 3) + T(630, y + 40, t, 24, HEAD, K, 'start', '400', 1)
        for j, ln in enumerate(textwrap.wrap(d, 58)): b += T(630, y + 64 + j * 20, ln, 14.5, SANS, '#333')
        uy = y + 64 + 20 * len(textwrap.wrap(d, 58)) + 8
        for u in urls: b += R(630, uy - 14, len(u) * 7.6 + 24, 24, W_, K, 2) + mono(642, uy + 3, u, 12, K, 'start', 0); uy += 32
        y += 170
    b += mono(1170, 380, 'MAY 2026 → AUG 2026', 10, G2, 'end', 2)
    save('experience.svg', svg(W, H, b, 'Experience', 'Workmates, Software Development Intern, May to August 2026, with production deployments.'))

# ============================================================ CASE FILES
def chips_row(x, y, tags, maxx, fg, bg):
    s = ''; cx, cy = x, y
    for t in tags:
        w = len(t) * 7.6 + 20
        if cx + w > maxx: cx, cy = x, cy + 32
        s += R(cx, cy, w, 24, 'none', fg, 1.8) + mono(cx + 10, cy + 16, t, 11, fg, 'start', 0)
        cx += w + 8
    return s
def box(x, y, w, h, l1, l2, ink, paper, fill=False, sw=2.5):
    bg, fg = (ink, paper) if fill else (paper, ink)
    s = R(x, y, w, h, bg, ink, sw)
    cy = y + h / 2
    s += T(x + w / 2, cy + (-3 if l2 else 6), l1, 16, HEAD, fg, 'middle', '400', 1)
    if l2: s += T(x + w / 2, cy + 14, l2, 9.5, MONO, fg, 'middle')
    return s

def d1(ink, pap):
    s = ''; ins = [('MULTILINGUAL', 'query'), ('AGRI KNOWLEDGE', 'base'), ('WEATHER · GEO', 'context'), ('CROP IMAGERY', 'computer vision')]
    hub = (370, 200)
    for i, (a_, b_) in enumerate(ins):
        y = 24 + i * 92; s += box(0, y, 200, 62, a_, b_, ink, pap, i % 2 == 1)
        ang = math.atan2(hub[1] - (y + 31), hub[0] - 200); s += arrow(200, y + 31, hub[0] - 82 * abs(math.cos(ang)), hub[1] - 82 * math.sin(ang), ink, 2)
    s += C(hub[0], hub[1], 66, ink, ink, 3) + C(hub[0], hub[1], 78, 'none', ink, 1.5, 'stroke-dasharray="4 5"') + T(hub[0], hub[1] - 2, 'RAG', 36, HEAD, pap, 'middle') + T(hub[0], hub[1] + 20, 'retrieve · ground', 10, MONO, pap, 'middle')
    s += arrow(hub[0] + 80, hub[1], 478, hub[1], ink, 3) + box(480, 130, 170, 140, 'CROP', 'INTELLIGENCE', ink, pap, True)
    s += mono(560, 300, 'UNIFIED SYSTEM OUTPUT', 9, ink, 'middle', 1) + mono(0, 392, 'FIG. 03 — GROUNDED GENERATION OVER FOUR SOURCES', 10, ink, 'start', 2)
    return s
def d2(ink, pap):
    random.seed(5); cx, cy = 325, 190; s = ''
    for r in (60, 120, 175): s += C(cx, cy, r, 'none', ink, 1.5, 'stroke-dasharray="3 6"')
    s += L(cx - 190, cy, cx + 190, cy, ink, 1.5) + L(cx, cy - 190, cx, cy + 190, ink, 1.5)
    for x, y, t, a in [(0, 26, 'MOVIES', 'start'), (650, 26, 'BOOKS', 'end'), (0, 372, 'MUSIC', 'start'), (650, 372, 'CODE / OPEN SOURCE', 'end')]: s += T(x, y, t, 20, HEAD, ink, a, '400', 1)
    pts = []
    for qx, qy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        for _ in range(6):
            r = random.uniform(55, 170); a = random.uniform(.15, 1.4); x, y = cx + qx * r * math.cos(a), cy + qy * r * math.sin(a); pts.append((x, y))
    near = sorted(pts, key=lambda p: (p[0]-cx)**2 + (p[1]-cy)**2)[:4]
    for p in near: s += L(cx, cy, f'{p[0]:.0f}', f'{p[1]:.0f}', ink, 3)
    for i, p in enumerate(pts): s += C(f'{p[0]:.0f}', f'{p[1]:.0f}', 6 if p in near else 4.5, ink if p in near or i % 3 == 0 else pap, ink, 2)
    s += C(cx, cy, 24, pap, ink, 4) + C(cx, cy, 12, ink, ink, 1)
    s += L(cx + 20, cy - 20, 500, 96, ink, 1.5) + R(470, 74, 150, 22, ink, ink, 0) + mono(545, 89, 'USER TASTE PROFILE', 9, pap, 'middle', 1)
    s += mono(0, 392, 'FIG. 04 — SEMANTIC SIMILARITY ACROSS FOUR CATALOGS', 10, ink, 'start', 2)
    return s
def face(x, y, w, h, ink, pap):
    cx = x + w / 2; s = R(x, y, w, h, pap, ink, 2.5)
    s += f'<ellipse cx="{cx}" cy="{y+h/2-6}" rx="{w*.27}" ry="{h*.34}" fill="none" stroke="{ink}" stroke-width="2.5"/>'
    s += L(cx - w * .13, y + h * .42, cx - w * .05, y + h * .42, ink, 3) + L(cx + w * .05, y + h * .42, cx + w * .13, y + h * .42, ink, 3) + L(cx, y + h * .46, cx - 3, y + h * .56, ink, 2) + L(cx - w * .08, y + h * .66, cx + w * .08, y + h * .66, ink, 2.5)
    return s
def d3(ink, pap):
    s = face(0, 50, 150, 200, ink, pap) + corners(24, 78, 102, 120, ink, 16, 4) + mono(75, 270, 'INPUT FRAME', 10, ink, 'middle', 1) + mono(75, 40, 'RETINAFACE', 10, ink, 'middle', 2)
    s += arrow(152, 150, 186, 150, ink, 2.5)
    for i in range(3): s += R(190 + i * 14, 98 + i * 14 - 14, 66, 108, pap if i < 2 else ink, ink, 2.5)
    s += T(251, 172, 'CNN', 22, HEAD, pap, 'middle') + mono(224, 270, 'CNN INFERENCE', 10, ink, 'middle', 1)
    s += arrow(290, 150, 322, 150, ink, 2.5)
    fx = 326; s += face(fx, 50, 150, 200, ink, pap)
    s += f'<defs><radialGradient id="hm"><stop offset="0" stop-color="{ink}"/><stop offset="1" stop-color="{ink}" stop-opacity="0"/></radialGradient></defs><ellipse cx="{fx+75}" cy="118" rx="52" ry="42" fill="url(#hm)" opacity=".85"/><ellipse cx="{fx+75}" cy="118" rx="52" ry="42" fill="url(#dots{"W" if ink==W_ else ""})" opacity=".6"/>'
    s += mono(fx + 75, 270, 'GRAD-CAM HEATMAP', 10, ink, 'middle', 1)
    s += arrow(478, 150, 508, 150, ink, 2.5) + box(510, 100, 140, 100, 'FASTAPI', 'STREAMLIT', ink, pap, True) + mono(580, 220, 'ANALYSIS OUTPUT', 10, ink, 'middle', 1)
    s += mono(0, 392, 'FIG. 05 — DETECT · CLASSIFY · EXPLAIN', 10, ink, 'start', 2)
    return s
def d4(ink, pap):
    s = R(0, 70, 170, 220, ink, ink, 3) + f'<ellipse cx="85" cy="180" rx="62" ry="78" fill="{pap}" stroke="{pap}" stroke-width="2"/>'
    s += f'<ellipse cx="85" cy="180" rx="50" ry="66" fill="url(#dots{"W" if ink==W_ else ""})" stroke="{ink}" stroke-width="2"/><path d="M85 118V244M58 150Q85 170 112 150M54 200Q85 180 116 200" stroke="{ink}" stroke-width="2.5"/>'
    s += mono(85, 312, 'MRI SLICE', 10, ink, 'middle', 1) + arrow(176, 180, 214, 180, ink, 2.5)
    xs = [220, 290, 352, 408]; ws = [58, 46, 36, 28]; hs = [170, 130, 96, 66]
    for i in range(4):
        cy = 180; s += R(xs[i], cy - hs[i] / 2, ws[i], hs[i], ink if i % 2 == 0 else pap, ink, 2.5)
    s += mono(320, 312, 'CONVOLUTIONAL FEATURE EXTRACTION', 10, ink, 'middle', 1)
    s += arrow(440, 180, 478, 180, ink, 2.5)
    for i in range(3): s += C(500, 130 + i * 50, 11, pap if i != 1 else ink, ink, 2.5)
    for i in range(3): s += L(511, 130 + i * 50, 568, 180, ink, 1.5)
    s += box(570, 140, 80, 80, 'CLASS', 'PREDICTION', ink, pap, True) + mono(505, 312, 'DENSE', 10, ink, 'middle', 1)
    s += mono(0, 392, 'FIG. 06 — IMAGE → CNN → CLASSIFICATION', 10, ink, 'start', 2)
    return s
def d5(ink, pap):
    s = box(0, 150, 100, 100, 'NL', 'QUERY', ink, pap, True) + arrow(102, 200, 140, 200, ink, 2.5)
    nodes = {'a': (190, 70), 'b': (300, 50), 'c': (390, 110), 'd': (160, 180), 'e': (270, 190), 'f': (370, 230), 'g': (200, 310), 'h': (310, 320)}
    ed = [('a', 'b'), ('b', 'c'), ('a', 'd'), ('b', 'e'), ('c', 'f'), ('d', 'e'), ('e', 'f'), ('d', 'g'), ('e', 'h'), ('g', 'h'), ('f', 'h')]
    path = {('a', 'd'), ('d', 'e'), ('e', 'f')}
    s += R(140, 20, 280, 340, 'none', ink, 1.5, 0, 'stroke-dasharray="4 5"')
    for p, q in ed:
        hl = (p, q) in path; s += L(nodes[p][0], nodes[p][1], nodes[q][0], nodes[q][1], ink, 5 if hl else 1.6)
    for k, (x, y) in nodes.items(): s += C(x, y, 15 if k in 'ade' or k == 'f' else 11, ink if k in 'adef' else pap, ink, 3)
    s += mono(280, 14, 'NEO4J KNOWLEDGE GRAPH', 10, ink, 'middle', 2) + mono(280, 378, 'entity · relation · fact', 10, ink, 'middle', 1)
    for i, (a_, b_) in enumerate([('GRAPHRAG', 'RETRIEVAL'), ('LLM', 'REASONING'), ('FINANCIAL', 'EXPLANATION')]):
        y = 30 + i * 130; s += box(450, y, 200, 76, a_, b_, ink, pap, i != 1)
        if i < 2: s += arrow(550, y + 78, 550, y + 128, ink, 2.5)
    s += arrow(420, 130, 448, 70, ink, 2.5) + mono(0, 392, 'FIG. 07 — GRAPH-GROUNDED REASONING', 10, ink, 'start', 2)
    return s

def case(fn, num, title_lines, desc, tags, link_label, diag, text_left, inv, figtitle):
    W, H = 1200, 460
    tp = "M0,0 L490,0 L450,460 L0,460 Z" if text_left else "M710,0 L1200,0 L1200,460 L750,460 Z"
    dp = "M506,0 L1200,0 L1200,460 L466,460 Z" if text_left else "M0,0 L694,0 L734,460 L0,460 Z"
    tb, tf = (K, W_) if inv else (W_, K); db, df = (W_, K) if inv else (K, W_)
    b = R(0, 0, W, H, W_, W_, 0)
    b += f'<path d="{dp}" fill="{db}"/><path d="{dp}" fill="url(#grid{"K" if db==W_ else "W"})"/>'
    b += f'<path d="{tp}" fill="{tb}"/>'
    tx = 40 if text_left else 770
    b += mono(tx, 50, f'CASE FILE / {num}', 12, tf, 'start', 3)
    b += head(tx - 4, 150, num, 118, tb, None, tf)
    y = 192
    for t in title_lines: b += head(tx, y, t, 32, tf, int(len(t) * 15.5)); y += 34
    y += 2
    for ln in textwrap.wrap(desc, 50): b += T(tx, y, ln, 14.5, SANS, tf, 'start', '400'); y += 20
    b += chips_row(tx, y + 8, tags, tx + 380, tf, tb)
    if link_label:
        pre, repo = link_label.rsplit('/', 1)
        b += mono(tx, 420, 'SOURCE', 9, tf, 'start', 3) + mono(tx, 436, pre + '/', 11, tf, 'start', 0) + mono(tx, 450, repo, 11, tf, 'start', 0)
    ox = 520 if text_left else 30
    b += f'<g transform="translate({ox} 34)">{diag(df, db)}</g>'
    b += R(2.5, 2.5, W - 5, H - 5, 'none', K, 5)
    save(fn, svg(W, H, b, f'Case file {num}: {" ".join(title_lines)}', figtitle))

# ============================================================ HIGHLIGHTS
def highlights():
    W, H = 1200, 400
    b = R(0, 0, W, H, K, K, 0) + halftone(0, 0, W, H, 'mV', W_, .18)
    cells = [(0, 0, 392, 188, 'SIH', 'Smart India Hackathon', 'Finalist', True), (402, 0, 392, 188, '05', 'AI / ML engineering projects', 'Agriculture, taste, forensics, medical imaging, finance', False),
             (804, 0, 396, 188, 'INTERN', 'Software development internship', 'Workmates · May–Aug 2026', True), (0, 200, 500, 200, 'LIVE', 'Deployed products', 'Two institutional websites and Find Your Niche', False),
             (510, 200, 330, 200, 'IEEE', 'Student branch team lead', 'Technical coordination', True), (850, 200, 350, 200, 'ML·GENAI', 'Technical experimentation', 'ML, GenAI and AI systems', False)]
    for x, y, w, h, big, l1, l2, inv in cells:
        bg, fg = (W_, K) if inv else (K, W_)
        b += R(x + 2, y + 2, w - 4, h - 4, bg, W_ if not inv else K, 3)
        b += head(x + 24, y + 86, big, 66, fg, min(len(big) * 31 + 10, w - 60)) + L(x + 24, y + 104, x + w - 30, y + 104, fg, 2)
        b += T(x + 24, y + 134, l1, 18, SANS, fg, 'start', '700')
        for j, ln in enumerate(textwrap.wrap(l2, 44)): b += T(x + 24, y + 158 + j * 18, ln, 13, SANS, fg)
    save('highlights.svg', svg(W, H, b, 'Highlights', 'Six highlight panels: SIH finalist, projects, internship, deployed products, IEEE, experimentation.'))

# ============================================================ FOOTER
def footer():
    W, H = 1200, 380
    b = R(0, 0, W, H, W_, W_, 0) + f'<polygon points="0,0 1200,0 1200,{H} 0,{H}" fill="{K}"/>' + halftone(0, 0, W, H, 'mH', W_, .25)
    b += f'<polygon points="30,30 1170,30 1150,350 30,350" fill="{W_}" stroke="{K}" stroke-width="5"/>'
    b += mono(64, 68, 'CONTACT / END OF DOSSIER', 12, K, 'start', 3)
    b += head(60, 150, "LET'S BUILD SOMETHING", 80, K, 760) + head(60, 232, 'INTELLIGENT.', 80, W_, 430, K)
    b += halftone(540, 170, 260, 70, 'mH', K)
    rows = [('GITHUB', 'github.com/ShlokMishra01'), ('LINKEDIN', 'linkedin.com/in/shlok-mishra-9a649b255'), ('EMAIL', 'shlokmishrawork@gmail.com')]
    for i, (a_, u) in enumerate(rows):
        y = 262 + i * 28
        b += mono(64, y + 4, a_, 11, G2, 'start', 3) + mono(190, y + 4, u, 14, K, 'start', 0) + L(64, y + 12, 600, y + 12, K, 1)
    b += C(1012, 190, 92, K, K, 3) + C(1012, 190, 80, 'none', W_, 1.5, 'stroke-dasharray="3 5"') + head(944, 232, 'SM', 100, W_, 136)
    b += mono(1012, 312, 'SHLOK MISHRA · AI / ML', 10, K, 'middle', 2)
    save('footer.svg', svg(W, H, b, 'Contact', "Let's build something intelligent. GitHub, LinkedIn and email."))

# ============================================================ BUILD
hero()
button('btn-github.svg', 'GITHUB', 'ShlokMishra01', 'GH')
button('btn-linkedin.svg', 'LINKEDIN', 'shlok-mishra', 'in')
button('btn-email.svg', 'EMAIL', 'shlokmishrawork', '@')
button('btn-resume.svg', 'RESUME', 'download pdf', 'CV', True)
header('h-about.svg', '01', 'PROFILE', 'SEC. 01 / IDENTITY'); about()
header('h-pipeline.svg', '02', 'ENGINEERING PIPELINE', 'SEC. 02 / METHOD'); pipeline()
header('h-stack.svg', '03', 'SYSTEM STACK', 'SEC. 03 / TOOLING'); stack()
header('h-exp.svg', '04', 'FIELD LOG', 'SEC. 04 / EXPERIENCE'); experience()
header('h-work.svg', '05', 'SELECTED WORK', 'SEC. 05 / CASE FILES')
case('p1.svg', '01', ['PRITHVI', 'AGRO AI'], 'AI-powered agricultural assistant combining multilingual RAG, agricultural knowledge, weather/geospatial context, computer vision and crop intelligence in one system.', ['RAG', 'Multilingual', 'Computer vision', 'Geospatial'], 'github.com/ShlokMishra01/prithvi-agro-ai', d1, True, True, 'Four input sources feed a RAG core that produces crop intelligence.')
case('p2.svg', '02', ['FIND YOUR', 'NICHE'], 'AI-powered taste discovery platform that understands preferences across movies, books, music and coding/open-source projects.', ['taste profiling', 'semantic similarity', 'recommendations', 'RAG chat', 'taste mapping', 'social discovery'], 'github.com/ShlokMishra01/Find-your-niche-', d2, False, False, 'Taste map with four catalog quadrants and similarity links to a user profile.')
case('p3.svg', '03', ['ADVANCED DEEPFAKE', 'DETECTION'], 'Computer-vision system for analysing potentially manipulated images and videos.', ['RetinaFace', 'CNN', 'Grad-CAM', 'FastAPI', 'Streamlit'], 'github.com/ShlokMishra01/Deepfake-Image-and-video-analyzer', d3, True, True, 'Face detection, CNN inference and Grad-CAM explanation behind an API.')
case('p4.svg', '04', ['NEURO', 'DETECT AI'], 'AI-based MRI analysis project using convolutional neural networks for medical-image classification.', ['CNN', 'MRI', 'image classification'], '', d4, False, False, 'MRI slice passes through convolutional blocks to a class prediction.')
case('p5.svg', '05', ['FINANCEFLOW AI'], 'Finance-focused GraphRAG system using structured financial knowledge and Neo4j to improve the reliability of AI-assisted financial reasoning.', ['GraphRAG', 'Neo4j', 'LLM reasoning', 'financial data workflows'], 'github.com/ShlokMishra01/Fintech-assistant-model-with-neo4j-and-Python', d5, True, True, 'Natural-language query retrieved from a Neo4j graph, then reasoned over by an LLM.')
header('h-hl.svg', '06', 'HIGHLIGHTS', 'SEC. 06 / RECORD'); highlights(); footer()
print(len(os.listdir(A)), 'svgs')
