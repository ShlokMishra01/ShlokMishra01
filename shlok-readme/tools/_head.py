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

