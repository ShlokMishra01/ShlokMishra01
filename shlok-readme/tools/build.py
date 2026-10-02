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


# ======================================================================
#  v2 additions: single connected panel, animated sections, character
# ======================================================================
import zlib
HERE = os.path.dirname(os.path.abspath(__file__))
CHAR_BODY = open(os.path.join(HERE, 'char_body.b64')).read().strip()
CHAR_FACE = open(os.path.join(HERE, 'char_face.b64')).read().strip()
ROOT = os.environ.get('OUT', os.path.join(HERE, '..') + os.sep)
A = os.path.join(ROOT, 'assets') + os.sep
os.makedirs(A, exist_ok=True)
MAIL = 'shlokmishrawork@gmail.com'
MAIL_URL = 'https://mail.google.com/mail/?view=cm&fs=1&to=' + MAIL

def FR(x, y, w, h, fill=K, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" {extra}/>'

def edges(W, H, top=5, bottom=0, left=5, right=5, outer_top=False, outer_bottom=False):
    """panel border: 5px ink rule inside a 4px white margin, so the whole README reads as one page on dark themes too"""
    s = ''
    if left: s += FR(0, 0, 4, H, W_) + FR(4, 0, left, H)
    if right: s += FR(W - 4, 0, 4, H, W_) + FR(W - 4 - right, 0, right, H)
    if top:
        if outer_top: s += FR(0, 0, W, 4, W_) + FR(0, 4, W, top)
        else: s += FR(0, 0, W, top)
    if bottom:
        if outer_bottom: s += FR(0, H - 4, W, 4, W_) + FR(0, H - 4 - bottom, W, bottom)
        else: s += FR(0, H - bottom, W, bottom)
    return s

def head(x, y, s, size, fill=K, tl=None, stroke=None, extra=''):
    tl = tl or round(len(s) * size * 0.49)
    ex = f'textLength="{tl}" lengthAdjust="spacingAndGlyphs" '
    if stroke: ex += f'stroke="{stroke}" stroke-width="4" paint-order="stroke" stroke-linejoin="round" '
    return T(x, y, s, size, HEAD, fill, 'start', '400', 0, ex + extra)

def anim(attr, values, dur, begin=0, keyTimes=None, extra=''):
    kt = f' keyTimes="{keyTimes}"' if keyTimes else ''
    return f'<animate attributeName="{attr}" values="{values}" dur="{dur}s" begin="{begin}s"{kt} repeatCount="indefinite" {extra}/>'

def atrans(kind, values, dur, begin=0, extra=''):
    return f'<animateTransform attributeName="transform" type="{kind}" values="{values}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite" {extra}/>'

def spin(cx, cy, dur, rev=False):
    a, b = (360, 0) if rev else (0, 360)
    return f'<animateTransform attributeName="transform" type="rotate" from="{a} {cx} {cy}" to="{b} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>'

def flash(x, y, w, h, i, n, color, peak=.22, step=1.0, d=None):
    """sequential tone-flash overlay: element i of n lights up in turn"""
    dur = d or n * step
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" opacity="0"><animate attributeName="opacity" values="0;{peak};0;0" keyTimes="0;.05;.2;1" dur="{dur}s" begin="{i*step}s" repeatCount="indefinite"/></rect>'

def packet(path, dur, begin, ink, ring, r=4.2, slot=None):
    """small data packet travelling along a path. slot=(start,end) in 0..1 limits motion to part of the cycle"""
    if slot:
        s0, s1 = slot
        mo = f'keyPoints="0;0;1;1" keyTimes="0;{s0:.3f};{s1:.3f};1" calcMode="linear"'
        op = f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{s0:.3f};{s0+.005:.3f};{s1-.005:.3f};{s1:.3f};1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
    else:
        mo = ''
        op = f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.12;.88;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
    return f'<circle r="{r}" fill="{ink}" stroke="{ring}" stroke-width="1.5" opacity="0"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" path="{path}" {mo}/>{op}</circle>'

def star(cx, cy, r, ink, delay, dur=3):
    d = f'M0 {-r}Q0 0 {r} 0Q0 0 0 {r}Q0 0 {-r} 0Q0 0 0 {-r}Z'
    return f'<g transform="translate({cx} {cy})"><path d="{d}" fill="{ink}" transform="scale(0)"><animateTransform attributeName="transform" type="scale" values="0;1;0;0" keyTimes="0;.18;.4;1" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></path></g>'

def marquee(x, y, w, h, text, size, ink, bg, ls_factor=0.49, dur=30, mono_font=False, gap='   ✦   '):
    unit = text + gap
    fam = MONO if mono_font else HEAD
    tl = round(len(unit) * size * (0.6 if mono_font else ls_factor))
    def one(dx):
        return f'<text x="{dx}" y="{y + h * .5 + size * .36:.0f}" font-family="{fam}" font-size="{size}" fill="{ink}" textLength="{tl}" lengthAdjust="spacingAndGlyphs" xml:space="preserve">{esc(unit)}</text>'
    reps = int(w / tl) + 2
    row = ''.join(one(x + k * tl) for k in range(reps + 1))
    cid = f'mq{zlib.crc32(f'{x}{y}{text}'.encode()) % 99999}'
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>'
            f'<g clip-path="url(#{cid})"><g>{atrans("translate", f"0 0;{-tl} 0", dur)}{row}</g></g>')

def svg2(fn, W, H, body, title, desc, defs=''):
    open(A + fn, 'w', encoding='utf-8').write(svg(W, H, body, title, desc, defs))

# ---------------------------------------------------------------- SECTION WRAPPER (animated header + body)
HH = 84
def section(fn, num, title, note, body, bh, desc):
    W = 1200; H = HH + bh
    tl = len(title) * 23; tw = 96 + tl + 20
    x0 = tw + 70
    b = FR(0, 0, W, H, W_)
    b += f'<polygon points="0,6 {tw+30},6 {tw},78 0,78" fill="{K}"/>'
    b += head(26, 58, num, 54, '#666') + head(100, 58, title, 50, W_, tl)
    # ruler with travelling wave + marker
    b += L(tw + 50, 42, W - 4, 42, K, 2)
    k = 0
    for x in range(x0, W - 24, 40):
        b += f'<line x1="{x}" y1="34" x2="{x}" y2="50" stroke="{K}" stroke-width="1.6">{anim("y1", "34;24;34", 3.2, k * .09)}{anim("y2", "50;60;50", 3.2, k * .09)}</line>'
        k += 1
    b += f'<polygon points="-7,22 7,22 0,36" fill="{K}"><animateTransform attributeName="transform" type="translate" values="{tw+60} 0;{W-40} 0;{tw+60} 0" dur="7s" repeatCount="indefinite"/></polygon>'
    b += FR(W - 306, 12, 282, 22, W_) + mono(W - 28, 28, note, 11, K, 'end', 2)
    b += f'<rect x="{W-20}" y="16" width="8" height="14" fill="{K}">{anim("opacity", "1;0;1", 1.1)}</rect>'
    # drifting hatch strip
    hx0 = tw + 40
    b += f'<clipPath id="hs"><rect x="{hx0}" y="62" width="{W - hx0 - 5}" height="12"/></clipPath><g clip-path="url(#hs)"><g>{atrans("translate", "0 0;12 0", 1.2)}'
    for xx in range(hx0 - 24, W, 12):
        b += f'<line x1="{xx}" y1="74" x2="{xx+12}" y2="62" stroke="{K}" stroke-width="1.4"/>'
    b += '</g></g>'
    b += FR(0, HH - 2, W, 4, K)
    b += f'<g transform="translate(0 {HH})">{body}</g>'
    b += edges(W, H)
    svg2(fn, W, H, b, title, desc)

