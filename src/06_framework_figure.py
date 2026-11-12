"""Step 6. DD-DSF framework figure (manuscript Figure 5) as draw.io and PNG.

Left: the four layers. Right: the proposed exchange-decision process of
Section 5.2 (request -> legal and policy determination -> identity, semantic and
policy checks -> actor decision -> exchange -> reuse in the application layer), with
rejection branches and the feedback path to governance. Black and white; there
are no data in this figure, and the process has not been evaluated empirically.
"""
from pathlib import Path

from drawio_lib import Diagram, export_png

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
K, WH, LIGHT = "#000000", "#ffffff", "#EBEBEB"

layers = [
    ("Governance and regulation layer", "regulators, policymakers, ethics boards"),
    ("Infrastructure layer", "connectors, DLT, federated learning, consent and access control"),
    ("Actors layer", "data providers, intermediaries, consumers"),
    ("Application and value layer", "sector use cases and data-driven innovation"),
]
steps = [
    "<b>2</b>&nbsp; Determine applicable obligations and permitted conditions of use",
    "<b>3</b>&nbsp; Check identity, semantic compatibility, and whether policies can be expressed and enforced",
    "<b>4</b>&nbsp; Organizations decide on expected benefit, effort, and remaining risk",
    "<b>5</b>&nbsp; Approved exchange&nbsp; &rarr;&nbsp; <b>6</b>&nbsp; Recipient reuses the data in a new service, analytical model, or joint activity",
]

W, H = 960, 585
LX, LW = 40, 320                 # layer column
PX, PW = 410, 330                # process column
RX, RW = 775, 175                # rejection box
ROW0, ROWH, BH = 80, 110, 88     # first row top, row pitch, box height
g = Diagram(W, H, "DD-DSF")

g.text(LX, 40, LW, 30, "<b>Layers</b>", size=16, color=K)
g.rect(PX, 14, PW, 50, fill=LIGHT, stroke=K, stroke_w=1.5, rounded=True, color=K, size=14,
       text="<b>1</b>&nbsp; Request: intended purpose and data required")

for i, ((t, sub), st) in enumerate(zip(layers, steps)):
    y = ROW0 + i * ROWH
    g.rect(LX, y, LW, BH, fill=WH, stroke=K, stroke_w=1.5, rounded=True, color=K, size=16,
           text=f"<b>{t}</b><br><font style='font-size:13px'>{sub}</font>")
    if i < 3:
        g.line(LX + LW / 2, y + BH, LX + LW / 2, y + ROWH, color=K, width=1.5)
    g.rect(PX, y + 6, PW, BH - 12, fill=WH, stroke=K, stroke_w=1.5, color=K, size=14, text=st)
    # dotted link: which layer carries the step
    g.line(LX + LW, y + BH / 2, PX, y + BH / 2, color=K, width=1, dashed=True)

# main path through the process column
g.line(PX + PW / 2, 64, PX + PW / 2, ROW0 + 6, color=K, width=2, arrow=True)
for i in range(3):
    y = ROW0 + i * ROWH
    g.line(PX + PW / 2, y + BH - 6, PX + PW / 2, y + ROWH + 6, color=K, width=2, arrow=True)
    g.text(PX + PW / 2 + 6, y + BH - 6, 70, 22, "pass", size=12, color=K, align="left")

# rejection branches from steps 2-4
ry, rh = ROW0 + 20, 2 * ROWH + BH - 40
g.rect(RX, ry, RW, rh, fill=WH, stroke=K, stroke_w=1.5, dashed=True, rounded=True, color=K,
       size=13, text="<b>Rejected or unresolved</b><br>policy conflict, missing semantic mapping, "
                     "excessive onboarding effort")
for i in range(3):
    yc = ROW0 + i * ROWH + BH / 2
    g.line(PX + PW, yc, RX, yc, color=K, width=1.5, dashed=True, arrow=True)

# feedback path: from the application layer and from rejections back to governance
bus = ROW0 + 3 * ROWH + BH + 26
app_y = ROW0 + 3 * ROWH + BH
g.line(LX + LW / 2, app_y, LX + LW / 2, bus, color=K, width=2)
g.line(RX + RW / 2, ry + rh, RX + RW / 2, bus, color=K, width=2, dashed=True)
g.line(RX + RW / 2, bus, 14, bus, color=K, width=2)
g.line(14, bus, 14, ROW0 + BH / 2, color=K, width=2)
g.line(14, ROW0 + BH / 2, LX, ROW0 + BH / 2, color=K, width=2, arrow=True)
g.text(LX + LW / 2 + 10, bus + 2, 420, 22,
       "feedback to the responsible governance and technical actors", size=13, color=K, align="left")
g.text(LX, bus + 30, W - 2 * LX, 24,
       "Proposed exchange-decision process; it has not been evaluated in an operating data space.",
       size=12, color=K, align="left")

d = FIG / "fig_ddsf_framework.drawio"
g.save(d)
d.write_text(d.read_text(encoding="utf-8").replace("#222222", K), encoding="utf-8")
print("png", export_png(d, FIG / "fig_ddsf_framework.png"))
