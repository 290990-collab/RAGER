"""Generates the animated README banner: python assets/make_hero.py assets -> hero-light.svg, hero-dark.svg."""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(exist_ok=True)

THEMES = {
    "light": dict(bg="#fcfcfb", card="#ffffff", line="#e2e1db", row="#f4f3ef", ink="#0b0b0b", muted="#6b6a66",
                  h="#2a78d6", p="#eb6834", er="#14966a", bad="#c43d2f", slot="#c3c2b7", onbadge="#ffffff"),
    "dark": dict(bg="#0d1117", card="#161b22", line="#30363d", row="#1f2630", ink="#e6edf3", muted="#8b949e",
                 h="#5a9cf0", p="#f08a5d", er="#2fc08d", bad="#f0776a", slot="#484f58", onbadge="#0d1117"),
}

DUR = 11
STARTS = {}


def fade(s):
    STARTS.setdefault(("f", s), None)
    return f'style="animation:f{s} {DUR}s ease-out infinite both"'


def draw(s):
    STARTS.setdefault(("d", s), None)
    return f'style="animation:d{s} {DUR}s ease-in-out infinite both"'


def body(c):
    mono = "ui-monospace,SFMono-Regular,Consolas,Menlo,monospace"
    sans = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
    parts = []
    a = parts.append
    # query
    a(f'<g {fade(2)}><rect x="30" y="20" width="900" height="44" rx="22" fill="{c["card"]}" stroke="{c["line"]}"/>'
      f'<text x="54" y="47" class="cap">QUERY</text>'
      f'<text x="118" y="48" class="t">Which drugs did <tspan class="m" style="fill:{c['h']}" font-weight="700">H:3</tspan> '
      f'receive across all sources?</text></g>')
    # source H
    a(f'<g {fade(6)}><rect x="30" y="86" width="300" height="86" rx="12" fill="{c["card"]}" stroke="{c["line"]}"/>'
      f'<rect x="30" y="98" width="4" height="62" rx="2" fill="{c["h"]}"/>'
      f'<text x="50" y="111" class="cap">HOSPITAL · SOURCE H</text>'
      f'<rect x="46" y="124" width="268" height="32" rx="7" fill="{c["row"]}"/>'
      f'<text x="60" y="145" class="m b" style="fill:{c['h']}">H:3</text><text x="98" y="145" class="t">received Insulin, 20</text></g>')
    # source P
    a(f'<g {fade(9)}><rect x="30" y="188" width="300" height="128" rx="12" fill="{c["card"]}" stroke="{c["line"]}"/>'
      f'<rect x="30" y="200" width="4" height="104" rx="2" fill="{c["p"]}"/>'
      f'<text x="50" y="213" class="cap">PHARMACY · SOURCE P</text>'
      f'<rect x="46" y="226" width="268" height="32" rx="7" fill="{c["row"]}"/>'
      f'<text x="60" y="247" class="m b" style="fill:{c['p']}">P:1</text><text x="98" y="247" class="t">received Aspirin, 100</text>'
      f'<rect x="46" y="266" width="268" height="32" rx="7" fill="{c["row"]}"/>'
      f'<text x="60" y="287" class="m b" style="fill:{c['p']}">P:1</text><text x="98" y="287" class="t">received Insulin, 15</text></g>')
    # ER link
    for d, s in [("M314,140 C346,140 340,202 372,202", 36), ("M372,202 C340,202 346,242 314,242", 46),
                 ("M372,202 C336,202 346,282 314,282", 48)]:
        a(f'<path d="{d}" pathLength="100" stroke-dasharray="100" fill="none" stroke="{c["er"]}" stroke-width="2.5" '
          f'stroke-linecap="round" {draw(s)}/>')
    a(f'<g {fade(43)}><rect x="372" y="188" width="100" height="28" rx="14" fill="{c["er"]}"/>'
      f'<text x="422" y="207" text-anchor="middle" class="m b" style="fill:{c["onbadge"]}">GID HP3</text></g>')
    a(f'<g {fade(52)}><text x="428" y="176" text-anchor="middle" class="cap" style="fill:{c["er"]}">ENTITY RESOLUTION</text>'
      f'<text x="422" y="236" text-anchor="middle" class="s">same person</text></g>')
    # lanes
    for y, title, start in [(86, "WITHOUT LINKAGE · BASE+seed, k = 4", 14), (210, "WITH ER · ER+seed, k = 4", 16)]:
        slots = "".join(f'<rect x="{538 + i * 66}" y="{y + 36}" width="58" height="30" rx="7" fill="none" '
                        f'stroke="{c["slot"]}" stroke-dasharray="4 3"/>' for i in range(4))
        a(f'<g {fade(start)}><rect x="520" y="{y}" width="410" height="106" rx="12" fill="{c["card"]}" '
          f'stroke="{c["line"]}"/><text x="538" y="{y + 24}" class="cap">{title}</text>{slots}</g>')

    def chip(x, y, label, col, s):
        a(f'<g {fade(s)}><rect x="{x}" y="{y}" width="58" height="30" rx="7" fill="{col}"/>'
          f'<text x="{x + 29}" y="{y + 20}" text-anchor="middle" class="m b" style="fill:{c["onbadge"]}">{label}</text></g>')

    chip(538, 122, "H:3", c["h"], 20)
    a(f'<g {fade(26)}><text x="538" y="176" class="t">→ <tspan font-weight="700">Insulin</tspan></text>'
      f'<text x="912" y="176" text-anchor="end" class="t b" style="fill:{c["bad"]}">✗ incomplete</text></g>')
    for i, (lab, col) in enumerate([("H:3", c["h"]), ("P:1", c["p"]), ("P:1", c["p"])]):
        chip(538 + i * 66, 246, lab, col, 58 + i * 3)
    a(f'<g {fade(70)}><text x="538" y="300" class="t">→ <tspan font-weight="700">Insulin, Aspirin</tspan></text>'
      f'<text x="912" y="300" text-anchor="end" class="t b" style="fill:{c["er"]}">✓ complete</text></g>')

    kf = []
    for (kind, s) in STARTS:
        if kind == "f":
            kf.append(f"@keyframes f{s}{{0%,{s}%{{opacity:0;transform:translateY(6px)}}"
                      f"{s + 4}%,93%{{opacity:1;transform:none}}98%,100%{{opacity:0;transform:none}}}}")
        else:
            kf.append(f"@keyframes d{s}{{0%,{s}%{{stroke-dashoffset:100;opacity:1}}"
                      f"{s + 7}%,93%{{stroke-dashoffset:0;opacity:1}}98%,100%{{stroke-dashoffset:0;opacity:0}}}}")
    style = (f"text{{font-family:{sans}}}.t{{font-size:15px;fill:{c['ink']}}}.s{{font-size:13px;fill:{c['muted']}}}"
             f".cap{{font-size:11px;letter-spacing:.08em;font-weight:600;fill:{c['muted']}}}"
             f".m{{font-family:{mono};font-size:14px}}.b{{font-weight:700}}"
             f"g,path{{transform-box:fill-box}}" + "".join(kf))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 340" width="960" height="340" role="img" '
            f'aria-label="Entity Resolution links H:3 and P:1 to the same person, so the retrieved context holds '
            f'evidence from both sources and the answer becomes complete">'
            f'<style>{style}</style><rect width="960" height="340" rx="16" fill="{c["bg"]}"/>' + "".join(parts) + "</svg>")


for name, c in THEMES.items():
    STARTS.clear()
    (OUT / f"hero-{name}.svg").write_text(body(c), encoding="utf-8")
print("ok")