# ============================================================ HERO
def hero():
    W, H = 1200, 600
    random.seed(11)
    Lp = "M14,14 L772,14 L662,466 L14,466 Z"; Rp = "M796,14 L1186,14 L1186,466 L686,466 Z"
    b = FR(0, 0, W, H, W_)
    b += f'<path d="{Lp}" fill="{W_}" stroke="{K}" stroke-width="5"/>'
    b += f'<path d="M744,14 L772,14 L662,466 L634,466 Z" fill="url(#hatch)"/>'
    b += f'<defs><clipPath id="cl"><path d="{Rp}"/></clipPath><clipPath id="rv"><rect x="0" y="0" width="0" height="470"><animate attributeName="width" from="0" to="700" dur="1.4s" begin=".2s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></rect></clipPath>'
    b += f'<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".28"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
    b += f'<path d="{Rp}" fill="{K}"/><g clip-path="url(#cl)">'
    cx, cy = 946, 240
    for i in range(96):
        a = random.random() * 2 * math.pi; w0 = random.uniform(.002, .006); r0 = random.uniform(120, 190)
        x1, y1, x2, y2 = cx+r0*math.cos(a-w0), cy+r0*math.sin(a-w0), cx+r0*math.cos(a+w0), cy+r0*math.sin(a+w0)
        w1 = w0 * random.uniform(5, 14); x3, y3, x4, y4 = cx+800*math.cos(a+w1), cy+800*math.sin(a+w1), cx+800*math.cos(a-w1), cy+800*math.sin(a-w1)
        b += f'<polygon points="{x1:.0f},{y1:.0f} {x2:.0f},{y2:.0f} {x3:.0f},{y3:.0f} {x4:.0f},{y4:.0f}" fill="{W_}" opacity="{random.choice([.35,.6,.9])}"/>'
    xs = [840, 920, 1000, 1080]; cnt = [3, 5, 5, 3]; top, bot = 92, 388
    lay = [[(x, top+(bot-top)*(i+.5)/c) for i in range(c)] for x, c in zip(xs, cnt)]
    edgs = [(p, q) for a_, b_ in zip(lay, lay[1:]) for p in a_ for q in b_]
    for p, q in edgs: b += L(p[0], f'{p[1]:.0f}', q[0], f'{q[1]:.0f}', W_, 1, 'opacity=".75"')
    for k, (p, q) in enumerate(random.sample(edgs, 14)):
        d = 2.0 + (k % 5) * .35
        b += f'<circle r="3.6" fill="{W_}"><animateMotion dur="{d:.1f}s" begin="{k*.37:.1f}s" repeatCount="indefinite" path="M{p[0]} {p[1]:.0f} L{q[0]} {q[1]:.0f}"/></circle>'
    nk = 0
    for l_ in lay:
        for x, y in l_:
            b += f'<circle cx="{x}" cy="{y:.0f}" r="11" fill="{K}" stroke="{W_}" stroke-width="2.5">{anim("r", "11;14;11", 2.4 + (nk % 4) * .4, (nk % 6) * .3)}</circle>'; nk += 1
    b += C(1000, 240, 22, W_, K, 3) + f'<circle cx="1000" cy="240" r="30" fill="none" stroke="{W_}" stroke-width="1.5" stroke-dasharray="3 5">{spin(1000, 240, 8)}</circle>'
    b += f'<circle cx="1000" cy="240" r="30" fill="none" stroke="{W_}" stroke-width="1.5">{anim("r", "26;74", 2.4)}{anim("opacity", ".8;0", 2.4)}</circle>'
    b += f'<rect y="0" width="120" height="470" fill="url(#beam)"><animate attributeName="x" values="640;1200" dur="5.5s" repeatCount="indefinite"/></rect>'
    for (sx, sy, sr, sd) in [(830, 60, 11, 0), (1150, 120, 15, 1.1), (1110, 420, 12, 2.0), (860, 440, 9, .6)]:
        b += star(sx, sy, sr, W_, sd, 3.4)
    b += '</g>'
    b += f'<path d="{Rp}" fill="none" stroke="{K}" stroke-width="5"/>'
    b += mono(1160, 44, 'FIG. 01 — INFERENCE GRAPH', 11, W_, 'end', 2)
    for x, l in zip(xs, ['IN', 'L1', 'L2', 'OUT']): b += mono(x, 432, l, 11, W_, 'middle', 2)
    # left text, wiped in
    b += mono(46, 52, 'DOSSIER Nº 01  /  AI-ML ENGINEERING', 12, K, 'start', 2)
    b += L(46, 64, 330, 64, K, 2)
    b += f'<rect x="46" y="58" width="12" height="12" fill="{K}">{anim("opacity", "1;0;1", 1.2)}</rect>'
    b += '<g clip-path="url(#rv)">'
    b += head(53, 197, 'SHLOK', 150, G3, 560, K) + head(48, 192, 'SHLOK', 150, K, 560)
    b += head(53, 331, 'MISHRA', 150, G3, 600, K) + head(48, 326, 'MISHRA', 150, W_, 600, K)
    b += f'<polygon points="48,350 572,350 548,398 48,398" fill="{K}"/>' + head(66, 387, 'AI / ML DEVELOPER', 40, W_, 340) + mono(540, 380, '// 2027', 12, W_, 'end', 2)
    b += '</g>'
    b += f'<rect x="418" y="360" width="14" height="28" fill="{W_}">{anim("opacity", "1;0;1", 1.1)}</rect>'
    b += T(48, 428, 'Building practical AI systems across ML, GenAI, RAG,', 17, SANS, K, 'start', '600') + T(48, 452, 'agentic AI and automation.', 17, SANS, K, 'start', '600')
    # pipeline strip
    b += FR(0, 478, W, H - 478, K)
    st = [('INPUT', 'raw signals'), ('DATA', 'clean · structure'), ('MODEL', 'learn · evaluate'), ('INFERENCE', 'serve · explain'), ('OUTPUT', 'decisions')]
    for i, (a_, s_) in enumerate(st):
        x = 44 + i * 226
        b += R(x, 510, 176, 56, K, W_, 2.5) + mono(x + 10, 504, f'0{i+1}', 10, W_, 'start', 2)
        b += T(x + 88, 541, a_, 27, HEAD, W_, 'middle') + mono(x + 88, 558, s_, 10, '#a8a8a8', 'middle', 1)
        b += flash(x, 510, 176, 56, i, 5, W_, .22, 1.0)
        if i < 4:
            b += f'<line x1="{x+176}" y1="538" x2="{x+222}" y2="538" stroke="{W_}" stroke-width="2.5" stroke-dasharray="7 5" marker-end="url(#ahW)"><animate attributeName="stroke-dashoffset" from="24" to="0" dur="1.4s" repeatCount="indefinite"/></line>'
            b += packet(f'M{x+178} 538 H{x+220}', 5, 0, W_, K, 3.2, slot=(i / 5, i / 5 + .2))
    b += edges(W, H, top=5, bottom=0, outer_top=True)
    svg2('hero.svg', W, H, b, 'Shlok Mishra — AI / ML Developer', 'Monochrome manga-style hero panel with an animated inference graph and an input to output pipeline.')

# ============================================================ LINK CELLS (clickable bars, flush under a panel)
def cell(fn, w, h, label, sub, glyph, inv, first=False, last=False, bottom=False, live=False):
    bg, fg = (K, W_) if inv else (W_, K)
    b = FR(0, 0, w, h, bg)
    # drifting tone band
    b += f'<clipPath id="cc"><rect width="{w}" height="{h}"/></clipPath><linearGradient id="cs" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{fg}" stop-opacity="0"/><stop offset=".5" stop-color="{fg}" stop-opacity=".18"/><stop offset="1" stop-color="{fg}" stop-opacity="0"/></linearGradient>'
    b += f'<g clip-path="url(#cc)"><rect y="0" width="90" height="{h}" fill="url(#cs)"><animate attributeName="x" values="-110;{w+20}" dur="4.2s" repeatCount="indefinite"/></rect></g>'
    gx = 22
    b += R(gx + 4, h / 2 - 17 + 4, 34, 34, fg, fg, 0, extra='opacity=".25"') + R(gx, h / 2 - 17, 34, 34, fg, fg, 0)
    if live:
        b += f'<circle cx="{gx+17}" cy="{h/2}" r="6" fill="{bg}"/><circle cx="{gx+17}" cy="{h/2}" r="6" fill="none" stroke="{bg}" stroke-width="2">{anim("r", "6;20", 2)}{anim("opacity", "1;0", 2)}</circle>'
    else:
        b += T(gx + 17, h / 2 + 5, glyph, 15, MONO, bg, 'middle', '700')
    b += T(gx + 52, h / 2 - 2, label, 24, HEAD, fg, 'start', '400', 1, f'textLength="{round(len(label)*24*.49+len(label))}" lengthAdjust="spacingAndGlyphs"')
    b += mono(gx + 52, h / 2 + 17, sub, 10.5, fg, 'start', 0)
    ax = w - 34
    b += f'<g><animateTransform attributeName="transform" type="translate" values="0 0;4 -4;0 0" dur="1.8s" repeatCount="indefinite"/><path d="M{ax-8} {h/2-3}H{ax+6}V{h/2+11}M{ax+6} {h/2-3}L{ax-8} {h/2+11}" stroke="{fg}" stroke-width="3" transform="translate(0 -4)"/></g>'
    b += FR(0, 0, w, 5)
    if bottom: b += FR(0, h - 9, w, 5) + FR(0, h - 4, w, 4, W_)
    if first: b += FR(0, 0, 4, h, W_) + FR(4, 0, 5, h)
    else: b += FR(0, 0, 3, h)
    if last: b += FR(w - 4, 0, 4, h, W_) + FR(w - 9, 0, 5, h)
    svg2(fn, w, h, b, label, f'{label} link')

