
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
    b += FR(14, 482, 1172, 104, K)
    st = [('INPUT', 'raw signals'), ('DATA', 'clean · structure'), ('MODEL', 'learn · evaluate'), ('INFERENCE', 'serve · explain'), ('OUTPUT', 'decisions')]
    for i, (a_, s_) in enumerate(st):
        x = 44 + i * 226
        b += R(x, 510, 176, 56, K, W_, 2.5) + mono(x + 10, 504, f'0{i+1}', 10, W_, 'start', 2)
        b += T(x + 88, 541, a_, 27, HEAD, W_, 'middle') + mono(x + 88, 558, s_, 10, '#a8a8a8', 'middle', 1)
        b += flash(x, 510, 176, 56, i, 5, W_, .22, 1.0)
        if i < 4:
            b += f'<line x1="{x+176}" y1="538" x2="{x+222}" y2="538" stroke="{W_}" stroke-width="2.5" stroke-dasharray="7 5" marker-end="url(#ahW)"><animate attributeName="stroke-dashoffset" from="24" to="0" dur="1.4s" repeatCount="indefinite"/></line>'
            b += packet(f'M{x+178} 538 H{x+220}', 5, 0, W_, K, 3.2, slot=(i / 5, i / 5 + .2))
    b += edges(W, H, top=5, bottom=0)
    b += f'<path d="M0 {H}V0H{W}V{H}" fill="none"/>'
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
    if bottom: b += FR(0, h - 5, w, 5)
    b += FR(0, 0, 5 if first else 3, h) if first else FR(0, 0, 3, h)
    if last: b += FR(w - 5, 0, 5, h)
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
    s += f'<text x="8" y="352" font-family="{HEAD}" font-size="330" fill="none" stroke="{W_}" stroke-width="2.5" textLength="450" lengthAdjust="spacingAndGlyphs" stroke-dasharray="2600" stroke-dashoffset="2600" opacity=".6">SM<animate attributeName="stroke-dashoffset" from="2600" to="0" dur="3.2s" fill="freeze"/></text>'
    s += f'<circle cx="236" cy="256" r="196" fill="none" stroke="{W_}" stroke-width="1.6" stroke-dasharray="2 9" opacity=".55">{spin(236, 256, 46)}</circle>'
    s += f'<circle cx="236" cy="256" r="236" fill="none" stroke="{W_}" stroke-width="1.6" stroke-dasharray="16 10" opacity=".3">{spin(236, 256, 60, True)}</circle>'
    s += f'<image href="data:image/jpeg;base64,{CHAR_BODY}" x="-22" y="14" width="486" height="504" preserveAspectRatio="xMidYMid slice" mask="url(#chm)"/>'
    for (sx, sy, sr, sd) in [(60, 118, 12, 0), (412, 96, 17, .9), (432, 300, 11, 1.7), (44, 330, 14, 2.3), (330, 36, 9, 1.2), (390, 410, 13, .4), (238, 226, 10, 2.8)]:
        s += star(sx, sy, sr, W_, sd, 3.6)
    s += f'<g><animateTransform attributeName="transform" type="translate" values="0 -70;0 {bh}" dur="5.4s" repeatCount="indefinite"/><rect y="0" width="480" height="70" fill="url(#scG)"/></g>'
    s += '</g>'
    s += f'<g>{anim("opacity", ".45;1;.45", 2.4)}{corners(24, 24, 398, 422, W_, 20, 3)}</g>'
    s += mono(40, 56, 'PROFILE / 01', 12, W_, 'start', 3)
    s += f'<polygon points="24,408 262,408 244,440 24,440" fill="{K}" stroke="{W_}" stroke-width="1.5"/>' + mono(38, 429, 'SHLOK MISHRA · AI / ML DEVELOPER', 10, W_, 'start', 1)
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
