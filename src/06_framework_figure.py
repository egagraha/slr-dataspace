"""Step 6. DD-DSF framework figure (manuscript Figure 5) as draw.io and PNG.

Four layers and a feedback loop, black and white. The content mirrors
Section 5.2 of the manuscript; there are no data in this figure.
"""
from pathlib import Path

from drawio_lib import Diagram, export_png

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
K, WH = "#000000", "#ffffff"

layers = [
    ("Governance and regulation layer", "regulators, policymakers, ethics boards"),
    ("Infrastructure layer", "connectors, DLT, federated learning, consent and access control"),
    ("Actors layer", "data providers, intermediaries, consumers"),
    ("Application and value layer", "sector use cases and data-driven innovation"),
]
W, H = 760, 400
BX, BW, BH, GAP, TOP = 40, 540, 72, 20, 20
g = Diagram(W, H, "DD-DSF")
for i, (t, sub) in enumerate(layers):
    y = TOP + i * (BH + GAP)
    g.rect(BX, y, BW, BH, fill=WH, stroke=K, stroke_w=1.5, rounded=True, color=K, size=17,
           text=f"<b>{t}</b><br><font style='font-size:14px'>{sub}</font>")
    if i < len(layers) - 1:
        g.line(BX + BW / 2, y + BH, BX + BW / 2, y + BH + GAP, color=K, width=1.5)
yb = TOP + 3 * (BH + GAP) + BH / 2
yt = TOP + BH / 2
xr = BX + BW + 50
g.line(BX + BW, yb, xr, yb, color=K, width=2)
g.line(xr, yb, xr, yt, color=K, width=2)
g.line(xr, yt, BX + BW + 2, yt, color=K, width=2, arrow=True)
g.text(xr + 8, (yt + yb) / 2 - 22, 110, 44, "feedback<br>loop", size=15, color=K, align="left")
d = FIG / "fig_ddsf_framework.drawio"
g.save(d)
d.write_text(d.read_text(encoding="utf-8").replace("#222222", K), encoding="utf-8")
print("png", export_png(d, FIG / "fig_ddsf_framework.png"))