# ============================================================ PROFILE (with manga character)
def profile():
    bh = 470
    lp = "M0,0 L480,0 L430,470 L0,470 Z"
    s = f'<defs><clipPath id="lpc"><path d="{lp}"/></clipPath>'
    s += '<radialGradient id="chf" cx=".5" cy=".5" r=".5"><stop offset=".72" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>'
    s += '<mask id="chm" maskContentUnits="objectBoundingBox"><rect width="1" height="1" fill="url(#chf)"/></mask>'
    s += f'<linearGradient id="scG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".9" stop-color="#fff" stop-opacity=".28"/><stop offset="1" stop-color="#fff" stop-opacity=".95"/></linearGradient></defs>'
    s += FR(0, 0, 1200, bh, W_) + R(0, 0, 1200, bh, 'url(#gridK)', 'none', 0)
    s += f'<path d="{lp}" fill="{K}"/><g clip-path="url(#lpc)">'
    s += halftone(0, 0, 480, bh, 'mHr', W_, .55)
    s += f'<text x="8" y="352" font-family="{HEAD}" font-size="330" fill="none" stroke="{W_}" stroke-width="3.2" textLength="450" lengthAdjust="spacingAndGlyphs" stroke-dasharray="2600" stroke-dashoffset="2600" opacity=".9">SM<animate attributeName="stroke-dashoffset" from="2600" to="0" dur="3.2s" fill="freeze"/></text>'
    s += f'<circle cx="236" cy="256" r="196" fill="none" stroke="{W_}" stroke-width="1.6" stroke-dasharray="2 9" opacity=".55">{spin(236, 256, 46)}</circle>'
    s += f'<circle cx="236" cy="256" r="236" fill="none" stroke="{W_}" stroke-width="1.6" stroke-dasharray="16 10" opacity=".3">{spin(236, 256, 60, True)}</circle>'
    s += f'<image href="data:image/jpeg;base64,{CHAR_BODY}" x="-22" y="14" width="486" height="504" preserveAspectRatio="xMidYMid slice" mask="url(#chm)"/>'
    for (sx, sy, sr, sd) in [(60, 118, 12, 0), (412, 96, 17, .9), (432, 300, 11, 1.7), (44, 330, 14, 2.3), (330, 36, 9, 1.2), (390, 410, 13, .4), (238, 226, 10, 2.8)]:
        s += star(sx, sy, sr, W_, sd, 3.6)
    s += f'<g><animateTransform attributeName="transform" type="translate" values="0 -70;0 {bh}" dur="5.4s" repeatCount="indefinite"/><rect y="0" width="480" height="70" fill="url(#scG)"/></g>'
    s += '</g>'
    s += f'<g>{anim("opacity", ".45;1;.45", 2.4)}{corners(24, 24, 398, 422, W_, 20, 3)}</g>'
    s += mono(40, 56, 'PROFILE / 01', 12, W_, 'start', 3)
    s += f'<polygon points="24,408 232,408 214,440 24,440" fill="{K}" stroke="{W_}" stroke-width="1.5"/>' + mono(38, 429, 'SHLOK MISHRA · AI / ML', 10, W_, 'start', 1)
    s += f'<path d="{lp}" fill="none" stroke="{K}" stroke-width="5"/>'
    # data sheet
    rows = [('NAME', 'Shlok Mishra'), ('FOCUS', 'AI / ML Engineering'), ('EDUCATION', 'BTech — Computer Science & Artificial Intelligence'),
            ('INSTITUTION', 'G H Raisoni College of Engineering, Nagpur'), ('BATCH', '2027')]
    x0 = 530
    for i, (k, v) in enumerate(rows):
        y = 26 + i * 52
        s += mono(x0, y + 14, k, 11, G2, 'start', 3) + T(x0, y + 38, v, 21, SANS, K, 'start', '700')
        ln = f'<line x1="{x0}" y1="{y+49}" x2="1160" y2="{y+49}" stroke="{K}" stroke-width="{3 if i == 0 else 1.5}" stroke-dasharray="640" stroke-dashoffset="640"><animate attributeName="stroke-dashoffset" from="640" to="0" dur=".9s" begin="{.3 + i*.25:.2f}s" fill="freeze"/></line>'
        s += ln
    # selection marker stepping through rows
    ys = ';'.join(str(26 + i * 52 + 2) for i in range(5))
    s += f'<rect x="{x0-20}" y="28" width="8" height="40" fill="{K}"><animate attributeName="y" values="{ys}" dur="7.5s" calcMode="discrete" repeatCount="indefinite"/></rect>'
    s += mono(x0, 304, 'FOCUS AREAS', 11, G2, 'start', 3)
    items = ['Machine Learning', 'Generative AI', 'RAG', 'Agentic AI', 'AI Automation', 'Computer Vision', 'Data / ML Systems']
    x, y = x0, 316
    for i, t in enumerate(items):
        w = len(t) * 8.2 + 34
        if x + w > 1160: x, y = x0, y + 40
        filled = i % 3 == 0; bg, fg = (K, W_) if filled else (W_, K)
        s += R(x, y, w, 32, bg, K, 2) + f'<rect x="{x+9}" y="{y+12}" width="8" height="8" fill="{fg}">{anim("opacity", "1;.1;1", 2.6, i * .35)}</rect>' + T(x + 24, y + 21, t, 13, SANS, fg, 'start', '600')
        s += f'<rect x="{x}" y="{y}" width="{w}" height="32" fill="none" stroke="{K}" stroke-width="2"><animate attributeName="stroke-width" values="2;5;2;2" keyTimes="0;.06;.16;1" dur="9.8s" begin="{i*1.4}s" repeatCount="indefinite"/></rect>'
        x += w + 10
    s += marquee(x0, 418, 630, 34, 'DATA → RETRIEVAL → REASONING → MODEL → API → PRODUCT', 13, W_, K, mono_font=True, dur=22, gap='     ■     ')
    section('s1-profile.svg', '01', 'PROFILE', 'SEC. 01 / IDENTITY', s, bh, 'Profile sheet with manga-style portrait: Shlok Mishra, AI/ML engineering, BTech Computer Science and Artificial Intelligence, G H Raisoni College of Engineering Nagpur, batch 2027.')

