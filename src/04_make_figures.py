"""Step 4. Draw the bibliometric figures as editable draw.io files and export PNG.

Input : results/*.csv (written by 03_build_tables.py)
Output: figures/fig_bib_*.drawio  and  figures/fig_bib_*.png
"""
import csv
import math
from pathlib import Path

from drawio_lib import Diagram, export_png

ROOT = Path(__file__).resolve().parents[1]
RES, FIG = ROOT / "results", ROOT / "figures"
FIG.mkdir(exist_ok=True)

RQ_NAME = {
    "RQ1": "RQ1 Frameworks, standards, regulations",
    "RQ2": "RQ2 Security and privacy mechanisms",
    "RQ3": "RQ3 Interoperability",
    "RQ4": "RQ4 Gaps and challenges",
    "RQ5": "RQ5 Emerging technologies",
}
# black-and-white palette: five grey steps, darkest first; legends carry the names
RQ_COL = {"RQ1": "#1A1A1A", "RQ2": "#4D4D4D", "RQ3": "#8C8C8C",
          "RQ4": "#BFBFBF", "RQ5": "#E6E6E6"}
RQ_LEGEND = {"RQ1": "RQ1 Frameworks", "RQ2": "RQ2 Security", "RQ3": "RQ3 Interoperability",
             "RQ4": "RQ4 Gaps", "RQ5": "RQ5 Technologies"}
BAR = "#4D4D4D"
EV_COL = {"A": "#1A1A1A", "S": "#8C8C8C", "M": "#D9D9D9"}
EV_NAME = {"A": "A  abstract assessed", "S": "S  sections read", "M": "M  metadata only"}
GRID, AXIS, TXT = "#E3E3E3", "#555555", "#222222"


def read(name):
    return list(csv.DictReader((RES / name).open(encoding="utf-8")))


def nice_max(v):
    return math.ceil(v / 10) * 10 if v > 10 else v


def ticks(vmax):
    step = 1 if vmax <= 10 else (10 if vmax <= 80 else 20)
    return list(range(0, int(vmax) + 1, step))


def cut_ties(items, cap):
    """Keep items with count >= k, k minimal such that at most `cap` remain,
    so that the cut never splits a tie."""
    vals = sorted({n for _, n in items}, reverse=True)
    k = vals[-1]
    for v in vals:
        if sum(1 for _, n in items if n >= v) <= cap:
            k = v
        else:
            break
    kept = [(a, n) for a, n in items if n >= k]
    return sorted(kept, key=lambda t: (-t[1], t[0])), k


def hbar(name, items, color, xlabel, label_w=250, width=760, bar_h=22, gap=9):
    n = len(items)
    top, bottom, right = 20, 58, 50
    vmax = nice_max(max(v for _, v in items))
    plot_w = width - label_w - right - 20
    height = top + n * (bar_h + gap) + bottom
    g = Diagram(width, height, name)
    x0 = label_w + 10
    for t in ticks(vmax):
        x = x0 + plot_w * t / vmax
        g.line(x, top, x, top + n * (bar_h + gap), color=GRID)
        g.text(x - 20, top + n * (bar_h + gap) + 4, 40, 18, str(t), size=11, color=AXIS)
    g.line(x0, top, x0, top + n * (bar_h + gap), color=AXIS)
    g.line(x0, top + n * (bar_h + gap), x0 + plot_w, top + n * (bar_h + gap), color=AXIS)
    for i, (lab, v) in enumerate(items):
        y = top + gap / 2 + i * (bar_h + gap)
        g.text(5, y, label_w, bar_h, lab, size=12, color=TXT, align="right")
        g.rect(x0, y, plot_w * v / vmax, bar_h, fill=color)
        g.text(x0 + plot_w * v / vmax + 4, y, 36, bar_h, str(v), size=11, color=TXT, align="left")
    g.text(x0, height - 30, plot_w, 22, xlabel, size=12, color=TXT)
    return g


def save(g, stem):
    d = FIG / f"{stem}.drawio"
    g.save(d)
    ok = export_png(d, FIG / f"{stem}.png")
    print(f"{stem}: drawio written, png {'ok' if ok else 'MISSING'}")


# ---- Figure 1: records per year, stacked by research question ---------------
rows = read("year_by_rq.csv")
RQS = ["RQ1", "RQ2", "RQ3", "RQ4", "RQ5"]
W, H = 760, 480
left, top, bottom = 70, 60, 120
plot_w, plot_h = W - left - 30, H - top - bottom
totals = [sum(int(r[q]) for q in RQS) for r in rows]
vmax = nice_max(max(totals))
g = Diagram(W, H, "records per year")
for t in ticks(vmax):
    y = top + plot_h - plot_h * t / vmax
    g.line(left, y, left + plot_w, y, color=GRID)
    g.text(left - 44, y - 9, 38, 18, str(t), size=11, color=AXIS, align="right")
