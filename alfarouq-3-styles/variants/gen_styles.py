#!/usr/bin/env python3
"""Three animated README art styles: blueprint, liquid, voronoi.

Usage: gen_styles.py <out_root>
Writes <out_root>/<style>/assets/*.svg (SMIL animation, opaque cards, no scripts).
"""
import math
import random
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])

FONT = "'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

# ----------------------------------------------------------------- shared content
SECTIONS = [
    ("01", "ABOUT", "who I am"),
    ("02", "FOCUS AREAS", "what I build"),
    ("03", "MILESTONES", "results so far"),
    ("04", "CASE STUDIES", "systems I designed"),
    ("05", "PUBLIC REPOSITORIES", "open work on GitHub"),
    ("06", "TECH STACK", "tools I use"),
    ("07", "LEADERSHIP", "teams and community"),
    ("08", "CONNECT", "let's talk"),
]
FOCUS = [
    ("EDGE-AI", ["Offline-first systems", "that run where the data", "is: the farm, the factory."]),
    ("COMPUTER VISION", ["Detection, tracking and", "re-identification with", "YOLOv8 + BoT-SORT."]),
    ("MACHINE LEARNING", ["Models built from scratch", "and production pipelines:", "CNNs, Random Forest."]),
    ("DATA SCIENCE", ["Synthetic datasets, signal", "analysis (FFT) and apps", "that explain results."]),
]
MILES = [
    ("1st", "Damietta AI Hackathon", "Agriculture Track · 37 teams"),
    ("2nd", "Egypt Cities Hackathon", "75,000 EGP prize · Raa'i"),
    ("50+", "ANOMALY Community", "members, 10 technical tracks"),
    ("4", "ML trainings & internships", "ITI · NTI · FlyRank AI|DecodeLabs"),
]
TECH = ["Python", "C++", "TypeScript", "Solidity", "NumPy", "scikit-learn", "YOLOv8", "BoT-SORT", "Re-ID",
        "RAG", "Local LLMs", "FastAPI", "React", "Streamlit", "Jupyter", "Blender", "FFT", "CNN",
        "Edge-AI", "Computer Vision", "Deep Learning", "Compiler Design"]

_nw, _pad = 126, 24
_gap = (900 - 2 * _pad - 6 * _nw) / 5
RAAI = dict(
    W=900, H=210, title="RAA'I  ·  OFFLINE EDGE-AI PIPELINE", badge="NO CLOUD",
    caption="data flows from camera frames to a diagnostic report, entirely on local hardware",
    alt="Raa'i pipeline: video input, YOLOv8 detection, BoT-SORT and Re-ID tracking, behavior monitoring, offline RAG with a local LLM, bilingual report.",
    nodes=[(_pad + i * (_nw + _gap), 70, _nw, 84, idx, a, b) for i, (idx, a, b) in enumerate([
        ("01", "Video input", "livestock cameras"),
        ("02", "YOLOv8", "object detection"),
        ("03", "BoT-SORT + Re-ID", "track each animal"),
        ("04", "Behavior", "health monitoring"),
        ("05", "Offline RAG", "+ local LLM"),
        ("06", "Bilingual report", "for farmers & vets")])],
    edges=[(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)],
    depth=[0, 1, 2, 3, 4, 5],
)
INSP = dict(
    W=900, H=280, title="MULTI-MODAL EDGE-AI INSPECTION SYSTEM", badge=None,
    caption="industrial gear defect detection: two independent detectors, one explainable decision",
    alt="Inspection pipeline: synthetic Blender data feeds a NumPy CNN and an FFT anomaly detector, fused into an explainable AI dashboard.",
    nodes=[
        (24, 108, 168, 76, "01", "Synthetic data", "2,000+ Blender images"),
        (252, 58, 210, 76, "02A", "CNN from scratch", "pure NumPy"),
        (252, 158, 210, 76, "02B", "FFT anomaly detector", "signal analysis"),
        (538, 108, 150, 76, "03", "Fusion", "combined verdict"),
        (726, 108, 150, 76, "04", "Explainable AI", "dashboard"),
    ],
    edges=[(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)],
    depth=[0, 1, 1, 2, 3],
)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(w, h, defs, body, title, desc=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">\n'
        f'<title id="t">{esc(title)}</title>\n<desc id="d">{esc(desc or title)}</desc>\n'
        f"<defs>{defs}</defs>\n{body}\n</svg>\n"
    )


class Out:
    def __init__(self, style):
        self.dir = ROOT / style / "assets"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.style = style

    def write(self, name, content):
        (self.dir / name).write_text(content, encoding="utf-8")


def fname(title):
    return "section-" + title.lower().replace(" ", "-") + ".svg"


def scroll_marquee(chip, W, H, items, widths, gap, speed=45):
    """chip(x, w, text, k) -> svg string. Returns (inner_group, T)."""
    T = sum(widths) + gap * len(items)

    def row(off):
        out, x = [], off
        for k, (s, w) in enumerate(zip(items, widths)):
            out.append(chip(x, w, s, k))
            x += w + gap
        return "".join(out)

    g = (f'<g><animateTransform attributeName="transform" type="translate" from="0 0" to="{-T:.0f} 0" '
         f'dur="{T/speed:.0f}s" repeatCount="indefinite"/>{row(0)}{row(T)}</g>')
    return g, T


