
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
    b = FR(0, 0, w, h, K)
    bars = ''.join(FR(x, 14, random.choice([2, 3, 5, 8]), h - 28, W_) for x in range(0, 1200, 14) if random.random() > .25)
    b += f'<clipPath id="es"><rect width="{w}" height="{h}"/></clipPath><g clip-path="url(#es)"><g>{atrans("translate", "0 0;-168 0", 6)}{bars}</g></g>'
    b += FR(0, 0, 560, h, K) + mono(28, h / 2 + 5, text, 13, W_, 'start', 3)
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
        b += head(x + 24, y + 96, big, 66, fg, min(len(big) * 31 + 10, w - 60))
        b += L(x + 24, y + 112, x + w - 30, y + 112, fg, 2) + f'<rect x="{x+24}" y="109" width="46" height="6" fill="{fg}"><animate attributeName="x" values="{x+24};{x+w-76};{x+24}" dur="{4+i*.5:.1f}s" repeatCount="indefinite"/></rect>'
        b += T(x + 24, y + 144, l1, 18, SANS, fg, 'start', '700')
        for j, ln in enumerate(textwrap.wrap(l2, 44)): b += T(x + 24, y + 168 + j * 18, ln, 13, SANS, fg)
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
