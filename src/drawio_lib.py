"""Minimal writer for draw.io (diagrams.net) files, plus PNG export through the
draw.io desktop CLI. Every shape is a native draw.io cell, so the figures stay
editable in draw.io after they have been generated.
"""
import shutil
import subprocess
import time
from pathlib import Path
from xml.sax.saxutils import escape

FONT = "Helvetica"
DRAWIO_BIN = [
    "/Applications/draw.io.app/Contents/MacOS/draw.io",
    shutil.which("drawio") or "",
]


def _style(d):
    return ";".join(f"{k}={v}" for k, v in d.items()) + ";"


class Diagram:
    def __init__(self, width, height, name="Figure"):
        self.w, self.h, self.name = width, height, name
        self.cells = []
        self._n = 1

    def _id(self):
        self._n += 1
        return f"c{self._n}"

    def rect(self, x, y, w, h, fill="#ffffff", stroke="none", text="", size=12,
             color="#222222", bold=False, align="center", valign="middle",
             rounded=False, dashed=False, stroke_w=1, arc=8, wrap=True, extra=None):
        st = dict(rounded=1 if rounded else 0, whiteSpace="wrap" if wrap else "nowrap",
                  html=1, fillColor=fill, strokeColor=stroke, strokeWidth=stroke_w,
                  fontFamily=FONT, fontSize=size, fontColor=color,
                  fontStyle=1 if bold else 0, align=align, verticalAlign=valign,
                  dashed=1 if dashed else 0)
        if rounded:
            st["arcSize"] = arc
        if fill == "none":
            st["fillColor"] = "none"
        if extra:
            st.update(extra)
        self.cells.append(
            f'<mxCell id="{self._id()}" value="{escape(text, {chr(34): "&quot;"})}" '
            f'style="{_style(st)}" vertex="1" parent="1">'
            f'<mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/>'
            f"</mxCell>")

    def text(self, x, y, w, h, text, size=12, color="#222222", bold=False,
             align="center", valign="middle", rotation=0, italic=False):
        st = dict(text=None, html=1, strokeColor="none", fillColor="none",
                  fontFamily=FONT, fontSize=size, fontColor=color,
                  fontStyle=(1 if bold else 0) | (2 if italic else 0),
                  align=align, verticalAlign=valign, whiteSpace="wrap", rotation=rotation)
        s = ";".join(k if v is None else f"{k}={v}" for k, v in st.items()) + ";"
        self.cells.append(
            f'<mxCell id="{self._id()}" value="{escape(text, {chr(34): "&quot;"})}" '
            f'style="{s}" vertex="1" parent="1">'
            f'<mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/>'
            f"</mxCell>")

    def line(self, x1, y1, x2, y2, color="#444444", width=1, dashed=False, arrow=False):
        st = dict(endArrow="classic" if arrow else "none", endFill=1, html=1,
                  strokeColor=color, strokeWidth=width, dashed=1 if dashed else 0)
        self.cells.append(
            f'<mxCell id="{self._id()}" value="" style="{_style(st)}" edge="1" parent="1">'
            f'<mxGeometry relative="1" as="geometry">'
            f'<mxPoint x="{x1:.1f}" y="{y1:.1f}" as="sourcePoint"/>'
            f'<mxPoint x="{x2:.1f}" y="{y2:.1f}" as="targetPoint"/>'
            f"</mxGeometry></mxCell>")

    def xml(self):
        body = "\n        ".join(self.cells)
        return (
            '<mxfile host="app.diagrams.net" agent="slr-dataspace/src/drawio_lib.py">\n'
            f'  <diagram id="d1" name="{escape(self.name)}">\n'
            f'    <mxGraphModel dx="{self.w}" dy="{self.h}" grid="0" gridSize="10" guides="1" '
            f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
            f'pageWidth="{self.w}" pageHeight="{self.h}" math="0" shadow="0" background="#ffffff">\n'
            "      <root>\n"
            '        <mxCell id="0"/>\n'
            '        <mxCell id="1" parent="0"/>\n'
            f"        {body}\n"
            "      </root>\n"
            "    </mxGraphModel>\n"
            "  </diagram>\n"
            "</mxfile>\n")

    def save(self, path):
        Path(path).write_text(self.xml(), encoding="utf-8")


def export_png(drawio_path, png_path, scale=3):
    """Render a .drawio file to PNG with the draw.io desktop CLI (if installed)."""
    binary = next((b for b in DRAWIO_BIN if b and Path(b).exists()), None)
    if binary is None:
        print(f"draw.io CLI not found; skipped PNG for {drawio_path}")
        return False
    cmd = [binary, "--no-sandbox", "-x", "-f", "png", "-s", str(scale), "-b", "10",
           "-o", str(png_path), str(drawio_path)]
    png_path = Path(png_path)
    png_path.unlink(missing_ok=True)  # so a stale PNG is never mistaken for a fresh export
    # Some draw.io desktop versions (seen with 32.6.10) write the PNG but never exit.
    # Wait for the process, or for the PNG to exist with a stable size, at most 180 s.
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    last, stable, start = -1, 0, time.monotonic()
    while proc.poll() is None and time.monotonic() - start < 180:
        size = png_path.stat().st_size if png_path.exists() else -1
        stable = stable + 1 if size > 0 and size == last else 0
        if stable >= 4:  # unchanged for 2 s
            break
        last = size
        time.sleep(0.5)
    if proc.poll() is None:
        proc.kill()
    err = proc.communicate()[1] or ""
    out = ""
    ok = png_path.exists() and png_path.stat().st_size > 0
    if not ok:
        print(out[-400:], err[-400:])
    return ok
