
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
        b += T(x + bw / 2, y + 136, s_, 9.5, MONO, fg, 'middle')
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
    b += f'<polygon points="0,0 520,0 470,{bh}" fill="{K}"/><polygon points="0,0 520,0 470,{bh} 0,{bh}" fill="{K}"/>' + halftone(0, 230, 450, bh - 230, 'mV', W_, .9)
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
    y = 44
    for i, (a_, t, d, tag) in enumerate(logs):
        b += mono(640, y + 12, a_, 11, G2, 'start', 3) + T(640, y + 44, t, 26, HEAD, K, 'start', '400', 1, f'textLength="{round(len(t)*26*.49+len(t))}" lengthAdjust="spacingAndGlyphs"')
        lines = textwrap.wrap(d, 60)
        for j, ln in enumerate(lines): b += T(640, y + 72 + j * 21, ln, 15, SANS, '#333')
        ty = y + 72 + len(lines) * 21 + 8
        b += R(640, ty, 118, 26, K, K, 0) + f'<circle cx="656" cy="{ty+13}" r="4" fill="{W_}">{anim("opacity", "1;.15;1", 1.4)}</circle>' + mono(668, ty + 17, tag, 11, W_, 'start', 2)
        y += 178
    b += mono(1170, 404, 'MAY 2026 → AUG 2026', 10, G2, 'end', 2)
    section('s4-field.svg', '04', 'FIELD LOG', 'SEC. 04 / EXPERIENCE', b, bh, 'Workmates, Software Development Intern, May to August 2026, with production deployments.')

# ============================================================ HEADER-ONLY SECTION
def header_only(fn, num, title, note, desc):
    body = FR(0, 0, 1200, 10, K) + FR(0, 0, 1200, 0, W_)
    # slim black band, so the cases below hang from the header
    section(fn, num, title, note, FR(0, 0, 1200, 14, W_), 14, desc)