# ============================================================ PIPELINE
def icon(kind, cx, cy, ink, bg):
    s = ''
    if kind == 'data':
        s += f'<ellipse cx="{cx}" cy="{cy-16}" rx="22" ry="8" fill="{bg}" stroke="{ink}" stroke-width="2.5"/><path d="M{cx-22} {cy-16}V{cy+14}A22 8 0 0 0 {cx+22} {cy+14}V{cy-16}" stroke="{ink}" stroke-width="2.5"/><path d="M{cx-22} {cy-1}A22 8 0 0 0 {cx+22} {cy-1}" stroke="{ink}" stroke-width="2"/>'
        s += f'<ellipse cx="{cx}" cy="{cy-16}" rx="22" ry="8" fill="{ink}" opacity="0">{anim("opacity", "0;.5;0", 2.4)}</ellipse>'
    elif kind == 'proc':
        g = C(cx, cy, 14, bg, ink, 3) + C(cx, cy, 5, ink, ink, 1) + ''.join(f'<rect x="{cx-4}" y="{cy-24}" width="8" height="9" fill="{ink}" transform="rotate({a} {cx} {cy})"/>' for a in range(0, 360, 60))
        s += f'<g>{spin(cx, cy, 7)}{g}</g>'
    elif kind == 'model':
        pts = [(cx-22, cy-14), (cx-22, cy+14), (cx, cy-20), (cx, cy), (cx, cy+20), (cx+22, cy-8), (cx+22, cy+8)]
        for p in pts[:2]:
            for q in pts[2:5]: s += L(p[0], p[1], q[0], q[1], ink, 1.2)
        for p in pts[2:5]:
            for q in pts[5:]: s += L(p[0], p[1], q[0], q[1], ink, 1.2)
        for i, p in enumerate(pts): s += f'<circle cx="{p[0]}" cy="{p[1]}" r="4.5" fill="{bg}" stroke="{ink}" stroke-width="2">{anim("r", "4.5;7;4.5", 1.8, i * .22)}</circle>'
    elif kind == 'ret':
        g = C(cx-4, cy-4, 15, bg, ink, 3) + L(cx+7, cy+7, cx+22, cy+22, ink, 5) + L(cx-12, cy-4, cx+4, cy-4, ink, 2) + L(cx-12, cy+3, cx+2, cy+3, ink, 2)
        s += f'<g>{atrans("translate", "-6 -2;6 2;-6 -2", 2.6)}{g}</g>'
    elif kind == 'reason':
        s += C(cx, cy-16, 6, ink, ink, 1) + C(cx-18, cy+16, 6, bg, ink, 2.5) + C(cx+18, cy+16, 6, bg, ink, 2.5) + f'<path d="M{cx} {cy-10}V{cy}M{cx} {cy}H{cx-18}V{cy+10}M{cx} {cy}H{cx+18}V{cy+10}" stroke="{ink}" stroke-width="2.5"/>'
        s += f'<circle cx="{cx}" cy="{cy-16}" r="6" fill="none" stroke="{ink}" stroke-width="2">{anim("r", "6;20", 2)}{anim("opacity", "1;0", 2)}</circle>'
    elif kind == 'api':
        s += f'<g>{atrans("translate", "-3 0;0 0;-3 0", 1.6)}<path d="M{cx-8} {cy-18}L{cx-24} {cy}L{cx-8} {cy+18}" stroke="{ink}" stroke-width="4"/></g><g>{atrans("translate", "3 0;0 0;3 0", 1.6)}<path d="M{cx+8} {cy-18}L{cx+24} {cy}L{cx+8} {cy+18}" stroke="{ink}" stroke-width="4"/></g>' + L(cx+4, cy-14, cx-4, cy+14, ink, 3)
    else:
        s += f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="1.8s" repeatCount="indefinite"/><path d="M{cx} {cy-22}L{cx+20} {cy-11}V{cy+11}L{cx} {cy+22}L{cx-20} {cy+11}V{cy-11}Z" fill="{bg}" stroke="{ink}" stroke-width="3"/><path d="M{cx} {cy}L{cx+20} {cy-11}M{cx} {cy}L{cx-20} {cy-11}M{cx} {cy}V{cy+22}" stroke="{ink}" stroke-width="2"/></g>'
    return s

