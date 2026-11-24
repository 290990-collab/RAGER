"""Generates the animated README banner: python assets/make_hero.py assets -> hero-light.svg, hero-dark.svg."""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(exist_ok=True)

THEMES = {
    "light": dict(bg="#fcfcfb", card="#ffffff", line="#e2e1db", row="#f4f3ef", ink="#0b0b0b", muted="#6b6a66",
                  h="#2a78d6", p="#eb6834", er="#14966a", bad="#c43d2f", on="#ffffff"),
    "dark": dict(bg="#0d1117", card="#161b22", line="#30363d", row="#1f2630", ink="#e6edf3", muted="#8b949e",
                 h="#5a9cf0", p="#f08a5d", er="#2fc08d", bad="#f0776a", on="#0d1117"),
}
DUR = 11
MONO = "ui-monospace,SFMono-Regular,Consolas,Menlo,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


def build(c):
    starts = set()
    parts = []

    def fade(s):
        starts.add(("f", s))
        return f'style="animation:f{s} {DUR}s ease-out infinite both"'

    def draw(s):
        starts.add(("d", s))
        return f'style="animation:d{s} {DUR}s ease-in-out infinite both"'

    def rid(x, y, txt, col):
        return f'<text x="{x}" y="{y}" class="m b" style="fill:{col}">{txt}</text>'

    a = parts.append
    # question
    a(f'<g {fade(2)}><rect x="30" y="20" width="900" height="48" rx="24" fill="{c["card"]}" stroke="{c["line"]}"/>'
      f'<circle cx="58" cy="42" r="7" fill="none" stroke="{c["muted"]}" stroke-width="2"/>'
      f'<path d="M63,47 L69,53" stroke="{c["muted"]}" stroke-width="2" stroke-linecap="round"/>'
      f'<text x="82" y="50" class="q">Which drugs did patient <tspan class="m b" style="fill:{c["h"]}">H:3</tspan>'
      f' receive?</text></g>')
    # hospital
    a(f'<g {fade(6)}><rect x="30" y="90" width="300" height="84" rx="12" fill="{c["card"]}" stroke="{c["line"]}"/>'
      f'<rect x="30" y="102" width="4" height="60" rx="2" fill="{c["h"]}"/>'
      f'<text x="50" y="116" class="h">Hospital</text>'
      f'<rect x="46" y="128" width="268" height="32" rx="7" fill="{c["row"]}"/>'
      + rid(60, 149, "H:3", c["h"]) + '<text x="104" y="149" class="t">Insulin</text></g>')
    # pharmacy
    a(f'<g {fade(9)}><rect x="30" y="190" width="300" height="124" rx="12" fill="{c["card"]}" stroke="{c["line"]}"/>'
      f'<rect x="30" y="202" width="4" height="100" rx="2" fill="{c["p"]}"/>'
      f'<text x="50" y="216" class="h">Pharmacy</text>'
      f'<rect x="46" y="228" width="268" height="32" rx="7" fill="{c["row"]}"/>'
      + rid(60, 249, "P:1", c["p"]) + '<text x="104" y="249" class="t">Aspirin</text>'
      f'<rect x="46" y="268" width="268" height="32" rx="7" fill="{c["row"]}"/>'
      + rid(60, 289, "P:1", c["p"]) + '<text x="104" y="289" class="t">Insulin</text></g>')
    # the link
    for d, s in [("M314,144 C346,144 340,206 372,206", 36), ("M372,206 C340,206 346,244 314,244", 45),
                 ("M372,206 C336,206 346,284 314,284", 47)]:
        a(f'<path d="{d}" pathLength="100" stroke-dasharray="100" fill="none" stroke="{c["er"]}" stroke-width="2.5" '
          f'stroke-linecap="round" {draw(s)}/>')
    a(f'<g {fade(42)}><rect x="372" y="190" width="112" height="32" rx="16" fill="{c["er"]}"/>'
      f'<text x="428" y="211" text-anchor="middle" class="m b" style="fill:{c["on"]}">H:3 = P:1</text></g>')

    # answers
    def chip(x, y, lid, drug, col, s):
        a(f'<g {fade(s)}><rect x="{x}" y="{y}" width="116" height="32" rx="7" fill="{c["row"]}" stroke="{col}" '
          f'stroke-width="1.5"/>' + rid(x + 12, y + 21, lid, col)
          + f'<text x="{x + 50}" y="{y + 21}" class="t">{drug}</text></g>')

    for y, title, s in [(90, "Without Entity Resolution", 14), (210, "With Entity Resolution", 54)]:
        a(f'<g {fade(s)}><rect x="520" y="{y}" width="410" height="104" rx="12" fill="{c["card"]}" '
          f'stroke="{c["line"]}"/><text x="538" y="{y + 26}" class="h">{title}</text></g>')
    chip(538, 128, "H:3", "Insulin", c["h"], 20)
    a(f'<g {fade(26)}><text x="538" y="182" class="t">Answer: <tspan class="b">Insulin</tspan></text>'
      f'<text x="912" y="182" text-anchor="end" class="t b" style="fill:{c["bad"]}">✗ Aspirin missing</text></g>')
    for i, (lid, drug, col) in enumerate([("H:3", "Insulin", c["h"]), ("P:1", "Aspirin", c["p"]),
                                          ("P:1", "Insulin", c["p"])]):
        chip(538 + i * 126, 248, lid, drug, col, 58 + i * 3)
    a(f'<g {fade(70)}><text x="538" y="302" class="t">Answer: <tspan class="b">Insulin, Aspirin</tspan></text>'
      f'<text x="912" y="302" text-anchor="end" class="t b" style="fill:{c["er"]}">✓ complete</text></g>')

    kf = []
    for kind, s in sorted(starts):
        if kind == "f":
            kf.append(f"@keyframes f{s}{{0%,{s}%{{opacity:0;transform:translateY(6px)}}"
                      f"{s + 4}%,93%{{opacity:1;transform:none}}98%,100%{{opacity:0;transform:none}}}}")
        else:   # hidden until it starts drawing, so the round caps do not show as dots
            kf.append(f"@keyframes d{s}{{0%,{s}%{{stroke-dashoffset:100;opacity:0}}{s + 0.5}%{{opacity:1}}"
                      f"{s + 7}%,93%{{stroke-dashoffset:0;opacity:1}}98%,100%{{stroke-dashoffset:0;opacity:0}}}}")
    style = (f"text{{font-family:{SANS}}}.t{{font-size:15px;fill:{c['ink']}}}.q{{font-size:17px;fill:{c['ink']}}}"
             f".h{{font-size:14px;font-weight:600;fill:{c['muted']}}}.m{{font-family:{MONO};font-size:14px}}"
             f".b{{font-weight:700}}g,path{{transform-box:fill-box}}" + "".join(kf))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 336" width="960" height="336" role="img" '
            f'aria-label="The hospital knows the patient as H:3, the pharmacy as P:1. Without Entity Resolution the '
            f'answer misses Aspirin; with it, both records are found and the answer is complete.">'
            f'<style>{style}</style><rect width="960" height="336" rx="16" fill="{c["bg"]}"/>'
            + "".join(parts) + "</svg>")


for name, c in THEMES.items():
    (OUT / f"hero-{name}.svg").write_text(build(c), encoding="utf-8")
print("ok")