# ===================================================================== BLUEPRINT
class BP:
    BG, LINE, DIM, ACC, MUT = "#0B3A6E", "#D6E8FF", "#86B6F2", "#FFD166", "#9DBDE8"

    @classmethod
    def defs(cls):
        return (
            f'<pattern id="gm" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M10 0H0V10" fill="none" stroke="#FFFFFF" stroke-opacity="0.055"/></pattern>'
            f'<pattern id="gM" width="50" height="50" patternUnits="userSpaceOnUse"><rect width="50" height="50" fill="url(#gm)"/><path d="M50 0H0V50" fill="none" stroke="#FFFFFF" stroke-opacity="0.13"/></pattern>'
            f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 1L10 5L0 9Z" fill="{cls.DIM}"/></marker>'
            f'<marker id="arA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 1L10 5L0 9Z" fill="{cls.ACC}"/></marker>'
            f'<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        )

    @classmethod
    def sheet(cls, W, H, frame=True):
        s = (f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{cls.BG}" stroke="{cls.DIM}" stroke-opacity=".6"/>'
             f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="url(#gM)"/>')
        if frame:
            s += cls.draw_rect(8.5, 8.5, W - 17, H - 17, 3, cls.LINE, 1, .55, 12, 0)
        return s

    @classmethod
    def draw_rect(cls, x, y, w, h, r, col, sw, op, dur=12, begin=0):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" stroke="{col}" stroke-width="{sw}" '
                f'stroke-opacity="{op}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">'
                f'<animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;0.2;0.88;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></rect>')

    @classmethod
    def draw_path(cls, d, col=None, sw=1.2, op=1, dur=12, begin=0, extra=""):
        col = col or cls.LINE
        return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-opacity="{op}" pathLength="1" '
                f'stroke-dasharray="1" stroke-dashoffset="1" {extra}>'
                f'<animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;0.25;0.88;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></path>')

    @classmethod
    def dim_h(cls, x1, x2, y, label=None, col=None, marker="ar"):
        col = col or cls.DIM
        s = (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="1" marker-start="url(#{marker})" marker-end="url(#{marker})"/>'
             f'<line x1="{x1}" y1="{y-6}" x2="{x1}" y2="{y+6}" stroke="{col}"/><line x1="{x2}" y1="{y-6}" x2="{x2}" y2="{y+6}" stroke="{col}"/>')
        if label:
            lw = len(label) * 6.6 + 16
            mx = (x1 + x2) / 2
            s += (f'<rect x="{mx-lw/2:.0f}" y="{y-8}" width="{lw:.0f}" height="16" fill="{cls.BG}"/>'
                  f'<text x="{mx:.0f}" y="{y+4}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{cls.LINE}" letter-spacing="1">{esc(label)}</text>')
        return s

    @classmethod
    def balloon(cls, cx, cy, r, text, size=9):
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{cls.BG}" stroke="{cls.ACC}" stroke-width="1.2"/>'
                f'<text x="{cx}" y="{cy+size*0.36:.1f}" text-anchor="middle" font-family="{MONO}" font-size="{size}" font-weight="700" fill="{cls.ACC}">{esc(text)}</text>')

    @classmethod
    def corner_ticks(cls, x, y, w, h, n=5):
        d = (f"M{x},{y+n}V{y}H{x+n}M{x+w-n},{y}H{x+w}V{y+n}M{x+w},{y+h-n}V{y+h}H{x+w-n}M{x+n},{y+h}H{x}V{y+h-n}")
        return f'<path d="{d}" fill="none" stroke="{cls.ACC}" stroke-width="1.4"/>'

    @classmethod
    def hero(cls, o):
        W, H = 900, 330
        random.seed(5)
        layers, xs, cy, gap = [4, 6, 6, 4, 3], [530, 616, 702, 788, 868], 148, 34
        pts = [[(x, cy + (i - (n - 1) / 2) * gap) for i in range(n)] for n, x in zip(layers, xs)]
        b = [cls.sheet(W, H)]
        for li in range(4):
            d = "".join(f"M{x1},{y1:.1f}L{x2},{y2:.1f}" for (x1, y1) in pts[li] for (x2, y2) in pts[li + 1])
            b.append(cls.draw_path(d, cls.DIM, .8, .5, 12, li * .7))
        for li, layer in enumerate(pts):
            ch = "".join(f"M{x-11},{y:.1f}H{x+11}M{x},{y-11:.1f}V{y+11:.1f}" for x, y in layer)
            b.append(f'<path d="{ch}" stroke="{cls.DIM}" stroke-opacity=".55" stroke-width=".8"/>')
            for x, y in layer:
                b.append(f'<circle cx="{x}" cy="{y:.1f}" r="6" fill="{cls.BG}" stroke="{cls.LINE}" stroke-width="1.4"/>')
        for k in range(10):
            path = [random.choice(l) for l in pts]
            d = "M" + " L".join(f"{x},{y:.1f}" for x, y in path)
            dur, bg = random.uniform(2.4, 3.6), random.uniform(0, 3.5)
            b.append(f'<circle r="2.8" fill="{cls.ACC}" filter="url(#glow)" opacity="0"><animateMotion dur="{dur:.2f}s" begin="{bg:.2f}s" repeatCount="indefinite" path="{d}"/>'
                     f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="{dur:.2f}s" begin="{bg:.2f}s" repeatCount="indefinite"/></circle>')
        b.append(cls.dim_h(xs[0], xs[-1], 266, "ILLUSTRATIVE NETWORK"))
        for lbl, x in zip(["IN", "H1", "H2", "H3", "OUT"], xs):
            b.append(f'<text x="{x}" y="296" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{cls.MUT}" letter-spacing="1.5">{lbl}</text>')
        # left block
        b.append(f'<text x="44" y="46" font-family="{MONO}" font-size="11" fill="{cls.ACC}" letter-spacing="2.5">SHEET 01  ·  AI SYSTEM ARCHITECTURE</text>')
        b.append(f'<text x="44" y="98" font-family="{FONT}" font-size="36" font-weight="700" fill="{cls.LINE}" textLength="430" lengthAdjust="spacingAndGlyphs">ALFAROUQ IBRAHIM</text>')
        b.append(cls.dim_h(44, 474, 116, "AI SYSTEM ARCHITECT"))
        b.append(f'<text x="44" y="150" font-family="{FONT}" font-size="18" font-weight="700" fill="{cls.ACC}">Edge-AI &amp; Computer Vision Specialist</text>')
        b.append(f'<text x="44" y="178" font-family="{FONT}" font-size="13.5" fill="{cls.MUT}">Architecting intelligent systems.</text>')
        b.append(f'<text x="44" y="198" font-family="{FONT}" font-size="13.5" fill="{cls.MUT}">Engineering real-world impact.</text>')
        tx, ty = 44, 226
        b.append(f'<rect x="{tx}" y="{ty}" width="430" height="62" fill="{cls.BG}" fill-opacity=".6" stroke="{cls.LINE}" stroke-opacity=".8"/>'
                 f'<line x1="{tx}" y1="{ty+31}" x2="{tx+430}" y2="{ty+31}" stroke="{cls.LINE}" stroke-opacity=".6"/>'
                 f'<line x1="{tx+215}" y1="{ty}" x2="{tx+215}" y2="{ty+62}" stroke="{cls.LINE}" stroke-opacity=".6"/>')
        for k, (a, v) in enumerate([("TITLE", "ALFAROUQ IBRAHIM"), ("ROLE", "AI SYSTEM ARCHITECT"), ("BASE", "SUEZ, EGYPT"), ("STATUS", "OPEN TO ROLES")]):
            cx, cy2 = tx + (k % 2) * 215 + 9, ty + (k // 2) * 31
            b.append(f'<text x="{cx}" y="{cy2+11}" font-family="{MONO}" font-size="8.5" fill="{cls.MUT}" letter-spacing="1.5">{a}</text>'
                     f'<text x="{cx}" y="{cy2+25}" font-family="{MONO}" font-size="11" fill="{cls.LINE}">{v}</text>')
        b.append(f'<g transform="translate(858 38)"><circle r="9" fill="none" stroke="{cls.ACC}"/><path d="M-14 0H14M0-14V14" stroke="{cls.ACC}"/>'
                 f'<animateTransform attributeName="transform" additive="sum" type="rotate" from="0" to="360" dur="14s" repeatCount="indefinite"/></g>')
        o.write("hero.svg", wrap(W, H, cls.defs(), "".join(b), "Alfarouq Ibrahim, AI System Architect",
                                 "Blueprint-style animated sheet: a neural network schematic with a title block for Alfarouq Ibrahim, AI System Architect, Edge-AI and Computer Vision Specialist."))

    @classmethod
    def section(cls, o, num, title, sub):
        W, H = 900, 56
        tw = len(title) * 12.4
        x0, x1 = 68 + tw + 18, W - 175
        b = [cls.sheet(W, H, frame=False), cls.draw_rect(4.5, 4.5, W - 9, H - 9, 3, cls.LINE, 1, .55, 10, 0)]
        b.append(cls.balloon(34, 28, 15, num, 12))
        b.append(f'<line x1="49" y1="28" x2="62" y2="28" stroke="{cls.ACC}"/>')
        b.append(f'<text x="68" y="34" font-family="{MONO}" font-size="17" font-weight="700" fill="{cls.LINE}" letter-spacing="2">{esc(title)}</text>')
        b.append(cls.dim_h(x0, x1, 28))
        b.append(f'<rect x="{x0}" y="22" width="9" height="12" fill="{cls.ACC}" opacity=".9"><animate attributeName="x" values="{x0};{x1-9}" dur="3.6s" repeatCount="indefinite"/></rect>')
        b.append(f'<text x="{W-20}" y="32" text-anchor="end" font-family="{MONO}" font-size="11" fill="{cls.MUT}">// {esc(sub)}</text>')
        o.write(fname(title), wrap(W, H, cls.defs(), "".join(b), f"Section {num}: {title.title()}"))

    @classmethod
    def icon(cls, k, ix, iy):
        L, A = cls.LINE, cls.ACC
        g = []
        if k == 0:
            g.append(f'<rect x="{ix+12}" y="{iy+12}" width="36" height="36" fill="none" stroke="{L}" stroke-width="1.6"/>')
            g.append(f'<rect x="{ix+22}" y="{iy+22}" width="16" height="16" fill="{A}" opacity=".3"><animate attributeName="opacity" values=".15;.8;.15" dur="2.4s" repeatCount="indefinite"/></rect>')
            for j in range(3):
                o = 20 + j * 10
                g.append(f'<path d="M{ix+o},{iy+4}V{iy+12}M{ix+o},{iy+48}V{iy+56}M{ix+4},{iy+o}H{ix+12}M{ix+48},{iy+o}H{ix+56}" stroke="{L}" stroke-width="1.6"/>')
        elif k == 1:
            g.append(f'<rect x="{ix+4}" y="{iy+8}" width="52" height="44" fill="none" stroke="{L}" stroke-width="1.2" stroke-dasharray="3 3"/>')
            for dx, dy, sx, sy in ((10, 14, 1, 1), (50, 14, -1, 1), (10, 46, 1, -1), (50, 46, -1, -1)):
                g.append(f'<path d="M{ix+dx},{iy+dy+sy*8}V{iy+dy}H{ix+dx+sx*8}" fill="none" stroke="{L}" stroke-width="1.8"/>')
            g.append(f'<circle cx="{ix+30}" cy="{iy+30}" r="6" fill="none" stroke="{A}" stroke-width="1.6"/>')
            g.append(f'<line x1="{ix+10}" x2="{ix+50}" y1="{iy+14}" y2="{iy+14}" stroke="{A}" stroke-width="1.6"><animate attributeName="y1" values="{iy+14};{iy+46};{iy+14}" dur="3s" repeatCount="indefinite"/><animate attributeName="y2" values="{iy+14};{iy+46};{iy+14}" dur="3s" repeatCount="indefinite"/></line>')
        elif k == 2:
            ns = [(8, 16), (8, 44), (30, 8), (30, 30), (30, 52), (52, 30)]
            ed = [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 5), (3, 5), (4, 5)]
            for a, c in ed:
                g.append(f'<line x1="{ix+ns[a][0]}" y1="{iy+ns[a][1]}" x2="{ix+ns[c][0]}" y2="{iy+ns[c][1]}" stroke="{L}" stroke-opacity=".5"/>')
            for j, (nx, ny) in enumerate(ns):
                g.append(f'<circle cx="{ix+nx}" cy="{iy+ny}" r="5" fill="{cls.BG}" stroke="{L}" stroke-width="1.6"><animate attributeName="fill" values="{cls.BG};{A};{cls.BG}" dur="3s" begin="{j*.4:.1f}s" repeatCount="indefinite"/></circle>')
        else:
            g.append(f'<path d="M{ix+4},{iy+6}V{iy+54}H{ix+58}" fill="none" stroke="{L}" stroke-width="1.6"/>')
            for j, hh in enumerate((20, 34, 26, 44)):
                bx = ix + 12 + j * 11
                g.append(f'<rect x="{bx}" y="{iy+54-hh}" width="7" height="{hh}" fill="none" stroke="{A}" stroke-width="1.4"><animate attributeName="height" values="{hh*.4:.0f};{hh};{hh*.4:.0f}" dur="3.2s" begin="{j*.25:.2f}s" repeatCount="indefinite"/>'
                         f'<animate attributeName="y" values="{iy+54-hh*.4:.0f};{iy+54-hh};{iy+54-hh*.4:.0f}" dur="3.2s" begin="{j*.25:.2f}s" repeatCount="indefinite"/></rect>')
        return "".join(g)

    @classmethod
    def focus(cls, o):
        W, H, cw, gp = 900, 250, 207, 24
        b = []
        for i, (title, lines) in enumerate(FOCUS):
            x = i * (cw + gp)
            b.append(f'<rect x="{x+.5}" y=".5" width="{cw-1}" height="{H-1}" rx="6" fill="{cls.BG}" stroke="{cls.DIM}" stroke-opacity=".6"/>'
                     f'<rect x="{x+.5}" y=".5" width="{cw-1}" height="{H-1}" rx="6" fill="url(#gM)"/>')
            b.append(cls.draw_rect(x + 5.5, 5.5, cw - 11, H - 11, 3, cls.LINE, 1, .5, 10, i * .3))
            b.append(cls.balloon(x + 24, 26, 11, "ABCD"[i], 11))
            b.append(f'<text x="{x+42}" y="30" font-family="{MONO}" font-size="10" fill="{cls.MUT}" letter-spacing="2">DETAIL {"ABCD"[i]}</text>')
            b.append(cls.icon(i, x + 24, 50))
            b.append(f'<text x="{x+22}" y="140" font-family="{FONT}" font-size="14.5" font-weight="700" fill="{cls.LINE}" letter-spacing="1.2">{title}</text>')
            for j, ln in enumerate(lines):
                b.append(f'<text x="{x+22}" y="{164+j*21}" font-family="{FONT}" font-size="12.5" fill="{cls.MUT}">{esc(ln)}</text>')
        o.write("focus.svg", wrap(W, H, cls.defs(), "".join(b), "Focus areas",
                                  "Four focus areas: Edge-AI, Computer Vision, Machine Learning, Data Science."))

    @classmethod
    def milestones(cls, o):
        W, H, cw, gp = 900, 150, 207, 24
        b = []
        for i, (big, l1, l2) in enumerate(MILES):
            x = i * (cw + gp)
            b.append(f'<rect x="{x+.5}" y=".5" width="{cw-1}" height="{H-1}" rx="6" fill="{cls.BG}" stroke="{cls.DIM}" stroke-opacity=".6"/>'
                     f'<rect x="{x+.5}" y=".5" width="{cw-1}" height="{H-1}" rx="6" fill="url(#gM)"/>')
            b.append(cls.draw_rect(x + 5.5, 5.5, cw - 11, H - 11, 3, cls.LINE, 1, .5, 10, i * .3))
            b.append(f'<text x="{x+20}" y="24" font-family="{MONO}" font-size="9.5" fill="{cls.MUT}" letter-spacing="2">SPEC 0{i+1}</text>')
            b.append(f'<text x="{x+20}" y="70" font-family="{FONT}" font-size="42" font-weight="800" fill="{cls.ACC}">{big}<animate attributeName="opacity" values=".7;1;.7" dur="4s" repeatCount="indefinite"/></text>')
            b.append(cls.dim_h(x + 20, x + cw - 20, 82, None))
            b.append(f'<text x="{x+20}" y="106" font-family="{FONT}" font-size="12.5" font-weight="700" fill="{cls.LINE}">{esc(l1)}</text>')
            for j, part in enumerate(l2.split("|")):
                b.append(f'<text x="{x+20}" y="{126+j*14}" font-family="{FONT}" font-size="11.5" fill="{cls.MUT}">{esc(part)}</text>')
        o.write("milestones.svg", wrap(W, H, cls.defs(), "".join(b), "Milestones",
                                       "1st place Damietta AI Hackathon, 2nd place Egypt Cities Hackathon, 50 plus ANOMALY members, 4 ML trainings and internships."))

    @classmethod
    def pipeline(cls, o, name, P):
        W, H = P["W"], P["H"]
        b = [cls.sheet(W, H)]
        b.append(f'<text x="28" y="38" font-family="{MONO}" font-size="11.5" fill="{cls.ACC}" letter-spacing="2.5">{esc(P["title"])}</text>')
        if P["badge"]:
            b.append(f'<rect x="{W-122}" y="22" width="96" height="22" fill="none" stroke="{cls.ACC}"/><text x="{W-74}" y="37" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{cls.ACC}">{P["badge"]}</text>')
        for (x1, y1, w1, h1, *_), (x2, y2, w2, h2, *_) in [(P["nodes"][a], P["nodes"][c]) for a, c in P["edges"]]:
            sx, sy, ex, ey = x1 + w1 + 1, y1 + h1 / 2, x2 - 1, y2 + h2 / 2
            xm = (sx + ex) / 2
            d = f"M{sx},{sy}H{ex}" if abs(sy - ey) < 1 else f"M{sx},{sy}H{xm}V{ey}H{ex}"
            b.append(f'<path d="{d}" fill="none" stroke="{cls.DIM}" stroke-width="1.4" stroke-dasharray="5 4" marker-end="url(#ar)"><animate attributeName="stroke-dashoffset" values="18;0" dur="1.2s" repeatCount="indefinite"/></path>')
        for (x, y, w, h, idx, l1, l2) in P["nodes"]:
            b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{cls.BG}" stroke="{cls.LINE}" stroke-width="1.3"/>')
            b.append(cls.corner_ticks(x - 3, y - 3, w + 6, h + 6))
            b.append(f'<text x="{x+14}" y="{y+46}" font-family="{FONT}" font-size="12.5" font-weight="700" fill="{cls.LINE}">{esc(l1)}</text>')
            b.append(f'<text x="{x+14}" y="{y+64}" font-family="{FONT}" font-size="11.5" fill="{cls.MUT}">{esc(l2)}</text>')
            b.append(cls.balloon(x + 4, y + 4, 12, idx, 8.5))
        b.append(f'<text x="{W/2}" y="{H-18}" text-anchor="middle" font-family="{FONT}" font-size="11.5" fill="{cls.MUT}">{esc(P["caption"])}</text>')
        o.write(name, wrap(W, H, cls.defs(), "".join(b), name[:-4].replace("-", " ").title(), P["alt"]))

    @classmethod
    def marquee(cls, o):
        W, H = 900, 62
        widths = [len(s) * 7.6 + 34 for s in TECH]

        def chip(x, w, s, k):
            return (f'<rect x="{x:.0f}" y="15" width="{w:.0f}" height="32" fill="{cls.BG}" stroke="{cls.LINE}" stroke-opacity=".8"/>'
                    f'<rect x="{x+10:.0f}" y="28" width="6" height="6" fill="{cls.ACC}"/>'
                    f'<text x="{x+24:.0f}" y="35.5" font-family="{MONO}" font-size="12.5" fill="{cls.LINE}">{esc(s)}</text>')
        g, _ = scroll_marquee(chip, W, H, TECH, widths, 10)
        body = (cls.sheet(W, H, frame=False) +
                f'<clipPath id="cl"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="7"/></clipPath><g clip-path="url(#cl)">{g}'
                f'<rect x="0" y="0" width="70" height="{H}" fill="url(#fl)"/><rect x="{W-70}" y="0" width="70" height="{H}" fill="url(#fr)"/></g>')
        defs = (cls.defs() + f'<linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="{cls.BG}"/><stop offset="1" stop-color="{cls.BG}" stop-opacity="0"/></linearGradient>'
                f'<linearGradient id="fr" x1="1" x2="0"><stop offset="0" stop-color="{cls.BG}"/><stop offset="1" stop-color="{cls.BG}" stop-opacity="0"/></linearGradient>')
        o.write("tech-marquee.svg", wrap(W, H, defs, body, "Technologies", "Scrolling list of technologies: " + ", ".join(TECH) + "."))

    @classmethod
    def divider(cls, o):
        W, H = 900, 22
        b = cls.dim_h(6, W - 6, 11) + f'<rect x="6" y="5" width="8" height="12" fill="{cls.ACC}"><animate attributeName="x" values="6;{W-14}" dur="5s" repeatCount="indefinite"/></rect>'
        o.write("divider.svg", wrap(W, H, cls.defs(), b, "Section divider"))

    @classmethod
    def build(cls):
        o = Out("blueprint")
        cls.hero(o)
        for s in SECTIONS:
            cls.section(o, *s)
        cls.focus(o)
        cls.milestones(o)
        cls.pipeline(o, "raai-pipeline.svg", RAAI)
        cls.pipeline(o, "inspection-pipeline.svg", INSP)
        cls.marquee(o)
        cls.divider(o)


# ===================================================================== LIQUID
class LQ:
    BG, CARD, T, MUT = "#0A0A14", "#14142A", "#F4F2FF", "#9A97B8"
    A, B, C, D = "#7C5CFF", "#FF5CA8", "#FFB36B", "#4FD1C5"

    @classmethod
    def defs(cls, W=900):
        return (
            f'<linearGradient id="gG" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0"><stop offset="0" stop-color="{cls.A}"/><stop offset=".55" stop-color="{cls.B}"/><stop offset="1" stop-color="{cls.C}"/></linearGradient>'
            f'<linearGradient id="gD" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{cls.A}"/><stop offset=".6" stop-color="{cls.B}"/><stop offset="1" stop-color="{cls.C}"/></linearGradient>'
            f'<linearGradient id="gCard" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1A1A38"/><stop offset="1" stop-color="{cls.CARD}"/></linearGradient>'
            f'<filter id="goo" x="-10%" y="-60%" width="120%" height="220%" color-interpolation-filters="sRGB"><feGaussianBlur in="SourceGraphic" stdDeviation="3" result="b"/>'
            f'<feColorMatrix in="b" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8"/></filter>'
            f'<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="34"/></filter>'
        )

    @classmethod
    def blob_d(cls, x, y, w, h, inset, jit, rng):
        c, m = inset, inset * 0.3
        base = [(x + c, y + c), (x + w / 2, y + m), (x + w - c, y + c), (x + w - m, y + h / 2),
                (x + w - c, y + h - c), (x + w / 2, y + h - m), (x + c, y + h - c), (x + m, y + h / 2)]
        pts = [(px + rng.uniform(-jit, jit), py + rng.uniform(-jit, jit)) for px, py in base]
        n = len(pts)
        d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
        for i in range(n):
            p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            d += f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
        return d + "Z"

    @classmethod
    def blob(cls, x, y, w, h, seed, inset=14, jit=6, dur=9, fill="url(#gCard)", stroke="url(#gD)", sw=1.6):
        rng = random.Random(seed)
        ds = [cls.blob_d(x, y, w, h, inset, jit, rng) for _ in range(3)]
        vals = ";".join(ds + [ds[0]])
        return (f'<path d="{ds[0]}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}">'
                f'<animate attributeName="d" values="{vals}" dur="{dur}s" repeatCount="indefinite"/></path>')

    @classmethod
    def bg(cls, W, H, rx=20):
        return f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{rx}" fill="{cls.BG}" stroke="#23234A"/>'

    @classmethod
    def hero(cls, o):
        W, H = 900, 350
        random.seed(8)
        defs = cls.defs(W) + (
            '<filter id="liq" x="-8%" y="-40%" width="116%" height="190%" color-interpolation-filters="sRGB">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.008 0.016" numOctaves="2" seed="4" result="n">'
            '<animate attributeName="baseFrequency" dur="11s" values="0.008 0.016;0.015 0.010;0.008 0.016" repeatCount="indefinite"/></feTurbulence>'
            '<feDisplacementMap in="SourceGraphic" in2="n" scale="9" xChannelSelector="R" yChannelSelector="G" result="d"/>'
            '<feGaussianBlur in="d" stdDeviation="2.6" result="b"/>'
            '<feColorMatrix in="b" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 16 -6"/></filter>'
            f'<clipPath id="cc"><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20"/></clipPath>')
        b = [cls.bg(W, H)]
        b.append('<g clip-path="url(#cc)" filter="url(#soft)" opacity=".5">'
                 f'<circle r="90" fill="{cls.A}"><animateMotion dur="16s" repeatCount="indefinite" path="M120,90 C300,40 500,160 300,230 C150,290 40,170 120,90Z"/></circle>'
                 f'<circle r="80" fill="{cls.B}"><animateMotion dur="19s" repeatCount="indefinite" path="M700,70 C820,150 740,290 600,260 C480,230 560,100 700,70Z"/></circle>'
                 f'<circle r="60" fill="{cls.C}"><animateMotion dur="14s" repeatCount="indefinite" path="M420,250 C520,300 640,230 560,170 C500,130 360,180 420,250Z"/></circle></g>')
        blobs = []
        for i, x in enumerate((92, 200, 318, 430, 552, 672, 790)):
            r = random.uniform(7, 11)
            y0, y1 = 206 + random.uniform(-2, 6), 150 + random.uniform(-14, 14)
            dur, bg_ = random.uniform(3.6, 5.8), random.uniform(0, 3)
            blobs.append(f'<circle cx="{x}" cy="{y0:.0f}" r="{r:.0f}"><animate attributeName="cy" values="{y0:.0f};{y1:.0f};{y0:.0f}" dur="{dur:.1f}s" begin="{bg_:.1f}s" repeatCount="indefinite"/>'
                         f'<animate attributeName="r" values="{r:.0f};{r*1.5:.0f};{r:.0f}" dur="{dur:.1f}s" begin="{bg_:.1f}s" repeatCount="indefinite"/></circle>')
        b.append(f'<g filter="url(#liq)" fill="url(#gG)"><text x="46" y="196" font-family="Arial Black, Impact, {FONT}" font-size="122" font-weight="900" '
                 f'textLength="808" lengthAdjust="spacingAndGlyphs">ALFAROUQ</text>{"".join(blobs)}</g>')
        b.append(f'<text x="48" y="48" font-family="{MONO}" font-size="12" fill="{cls.D}" letter-spacing="3">AI SYSTEM ARCHITECT</text>')
        b.append(f'<text x="852" y="48" text-anchor="end" font-family="{MONO}" font-size="12" fill="{cls.MUT}" letter-spacing="3">SUEZ · EGYPT</text>')
        b.append(f'<text x="48" y="252" font-family="{FONT}" font-size="21" font-weight="600" fill="{cls.T}" letter-spacing="9">IBRAHIM</text>')
        b.append(f'<text x="48" y="284" font-family="{FONT}" font-size="20" font-weight="700" fill="url(#gG)">Edge-AI &amp; Computer Vision Specialist</text>')
        b.append(f'<text x="48" y="312" font-family="{FONT}" font-size="14" fill="{cls.MUT}">Architecting intelligent systems. Engineering real-world impact.</text>')
        x = 478
        for c, col in (("Machine Learning", cls.A), ("Deep Learning", cls.B), ("Data Science", cls.C)):
            w = len(c) * 7.2 + 26
            b.append(f'<rect x="{x:.0f}" y="262" width="{w:.0f}" height="28" rx="14" fill="{cls.CARD}" stroke="{col}" stroke-opacity=".8"/>'
                     f'<text x="{x+w/2:.0f}" y="280.5" text-anchor="middle" font-family="{FONT}" font-size="12.5" fill="{cls.T}">{c}</text>')
            x += w + 10
        o.write("hero.svg", wrap(W, H, defs, "".join(b), "Alfarouq Ibrahim, AI System Architect",
                                 "Animated liquid wordmark ALFAROUQ with morphing drops. Alfarouq Ibrahim, AI System Architect, Edge-AI and Computer Vision Specialist."))

    @classmethod
    def section(cls, o, num, title, sub):
        W, H = 900, 64
        tw = len(title) * 12.6
        x0, x1 = 84 + tw + 16, W - 190
        b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{H/2}" fill="{cls.CARD}" stroke="url(#gG)" stroke-width="1.4"/>',
             f'<circle cx="34" cy="32" r="18" fill="url(#gD)"/><text x="34" y="37" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="{cls.BG}">{num}</text>',
             f'<text x="64" y="38" font-family="{FONT}" font-size="18" font-weight="700" fill="{cls.T}" letter-spacing="2">{esc(title)}</text>']
        beads = "".join(f'<circle cy="32" r="{7+k}" fill="url(#gG)"><animate attributeName="cx" values="{x0};{x1}" dur="{3.2+k*.9:.1f}s" begin="{-k*1.1:.1f}s" repeatCount="indefinite"/>'
                        f'<animate attributeName="r" values="{6+k};{11+k};{6+k}" dur="{1.8+k*.5:.1f}s" repeatCount="indefinite"/></circle>' for k in range(4))
        b.append(f'<g filter="url(#goo)"><line x1="{x0}" y1="32" x2="{x1}" y2="32" stroke="url(#gG)" stroke-width="5" stroke-linecap="round"/>{beads}</g>')
        b.append(f'<text x="{W-26}" y="37" text-anchor="end" font-family="{FONT}" font-size="12.5" fill="{cls.MUT}">{esc(sub)}</text>')
        o.write(fname(title), wrap(W, H, cls.defs(W), "".join(b), f"Section {num}: {title.title()}"))

    @classmethod
    def focus(cls, o):
        W, H, cw, gp = 900, 250, 207, 24
        b = []
        for i, (title, lines) in enumerate(FOCUS):
            x = i * (cw + gp)
            b.append(cls.blob(x + 2, 2, cw - 4, H - 4, 100 + i, 16, 6, 9 + i))
            b.append(f'<text x="{x+26}" y="62" font-family="{FONT}" font-size="34" font-weight="800" fill="url(#gD)">0{i+1}</text>')
            b.append(f'<circle cx="{x+cw-34}" cy="46" r="7" fill="url(#gD)"><animate attributeName="r" values="5;10;5" dur="{3+i*.4:.1f}s" repeatCount="indefinite"/></circle>')
            b.append(f'<text x="{x+26}" y="130" font-family="{FONT}" font-size="14.5" font-weight="700" fill="{cls.T}" letter-spacing="1.2">{title}</text>')
            for j, ln in enumerate(lines):
                b.append(f'<text x="{x+26}" y="{156+j*21}" font-family="{FONT}" font-size="12.5" fill="{cls.MUT}">{esc(ln)}</text>')
        o.write("focus.svg", wrap(W, H, cls.defs(W), "".join(b), "Focus areas", "Four focus areas: Edge-AI, Computer Vision, Machine Learning, Data Science."))

    @classmethod
    def milestones(cls, o):
        W, H, cw, gp = 900, 150, 207, 24
        b = []
        for i, (big, l1, l2) in enumerate(MILES):
            x = i * (cw + gp)
            b.append(cls.blob(x + 2, 2, cw - 4, H - 4, 200 + i, 14, 5, 8 + i))
            b.append(f'<text x="{x+26}" y="66" font-family="{FONT}" font-size="44" font-weight="800" fill="url(#gD)">{big}</text>')
            b.append(f'<text x="{x+26}" y="96" font-family="{FONT}" font-size="12.5" font-weight="700" fill="{cls.T}">{esc(l1)}</text>')
            for j, part in enumerate(l2.split("|")):
                b.append(f'<text x="{x+26}" y="{116+j*14}" font-family="{FONT}" font-size="11.5" fill="{cls.MUT}">{esc(part)}</text>')
        o.write("milestones.svg", wrap(W, H, cls.defs(W), "".join(b), "Milestones",
                                       "1st place Damietta AI Hackathon, 2nd place Egypt Cities Hackathon, 50 plus ANOMALY members, 4 ML trainings and internships."))

    @classmethod
    def pipeline(cls, o, name, P):
        W, H = P["W"], P["H"]
        b = [cls.bg(W, H, 18)]
        b.append(f'<text x="28" y="38" font-family="{MONO}" font-size="11.5" fill="{cls.D}" letter-spacing="2.5">{esc(P["title"])}</text>')
        if P["badge"]:
            b.append(f'<rect x="{W-122}" y="20" width="96" height="24" rx="12" fill="{cls.CARD}" stroke="{cls.D}"/><text x="{W-74}" y="36" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{cls.D}">{P["badge"]}</text>')
        tubes = []
        for k, (a, c) in enumerate(P["edges"]):
            x1, y1, w1, h1, *_ = P["nodes"][a]
            x2, y2, w2, h2, *_ = P["nodes"][c]
            sx, sy, ex, ey = x1 + w1 - 6, y1 + h1 / 2, x2 + 6, y2 + h2 / 2
            xm = (sx + ex) / 2
            d = f"M{sx},{sy}C{xm},{sy} {xm},{ey} {ex},{ey}"
            tubes.append(f'<path d="{d}" fill="none" stroke="url(#gG)" stroke-width="6" stroke-linecap="round"/>')
            for q in range(2):
                tubes.append(f'<circle r="7" fill="url(#gG)"><animateMotion dur="2.4s" begin="{-q*1.2 - k*.3:.1f}s" repeatCount="indefinite" path="{d}"/></circle>')
        b.append(f'<g filter="url(#goo)">{"".join(tubes)}</g>')
        for i, (x, y, w, h, idx, l1, l2) in enumerate(P["nodes"]):
            b.append(cls.blob(x, y, w, h, 300 + i, 9, 3, 8 + i * .7))
            b.append(f'<text x="{x+16}" y="{y+23}" font-family="{MONO}" font-size="10.5" fill="{cls.D}">{idx}</text>')
            b.append(f'<text x="{x+14}" y="{y+46}" font-family="{FONT}" font-size="11.5" font-weight="700" fill="{cls.T}">{esc(l1)}</text>')
            b.append(f'<text x="{x+16}" y="{y+64}" font-family="{FONT}" font-size="11.5" fill="{cls.MUT}">{esc(l2)}</text>')
        b.append(f'<text x="{W/2}" y="{H-14}" text-anchor="middle" font-family="{FONT}" font-size="11.5" fill="{cls.MUT}">{esc(P["caption"])}</text>')
        o.write(name, wrap(W, H, cls.defs(W), "".join(b), name[:-4].replace("-", " ").title(), P["alt"]))

    @classmethod
    def marquee(cls, o):
        W, H = 900, 62
        widths = [len(s) * 7.6 + 34 for s in TECH]
        cols = [cls.A, cls.B, cls.C, cls.D]

        def chip(x, w, s, k):
            col = cols[k % 4]
            return (f'<rect x="{x:.0f}" y="15" width="{w:.0f}" height="32" rx="16" fill="{cls.CARD}" stroke="{col}" stroke-opacity=".8"/>'
                    f'<circle cx="{x+16:.0f}" cy="31" r="4" fill="{col}"><animate attributeName="r" values="3;5.5;3" dur="{2+k%3*.5:.1f}s" repeatCount="indefinite"/></circle>'
                    f'<text x="{x+28:.0f}" y="35.5" font-family="{FONT}" font-size="13" fill="{cls.T}">{esc(s)}</text>')
        g, _ = scroll_marquee(chip, W, H, TECH, widths, 10)
        defs = (cls.defs(W) + f'<clipPath id="cl"><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16"/></clipPath>'
                f'<linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="{cls.BG}"/><stop offset="1" stop-color="{cls.BG}" stop-opacity="0"/></linearGradient>'
                f'<linearGradient id="fr" x1="1" x2="0"><stop offset="0" stop-color="{cls.BG}"/><stop offset="1" stop-color="{cls.BG}" stop-opacity="0"/></linearGradient>')
        body = (cls.bg(W, H, 16) + f'<g clip-path="url(#cl)">{g}<rect width="80" height="{H}" fill="url(#fl)"/><rect x="{W-80}" width="80" height="{H}" fill="url(#fr)"/></g>')
        o.write("tech-marquee.svg", wrap(W, H, defs, body, "Technologies", "Scrolling list of technologies: " + ", ".join(TECH) + "."))

    @classmethod
    def divider(cls, o):
        W, H = 900, 26
        beads = "".join(f'<circle cy="13" r="{6+k}" fill="url(#gG)"><animate attributeName="cx" values="10;{W-10}" dur="{4+k}s" begin="{-k*1.3:.1f}s" repeatCount="indefinite"/></circle>' for k in range(4))
        b = f'<g filter="url(#goo)"><line x1="10" y1="13" x2="{W-10}" y2="13" stroke="url(#gG)" stroke-width="3" stroke-linecap="round"/>{beads}</g>'
        o.write("divider.svg", wrap(W, H, cls.defs(W), b, "Section divider"))

    @classmethod
    def build(cls):
        o = Out("liquid")
        cls.hero(o)
        for s in SECTIONS:
            cls.section(o, *s)
        cls.focus(o)
        cls.milestones(o)
        cls.pipeline(o, "raai-pipeline.svg", RAAI)
        cls.pipeline(o, "inspection-pipeline.svg", INSP)
        cls.marquee(o)
        cls.divider(o)


# ===================================================================== VORONOI
class VR:
    PAPER, INK, MUT = "#F3EEE4", "#1C1C20", "#5E5A52"
    COLORS = ["#E8C9A0", "#C9D7C0", "#B9CBD9", "#E2B7A5", "#D6CBE3", "#F0DE9E"]
    FLASH = "#FFF9DD"

    @staticmethod
    def cell(i, seeds, W, H, N):
        sx, sy = seeds[i]
        out = []
        for k in range(N):
            th = 2 * math.pi * k / N
            dx, dy = math.cos(th), math.sin(th)
            t = 1e9
            for j, (ox, oy) in enumerate(seeds):
                if j == i:
                    continue
                vx, vy = ox - sx, oy - sy
                dot = dx * vx + dy * vy
                if dot > 1e-9:
                    t = min(t, (vx * vx + vy * vy) / (2 * dot))
            if dx > 1e-9:
                t = min(t, (W - sx) / dx)
            if dx < -1e-9:
                t = min(t, (0 - sx) / dx)
            if dy > 1e-9:
                t = min(t, (H - sy) / dy)
            if dy < -1e-9:
                t = min(t, (0 - sy) / dy)
            out.append((sx + dx * t, sy + dy * t))
        return out

    @classmethod
    def map_svg(cls, W, H, seeds, title, desc, dur=30, K=10, N=56, under="", over="", rx=14, border=True):
        """seeds: list of dict(x,y,ax,ay,ph,lines,color,flash)"""
        frames = []
        for k in range(K + 1):
            a = 2 * math.pi * k / K
            pos = []
            for s in seeds:
                px = s["x"] + s.get("ax", 0) * math.sin(a + s.get("ph", 0))
                py = s["y"] + s.get("ay", 0) * math.sin(2 * a + s.get("ph", 0) * 1.3)
                pos.append((min(max(px, 6), W - 6), min(max(py, 6), H - 6)))
            frames.append(pos)
        cells = [[cls.cell(i, fr, W, H, N) for i in range(len(seeds))] for fr in frames]
        defs = f'<clipPath id="cm"><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{rx}"/></clipPath>'
        poly, labels = [], []
        for i, s in enumerate(seeds):
            col = cls.COLORS[s.get("color", i) % len(cls.COLORS)]
            vals = ";".join(" ".join(f"{x:.1f},{y:.1f}" for x, y in cells[k][i]) for k in range(K + 1))
            first = " ".join(f"{x:.1f},{y:.1f}" for x, y in cells[0][i])
            anim = f'<animate attributeName="points" dur="{dur}s" repeatCount="indefinite" values="{vals}"/>'
            if s.get("flash") is not None:
                d0 = s["flash"]
                cyc = 7.0
                kt = f"0;{(d0*.8)/cyc:.3f};{(d0*.8+.6)/cyc:.3f};{(d0*.8+1.6)/cyc:.3f};1"
                anim += (f'<animate attributeName="fill" dur="{cyc}s" repeatCount="indefinite" values="{col};{col};{cls.FLASH};{col};{col}" keyTimes="{kt}"/>')
            poly.append(f'<polygon points="{first}" fill="{col}" stroke="{cls.PAPER}" stroke-width="2.4" stroke-linejoin="round">{anim}</polygon>')
            tv = ";".join(f"{frames[k][i][0]:.1f},{frames[k][i][1]:.1f}" for k in range(K + 1))
            txt = "".join(
                f'<text x="0" y="{dy}" text-anchor="middle" font-family="{fam}" font-size="{sz}" font-weight="{wt}" fill="{fill}" letter-spacing="{ls}">{esc(t)}</text>'
                for (t, sz, wt, dy, fill, fam, ls) in s.get("lines", []))
            dot = f'<circle r="2.4" fill="{cls.INK}"/>' if s.get("dot", False) else ""
            labels.append(f'<g transform="translate({frames[0][i][0]:.1f} {frames[0][i][1]:.1f})"><animateTransform attributeName="transform" type="translate" dur="{dur}s" repeatCount="indefinite" values="{tv}"/>{dot}{txt}</g>')
        body = (f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{rx}" fill="{cls.PAPER}"/>'
                f'<g clip-path="url(#cm)">{under}{"".join(poly)}{"".join(labels)}{over}</g>')
        if border:
            body += f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{rx}" fill="none" stroke="{cls.INK}" stroke-width="1.2"/>'
        return wrap(W, H, defs, body, title, desc)

    @classmethod
    def L(cls, text, size=10, wt=400, dy=0, fill=None, fam=None, ls=1):
        return (text, size, wt, dy, fill or cls.INK, fam or MONO, ls)

    @classmethod
    def hero(cls, o):
        W, H = 900, 340
        rnd = random.Random(21)
        lab = [(520, 62, "EDGE-AI"), (668, 44, "COMPUTER VISION"), (815, 72, "MACHINE LEARNING"), (560, 172, "DATA SCIENCE"),
               (705, 152, "RAA'I"), (840, 190, "ANOMALY"), (540, 278, "COMPILERS"), (690, 262, "INSPECTION"), (825, 290, "LEADERSHIP")]
        deco = [(60, 50), (190, 28), (330, 46), (420, 122), (70, 204), (220, 236), (380, 292), (130, 306), (300, 164)]
        seeds = []
        for i, (x, y, t) in enumerate(lab):
            seeds.append(dict(x=x, y=y, ax=16, ay=12, ph=rnd.uniform(0, 6.28), color=i,
                              lines=[cls.L(t, 10.5, 700, 18, ls=1.2)], dot=True))
        for i, (x, y) in enumerate(deco):
            seeds.append(dict(x=x, y=y, ax=14, ay=10, ph=rnd.uniform(0, 6.28), color=i + 3))
        px, py, pw, ph_ = 36, 34, 408, 272
        panel = (f'<rect x="{px}" y="{py}" width="{pw}" height="{ph_}" rx="6" fill="{cls.PAPER}" fill-opacity=".93" stroke="{cls.INK}" stroke-width="1.2"/>'
                 f'<text x="{px+22}" y="{py+34}" font-family="{MONO}" font-size="11" fill="{cls.MUT}" letter-spacing="3">TERRITORY MAP / AI SYSTEMS</text>'
                 f'<text x="{px+22}" y="{py+88}" font-family="{FONT}" font-size="35" font-weight="800" fill="{cls.INK}" textLength="364" lengthAdjust="spacingAndGlyphs">ALFAROUQ IBRAHIM</text>'
                 f'<text x="{px+22}" y="{py+120}" font-family="{FONT}" font-size="19" font-weight="700" fill="{cls.INK}">AI System Architect</text>'
                 f'<text x="{px+22}" y="{py+146}" font-family="{FONT}" font-size="15" fill="{cls.MUT}">Edge-AI &amp; Computer Vision Specialist</text>'
                 f'<line x1="{px+22}" y1="{py+166}" x2="{px+pw-22}" y2="{py+166}" stroke="{cls.INK}" stroke-opacity=".3"/>'
                 f'<text x="{px+22}" y="{py+192}" font-family="{FONT}" font-size="13.5" fill="{cls.INK}">Architecting intelligent systems.</text>'
                 f'<text x="{px+22}" y="{py+212}" font-family="{FONT}" font-size="13.5" fill="{cls.INK}">Engineering real-world impact.</text>')
        x = px + 22
        for c in ("Machine Learning", "Deep Learning", "Data Science"):
            w = len(c) * 7 + 22
            panel += (f'<rect x="{x}" y="{py+228}" width="{w:.0f}" height="26" fill="none" stroke="{cls.INK}" stroke-width="1.1"/>'
                      f'<text x="{x+w/2:.0f}" y="{py+245}" text-anchor="middle" font-family="{FONT}" font-size="12" fill="{cls.INK}">{c}</text>')
            x += w + 8
        o.write("hero.svg", cls.map_svg(W, H, seeds, "Alfarouq Ibrahim, AI System Architect",
                                        "Animated Voronoi territory map. Regions: Edge-AI, Computer Vision, Machine Learning, Data Science, Raa'i, ANOMALY, Compilers, Inspection, Leadership. Alfarouq Ibrahim, AI System Architect.",
                                        dur=36, K=12, N=64, over=panel, rx=16))

    @classmethod
    def section(cls, o, num, title, sub):
        W, H = 900, 64
        rnd = random.Random(int(num) * 7)
        seeds = [dict(x=122, y=32, ax=4, ay=3, ph=0, color=int(num), lines=[cls.L(f"{num}  {title}", 15, 800, 5, fam=FONT, ls=1.6)])]
        for i, (x, y) in enumerate([(330, 18), (352, 50), (500, 14), (520, 52), (640, 30)]):
            seeds.append(dict(x=x, y=y, ax=14, ay=7, ph=rnd.uniform(0, 6.28), color=int(num) + i + 1))
        seeds.append(dict(x=770, y=32, ax=6, ay=3, ph=1.2, color=int(num) + 7, lines=[cls.L(sub, 10.5, 400, 4, fill=cls.INK, ls=.5)]))
        seeds.append(dict(x=884, y=32, ax=5, ay=10, ph=2.1, color=int(num) + 2))
        o.write(fname(title), cls.map_svg(W, H, seeds, f"Section {num}: {title.title()}", f"Voronoi strip titled {title.title()}", dur=24, K=8, N=44, rx=10))

    @classmethod
    def focus(cls, o):
        W, H = 900, 250
        pos = [(115, 100), (338, 156), (562, 94), (786, 152)]
        seeds = []
        for i, ((x, y), (title, lines)) in enumerate(zip(pos, FOCUS)):
            ls_ = [cls.L(f"0{i+1}", 10, 700, -42, fill=cls.MUT, ls=2), cls.L(title, 13.5, 800, -20, fam=FONT, ls=1)]
            ls_ += [cls.L(t, 12, 400, 4 + j * 19, fam=FONT, fill=cls.INK, ls=0) for j, t in enumerate(lines)]
            seeds.append(dict(x=x, y=y, ax=7, ay=6, ph=i * 1.3, color=i, lines=ls_))
        for i, (x, y) in enumerate([(28, 232), (450, 236), (884, 28), (440, 16)]):
            seeds.append(dict(x=x, y=y, ax=5, ay=4, ph=i, color=i + 4))
        o.write("focus.svg", cls.map_svg(W, H, seeds, "Focus areas", "Four territories: Edge-AI, Computer Vision, Machine Learning, Data Science.", dur=32, K=10, N=56))

    @classmethod
    def milestones(cls, o):
        W, H = 900, 150
        pos = [(115, 66), (338, 86), (562, 62), (786, 84)]
        seeds = []
        for i, ((x, y), (big, l1, l2)) in enumerate(zip(pos, MILES)):
            seeds.append(dict(x=x, y=y - (6 if "|" in l2 else 0), ax=6, ay=5, ph=i * 1.1, color=i + 1, lines=[
                cls.L(big, 38, 800, -2, fam=FONT, ls=0), cls.L(l1, 12.5, 700, 22, fam=FONT, ls=0)]
                + [cls.L(part, 10.5, 400, 40 + j * 13, fam=FONT, fill=cls.MUT, ls=0) for j, part in enumerate(l2.split("|"))]))
        for i, (x, y) in enumerate([(26, 130), (450, 140), (884, 20), (448, 12)]):
            seeds.append(dict(x=x, y=y, ax=4, ay=3, ph=i, color=i + 5))
        o.write("milestones.svg", cls.map_svg(W, H, seeds, "Milestones",
                                              "1st place Damietta AI Hackathon, 2nd place Egypt Cities Hackathon, 50 plus ANOMALY members, 4 ML trainings and internships.", dur=30, K=10, N=56))

    @classmethod
    def pipeline(cls, o, name, P):
        W, H = P["W"], P["H"]
        seeds = []
        for i, ((x, y, w, h, idx, l1, l2), dpt) in enumerate(zip(P["nodes"], P["depth"])):
            cx = x + w / 2
            cy = y + h / 2 + ((-14 if i % 2 == 0 else 14) if len(P["nodes"]) == 6 else 0)
            seeds.append(dict(x=cx, y=cy, ax=4, ay=3, ph=i, color=i, flash=dpt, lines=[
                cls.L(idx, 10, 700, -22, fill=cls.MUT, ls=2), cls.L(l1, 12.5, 800, -2, fam=FONT, ls=0), cls.L(l2, 11, 400, 16, fam=FONT, fill=cls.MUT, ls=0)]))
        fill = [(90, 12), (260, 200), (420, 14), (590, 204), (770, 14), (872, 190)] if len(P["nodes"]) == 6 else [(110, 22), (110, 262), (470, 20), (470, 262), (880, 30), (880, 262)]
        for i, (x, y) in enumerate(fill):
            seeds.append(dict(x=x, y=y, ax=5, ay=4, ph=i * .9, color=i + 3))
        head = (f'<text x="22" y="26" font-family="{MONO}" font-size="11" fill="{cls.INK}" letter-spacing="2.5" font-weight="700">{esc(P["title"])}</text>')
        if P["badge"]:
            head += f'<rect x="{W-118}" y="10" width="94" height="22" fill="{cls.PAPER}" stroke="{cls.INK}"/><text x="{W-71}" y="25" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{cls.INK}" font-weight="700">{P["badge"]}</text>'
        head += f'<rect x="{W/2-330}" y="{H-30}" width="660" height="20" fill="{cls.PAPER}" fill-opacity=".92"/><text x="{W/2}" y="{H-16}" text-anchor="middle" font-family="{FONT}" font-size="11.5" fill="{cls.MUT}">{esc(P["caption"])}</text>'
        o.write(name, cls.map_svg(W, H, seeds, name[:-4].replace("-", " ").title(), P["alt"] + " Cells light up in order of data flow.", dur=34, K=10, N=56, over=head, rx=16))

    @classmethod
    def marquee(cls, o):
        W, H = 900, 62
        widths = [len(s) * 7.6 + 30 for s in TECH]

        def chip(x, w, s, k):
            return (f'<rect x="{x:.0f}" y="15" width="{w:.0f}" height="32" fill="{cls.COLORS[k%6]}" stroke="{cls.INK}" stroke-width="1"/>'
                    f'<text x="{x+w/2:.0f}" y="35.5" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" fill="{cls.INK}">{esc(s)}</text>')
        g, _ = scroll_marquee(chip, W, H, TECH, widths, 8)
        defs = (f'<clipPath id="cl"><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10"/></clipPath>'
                f'<linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="{cls.PAPER}"/><stop offset="1" stop-color="{cls.PAPER}" stop-opacity="0"/></linearGradient>'
                f'<linearGradient id="fr" x1="1" x2="0"><stop offset="0" stop-color="{cls.PAPER}"/><stop offset="1" stop-color="{cls.PAPER}" stop-opacity="0"/></linearGradient>')
        body = (f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{cls.PAPER}"/><g clip-path="url(#cl)">{g}'
                f'<rect width="80" height="{H}" fill="url(#fl)"/><rect x="{W-80}" width="80" height="{H}" fill="url(#fr)"/></g>'
                f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="{cls.INK}" stroke-width="1.2"/>')
        o.write("tech-marquee.svg", wrap(W, H, defs, body, "Technologies", "Scrolling list of technologies: " + ", ".join(TECH) + "."))

    @classmethod
    def divider(cls, o):
        W, H = 900, 22
        rnd = random.Random(3)
        seeds = [dict(x=40 + i * 82, y=11, ax=18, ay=6, ph=rnd.uniform(0, 6.28), color=i) for i in range(11)]
        o.write("divider.svg", cls.map_svg(W, H, seeds, "Section divider", "", dur=20, K=8, N=36, rx=6, border=False))

    @classmethod
    def build(cls):
        o = Out("voronoi")
        cls.hero(o)
        for s in SECTIONS:
            cls.section(o, *s)
        cls.focus(o)
        cls.milestones(o)
        cls.pipeline(o, "raai-pipeline.svg", RAAI)
        cls.pipeline(o, "inspection-pipeline.svg", INSP)
        cls.marquee(o)
        cls.divider(o)


if __name__ == "__main__":
    BP.build()
    LQ.build()
    VR.build()
    print("done")
