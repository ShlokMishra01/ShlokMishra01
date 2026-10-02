
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

def edges(W, H, top=5, bottom=0, left=5, right=5):
    s = ''
    if top: s += FR(0, 0, W, top)
    if bottom: s += FR(0, H - bottom, W, bottom)
    if left: s += FR(0, 0, left, H)
    if right: s += FR(W - right, 0, right, H)
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
