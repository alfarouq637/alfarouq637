#!/usr/bin/env python3
"""Generates the self-hosted SVG assets for the profile README.

Every asset is an opaque card (own background + border) so it looks the same on
GitHub light and dark themes. Animation uses SMIL only (works inside <img>).
"""
import random
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

BG = "#0B1020"
PANEL = "#111833"
PANEL2 = "#161F42"
BORDER = "#24305A"
TEXT = "#E6EAF5"
MUTED = "#8B97B8"
BLUE = "#6C8CFF"
CYAN = "#4FD1C5"
GOLD = "#F5B971"
VIOLET = "#A78BFA"
FONT = "'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, title, desc=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">
<title id="t">{esc(title)}</title>
<desc id="d">{esc(desc or title)}</desc>
<defs>
<linearGradient id="gA" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="gB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{PANEL2}"/><stop offset="1" stop-color="{PANEL}"/></linearGradient>
<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#FFFFFF" stroke-opacity="0.035" stroke-width="1"/></pattern>
</defs>
{body}
</svg>
"""


def card_bg(w, h, r=18):
    return (
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="{BG}" stroke="{BORDER}"/>'
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="url(#grid)"/>'
    )


def write(name, content):
    (OUT / name).write_text(content, encoding="utf-8")
    print("wrote", name, len(content), "bytes")


# --------------------------------------------------------------------------- hero
def hero():
    W, H = 900, 340
    random.seed(11)
    layers = [4, 6, 6, 4, 3]
    xs = [520, 610, 700, 790, 870]
    cy = 170
    gap = 38
    pts = []
    for n, x in zip(layers, xs):
        pts.append([(x, cy + (i - (n - 1) / 2) * gap) for i in range(n)])

    parts = [card_bg(W, H, 20)]
    parts.append(
        f'<radialGradient id="rg" cx="0.78" cy="0.5" r="0.55"><stop offset="0" stop-color="{BLUE}" stop-opacity="0.22"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>'
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="20" fill="url(#rg)"/>'
    )

    # edges
    edges = []
    for li in range(len(layers) - 1):
        for (x1, y1) in pts[li]:
            for (x2, y2) in pts[li + 1]:
                edges.append(f'<line x1="{x1}" y1="{y1:.1f}" x2="{x2}" y2="{y2:.1f}"/>')
    parts.append(f'<g stroke="{BLUE}" stroke-opacity="0.16" stroke-width="1">{"".join(edges)}</g>')

    # travelling pulses
    pulses = []
    for k in range(12):
        path = [random.choice(layer) for layer in pts]
        d = "M" + " L".join(f"{x},{y:.1f}" for x, y in path)
        dur = random.uniform(2.6, 3.8)
        begin = random.uniform(0, 3.5)
        col = CYAN if k % 3 else GOLD
        pulses.append(
            f'<circle r="3.2" fill="{col}" filter="url(#glow)" opacity="0">'
            f'<animateMotion dur="{dur:.2f}s" begin="{begin:.2f}s" repeatCount="indefinite" path="{d}"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.85;1" dur="{dur:.2f}s" begin="{begin:.2f}s" repeatCount="indefinite"/>'
            f"</circle>"
        )
    parts.append("<g>" + "".join(pulses) + "</g>")

    # nodes
    cols = [BLUE, VIOLET, VIOLET, CYAN, GOLD]
    nodes = []
    for li, layer in enumerate(pts):
        for (x, y) in layer:
            b = random.uniform(0, 3)
            nodes.append(
                f'<circle cx="{x}" cy="{y:.1f}" r="6.5" fill="{BG}" stroke="{cols[li]}" stroke-width="1.6"/>'
                f'<circle cx="{x}" cy="{y:.1f}" r="6.5" fill="none" stroke="{cols[li]}" stroke-width="1">'
                f'<animate attributeName="r" values="6.5;15" dur="3.2s" begin="{b:.2f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0.55;0" dur="3.2s" begin="{b:.2f}s" repeatCount="indefinite"/></circle>'
            )
    parts.append("<g>" + "".join(nodes) + "</g>")

    # layer labels
    for lbl, x in (("INPUT", xs[0]), ("HIDDEN", (xs[1] + xs[2]) / 2), ("OUTPUT", xs[-1])):
        parts.append(f'<text x="{x}" y="{H-24}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{MUTED}" letter-spacing="2">{lbl}</text>')

    # text block
    parts.append(f'<text x="44" y="64" font-family="{MONO}" font-size="12" fill="{CYAN}" letter-spacing="3">// AI SYSTEM ARCHITECT</text>')
    parts.append(f'<text x="44" y="112" font-family="{FONT}" font-size="36" font-weight="700" fill="{TEXT}" letter-spacing="0.5">ALFAROUQ IBRAHIM</text>')
    parts.append(f'<text x="44" y="150" font-family="{FONT}" font-size="21" font-weight="600" fill="url(#gA)">Edge-AI &amp; Computer Vision Specialist</text>')
    parts.append(f'<text x="44" y="182" font-family="{FONT}" font-size="14" fill="{MUTED}">Architecting intelligent systems.</text>')
    parts.append(f'<text x="44" y="204" font-family="{FONT}" font-size="14" fill="{MUTED}">Engineering real-world impact.</text>')
    # blinking cursor
    parts.append(
        f'<rect x="278" y="52" width="8" height="14" fill="{CYAN}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>'
    )

    # chips
    chips = ["Machine Learning", "Deep Learning", "Data Science"]
    x = 44
    for c in chips:
        w = 14 * 0.0 + len(c) * 7.2 + 26
        parts.append(
            f'<rect x="{x}" y="240" width="{w:.0f}" height="28" rx="14" fill="{PANEL}" stroke="{BORDER}"/>'
            f'<text x="{x + w/2:.0f}" y="259" text-anchor="middle" font-family="{FONT}" font-size="12.5" fill="{TEXT}">{c}</text>'
        )
        x += w + 10
    parts.append(f'<text x="44" y="304" font-family="{FONT}" font-size="12.5" fill="{MUTED}">Suez, Egypt  ·  Open to AI Architecture &amp; ML Engineering roles</text>')

    write(
        "hero.svg",
        svg(W, H, "".join(parts), "Alfarouq Ibrahim, AI System Architect",
            "Animated neural network banner. Alfarouq Ibrahim, AI System Architect, Edge-AI and Computer Vision Specialist."),
    )


# --------------------------------------------------------------------------- divider
def divider():
    W, H = 900, 22
    body = (
        f'<line x1="0" y1="11" x2="{W}" y2="11" stroke="{BORDER}" stroke-width="1"/>'
        f'<line x1="0" y1="11" x2="{W}" y2="11" stroke="url(#gA)" stroke-width="1.5" stroke-dasharray="90 810" stroke-opacity="0.9">'
        f'<animate attributeName="stroke-dashoffset" values="0;-900" dur="5s" repeatCount="indefinite"/></line>'
        + "".join(f'<circle cx="{x}" cy="11" r="3" fill="{BG}" stroke="{BLUE}" stroke-width="1.4"/>' for x in (150, 450, 750))
    )
    write("divider.svg", svg(W, H, body, "Section divider"))


# --------------------------------------------------------------------------- section banners
def banners():
    sections = [
        ("01", "ABOUT", "who I am"),
        ("02", "FOCUS AREAS", "what I build"),
        ("03", "MILESTONES", "results so far"),
        ("04", "CASE STUDIES", "systems I designed"),
        ("05", "PUBLIC REPOSITORIES", "open work on GitHub"),
        ("06", "TECH STACK", "tools I use"),
        ("07", "LEADERSHIP", "teams and community"),
        ("08", "CONNECT", "let's talk"),
    ]
    for num, title, sub in sections:
        W, H = 900, 56
        tw = len(title) * 11.5 + 8
        body = (
            f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="{PANEL}" stroke="{BORDER}"/>'
            f'<rect x="12" y="12" width="40" height="32" rx="9" fill="{BG}" stroke="{BLUE}" stroke-opacity="0.7"/>'
            f'<text x="32" y="33" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="700" fill="{CYAN}">{num}</text>'
            f'<text x="68" y="34" font-family="{FONT}" font-size="19" font-weight="700" fill="{TEXT}" letter-spacing="2">{title}</text>'
            f'<line x1="{68+tw+14:.0f}" y1="28" x2="{W-150}" y2="28" stroke="{BORDER}" stroke-dasharray="3 5"/>'
            f'<circle r="3" cy="28" fill="{CYAN}" filter="url(#glow)"><animate attributeName="cx" values="{68+tw+14:.0f};{W-150}" dur="3.4s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.85;1" dur="3.4s" repeatCount="indefinite"/></circle>'
            f'<text x="{W-18}" y="33" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">{sub}</text>'
        )
        fname = "section-" + title.lower().replace(" ", "-") + ".svg"
        write(fname, svg(W, H, body, f"Section {num}: {title.title()}"))


# --------------------------------------------------------------------------- focus cards
def focus():
    W, H = 900, 250
    cw, gap = 207, 24
    xs = [i * (cw + gap) for i in range(4)]
    cards = [
        ("EDGE-AI", CYAN, ["Offline-first systems", "that run where the data", "is: the farm, the factory."]),
        ("COMPUTER VISION", BLUE, ["Detection, tracking and", "re-identification with", "YOLOv8 + BoT-SORT."]),
        ("MACHINE LEARNING", VIOLET, ["Models built from scratch", "and production pipelines:", "CNNs, Random Forest."]),
        ("DATA SCIENCE", GOLD, ["Synthetic datasets, signal", "analysis (FFT) and apps", "that explain results."]),
    ]
    parts = []
    for (title, col, lines), x in zip(cards, xs):
        g = [
            f'<rect x="{x+0.5}" y="0.5" width="{cw-1}" height="{H-1}" rx="16" fill="url(#gB)" stroke="{BORDER}"/>',
            f'<rect x="{x+0.5}" y="0.5" width="{cw-1}" height="3" rx="1.5" fill="{col}" opacity="0.9"/>',
        ]
        ix, iy = x + 26, 30  # icon origin (60x60 box)
        if title == "EDGE-AI":
            g.append(f'<rect x="{ix+10}" y="{iy+10}" width="40" height="40" rx="6" fill="{BG}" stroke="{col}" stroke-width="2"/>')
            g.append(f'<rect x="{ix+21}" y="{iy+21}" width="18" height="18" rx="3" fill="{col}" opacity="0.35"><animate attributeName="opacity" values="0.2;0.8;0.2" dur="2.4s" repeatCount="indefinite"/></rect>')
            for k in range(3):
                o = 18 + k * 12
                g.append(f'<line x1="{ix+o}" y1="{iy+3}" x2="{ix+o}" y2="{iy+10}" stroke="{col}" stroke-width="2"/>')
                g.append(f'<line x1="{ix+o}" y1="{iy+50}" x2="{ix+o}" y2="{iy+57}" stroke="{col}" stroke-width="2"/>')
                g.append(f'<line x1="{ix+3}" y1="{iy+o}" x2="{ix+10}" y2="{iy+o}" stroke="{col}" stroke-width="2"/>')
                g.append(f'<line x1="{ix+50}" y1="{iy+o}" x2="{ix+57}" y2="{iy+o}" stroke="{col}" stroke-width="2"/>')
        elif title == "COMPUTER VISION":
            g.append(f'<rect x="{ix+4}" y="{iy+8}" width="52" height="44" rx="6" fill="{BG}" stroke="{col}" stroke-width="2"/>')
            for dx, dy in ((10, 14), (40, 14), (10, 38), (40, 38)):
                sx = 1 if dx < 30 else -1
                sy = 1 if dy < 30 else -1
                g.append(f'<path d="M{ix+dx},{iy+dy+sy*8} V{iy+dy} H{ix+dx+sx*8}" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round"/>')
            g.append(f'<circle cx="{ix+30}" cy="{iy+30}" r="6" fill="none" stroke="{col}" stroke-width="2"/>')
            g.append(f'<line x1="{ix+10}" x2="{ix+50}" y1="{iy+14}" y2="{iy+14}" stroke="{col}" stroke-width="2" opacity="0.8"><animate attributeName="y1" values="{iy+14};{iy+46};{iy+14}" dur="3s" repeatCount="indefinite"/><animate attributeName="y2" values="{iy+14};{iy+46};{iy+14}" dur="3s" repeatCount="indefinite"/></line>')
        elif title == "MACHINE LEARNING":
            ns = [(8, 16), (8, 44), (30, 8), (30, 30), (30, 52), (52, 30)]
            ed = [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 5), (3, 5), (4, 5)]
            for a, b in ed:
                g.append(f'<line x1="{ix+ns[a][0]}" y1="{iy+ns[a][1]}" x2="{ix+ns[b][0]}" y2="{iy+ns[b][1]}" stroke="{col}" stroke-opacity="0.45" stroke-width="1.4"/>')
            for k, (nx, ny) in enumerate(ns):
                g.append(f'<circle cx="{ix+nx}" cy="{iy+ny}" r="5" fill="{BG}" stroke="{col}" stroke-width="2"><animate attributeName="fill" values="{BG};{col};{BG}" dur="3s" begin="{k*0.4:.1f}s" repeatCount="indefinite"/></circle>')
        else:
            for k, hh in enumerate((20, 34, 26, 46)):
                bx = ix + 6 + k * 13
                g.append(
                    f'<rect x="{bx}" y="{iy+52-hh}" width="9" height="{hh}" rx="2" fill="{col}" opacity="0.85">'
                    f'<animate attributeName="height" values="{hh*0.4:.0f};{hh};{hh*0.4:.0f}" dur="3.2s" begin="{k*0.25:.2f}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="y" values="{iy+52-hh*0.4:.0f};{iy+52-hh};{iy+52-hh*0.4:.0f}" dur="3.2s" begin="{k*0.25:.2f}s" repeatCount="indefinite"/></rect>'
                )
            g.append(f'<line x1="{ix}" y1="{iy+54}" x2="{ix+60}" y2="{iy+54}" stroke="{col}" stroke-width="2"/>')
        g.append(f'<text x="{x+22}" y="130" font-family="{FONT}" font-size="14.5" font-weight="700" fill="{TEXT}" letter-spacing="1.2">{title}</text>')
        for i, ln in enumerate(lines):
            g.append(f'<text x="{x+22}" y="{156+i*21}" font-family="{FONT}" font-size="12.5" fill="{MUTED}">{esc(ln)}</text>')
        parts.append("".join(g))
    write("focus.svg", svg(W, H, "".join(parts), "Focus areas",
                           "Four focus areas: Edge-AI, Computer Vision, Machine Learning, Data Science."))


# --------------------------------------------------------------------------- milestones
def milestones():
    W, H = 900, 150
    cw, gap = 207, 24
    xs = [i * (cw + gap) for i in range(4)]
    items = [
        ("1st", GOLD, "Damietta AI Hackathon", "Agriculture Track · 37 teams"),
        ("2nd", BLUE, "Egypt Cities Hackathon", "75,000 EGP prize · Raa'i"),
        ("50+", CYAN, "ANOMALY Community", "members, 10 technical tracks"),
        ("4", VIOLET, "ML trainings & internships", "ITI · NTI · FlyRank AI · DecodeLabs"),
    ]
    parts = []
    for (big, col, l1, l2), x in zip(items, xs):
        parts.append(
            f'<rect x="{x+0.5}" y="0.5" width="{cw-1}" height="{H-1}" rx="16" fill="url(#gB)" stroke="{BORDER}"/>'
            f'<text x="{x+22}" y="62" font-family="{FONT}" font-size="44" font-weight="800" fill="{col}">{big}'
            f'<animate attributeName="opacity" values="0.75;1;0.75" dur="4s" repeatCount="indefinite"/></text>'
            f'<text x="{x+22}" y="94" font-family="{FONT}" font-size="13.5" font-weight="700" fill="{TEXT}">{esc(l1)}</text>'
            f'<text x="{x+22}" y="116" font-family="{FONT}" font-size="11.5" fill="{MUTED}">{esc(l2)}</text>'
        )
    write("milestones.svg", svg(W, H, "".join(parts), "Milestones",
                                "1st place Damietta AI Hackathon, 2nd place Egypt Cities Hackathon, 50 plus ANOMALY members, 4 ML trainings and internships."))


# --------------------------------------------------------------------------- pipelines
def node(x, y, w, h, idx, l1, l2, col):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="url(#gB)" stroke="{col}" stroke-opacity="0.8"/>'
        f'<text x="{x+12}" y="{y+19}" font-family="{MONO}" font-size="10.5" fill="{col}">{idx}</text>'
        f'<text x="{x+12}" y="{y+41}" font-family="{FONT}" font-size="12.5" font-weight="700" fill="{TEXT}">{esc(l1)}</text>'
        f'<text x="{x+12}" y="{y+59}" font-family="{FONT}" font-size="11.5" fill="{MUTED}">{esc(l2)}</text>'
    )


def arrow(x1, y1, x2, y2, col=BLUE):
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2-5}" y2="{y2}" stroke="{col}" stroke-width="1.6" stroke-dasharray="4 4">'
        f'<animate attributeName="stroke-dashoffset" values="16;0" dur="1.1s" repeatCount="indefinite"/></line>'
        f'<path d="M{x2-7},{y2-4.5} L{x2},{y2} L{x2-7},{y2+4.5}" fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def raai_pipeline():
    W, H = 900, 200
    nw, nh = 122, 84
    pad = 24
    gap = (W - 2 * pad - 6 * nw) / 5
    y = 70
    spec = [
        ("01", "Video input", "livestock cameras", CYAN),
        ("02", "YOLOv8", "object detection", BLUE),
        ("03", "BoT-SORT + Re-ID", "track each animal", BLUE),
        ("04", "Behavior", "health monitoring", VIOLET),
        ("05", "Offline RAG", "+ local LLM", VIOLET),
        ("06", "Bilingual report", "for farmers & vets", GOLD),
    ]
    parts = [card_bg(W, H, 18)]
    parts.append(f'<text x="24" y="34" font-family="{MONO}" font-size="11.5" fill="{CYAN}" letter-spacing="2.5">RAA\'I  ·  OFFLINE EDGE-AI PIPELINE</text>')
    parts.append(f'<rect x="{W-118}" y="19" width="94" height="22" rx="11" fill="{BG}" stroke="{CYAN}" stroke-opacity="0.7"/>'
                 f'<text x="{W-71}" y="34" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{CYAN}">NO CLOUD</text>')
    xs = []
    for i, (idx, a, b, col) in enumerate(spec):
        x = pad + i * (nw + gap)
        xs.append(x)
        parts.append(node(x + 0, y, nw, nh, idx, a, b, col))
    for i in range(5):
        parts.append(arrow(xs[i] + nw + 2, y + nh / 2, xs[i + 1] - 2, y + nh / 2))
    # moving data dot
    path = f"M{xs[0]+nw/2},{y+nh+18} L{xs[-1]+nw/2},{y+nh+18}"
    parts.append(f'<line x1="{xs[0]+nw/2}" y1="{y+nh+18}" x2="{xs[-1]+nw/2}" y2="{y+nh+18}" stroke="{BORDER}" stroke-dasharray="2 5"/>')
    parts.append(f'<circle r="4" fill="{CYAN}" filter="url(#glow)"><animateMotion dur="5s" repeatCount="indefinite" path="{path}"/></circle>')
    parts.append(f'<text x="{W/2}" y="{H-14}" text-anchor="middle" font-family="{FONT}" font-size="11.5" fill="{MUTED}">data flows from camera frames to a diagnostic report, entirely on local hardware</text>')
    write("raai-pipeline.svg", svg(W, H, "".join(parts), "Raa'i pipeline",
                                   "Raa'i pipeline: video input, YOLOv8 detection, BoT-SORT and Re-ID tracking, behavior analysis, offline RAG with a local LLM, bilingual report."))


def inspection_pipeline():
    W, H = 900, 250
    nw, nh = 150, 84
    parts = [card_bg(W, H, 18)]
    parts.append(f'<text x="24" y="34" font-family="{MONO}" font-size="11.5" fill="{CYAN}" letter-spacing="2.5">MULTI-MODAL EDGE-AI INSPECTION SYSTEM</text>')
    colx = [0, 190, 400, 600, 750]
    mid_y = 100
    top_y, bot_y = 56, 148
    parts.append(node(colx[0], mid_y - 0, nw, nh, "01", "Synthetic data", "2,000+ Blender images", CYAN).replace(f'y="{mid_y}"', f'y="{mid_y}"'))
    parts.append(node(colx[1] + 20, top_y + 0, 190, nh, "02A", "CNN from scratch", "pure NumPy, no framework", BLUE))
    parts.append(node(colx[1] + 20, bot_y + 20, 190, nh, "02B", "FFT anomaly detector", "signal / frequency analysis", VIOLET))
    parts.append(node(colx[3] - 30, mid_y, 140, nh, "03", "Fusion", "combined verdict", GOLD))
    parts.append(node(colx[4], mid_y, 150, nh, "04", "Explainable AI", "dashboard", GOLD))
    # arrows
    parts.append(arrow(150 + 2, mid_y + nh / 2, 210 - 2, top_y + nh / 2))
    parts.append(arrow(150 + 2, mid_y + nh / 2, 210 - 2, bot_y + 20 + nh / 2, VIOLET))
    parts.append(arrow(210 + 190 + 2, top_y + nh / 2, 570 - 2, mid_y + nh / 2 - 12))
    parts.append(arrow(210 + 190 + 2, bot_y + 20 + nh / 2, 570 - 2, mid_y + nh / 2 + 12, VIOLET))
    parts.append(arrow(570 + 140 + 2, mid_y + nh / 2, 750 - 2, mid_y + nh / 2, GOLD))
    parts.append(f'<text x="{W/2}" y="{H-12}" text-anchor="middle" font-family="{FONT}" font-size="11.5" fill="{MUTED}">industrial gear defect detection: two independent detectors, one explainable decision</text>')
    write("inspection-pipeline.svg", svg(W, H, "".join(parts), "Inspection system pipeline",
                                         "Synthetic Blender data feeds a NumPy CNN and an FFT anomaly detector, fused into an explainable AI dashboard."))


def inspection_pipeline():  # noqa: F811  (layout fix: padding + no overlap)
    W, H = 900, 280
    pad = 24
    nh = 76
    parts = [card_bg(W, H, 18)]
    parts.append(f'<text x="{pad}" y="34" font-family="{MONO}" font-size="11.5" fill="{CYAN}" letter-spacing="2.5">MULTI-MODAL EDGE-AI INSPECTION SYSTEM</text>')
    x1, w1 = pad, 168
    x2, w2 = 252, 210
    x3, w3 = 538, 150
    x4, w4 = 726, 150
    y_top, y_bot = 58, 158
    y_mid = (y_top + y_bot) / 2
    parts.append(node(x1, y_mid, w1, nh, "01", "Synthetic data", "2,000+ Blender images", CYAN))
    parts.append(node(x2, y_top, w2, nh, "02A", "CNN from scratch", "pure NumPy", BLUE))
    parts.append(node(x2, y_bot, w2, nh, "02B", "FFT anomaly detector", "signal analysis", VIOLET))
    parts.append(node(x3, y_mid, w3, nh, "03", "Fusion", "combined verdict", GOLD))
    parts.append(node(x4, y_mid, w4, nh, "04", "Explainable AI", "dashboard", GOLD))
    cy = y_mid + nh / 2
    parts.append(arrow(x1 + w1 + 2, cy - 10, x2 - 2, y_top + nh / 2))
    parts.append(arrow(x1 + w1 + 2, cy + 10, x2 - 2, y_bot + nh / 2, VIOLET))
    parts.append(arrow(x2 + w2 + 2, y_top + nh / 2, x3 - 2, cy - 10))
    parts.append(arrow(x2 + w2 + 2, y_bot + nh / 2, x3 - 2, cy + 10, VIOLET))
    parts.append(arrow(x3 + w3 + 2, cy, x4 - 2, cy, GOLD))
    parts.append(f'<text x="{W/2}" y="{H-14}" text-anchor="middle" font-family="{FONT}" font-size="11.5" fill="{MUTED}">industrial gear defect detection: two independent detectors, one explainable decision</text>')
    write("inspection-pipeline.svg", svg(W, H, "".join(parts), "Inspection system pipeline",
                                         "Synthetic Blender data feeds a NumPy CNN and an FFT anomaly detector, fused into an explainable AI dashboard."))


NB = " "


def terminal():
    W, H = 900, 236
    pad = 30
    cw = 8.6  # generous mono advance for clip widths
    segs = [
        [("class ", VIOLET), ("Alfarouq", GOLD), (":", MUTED)],
        [(NB * 4 + "role", TEXT), (NB * 3 + "=" + NB, MUTED), ('"AI System Architect"', CYAN)],
        [(NB * 4 + "focus", TEXT), (NB * 2 + "=" + NB, MUTED), ('["Edge-AI", "Computer Vision", "ML", "Data Science"]', CYAN)],
        [(NB * 4 + "builds", TEXT), (NB + "=" + NB, MUTED), ('"offline systems that run where the data is"', CYAN)],
        [(NB * 4 + "status", TEXT), (NB + "=" + NB, MUTED), ('"open to AI Architecture / ML Engineering roles"', CYAN)],
    ]
    cycle = 15.0
    parts = [
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="{BG}" stroke="{BORDER}"/>',
        f'<path d="M0.5 16.5 A16 16 0 0 1 16.5 0.5 H{W-16.5} A16 16 0 0 1 {W-0.5} 16.5 V40 H0.5 Z" fill="{PANEL}" stroke="{BORDER}"/>',
        f'<circle cx="26" cy="21" r="5" fill="{MUTED}" opacity="0.6"/><circle cx="46" cy="21" r="5" fill="{GOLD}" opacity="0.8"/><circle cx="66" cy="21" r="5" fill="{CYAN}" opacity="0.8"/>',
        f'<text x="{W/2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">profile.py</text>',
    ]
    defs = []
    y0, lh = 78, 30
    for i, segments in enumerate(segs):
        y = y0 + i * lh
        n = sum(len(t) for t, _ in segments)
        full = n * cw + 12
        t0 = 0.5 + i * 1.5
        t1 = t0 + 1.3
        kt = f"0;{t0/cycle:.4f};{t1/cycle:.4f};{12.8/cycle:.4f};1"
        defs.append(
            f'<clipPath id="c{i}"><rect x="{pad-4}" y="{y-20}" width="0" height="28">'
            f'<animate attributeName="width" dur="{cycle}s" repeatCount="indefinite" values="0;0;{full:.0f};{full:.0f};0" keyTimes="{kt}"/></rect></clipPath>'
        )
        tspans = "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in segments)
        parts.append(f'<text x="{pad}" y="{y}" font-family="{MONO}" font-size="14" xml:space="preserve" clip-path="url(#c{i})">{tspans}</text>')
        parts.append(f'<text x="{W-22}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}" opacity="0.5">{i+1}</text>')
    cy = y0 + len(segs) * lh
    parts.append(f'<text x="{pad}" y="{cy}" font-family="{MONO}" font-size="14" fill="{MUTED}">&gt;&gt;&gt;</text>')
    parts.append(f'<rect x="{pad+36}" y="{cy-12}" width="8" height="15" fill="{CYAN}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.0s" repeatCount="indefinite"/></rect>')
    body = f"<defs>{''.join(defs)}</defs>" + "".join(parts)
    write("terminal.svg", svg(W, H, body, "profile.py",
                              "Animated terminal typing a Python class: role AI System Architect, focus Edge-AI, Computer Vision, ML, Data Science."))


def marquee():
    W, H = 900, 62
    items = ["Python", "C++", "TypeScript", "Solidity", "NumPy", "scikit-learn", "YOLOv8", "BoT-SORT", "Re-ID",
             "RAG", "Local LLMs", "FastAPI", "React", "Streamlit", "Jupyter", "Blender", "FFT", "CNN",
             "Edge-AI", "Computer Vision", "Deep Learning", "Compiler Design"]
    gap = 10
    widths = [len(s) * 7.6 + 32 for s in items]
    T = sum(widths) + gap * len(items)
    cols = [BLUE, CYAN, VIOLET, GOLD]

    def row(off):
        out, x = [], off
        for k, (s, w) in enumerate(zip(items, widths)):
            col = cols[k % 4]
            out.append(
                f'<rect x="{x:.0f}" y="15" width="{w:.0f}" height="32" rx="16" fill="{PANEL}" stroke="{col}" stroke-opacity="0.55"/>'
                f'<circle cx="{x+16:.0f}" cy="31" r="3" fill="{col}"/>'
                f'<text x="{x+26:.0f}" y="35.5" font-family="{FONT}" font-size="13" fill="{TEXT}">{esc(s)}</text>'
            )
            x += w + gap
        return "".join(out)

    body = (
        f'<defs><clipPath id="cl"><rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14"/></clipPath>'
        f'<linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
        f'<linearGradient id="fr" x1="1" x2="0"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient></defs>'
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="{BG}" stroke="{BORDER}"/>'
        f'<g clip-path="url(#cl)"><g><animateTransform attributeName="transform" type="translate" from="0 0" to="{-T:.0f} 0" dur="{T/45:.0f}s" repeatCount="indefinite"/>'
        f'{row(0)}{row(T)}</g>'
        f'<rect x="0" y="0" width="80" height="{H}" fill="url(#fl)"/><rect x="{W-80}" y="0" width="80" height="{H}" fill="url(#fr)"/></g>'
    )
    write("tech-marquee.svg", svg(W, H, body, "Technologies",
                                  "Scrolling list of technologies: " + ", ".join(items) + "."))


def animal(x_start, ground_y, ident, dur, begin, col):
    """Cow-like silhouette with tracking box; walks left to right and wraps."""
    body = (
        f'<g fill="#2E3E78"><rect x="0" y="0" width="58" height="26" rx="10"/><rect x="52" y="-7" width="20" height="17" rx="6"/>'
        f'<rect x="8" y="22" width="6" height="15" rx="2"/><rect x="20" y="22" width="6" height="15" rx="2"/>'
        f'<rect x="38" y="22" width="6" height="15" rx="2"/><rect x="48" y="22" width="6" height="15" rx="2"/></g>'
        f'<path d="M0 6 Q-9 8 -8 20" stroke="#2E3E78" stroke-width="3" fill="none" stroke-linecap="round"/>'
    )
    box = (
        f'<rect x="-14" y="-19" width="96" height="62" rx="3" fill="none" stroke="{col}" stroke-width="1.6"/>'
        f'<rect x="-14" y="-33" width="40" height="14" rx="3" fill="{col}"/>'
        f'<text x="-8" y="-22.5" font-family="{MONO}" font-size="10" font-weight="700" fill="{BG}">ID {ident}</text>'
    )
    return (
        f'<g transform="translate({x_start} {ground_y})">'
        f'<animateTransform attributeName="transform" type="translate" values="-120 {ground_y};660 {ground_y}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
        f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -1.6;0 0" dur="0.9s" repeatCount="indefinite"/>{body}{box}</g></g>'
    )


def raai_vision():
    W, H = 900, 264
    parts = [card_bg(W, H, 18)]
    parts.append(f'<text x="24" y="34" font-family="{MONO}" font-size="11.5" fill="{CYAN}" letter-spacing="2.5">RAA\'I  ·  DETECTION, TRACKING, REPORT</text>')
    fx, fy, fw, fh = 24, 50, 540, 182
    ground = fy + 128
    parts.append(
        f'<defs><clipPath id="fr"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="12"/></clipPath>'
        f'<clipPath id="rp"><rect x="0" y="0" width="0" height="0"/></clipPath></defs>'
        f'<g clip-path="url(#fr)">'
        f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="#0E1630"/>'
        f'<path d="M{fx} {fy+95} Q{fx+120} {fy+55} {fx+260} {fy+92} T{fx+fw} {fy+80} V{fy+fh} H{fx} Z" fill="#14224D"/>'
        f'<path d="M{fx} {fy+120} Q{fx+160} {fy+90} {fx+330} {fy+118} T{fx+fw} {fy+108} V{fy+fh} H{fx} Z" fill="#1A2C63"/>'
        f'<rect x="{fx}" y="{fy+150}" width="{fw}" height="{fh-150}" fill="#101B3C"/>'
        + animal(0, ground - 6, 1, 22, -3, CYAN)
        + animal(0, ground - 30, 2, 27, -15, GOLD)
        + animal(0, ground - 50, 3, 31, -22, VIOLET)
        + f'<rect x="{fx}" y="{fy}" width="{fw}" height="2" fill="#FFFFFF" opacity="0.07"><animate attributeName="y" values="{fy};{fy+fh}" dur="4s" repeatCount="indefinite"/></rect>'
        f'</g>'
        f'<rect x="{fx+0.5}" y="{fy+0.5}" width="{fw-1}" height="{fh-1}" rx="12" fill="none" stroke="{BORDER}"/>'
        f'<circle cx="{fx+18}" cy="{fy+18}" r="4" fill="{GOLD}"><animate attributeName="opacity" values="1;0.15;1" dur="1.6s" repeatCount="indefinite"/></circle>'
        f'<text x="{fx+30}" y="{fy+22}" font-family="{MONO}" font-size="10.5" fill="{TEXT}" letter-spacing="1.5">LIVE  ·  OFFLINE</text>'
    )
    # report panel
    px, py, pw, ph = 588, 50, 288, 182
    parts.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="url(#gB)" stroke="{BORDER}"/>')
    parts.append(f'<text x="{px+16}" y="{py+26}" font-family="{MONO}" font-size="10.5" fill="{MUTED}" letter-spacing="1.5">VETERINARY REPORT</text>')
    parts.append(
        f'<rect x="{px+pw-96}" y="{py+11}" width="36" height="22" rx="11" fill="{BG}" stroke="{GOLD}"/>'
        f'<text x="{px+pw-78}" y="{py+26}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{GOLD}">EN</text>'
        f'<rect x="{px+pw-52}" y="{py+11}" width="36" height="22" rx="11" fill="{BG}" stroke="{CYAN}"/>'
        f'<text x="{px+pw-34}" y="{py+26}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{CYAN}">AR</text>'
    )
    widths = [250, 220, 240, 150, 236, 190, 120]
    cycle = 12.0
    for i, w in enumerate(widths):
        y = py + 54 + i * 17
        t0 = 0.4 + i * 1.0
        t1 = t0 + 0.9
        col = BLUE if i % 3 != 2 else CYAN
        parts.append(
            f'<rect x="{px+16}" y="{y}" width="{w}" height="7" rx="3.5" fill="{col}" opacity="0.5">'
            f'<animate attributeName="width" dur="{cycle}s" repeatCount="indefinite" values="0;0;{w};{w};0" keyTimes="0;{t0/cycle:.4f};{t1/cycle:.4f};{10.4/cycle:.4f};1"/></rect>'
        )
    parts.append(f'<text x="{W/2}" y="{H-9}" text-anchor="middle" font-family="{FONT}" font-size="10.5" fill="{MUTED}">illustration of the pipeline, not real footage</text>')
    write("raai-vision.svg", svg(W, H, "".join(parts), "Raa'i detection and tracking",
                                 "Animated illustration: animals detected and tracked with ID boxes, next to a bilingual veterinary report being written."))


def fft_demo():
    import math
    W, H = 900, 250
    parts = [card_bg(W, H, 18)]
    parts.append(f'<text x="24" y="34" font-family="{MONO}" font-size="11.5" fill="{CYAN}" letter-spacing="2.5">FFT-BASED ANOMALY DETECTION</text>')
    lx, ly, lw, lh = 24, 50, 520, 170
    base = ly + lh / 2
    P = 300
    pts = []
    for x in range(0, 2 * P + 1, 3):
        xm = x % P
        v = 26 * math.sin(2 * math.pi * xm / 64) + 9 * math.sin(2 * math.pi * xm / 19)
        if 190 <= xm <= 245:
            win = math.sin(math.pi * (xm - 190) / 55)
            v += 46 * win * math.sin(2 * math.pi * xm / 8.5)
        pts.append((x, base - v))
    d = "M" + " L".join(f"{x+lx},{y:.1f}" for x, y in pts)
    parts.append(
        f'<defs><clipPath id="wf"><rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="12"/></clipPath></defs>'
        f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="12" fill="url(#gB)" stroke="{BORDER}"/>'
        f'<g clip-path="url(#wf)"><line x1="{lx}" y1="{base}" x2="{lx+lw}" y2="{base}" stroke="{BORDER}"/>'
        f'<g><animateTransform attributeName="transform" type="translate" from="0 0" to="{-P} 0" dur="5s" repeatCount="indefinite"/>'
        f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="1.8" stroke-linejoin="round"/></g>'
        f'<rect x="{lx+lw-110}" y="{ly}" width="110" height="{lh}" fill="{CYAN}" opacity="0.06"/></g>'
        f'<text x="{lx+14}" y="{ly+22}" font-family="{MONO}" font-size="10.5" fill="{MUTED}" letter-spacing="1.5">TIME DOMAIN</text>'
        f'<circle cx="{lx+lw-14}" cy="{ly+18}" r="3.5" fill="{CYAN}"><animate attributeName="opacity" values="1;0.2;1" dur="1.4s" repeatCount="indefinite"/></circle>'
    )
    # spectrum
    sx, sy, sw, sh = 568, 50, 308, 170
    parts.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="12" fill="url(#gB)" stroke="{BORDER}"/>')
    parts.append(f'<text x="{sx+14}" y="{sy+22}" font-family="{MONO}" font-size="10.5" fill="{MUTED}" letter-spacing="1.5">FREQUENCY DOMAIN</text>')
    hs = [34, 46, 62, 40, 54, 72, 48, 36, 50, 104, 38, 30, 26, 22, 18, 14]
    floor = sy + sh - 22
    bw, bg = 12, 6.4
    x0 = sx + 16
    for i, h in enumerate(hs):
        x = x0 + i * (bw + bg)
        anomaly = i == 9
        col = GOLD if anomaly else BLUE
        lo, hi = h * 0.78, h * 1.18
        dur = 2.2 + (i % 5) * 0.37
        parts.append(
            f'<rect x="{x:.1f}" y="{floor-h}" width="{bw}" height="{h}" rx="3" fill="{col}" opacity="{0.95 if anomaly else 0.75}">'
            f'<animate attributeName="height" values="{h};{hi:.0f};{lo:.0f};{h}" dur="{dur:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{floor-h};{floor-hi:.0f};{floor-lo:.0f};{floor-h}" dur="{dur:.2f}s" repeatCount="indefinite"/></rect>'
        )
    ax = x0 + 9 * (bw + bg) + bw / 2
    parts.append(
        f'<g><animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/>'
        f'<rect x="{ax-36:.0f}" y="{sy+32}" width="72" height="20" rx="10" fill="{BG}" stroke="{GOLD}"/>'
        f'<text x="{ax:.0f}" y="{sy+46}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{GOLD}" letter-spacing="1">ANOMALY</text></g>'
    )
    parts.append(f'<line x1="{sx+12}" y1="{floor+1}" x2="{sx+sw-12}" y2="{floor+1}" stroke="{BORDER}"/>')
    parts.append(f'<text x="{W/2}" y="{H-9}" text-anchor="middle" font-family="{FONT}" font-size="10.5" fill="{MUTED}">illustrative signal, not measured data</text>')
    write("inspection-signal.svg", svg(W, H, "".join(parts), "FFT anomaly detection",
                                       "Animated illustration: a scrolling vibration waveform with a burst, and a frequency spectrum with one flagged anomaly peak."))


if __name__ == "__main__":
    terminal()
    marquee()
    raai_vision()
    fft_demo()
    hero()
    divider()
    banners()
    focus()
    milestones()
    raai_pipeline()
    inspection_pipeline()