g.line(left, top, left, top + plot_h, color=AXIS)
g.line(left, top + plot_h, left + plot_w, top + plot_h, color=AXIS)
slot = plot_w / len(rows)
bw = slot * 0.55
for i, r in enumerate(rows):
    x = left + slot * i + (slot - bw) / 2
    ycur = top + plot_h
    for q in RQS:
        v = int(r[q])
        if v == 0:
            continue
        h = plot_h * v / vmax
        ycur -= h
        g.rect(x, ycur, bw, h, fill=RQ_COL[q], stroke="#ffffff", stroke_w=1,
               text=str(v) if h >= 13 else "", size=11,
               color="#ffffff" if q in ("RQ1", "RQ2") else "#222222")
    g.text(x - 10, ycur - 20, bw + 20, 18, str(totals[i]), size=12, bold=True)
    g.text(x - 15, top + plot_h + 4, bw + 30, 36,
           f"{r['year']}<br>({r['unique_records']} unique)", size=11, color=TXT)
g.text(8, top + plot_h / 2 - 10, 20, 20, "", size=11)
g.text(left - 60, 8, 220, 22, "Placements (bold: total per year)", size=11, color=AXIS, align="left")
g.text(left, H - 84, 300, 20, "Research question (stack order, bottom to top):", size=11,
       color=AXIS, align="left")
for i, q in enumerate(RQS):
    lx = left + (i % 3) * 215
    ly = H - 60 + (i // 3) * 28
    g.rect(lx, ly + 4, 14, 14, fill=RQ_COL[q], stroke="#666666", stroke_w=0.5)
    g.text(lx + 19, ly, 190, 22, RQ_LEGEND[q], size=11, align="left")
g.text(left + 2 * 215, H - 32, 280, 22, "n = unique records", size=11, color=AXIS, align="left")
save(g, "fig_bib_1_records_per_year")

# ---- Figure 2: evidence level by research question --------------------------
rows = read("evidence_by_rq.csv")
W, H = 760, 330
label_w, top = 270, 20
plot_w = W - label_w - 60
g = Diagram(W, H, "evidence by RQ")
bar_h, gap = 30, 14
x0 = label_w + 10
for t in range(0, 51, 10):
    x = x0 + plot_w * t / 50
    g.line(x, top, x, top + 5 * (bar_h + gap), color=GRID)
    g.text(x - 20, top + 5 * (bar_h + gap) + 4, 40, 18, str(t), size=11, color=AXIS)
g.line(x0, top, x0, top + 5 * (bar_h + gap), color=AXIS)
g.line(x0, top + 5 * (bar_h + gap), x0 + plot_w, top + 5 * (bar_h + gap), color=AXIS)
for i, r in enumerate(rows):
    y = top + gap / 2 + i * (bar_h + gap)
    g.text(5, y, label_w, bar_h, RQ_NAME[r["rq"]], size=12, align="right")
    x = x0
    for e in ("A", "S", "M"):
        v = int(r[e])
        if v == 0:
            continue
        w = plot_w * v / 50
        g.rect(x, y, w, bar_h, fill=EV_COL[e], stroke="#ffffff", text=str(v), size=11,
               color="#ffffff" if e == "A" else "#222222")
        x += w
g.text(x0, top + 5 * (bar_h + gap) + 24, plot_w, 20, "Records per research question (50 each)", size=12)
lx, ly = 20, H - 30
for e in ("A", "S", "M"):
    g.rect(lx, ly + 4, 14, 14, fill=EV_COL[e], stroke="#666666", stroke_w=0.5)
    g.text(lx + 15, ly, 170, 20, EV_NAME[e], size=11, align="left")
    lx += 200
save(g, "fig_bib_2_evidence_by_rq")

# ---- Figure 3: keywords -----------------------------------------------------
kw = [(r["keyword"], int(r["records"])) for r in read("keywords_top.csv")]
kw, k_kw = cut_ties(kw, 15)
print(f"keywords shown: {len(kw)} (records >= {k_kw})")
save(hbar("keywords", kw, BAR,
          "Records (of 189) carrying the keyword in OpenAlex", label_w=210), "fig_bib_3_keywords")

# ---- Figure 4: countries ----------------------------------------------------
co = [(r["country"], int(r["records"])) for r in read("countries.csv")]
co, k_co = cut_ties(co, 15)
print(f"countries shown: {len(co)} (records >= {k_co})")
save(hbar("countries", co, BAR,
          "Records (of 168 with affiliation data) with at least one author in the country",
          label_w=150), "fig_bib_4_countries")

# ---- Figure 5: authors ------------------------------------------------------
au = [(r["author"], int(r["records"])) for r in read("authors_top.csv")]
au, k_au = cut_ties(au, 12)
print(f"authors shown: {len(au)} (records >= {k_au})")
save(hbar("authors", au, BAR, "Records (of 189) with the person as author",
          label_w=150), "fig_bib_5_authors")
(RES / "figure_cutoffs.json").write_text(
    f'{{"keywords_min_records": {k_kw}, "countries_min_records": {k_co}, '
    f'"authors_min_records": {k_au}, "keywords_shown": {len(kw)}, '
    f'"countries_shown": {len(co)}, "authors_shown": {len(au)}}}\n', encoding="utf-8")