def pipeline():
    bh = 500
    st = [('DATA', 'Pandas · NumPy · SQL', 'data'), ('PROCESS', 'clean · transform', 'proc'), ('MODEL', 'ML · DL · CV · NLP', 'model'), ('RETRIEVAL', 'RAG · GraphRAG · Neo4j', 'ret'),
          ('REASONING', 'LLMs · LangChain · LangGraph', 'reason'), ('API', 'FastAPI · REST', 'api'), ('DEPLOYMENT', 'Git · GitHub · AWS', 'dep')]
    b = FR(0, 0, 1200, bh, W_) + R(0, 0, 1200, bh, 'url(#gridK)', 'none', 0)
    bw, gap = 140, 28; x0 = 30
    ys = [250, 222, 194, 166, 138, 110, 82]
    pts = []
    for i, (n, s_, k) in enumerate(st):
        x = x0 + i * (bw + gap); y = ys[i]; inv = i in (2, 4, 6)
        bg, fg = (K, W_) if inv else (W_, K)
        b += R(x + 6, y + 6, bw, 150, K, K, 0) + R(x, y, bw, 150, bg, K, 3)
        b += mono(x + 10, y + 20, f'STAGE {i+1:02d}', 10, fg, 'start', 2) + icon(k, x + bw // 2, y + 66, fg, bg)
        b += T(x + bw / 2, y + 116, n, 22, HEAD, fg, 'middle', '400', 1, f'textLength="{round(len(n)*22*.49+len(n))}" lengthAdjust="spacingAndGlyphs"')
        b += T(x + bw / 2, y + 136, s_, 9.5, MONO, fg, 'middle', '400', 0, f'textLength="{min(len(s_)*5.7, 118):.0f}" lengthAdjust="spacingAndGlyphs"')
        b += flash(x, y, bw, 150, i, 7, W_ if inv else K, .26, 1.0)
        b += L(x + bw / 2, y + 158, x + bw / 2, 440, K, 1, 'stroke-dasharray="2 4"')
        b += f'<rect x="{x+bw/2-4}" y="436" width="8" height="8" fill="{K}" opacity="0"><animate attributeName="opacity" values="0;1;0;0" keyTimes="0;.05;.2;1" dur="7s" begin="{i}s" repeatCount="indefinite"/></rect>'
        pts.append((x, y))
    for i in range(6):
        x1 = pts[i][0] + bw; y1 = pts[i][1] + 75; x2 = pts[i+1][0]; y2 = pts[i+1][1] + 75
        path = f'M{x1+6} {y1}H{x1+14}V{y2}H{x2}'
        b += f'<path d="{path}" stroke="{K}" stroke-width="2.5" stroke-dasharray="7 5" marker-end="url(#ahK)"><animate attributeName="stroke-dashoffset" from="24" to="0" dur="1.6s" repeatCount="indefinite"/></path>'
        b += packet(path, 7, 0, K, W_, 5, slot=(i / 7 + .03, i / 7 + .15))
    b += L(30, 440, 1170, 440, K, 3)
    for x in range(30, 1171, 20): b += L(x, 440, x, 448 if (x - 30) % 100 else 456, K, 1.5)
    b += f'<polygon points="-8,424 8,424 0,438" fill="{K}"><animateTransform attributeName="transform" type="translate" values="30 0;1170 0" dur="7s" repeatCount="indefinite"/></polygon>'
    b += mono(30, 30, 'ENGINEERING MANUAL / SYSTEM FLOW', 12, K, 'start', 3) + mono(1170, 30, 'FIG. 02 — ABSTRACTION RISES →', 11, K, 'end', 2)
    b += f'<rect x="1086" y="18" width="10" height="14" fill="{K}" opacity="0"/>'
    b += mono(30, 484, 'raw data', 10, G2, 'start', 2) + mono(1170, 484, 'deployed system', 10, G2, 'end', 2)
    section('s2-pipeline.svg', '02', 'ENGINEERING PIPELINE', 'SEC. 02 / METHOD', b, bh, 'Seven stage flow: data, process, model, retrieval, reasoning, API, deployment.')

# ============================================================ STACK (flush grid)
def stack():
    W = 1200; rh = [236, 246]; tk = 54; bh = sum(rh) + tk
    cells = [('Languages', ['Python', 'SQL'], 'L1'), ('AI / ML', ['Machine Learning', 'Deep Learning', 'Computer Vision', 'NLP'], 'L2'), ('Generative AI', ['LLMs', 'RAG', 'Agentic AI', 'LangChain', 'LangGraph'], 'L3'),
             ('Backend', ['FastAPI', 'REST APIs'], 'L4'), ('Data', ['Pandas', 'NumPy', 'Neo4j'], 'L5'), ('Engineering', ['Git', 'GitHub', 'AWS'], 'L6')]
    b = FR(0, 0, W, bh, W_)
    cw = 400; k = 0; defs = ''
    for idx, (title, items, tag) in enumerate(cells):
        r, c = divmod(idx, 3)
        x = c * cw; y = 0 if r == 0 else rh[0]; h = rh[r]
        inv = (r + c) % 2 == 1
        bg, fg = (K, W_) if inv else (W_, K)
        b += FR(x, y, cw, h, bg)
        b += FR(x, y, cw, 48, fg)
        b += T(x + 24, y + 35, title.upper(), 27, HEAD, bg, 'start', '400', 1, f'textLength="{round(len(title)*27*.49+len(title))}" lengthAdjust="spacingAndGlyphs"') + mono(x + cw - 24, y + 30, tag, 11, bg, 'end', 2)
        b += f'<clipPath id="cb{idx}"><rect x="{x}" y="{y}" width="{cw}" height="48"/></clipPath><linearGradient id="sw{idx}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{bg}" stop-opacity="0"/><stop offset=".5" stop-color="{bg}" stop-opacity=".4"/><stop offset="1" stop-color="{bg}" stop-opacity="0"/></linearGradient>'
        b += f'<g clip-path="url(#cb{idx})"><rect y="{y}" width="110" height="48" fill="url(#sw{idx})"><animate attributeName="x" values="{x-130};{x+cw+20}" dur="3.6s" begin="{idx*.45}s" repeatCount="indefinite"/></rect></g>'
        n = len(items); cols = 2 if n > 3 else 1; per = math.ceil(n / cols)
        for i, t in enumerate(items):
            cc, rr = divmod(i, per)
            ix = x + 28 + cc * 190; iy = y + 92 + rr * 36
            b += f'<rect x="{ix}" y="{iy-12}" width="12" height="12" fill="{fg}">{anim("opacity", "1;.12;1", 3.6, k * .22)}</rect>' + T(ix + 26, iy, t, 18, SANS, fg, 'start', '600')
            k += 1
        b += halftone(x + 24, y + h - 62, cw - 48, 50, 'mVr', fg, .9)
    # dividers
    for xx in (cw, 2 * cw): b += FR(xx - 2.5, 0, 5, sum(rh))
    b += FR(0, rh[0] - 2.5, W, 5) + FR(0, sum(rh) - 2.5, W, 5)
    txt = 'PYTHON  •  SQL  •  MACHINE LEARNING  •  DEEP LEARNING  •  COMPUTER VISION  •  NLP  •  LLMS  •  RAG  •  AGENTIC AI  •  LANGCHAIN  •  LANGGRAPH  •  FASTAPI  •  REST APIS  •  PANDAS  •  NUMPY  •  NEO4J  •  GIT  •  GITHUB  •  AWS'
    b += marquee(0, sum(rh) + 2.5, W, tk - 2.5, txt, 26, K, W_, dur=60, gap='  •  ')
    section('s3-stack.svg', '03', 'SYSTEM STACK', 'SEC. 03 / TOOLING', b, bh, 'Six layer technical stack: languages, AI/ML, generative AI, backend, data and engineering.')

# ============================================================ FIELD LOG
def field():
    bh = 420
    b = FR(0, 0, 1200, bh, W_)
    b += f'<polygon points="0,0 520,0 470,{bh}" fill="{K}"/><polygon points="0,0 520,0 470,{bh} 0,{bh}" fill="{K}"/>' + halftone(300, 200, 150, bh - 200, 'mVr', W_, .9)
    b += mono(34, 44, 'FIELD LOG / ENGINEERING RECORD', 11, W_, 'start', 3)
    b += f'<circle cx="440" cy="40" r="5" fill="{W_}">{anim("opacity", "1;.1;1", 1.2)}</circle>' + mono(452, 44, 'REC', 10, W_, 'start', 2)
    b += head(34, 142, 'WORKMATES', 100, W_, 400)
    b += FR(34, 166, 430, 2, W_) + f'<rect x="34" y="166" width="60" height="2" fill="{K}"><animate attributeName="x" values="34;404;34" dur="4s" repeatCount="indefinite"/></rect>'
    b += T(34, 204, 'Software Development Intern', 22, SANS, W_, 'start', '700')
    b += FR(34, 224, 250, 30, W_) + mono(46, 244, 'MAY 2026 — AUGUST 2026', 12, K, 'start', 1)
    b += mono(34, 292, 'AFFILIATED WITH', 10, '#aaa', 'start', 3) + T(34, 316, 'Pragatishil Bahuuddeshiya Sanstha,', 16, SANS, W_, 'start', '600') + T(34, 338, 'Washim', 16, SANS, W_, 'start', '600')
    # timeline May -> Aug
    for i, m in enumerate(['MAY', 'JUN', 'JUL', 'AUG']):
        x = 34 + i * 104
        b += mono(x, 372, m, 10, W_, 'start', 2) + R(x, 380, 96, 12, K, W_, 1.5) + f'<rect x="{x}" y="380" width="0" height="12" fill="{W_}"><animate attributeName="width" values="0;96;96;0" keyTimes="0;.18;.9;1" dur="8s" begin="{i*1.2}s" repeatCount="indefinite"/></rect>'
    b += L(600, 40, 600, 380, K, 3) + f'<rect x="592" y="40" width="16" height="16" fill="{K}"><animate attributeName="y" values="40;364;40" dur="7s" repeatCount="indefinite"/></rect>'
    logs = [('LOG 01', 'Production deployments', 'Institutional web platforms for Sunita Nursing School and Narendra Suryawanshi College of Pharmacy, deployed to the web.', 'DEPLOYED'),
            ('LOG 02', 'Live product', 'Find Your Niche — AI-powered taste discovery platform, live on the web.', 'LIVE')]
    y = 34
    for i, (a_, t, d, tag) in enumerate(logs):
        b += mono(640, y + 12, a_, 11, G2, 'start', 3) + T(640, y + 44, t, 26, HEAD, K, 'start', '400', 1, f'textLength="{round(len(t)*26*.49+len(t))}" lengthAdjust="spacingAndGlyphs"')
        lines = textwrap.wrap(d, 60)
        for j, ln in enumerate(lines): b += T(640, y + 72 + j * 21, ln, 15, SANS, '#333')
        ty = y + 72 + len(lines) * 21 + 8
        b += R(640, ty, 118, 26, K, K, 0) + f'<circle cx="656" cy="{ty+13}" r="4" fill="{W_}">{anim("opacity", "1;.15;1", 1.4)}</circle>' + mono(668, ty + 17, tag, 11, W_, 'start', 2)
        y += 190
    b += mono(1170, 404, 'MAY 2026 → AUG 2026', 10, G2, 'end', 2)
    section('s4-field.svg', '04', 'FIELD LOG', 'SEC. 04 / EXPERIENCE', b, bh, 'Workmates, Software Development Intern, May to August 2026, with production deployments.')

# ============================================================ HEADER-ONLY SECTION
def header_only(fn, num, title, note, desc):
    body = FR(0, 0, 1200, 10, K) + FR(0, 0, 1200, 0, W_)
    # slim black band, so the cases below hang from the header
    section(fn, num, title, note, FR(0, 0, 1200, 4, W_), 4, desc)

# ============================================================ CASE FILES
def chips_row(x, y, tags, maxx, fg, bg):
    s = ''; cx, cy = x, y
    for i, t in enumerate(tags):
        w = len(t) * 7.6 + 20
        if cx + w > maxx: cx, cy = x, cy + 32
        s += R(cx, cy, w, 24, 'none', fg, 1.8) + mono(cx + 10, cy + 16, t, 11, fg, 'start', 0)
        s += f'<rect x="{cx}" y="{cy}" width="{w:.0f}" height="24" fill="{fg}" opacity="0"><animate attributeName="opacity" values="0;.18;0;0" keyTimes="0;.05;.16;1" dur="{len(tags)*1.3:.1f}s" begin="{i*1.3:.1f}s" repeatCount="indefinite"/></rect>'
        cx += w + 8
    return s

def box(x, y, w, h, l1, l2, ink, paper, fill=False, sw=2.5):
    bg, fg = (ink, paper) if fill else (paper, ink)
    s = R(x, y, w, h, bg, ink, sw)
    cy = y + h / 2
    s += T(x + w / 2, cy + (-3 if l2 else 6), l1, 16, HEAD, fg, 'middle', '400', 1, f'textLength="{round(len(l1)*16*.49+len(l1))}" lengthAdjust="spacingAndGlyphs"')
    if l2: s += T(x + w / 2, cy + 14, l2, 9.5, MONO, fg, 'middle')
    return s

def d1(ink, pap):
    s = ''; ins = [('MULTILINGUAL', 'query'), ('AGRI KNOWLEDGE', 'base'), ('WEATHER · GEO', 'context'), ('CROP IMAGERY', 'computer vision')]
    hub = (370, 200)
    for i, (a_, b_) in enumerate(ins):
        y = 24 + i * 92; s += box(0, y, 200, 62, a_, b_, ink, pap, i % 2 == 1)
        ang = math.atan2(hub[1] - (y + 31), hub[0] - 200)
        ex = hub[0] - 82 * math.cos(ang); ey = hub[1] - 82 * math.sin(ang)
        s += arrow(200, y + 31, round(ex), round(ey), ink, 2)
        s += packet(f'M202 {y+31} L{ex:.0f} {ey:.0f}', 2.4, i * .55, ink, pap, 4)
        s += flash(0, y, 200, 62, i, 4, pap if i % 2 == 1 else ink, .22, .6)
    s += C(hub[0], hub[1], 66, ink, ink, 3)
    s += f'<circle cx="{hub[0]}" cy="{hub[1]}" r="78" fill="none" stroke="{ink}" stroke-width="1.5" stroke-dasharray="4 5">{spin(hub[0], hub[1], 12)}</circle>'
    s += f'<circle cx="{hub[0]}" cy="{hub[1]}" r="66" fill="none" stroke="{ink}" stroke-width="2">{anim("r", "66;104", 2.6)}{anim("opacity", ".8;0", 2.6)}</circle>'
    s += T(hub[0], hub[1] - 2, 'RAG', 36, HEAD, pap, 'middle') + T(hub[0], hub[1] + 20, 'retrieve · ground', 10, MONO, pap, 'middle')
    s += arrow(hub[0] + 80, hub[1], 478, hub[1], ink, 3) + packet(f'M{hub[0]+82} {hub[1]} H476', 1.8, 0, ink, pap, 4.5)
    s += box(480, 130, 170, 140, 'CROP', 'INTELLIGENCE', ink, pap, True)
    s += f'<rect x="480" y="130" width="170" height="140" fill="{pap}" opacity="0">{anim("opacity", "0;.2;0;0", 2.4, 0.9, "0;.2;.45;1")}</rect>'
    s += mono(565, 300, 'UNIFIED SYSTEM OUTPUT', 9, ink, 'middle', 1) + mono(0, 392, 'FIG. 03 — GROUNDED GENERATION OVER FOUR SOURCES', 10, ink, 'start', 2)
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
    # radar sweep
    wedge = f'M{cx} {cy}L{cx+176} {cy}A176 176 0 0 0 {cx+176*math.cos(math.radians(-42)):.1f} {cy+176*math.sin(math.radians(-42)):.1f}Z'
    s += f'<g>{spin(cx, cy, 6)}<path d="{wedge}" fill="{ink}" opacity=".16"/><line x1="{cx}" y1="{cy}" x2="{cx+176}" y2="{cy}" stroke="{ink}" stroke-width="2.5"/></g>'
    for p in near: s += f'<line x1="{cx}" y1="{cy}" x2="{p[0]:.0f}" y2="{p[1]:.0f}" stroke="{ink}" stroke-width="3" stroke-dasharray="9 5"><animate attributeName="stroke-dashoffset" from="28" to="0" dur="1.2s" repeatCount="indefinite"/></line>'
    for i, p in enumerate(pts):
        th = (math.degrees(math.atan2(p[1] - cy, p[0] - cx)) + 360) % 360
        big = p in near
        r0 = 6 if big else 4.5
        s += f'<circle cx="{p[0]:.0f}" cy="{p[1]:.0f}" r="{r0}" fill="{ink if big or i % 3 == 0 else pap}" stroke="{ink}" stroke-width="2"><animate attributeName="r" values="{r0};{r0+4};{r0}" keyTimes="0;.04;.14" dur="6s" begin="{th/360*6:.2f}s" repeatCount="indefinite"/></circle>'
    for r, d_ in ((60, 9), (120, 15), (175, 22)):
        s += f'<circle r="3.2" fill="{ink}" stroke="{pap}" stroke-width="1.2"><animateMotion dur="{d_}s" repeatCount="indefinite" path="M{cx+r} {cy}a{r} {r} 0 1 1 {-2*r} 0a{r} {r} 0 1 1 {2*r} 0"/></circle>'
    s += C(cx, cy, 24, pap, ink, 4) + C(cx, cy, 12, ink, ink, 1)
    s += f'<circle cx="{cx}" cy="{cy}" r="24" fill="none" stroke="{ink}" stroke-width="2">{anim("r", "24;50", 2.2)}{anim("opacity", ".9;0", 2.2)}</circle>'
    s += L(cx + 20, cy - 20, 500, 96, ink, 1.5) + R(470, 74, 150, 22, ink, ink, 0) + mono(545, 89, 'USER TASTE PROFILE', 9, pap, 'middle', 1)
    s += f'<rect x="470" y="74" width="150" height="22" fill="{pap}" opacity="0">{anim("opacity", "0;.3;0;0", 3, 0, "0;.1;.3;1")}</rect>'
    s += mono(0, 392, 'FIG. 04 — SEMANTIC SIMILARITY ACROSS FOUR CATALOGS', 10, ink, 'start', 2)
    return s

def face(x, y, w, h, ink, pap):
    cx = x + w / 2; s = R(x, y, w, h, pap, ink, 2.5)
    s += f'<ellipse cx="{cx}" cy="{y+h/2-6}" rx="{w*.27}" ry="{h*.34}" fill="none" stroke="{ink}" stroke-width="2.5"/>'
    s += L(cx - w * .13, y + h * .42, cx - w * .05, y + h * .42, ink, 3) + L(cx + w * .05, y + h * .42, cx + w * .13, y + h * .42, ink, 3) + L(cx, y + h * .46, cx - 3, y + h * .56, ink, 2) + L(cx - w * .08, y + h * .66, cx + w * .08, y + h * .66, ink, 2.5)
    return s

def d3(ink, pap):
    s = face(0, 50, 150, 200, ink, pap)
    s += f'<g>{anim("opacity", ".5;1;.5", 1.6)}{corners(24, 78, 102, 120, ink, 16, 4)}</g>'
    s += f'<rect x="2" y="50" width="146" height="3" fill="{ink}"><animate attributeName="y" values="52;246;52" dur="2.8s" repeatCount="indefinite"/></rect>'
    s += mono(75, 270, 'INPUT FRAME', 10, ink, 'middle', 1) + mono(75, 40, 'RETINAFACE', 10, ink, 'middle', 2)
    s += arrow(152, 150, 186, 150, ink, 2.5) + packet('M154 150 H184', 1.6, 0, ink, pap, 3.6)
    for i in range(3):
        s += f'<g>{atrans("translate", "0 0;6 -6;0 0", 2.4, i * .3)}{R(190 + i * 14, 98 + i * 14 - 14, 66, 108, pap if i < 2 else ink, ink, 2.5)}</g>'
    s += T(251, 172, 'CNN', 22, HEAD, pap, 'middle') + mono(224, 270, 'CNN INFERENCE', 10, ink, 'middle', 1)
    s += arrow(290, 150, 322, 150, ink, 2.5) + packet('M292 150 H320', 1.6, .5, ink, pap, 3.6)
    fx = 326; s += face(fx, 50, 150, 200, ink, pap)
    s += f'<defs><radialGradient id="hm"><stop offset="0" stop-color="{ink}"/><stop offset="1" stop-color="{ink}" stop-opacity="0"/></radialGradient></defs><ellipse cx="{fx+75}" cy="118" rx="52" ry="42" fill="url(#hm)" opacity=".85">{anim("rx", "46;58;46", 2.2)}{anim("opacity", ".5;.95;.5", 2.2)}</ellipse><ellipse cx="{fx+75}" cy="118" rx="52" ry="42" fill="url(#dots{"W" if ink==W_ else ""})" opacity=".6"/>'
    s += mono(fx + 75, 270, 'GRAD-CAM HEATMAP', 10, ink, 'middle', 1)
    s += arrow(478, 150, 508, 150, ink, 2.5) + packet('M480 150 H506', 1.6, 1, ink, pap, 3.6) + box(510, 100, 140, 100, 'FASTAPI', 'STREAMLIT', ink, pap, True) + mono(580, 220, 'ANALYSIS OUTPUT', 10, ink, 'middle', 1)
    s += f'<rect x="510" y="100" width="140" height="100" fill="{pap}" opacity="0">{anim("opacity", "0;.22;0;0", 3, .6, "0;.1;.3;1")}</rect>'
    s += mono(0, 392, 'FIG. 05 — DETECT · CLASSIFY · EXPLAIN', 10, ink, 'start', 2)
    return s

def d4(ink, pap):
    s = R(0, 70, 170, 220, ink, ink, 3) + f'<ellipse cx="85" cy="180" rx="62" ry="78" fill="{pap}" stroke="{pap}" stroke-width="2"/>'
    s += f'<ellipse cx="85" cy="180" rx="50" ry="66" fill="url(#dots{"W" if ink==W_ else ""})" stroke="{ink}" stroke-width="2"/><path d="M85 118V244M58 150Q85 170 112 150M54 200Q85 180 116 200" stroke="{ink}" stroke-width="2.5"/>'
    s += f'<rect x="2" y="72" width="166" height="3" fill="{pap}"><animate attributeName="y" values="72;286;72" dur="3.2s" repeatCount="indefinite"/></rect>'
    s += mono(85, 312, 'MRI SLICE', 10, ink, 'middle', 1) + arrow(176, 180, 214, 180, ink, 2.5)
    xs = [220, 290, 352, 408]; ws = [58, 46, 36, 28]; hs = [170, 130, 96, 66]
    for i in range(4):
        cy = 180; filled = i % 2 == 0
        s += R(xs[i], cy - hs[i] / 2, ws[i], hs[i], ink if filled else pap, ink, 2.5)
        s += flash(xs[i], cy - hs[i] / 2, ws[i], hs[i], i, 4, pap if filled else ink, .4, .7)
    s += mono(320, 312, 'CONVOLUTIONAL FEATURE EXTRACTION', 10, ink, 'middle', 1)
    s += arrow(440, 180, 478, 180, ink, 2.5)
    for i in range(3): s += f'<circle cx="500" cy="{130+i*50}" r="11" fill="{pap if i != 1 else ink}" stroke="{ink}" stroke-width="2.5">{anim("r", "11;14;11", 1.6, i * .3)}</circle>'
    for i in range(3): s += L(511, 130 + i * 50, 568, 180, ink, 1.5)
    s += box(570, 140, 80, 80, 'CLASS', 'PREDICTION', ink, pap, True) + mono(505, 312, 'DENSE', 10, ink, 'middle', 1)
    s += f'<rect x="570" y="140" width="80" height="80" fill="{pap}" opacity="0">{anim("opacity", "0;.3;0;0", 3.2, 2.4, "0;.1;.3;1")}</rect>'
    s += packet('M176 180 H566', 3.2, 0, ink, pap, 5)
    s += mono(0, 392, 'FIG. 06 — IMAGE → CNN → CLASSIFICATION', 10, ink, 'start', 2)
    return s

def d5(ink, pap):
    s = box(0, 150, 100, 100, 'NL', 'QUERY', ink, pap, True) + arrow(102, 200, 140, 200, ink, 2.5) + packet('M104 200 H138', 1.8, 0, ink, pap, 3.8)
    nodes = {'a': (190, 70), 'b': (300, 50), 'c': (390, 110), 'd': (160, 180), 'e': (270, 190), 'f': (370, 230), 'g': (200, 310), 'h': (310, 320)}
    ed = [('a', 'b'), ('b', 'c'), ('a', 'd'), ('b', 'e'), ('c', 'f'), ('d', 'e'), ('e', 'f'), ('d', 'g'), ('e', 'h'), ('g', 'h'), ('f', 'h')]
    path = {('a', 'd'), ('d', 'e'), ('e', 'f')}
    s += R(140, 20, 280, 340, 'none', ink, 1.5, 0, 'stroke-dasharray="4 5"')
    for p, q in ed:
        hl = (p, q) in path; s += L(nodes[p][0], nodes[p][1], nodes[q][0], nodes[q][1], ink, 5 if hl else 1.6)
    for k, (x, y) in nodes.items(): s += C(x, y, 15 if k in 'adef' else 11, ink if k in 'adef' else pap, ink, 3)
    for i, k in enumerate('adef'):
        x, y = nodes[k]
        s += f'<circle cx="{x}" cy="{y}" r="15" fill="none" stroke="{ink}" stroke-width="2.5" opacity="0"><animate attributeName="r" values="15;36" dur="3.6s" begin="{i*.8:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".9;0" dur="3.6s" begin="{i*.8:.1f}s" repeatCount="indefinite"/></circle>'
    s += packet('M190 70 L160 180 L270 190 L370 230', 3.6, 0, pap, ink, 4.5)
    s += mono(280, 14, 'NEO4J KNOWLEDGE GRAPH', 10, ink, 'middle', 2) + mono(280, 378, 'entity · relation · fact', 10, ink, 'middle', 1)
    for i, (a_, b_) in enumerate([('GRAPHRAG', 'RETRIEVAL'), ('LLM', 'REASONING'), ('FINANCIAL', 'EXPLANATION')]):
        y = 30 + i * 130; s += box(450, y, 200, 76, a_, b_, ink, pap, i != 1)
        s += flash(450, y, 200, 76, i, 3, pap if i != 1 else ink, .24, 1.2)
        if i < 2: s += arrow(550, y + 78, 550, y + 128, ink, 2.5) + packet(f'M550 {y+80} V{y+126}', 1.6, i * .8, ink, pap, 3.6)
    s += arrow(420, 130, 448, 70, ink, 2.5) + mono(0, 392, 'FIG. 07 — GRAPH-GROUNDED REASONING', 10, ink, 'start', 2)
    return s

def case(fn, num, title_lines, desc, tags, diag, text_left, inv, figtitle):
    W, H = 1200, 460
    tp = "M0,0 L490,0 L450,460 L0,460 Z" if text_left else "M710,0 L1200,0 L1200,460 L750,460 Z"
    dp = "M506,0 L1200,0 L1200,460 L466,460 Z" if text_left else "M0,0 L694,0 L734,460 L0,460 Z"
    tb, tf = (K, W_) if inv else (W_, K); db, df = (W_, K) if inv else (K, W_)
    b = FR(0, 0, W, H, W_)
    b += f'<path d="{dp}" fill="{db}"/><path d="{dp}" fill="url(#grid{"K" if db==W_ else "W"})"/>'
    b += f'<path d="{tp}" fill="{tb}"/>'
    tx = 40 if text_left else 774
    b += mono(tx, 48, f'CASE FILE / {num}', 12, tf, 'start', 3) + f'<rect x="{tx+190}" y="38" width="10" height="10" fill="{tf}">{anim("opacity", "1;0;1", 1.2)}</rect>'
    b += head(tx - 4, 138, num, 108, tb, None, tf)
    y = 178
    for t in title_lines: b += head(tx, y, t, 32, tf, int(len(t) * 15.5)); y += 36
    y += 4
    for ln in textwrap.wrap(desc, 50): b += T(tx, y, ln, 14.5, SANS, tf, 'start', '400'); y += 20
    b += chips_row(tx, y + 8, tags, tx + 384, tf, tb)
    ox = 520 if text_left else 30
    b += f'<g transform="translate({ox} 34)">{diag(df, db)}</g>'
    b += edges(W, H, top=5, bottom=0)
    svg2(fn, W, H, b, f'Case file {num}: {" ".join(title_lines)}', figtitle)

def endstrip(fn, w, h, text):
    random.seed(3)
    b = FR(0, 0, w, h, W_)
    bars = ''.join(FR(x, 14, random.choice([2, 3, 5, 8]), h - 28, K) for x in range(0, 1200, 14) if random.random() > .25)
    b += f'<clipPath id="es"><rect width="{w}" height="{h}"/></clipPath><g clip-path="url(#es)"><g>{atrans("translate", "0 0;-168 0", 6)}{bars}</g></g>'
    b += FR(0, 0, 470, h, W_) + mono(28, h / 2 + 5, text, 13, K, 'start', 3)
    b += edges(w, h, top=5, bottom=0)
    svg2(fn, w, h, b, text, text)

# ============================================================ HIGHLIGHTS (flush grid)
def highlights():
    bh = 400
    cells = [(0, 0, 400, 190, 'SIH', 'Smart India Hackathon', 'Finalist', True), (400, 0, 400, 190, '05', 'AI / ML engineering projects', 'Agriculture, taste, forensics, medical imaging, finance', False),
             (800, 0, 400, 190, 'INTERN', 'Software development internship', 'Workmates · May–Aug 2026', True), (0, 190, 500, 210, 'LIVE', 'Deployed products', 'Two institutional websites and Find Your Niche', False),
             (500, 190, 340, 210, 'IEEE', 'Student branch team lead', 'Technical coordination', True), (840, 190, 360, 210, 'ML·GENAI', 'Technical experimentation', 'ML, GenAI and AI systems', False)]
    b = FR(0, 0, 1200, bh, K)
    for i, (x, y, w, h, big, l1, l2, inv) in enumerate(cells):
        bg, fg = (W_, K) if inv else (K, W_)
        b += FR(x, y, w, h, bg)
        b += halftone(x + w - 150, y + 10, 140, 70, 'mH', fg, .5)
        b += mono(x + 24, y + 30, f'H-0{i+1}', 10, fg, 'start', 3)
        b += head(x + 24, y + 90, big, 66, fg, min(len(big) * 31 + 10, w - 60))
        b += L(x + 24, y + 104, x + w - 30, y + 104, fg, 2) + f'<rect x="{x+24}" y="{y+101}" width="46" height="6" fill="{fg}"><animate attributeName="x" values="{x+24};{x+w-76};{x+24}" dur="{4+i*.5:.1f}s" repeatCount="indefinite"/></rect>'
        b += T(x + 24, y + 134, l1, 18, SANS, fg, 'start', '700')
        for j, ln in enumerate(textwrap.wrap(l2, 44)): b += T(x + 24, y + 156 + j * 17, ln, 13, SANS, fg)
        b += flash(x, y, w, h, i, 6, W_ if not inv else K, .16, 1.5)
    for xx in (400, 800): b += FR(xx - 2.5, 0, 5, 190)
    for xx in (500, 840): b += FR(xx - 2.5, 190, 5, 210)
    b += FR(0, 187.5, 1200, 5)
    section('s6-highlights.svg', '06', 'HIGHLIGHTS', 'SEC. 06 / RECORD', b, bh, 'Six highlight panels: SIH finalist, projects, internship, deployed products, IEEE, experimentation.')

# ============================================================ FOOTER
def footer():
    W, H = 1200, 390
    b = FR(0, 0, W, H, K) + halftone(0, 49, W, H - 49, 'mH', W_, .25)
    b += marquee(0, 5, W, 44, 'BUILD.  EXPERIMENT.  DEPLOY.', 30, K, W_, dur=24, gap='   ✦   ')
    b += FR(0, 47, W, 4, K)
    b += f'<polygon points="30,78 1170,78 1150,366 30,366" fill="{W_}"/>'
    b += mono(64, 112, 'CONTACT / END OF DOSSIER', 12, K, 'start', 3)
    b += head(60, 194, "LET'S BUILD SOMETHING", 80, K, 760) + head(60, 276, 'INTELLIGENT.', 80, W_, 430, K)
    b += f'<rect x="510" y="222" width="16" height="54" fill="{K}">{anim("opacity", "1;0;1", 1.1)}</rect>'
    b += halftone(560, 200, 250, 70, 'mH', K)
    b += mono(64, 326, 'DATA → RETRIEVAL → REASONING → MODEL → API → PRODUCT', 12, K, 'start', 2)
    b += f'<rect x="64" y="336" width="60" height="4" fill="{K}"><animate attributeName="x" values="64;470;64" dur="5s" repeatCount="indefinite"/></rect>' + L(64, 338, 530, 338, K, 1)
    fcx, fcy = 1000, 218
    b += f'<defs><clipPath id="fc"><circle cx="{fcx}" cy="{fcy}" r="78"/></clipPath></defs>'
    b += C(fcx, fcy, 86, K, K, 3)
    b += f'<g clip-path="url(#fc)"><image href="data:image/jpeg;base64,{CHAR_FACE}" x="{fcx-90}" y="{fcy-92}" width="180" height="180" preserveAspectRatio="xMidYMid slice"/></g>'
    b += f'<circle cx="{fcx}" cy="{fcy}" r="100" fill="none" stroke="{K}" stroke-width="2" stroke-dasharray="3 7">{spin(fcx, fcy, 18)}</circle>'
    b += f'<circle cx="{fcx}" cy="{fcy}" r="112" fill="none" stroke="{K}" stroke-width="1.5" stroke-dasharray="18 10">{spin(fcx, fcy, 30, True)}</circle>'
    b += f'<circle cx="{fcx}" cy="{fcy}" r="86" fill="none" stroke="{K}" stroke-width="2">{anim("r", "86;126", 2.8)}{anim("opacity", ".7;0", 2.8)}</circle>'
    for (sx, sy, sr, sd) in [(912, 150, 11, 0), (1090, 164, 14, .9), (1070, 300, 9, 1.8)]: b += star(sx, sy, sr, K, sd, 3)
    b += mono(fcx, 350, 'SHLOK MISHRA · AI / ML', 10, K, 'middle', 2)
    b += edges(W, H, top=5, bottom=0)
    svg2('footer.svg', W, H, b, 'Contact', "Let's build something intelligent.")

# ============================================================ BUILD
hero()
# link bar under hero (4 cells, 25% each)
cell('lk-github.svg', 300, 70, 'GITHUB', 'github.com/ShlokMishra01', 'GH', False, first=True)
cell('lk-linkedin.svg', 300, 70, 'LINKEDIN', 'in/shlok-mishra-9a649b255', 'in', True)
cell('lk-email.svg', 300, 70, 'EMAIL', MAIL, '@', False)
cell('lk-resume.svg', 300, 70, 'RESUME', 'download pdf', 'CV', True, last=True)
profile(); pipeline(); stack(); field()
# live links (34 / 33 / 33 %)
cell('lv-sunita.svg', 408, 70, 'SUNITA NURSING SCHOOL', 'sunitanursingschool.in', '', False, first=True, live=True)
cell('lv-pharmacy.svg', 396, 70, 'COLLEGE OF PHARMACY', 'nsuryawanshicop.com', '', True, live=True)
cell('lv-niche.svg', 396, 70, 'FIND YOUR NICHE', 'find-your-niche-01.vercel.app', '', False, last=True, live=True)
header_only('s5-work.svg', '05', 'SELECTED WORK', 'SEC. 05 / CASE FILES', 'Section 05: selected work, five case files.')
case('c1.svg', '01', ['PRITHVI', 'AGRO AI'], 'AI-powered agricultural assistant combining multilingual RAG, agricultural knowledge, weather/geospatial context, computer vision and crop intelligence in one system.', ['RAG', 'Multilingual', 'Computer vision', 'Geospatial'], d1, True, True, 'Four input sources feed a RAG core that produces crop intelligence.')
cell('c1-repo.svg', 1200, 64, 'OPEN REPOSITORY', 'github.com/ShlokMishra01/prithvi-agro-ai', 'GH', False, first=True, last=True)
case('c2.svg', '02', ['FIND YOUR', 'NICHE'], 'AI-powered taste discovery platform that understands preferences across movies, books, music and coding/open-source projects.', ['taste profiling', 'semantic similarity', 'recommendations', 'RAG chat', 'taste mapping', 'social discovery'], d2, False, False, 'Taste map with four catalog quadrants and similarity links to a user profile.')
cell('c2-live.svg', 600, 64, 'LIVE DEMO', 'find-your-niche-01.vercel.app', '', True, first=True, live=True)
cell('c2-repo.svg', 600, 64, 'REPOSITORY', 'github.com/ShlokMishra01/Find-your-niche-', 'GH', False, last=True)
case('c3.svg', '03', ['ADVANCED DEEPFAKE', 'DETECTION'], 'Computer-vision system for analysing potentially manipulated images and videos.', ['RetinaFace', 'CNN', 'Grad-CAM', 'FastAPI', 'Streamlit'], d3, True, True, 'Face detection, CNN inference and Grad-CAM explanation behind an API.')
cell('c3-repo.svg', 1200, 64, 'OPEN REPOSITORY', 'github.com/ShlokMishra01/Deepfake-Image-and-video-analyzer', 'GH', False, first=True, last=True)
case('c4.svg', '04', ['NEURO', 'DETECT AI'], 'AI-based MRI analysis project using convolutional neural networks for medical-image classification.', ['CNN', 'MRI', 'image classification'], d4, False, False, 'MRI slice passes through convolutional blocks to a class prediction.')
endstrip('c4-end.svg', 1200, 64, 'CASE FILE 04  /  END OF FILE')
case('c5.svg', '05', ['FINANCEFLOW AI'], 'Finance-focused GraphRAG system using structured financial knowledge and Neo4j to improve the reliability of AI-assisted financial reasoning.', ['GraphRAG', 'Neo4j', 'LLM reasoning', 'financial data workflows'], d5, True, True, 'Natural-language query retrieved from a Neo4j graph, then reasoned over by an LLM.')
cell('c5-repo.svg', 1200, 64, 'OPEN REPOSITORY', 'github.com/ShlokMishra01/Fintech-assistant-model-with-neo4j-and-Python', 'GH', False, first=True, last=True)
highlights(); footer()
cell('ct-github.svg', 408, 72, 'GITHUB', 'github.com/ShlokMishra01', 'GH', True, first=True, bottom=True)
cell('ct-linkedin.svg', 396, 72, 'LINKEDIN', 'in/shlok-mishra-9a649b255', 'in', False, bottom=True)
cell('ct-email.svg', 396, 72, 'EMAIL', MAIL, '@', True, last=True, bottom=True)
print(len(os.listdir(A)), 'svgs written to', A)
