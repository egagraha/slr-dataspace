"""Step 5. Graphical abstract as an editable draw.io file and a PNG.

Elsevier asks for at least 531 x 1328 pixels (height x width); the canvas is
1328 x 531 and the PNG is exported at 2x. All numbers are read from
results/numbers.json and data/raw/References-Lists.md; none is typed in.
"""
import json
import re
from pathlib import Path

from drawio_lib import Diagram, export_png

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
num = json.loads((ROOT / "results/numbers.json").read_text(encoding="utf-8"))
raw = (ROOT / "data/raw/References-Lists.md").read_text(encoding="utf-8")
m = re.search(r"([\d,]+) distinct retrieved DOIs", raw)
retrieved = m.group(1)                      # "2,047"
unique, placements = num["n_unique"], num["n_placements"]
ev = num["evidence_total"]

# black-and-white version: the former colour names now hold grey tones
NAVY, GREY = "#000000", "#555555"
BLUE, SKY, ORANGE, GREEN, PINK = "#1A1A1A", "#D9D9D9", "#8C8C8C", "#4D4D4D", "#BFBFBF"
W, H = 1328, 531
g = Diagram(W, H, "Graphical abstract")

# header band
g.rect(0, 0, W, 56, fill=NAVY, text="Data sovereignty and open innovation in data spaces: "
       "what 189 publications show", size=28, color="#ffffff", bold=True)


def panel(x, w, title, color):
    g.rect(x, 70, w, 450, fill="#F2F2F2", stroke="#999999", rounded=True, arc=3)
    g.rect(x, 70, w, 44, fill=color, text=title, size=26, color="#ffffff", bold=True,
           rounded=True, arc=18)


def chevron(x, y):
    g.line(x, y, x + 28, y, color=GREY, width=6, arrow=True)


# ---- panel 1: problem ------------------------------------------------------
P1X, P1W = 12, 300
panel(P1X, P1W, "Problem", GREY)
items = [("Regulation", "GDPR, DGA, Data Act"),
         ("Sovereignty", "control over own data"),
         ("Interoperability", "connectors, semantics")]
for i, (a, b) in enumerate(items):
    y = 130 + i * 84
    g.rect(P1X + 14, y, P1W - 28, 72, fill="#ffffff", stroke="#999999", rounded=True,
           text=f"<b>{a}</b><br><font style='font-size:21px'>{b}</font>", size=25, color="#222222"
           )
g.rect(P1X + 14, 388, P1W - 28, 120, fill="none",
       text="Do rules and technology alone deliver sovereign data sharing?",
       size=23, color=NAVY, bold=True)
chevron(P1X + P1W + 3, 295)

# ---- panel 2: review -------------------------------------------------------
P2X, P2W = 346, 340
panel(P2X, P2W, "Systematic review", BLUE)
g.rect(P2X + 14, 128, 120, 74, fill="none", text=str(unique), size=54, color=BLUE, bold=True)
g.rect(P2X + 136, 128, P2W - 150, 74, fill="none", align="left",
       text="publications<br>2021–2026", size=24, color="#222222")
g.rect(P2X + 14, 206, P2W - 28, 58, fill="none", align="left",
       text=f"{retrieved} DOIs retrieved<br>{placements} placements, {unique} unique", size=21,
       color="#222222")
rq = [("RQ1", BLUE), ("RQ2", ORANGE), ("RQ3", GREEN), ("RQ4", PINK), ("RQ5", SKY)]
cw = (P2W - 28 - 4 * 6) / 5
for i, (q, c) in enumerate(rq):
    g.rect(P2X + 14 + i * (cw + 6), 270, cw, 44, fill=c, text=q, size=21, bold=True,
           color="#222222" if c in (ORANGE, SKY, PINK) else "#ffffff", rounded=True, arc=20)
g.rect(P2X + 14, 318, P2W - 28, 52, fill="none",
       text="Frameworks, security, interoperability, gaps, technologies", size=19,
       color="#222222")
tot = sum(ev.values())
bx, bw = P2X + 14, P2W - 28
g.rect(bx, 376, bw, 26, fill="none", text="Evidence level of the records", size=19,
       color=GREY, bold=True)
x = bx
for k, c, tc in (("A", BLUE, "#ffffff"), ("S", SKY, "#222222"), ("M", "#8C8C8C", "#222222")):
    w = bw * ev[k] / tot
    g.rect(x, 406, w, 42, fill=c, text=f"{ev[k]}", size=21, bold=True, color=tc,
           stroke="#ffffff")
    x += w
g.rect(bx, 452, bw, 30, fill="none", text="A abstract, S sections, M metadata",
       size=17, color="#222222")
chevron(P2X + P2W + 3, 295)

# ---- panel 3: findings -----------------------------------------------------
P3X, P3W = 722, 594
panel(P3X, P3W, "Findings", GREEN)
g.rect(P3X + 12, 122, 272, 32, fill="none", text="Three tensions", size=24, bold=True,
       color=NAVY)
tens = ["Regulation versus routine", "Interoperability across environments",
        "Privacy technology versus daily workflows"]
for i, t in enumerate(tens):
    y = 162 + i * 104
    g.rect(P3X + 12, y, 272, 96, fill="#ffffff", stroke="#999999", rounded=True)
    g.rect(P3X + 22, y + 26, 44, 44, fill=GREEN, text=str(i + 1), size=24, bold=True,
           color="#ffffff", rounded=True, arc=50)
    g.rect(P3X + 72, y + 2, 208, 92, fill="none", text=t, size=21, color="#222222",
           align="left")
g.rect(P3X + 300, 122, 282, 32, fill="none", text="Framework DD-DSF", size=24, bold=True,
       color=NAVY)
layers = [("Governance and regulation", BLUE, "#ffffff"),
          ("Infrastructure", SKY, "#222222"),
          ("Actors", ORANGE, "#222222"),
          ("Application and value", GREEN, "#ffffff")]
for i, (t, c, tc) in enumerate(layers):
    y = 162 + i * 78
    g.rect(P3X + 300, y, 226, 68, fill=c, text=t, size=21, bold=True, color=tc, rounded=True)
g.line(P3X + 526 + 8, 162 + 3 * 78 + 34, P3X + 526 + 30, 162 + 3 * 78 + 34, color=GREY, width=4)
g.line(P3X + 526 + 30, 162 + 3 * 78 + 34, P3X + 526 + 30, 162 + 34, color=GREY, width=4)
g.line(P3X + 526 + 30, 162 + 34, P3X + 526 + 8, 162 + 34, color=GREY, width=4, arrow=True)
g.rect(P3X + 12, 478, 570, 34, fill="none", size=19, bold=True, color=NAVY,
       text="Four propositions for empirical testing")

d = FIG / "graphical_abstract.drawio"
g.save(d)
print("png", export_png(d, FIG / "graphical_abstract.png", scale=2))
