"""Draws the GitHub profile's SVGs in omxqua (Developer · Graphite · night): solid surfaces, one hairline, liquid motion.
Usage: python3 tools/gen.py tools/fonts assets   (fonts: Geist, subset to Latin, OFL)"""
import base64, sys
from pathlib import Path

FONTS, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
b64 = lambda p: base64.b64encode((FONTS / p).read_bytes()).decode()
FONT_CSS = (f"@font-face{{font-family:G;font-weight:100 900;src:url(data:font/woff2;base64,{b64('geist.woff2')}) format('woff2')}}"
            f"@font-face{{font-family:GM;font-weight:100 900;src:url(data:font/woff2;base64,{b64('geist-mono.woff2')}) format('woff2')}}")

BG, S1, S2, LINE, INK, INK2, INK3 = "#060607", "#0f0f11", "#18181b", "#ffffff17", "#ededef", "#a1a1aa", "#6b6b73"
SPRING = "cubic-bezier(.34,1.56,.64,1)"      # small things under the finger overshoot a touch
SETTLE = "cubic-bezier(.22,1,.36,1)"         # bigger things decelerate, no bounce
BASE_CSS = f"""
text{{font-family:G,system-ui,sans-serif;fill:{INK}}} .m{{font-family:GM,ui-monospace,monospace}}
.rise{{animation:rise .9s {SETTLE} both}} .pop{{animation:pop .7s {SPRING} both}}
@keyframes rise{{from{{transform:translateY(16px)}}to{{transform:none}}}}
@keyframes pop{{from{{transform:scale(.7)}}to{{transform:none}}}}
@keyframes drift{{to{{transform:translateX(-400px)}}}}
@keyframes bob{{50%{{transform:translateY(-6px)}}}}
@keyframes bubble{{0%{{opacity:0;transform:translateY(0)}}15%{{opacity:1}}80%{{opacity:.9}}100%{{opacity:0;transform:translateY(var(--h,-120px))}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""

ICONS = {
  "plorer": "<circle cx='12' cy='12' r='10'/><path d='m16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z'/>",
  "core": "<path d='M12 20a8 8 0 1 0 0-16 8 8 0 0 0 0 16Z'/><path d='M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z'/><path d='M12 2v2'/><path d='M12 22v-2'/><path d='m17 20.66-1-1.73'/><path d='M11 10.27 7 3.34'/><path d='m20.66 17-1.73-1'/><path d='m3.34 7 1.73 1'/><path d='M14 12h8'/><path d='M2 12h2'/><path d='m20.66 7-1.73 1'/><path d='m3.34 17 1.73-1'/><path d='m17 3.34-1 1.73'/><path d='m11 13.73-4 6.93'/>",
  "code": "<path d='m18 16 4-4-4-4'/><path d='m6 8-4 4 4 4'/><path d='m14.5 4-5 16'/>",
  "qua": "<circle cx='13.5' cy='6.5' r='1' fill='currentColor'/><circle cx='17.5' cy='10.5' r='1' fill='currentColor'/><circle cx='8.5' cy='7.5' r='1' fill='currentColor'/><circle cx='6.5' cy='12.5' r='1' fill='currentColor'/><path d='M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z'/>",
  "console": "<path d='M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z'/><path d='M20 3v4'/><path d='M22 5h-4'/><path d='M4 17v2'/><path d='M5 18H3'/>",
  "labs": "<path d='M10 2v7.527a2 2 0 0 1-.211.896L4.72 20.55a1 1 0 0 0 .9 1.45h12.76a1 1 0 0 0 .9-1.45l-5.069-10.127A2 2 0 0 1 14 9.527V2'/><path d='M8.5 2h7'/><path d='M7 16h10'/>",
  "layers": "<path d='M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z'/><path d='m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65'/><path d='m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65'/>",
  "note": "<path d='M13.4 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7.4'/><path d='M2 6h4'/><path d='M2 10h4'/><path d='M2 14h4'/><path d='M2 18h4'/><path d='M21.378 5.626a1 1 0 1 0-3.004-3.004l-5.01 5.012a2 2 0 0 0-.506.854l-.837 2.87a.5.5 0 0 0 .62.62l2.87-.837a2 2 0 0 0 .854-.506z'/>",
  "map": "<path d='M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z'/><path d='M15 5.764v15'/><path d='M9 3.236v15'/>",
  "house": "<path d='M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8'/><path d='M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/>",
}
COL = {"plorer": "#3ccf6e", "console": "#ff9f40", "core": "#4aa8ff", "code": "#ff5d6c", "qua": "#c084fc", "labs": INK}
ORDER = ["plorer", "console", "core", "code", "qua"]


def mark(icon, x, y, s, c, tint=True, cls=""):
    """A product's mark: its outline icon in its colour on a faint tile of the same colour (suite.css .pm)."""
    k = s / 24 * .62
    o = (s - 24 * k) / 2
    tile = (f"<rect width='{s}' height='{s}' rx='{s*.3:.1f}' fill='{c}' fill-opacity='{.12 if tint else .06}' stroke='{c}' stroke-opacity='{.55 if tint else .25}' stroke-width='1.5'/>")
    return (f"<g transform='translate({x} {y})'><g class='{cls}' style='transform-origin:{s/2}px {s/2}px'>{tile}"
            f"<g transform='translate({o:.2f} {o:.2f}) scale({k:.4f})' fill='none' stroke='{c}' color='{c}' stroke-width='1.9' stroke-linecap='round' stroke-linejoin='round'>{ICONS[icon]}</g></g></g>")


def wave(width, amp, period=400):
    """A seamless wave path twice as wide as needed, so sliding it one period left loops."""
    d, x = [f"M0 0"], 0
    while x < width + period * 2:
        d.append(f"q{period/4} {-amp} {period/2} 0 t{period/2} 0")
        x += period
    d.append(f"V600 H0 Z")
    return " ".join(d)


def svg(w, h, body, css="", title=""):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}' role='img' aria-label='{title}'>"
            f"<title>{title}</title><style>{FONT_CSS}{BASE_CSS}{css}</style>{body}</svg>")


def write(name, s):
    (OUT / name).write_text(s)
    print(f"{name}: {len(s)//1024} KB")


# ---------- the hero: omxlabs, filled with the five product colours like liquid in the flask ----------
def hero():
    W, H = 1280, 560
    stops = "".join(f"<stop offset='{i/10:.2f}' stop-color='{COL[ORDER[i%5]]}'/>" for i in range(11))
    css = f"""
    .wv{{animation:drift 7s linear infinite}} .wv2{{animation:drift 11s linear infinite reverse}}
    .fill{{animation:fill 2.4s {SPRING} .3s both}} .hue{{animation:hue 24s linear infinite}}
    @keyframes fill{{from{{transform:translateY(70px)}}to{{transform:none}}}}
    @keyframes hue{{to{{transform:translateX(-1400px)}}}}
    .b{{animation:bubble var(--t,3.2s) cubic-bezier(.3,.6,.4,1) var(--d) infinite;opacity:0}}
    .bob{{animation:bob 5s ease-in-out infinite}}
    """
    head_y = 318
    # bubbles rise through the liquid and out of the letters
    bubbles = "".join(
        f"<circle class='b' cx='{x}' cy='{head_y-30}' r='{r}' fill='{COL[ORDER[i%5]]}' style='--d:{d}s;--t:{t}s;--h:-{hh}px'/>"
        for i, (x, r, d, t, hh) in enumerate([(120, 4, .2, 3.4, 95), (215, 3, 1.4, 3, 80), (330, 5, 2.2, 3.8, 100), (430, 3, .8, 2.9, 85), (540, 4, 1.9, 3.5, 100), (600, 3, 2.9, 3.1, 70), (270, 2.5, 3.3, 2.7, 60)]))
    pills, x = [], 64
    names = {"plorer": "omxplorer", "console": "omxconsole", "core": "omxcore", "code": "omxcode", "qua": "omxqua"}
    for i, k in enumerate(ORDER):
        w = 52 + len(names[k]) * 9.6
        pills.append(f"<g class='pop' style='animation-delay:{1.4+i*.09:.2f}s;transform-origin:{x+w/2}px 478px'>"
                     f"<rect x='{x}' y='456' width='{w:.0f}' height='44' rx='22' fill='{S1}' stroke='{LINE}'/>"
                     f"{mark(k, x+8, 464, 28, COL[k])}<text x='{x+44}' y='484' font-size='16' font-weight='550'>{names[k]}</text></g>")
        x += w + 10
    body = f"""
    <defs>
      <linearGradient id='g' x1='0' x2='1400' gradientUnits='userSpaceOnUse' spreadMethod='repeat'>{stops}</linearGradient>
      <clipPath id='t'><text x='56' y='{head_y}' font-size='158' font-weight='800' letter-spacing='-8'>omxlabs</text></clipPath>
      <mask id='liq'><g class='fill'>
        <g transform='translate(0 {head_y-80})'><path class='wv2' d='{wave(1400, 14, 400)}' fill='#fff' fill-opacity='.45' transform='translate(0 -10)'/></g>
        <g transform='translate(0 {head_y-70})'><path class='wv' d='{wave(1400, 18, 400)}' fill='#fff'/></g>
      </g></mask>
    </defs>
    <rect width='{W}' height='{H}' rx='28' fill='{BG}'/><rect x='.5' y='.5' width='{W-1}' height='{H-1}' rx='27.5' fill='none' stroke='{LINE}'/>
    <g class='rise'>{mark('labs', 64, 52, 40, INK, cls='bob')}<text x='118' y='80' font-size='22' font-weight='700' letter-spacing='-.4'>omxlabs</text></g>
    <text class='m rise' x='{W-64}' y='78' font-size='14' text-anchor='end' style='fill:{INK2};animation-delay:.1s'>abhishek sreesaila · solo founder</text>
    <text class='m rise' x='64' y='150' font-size='14' letter-spacing='2.6' style='fill:{INK2};animation-delay:.15s'>EVERY KIND OF DATA · ONE GPU · BUILT FOR PEOPLE AND AGENTS</text>
    <g clip-path='url(#t)'>
      <rect width='{W}' height='{H}' fill='{S2}'/>
      <g mask='url(#liq)'><rect class='hue' width='4200' height='{H}' fill='url(#g)'/></g>
    </g>
    <text x='56' y='{head_y}' font-size='158' font-weight='800' letter-spacing='-8' style='fill:none;stroke:#fff;stroke-opacity:.12;stroke-width:1.2'>omxlabs</text>
    {bubbles}
    <g class='rise' style='animation-delay:.5s'>
      <text x='780' y='232' font-size='27' font-weight='600' letter-spacing='-.5'>The best personal AI agents,</text>
      <text x='780' y='268' font-size='27' font-weight='600' letter-spacing='-.5'>running locally on hardware</text>
      <text x='780' y='304' font-size='27' font-weight='600' letter-spacing='-.5' style='fill:{INK2}'>you already own.</text>
      <text class='m' x='780' y='346' font-size='14' style='fill:{INK3}'>Built in Mojo · styled with omxqua</text>
    </g>
    <line x1='64' x2='{W-64}' y1='416' y2='416' stroke='{LINE}'/>
    {''.join(pills)}
    <text class='m rise' x='{W-64}' y='484' font-size='14' text-anchor='end' style='fill:{INK2};animation-delay:2s'>two apps · three technologies →</text>
    """
    write("hero.svg", svg(W, H, body, css, "omxlabs: every kind of data, one GPU, built for people and agents"))


# ---------- a product card: its mark, its job, one line, one proof; a band of its colour sloshing along the bottom ----------
def card(k, name, role, lines, proof, proof_big=None, w=640, h=330, delay=0):
    c = COL[k]
    lite = "#" + "".join(f"{int(c[i:i+2], 16) + (255 - int(c[i:i+2], 16)) * 45 // 100:02x}" for i in (1, 3, 5))
    css = (f".wv{{animation:drift2 4.5s linear infinite}} .wv2{{animation:drift2 7s linear infinite reverse}} .hue{{animation:hue 9s linear infinite}}"
           f" .fill{{animation:fill 2s {SPRING} {delay+.3}s both}} .b{{animation:bubble var(--t,3s) cubic-bezier(.3,.6,.4,1) var(--d) infinite;opacity:0}}"
           f" @keyframes drift2{{to{{transform:translateX(-200px)}}}} @keyframes hue{{to{{transform:translateX(-400px)}}}} @keyframes fill{{from{{transform:translateY(12px)}}to{{transform:none}}}}")
    txt = "".join(f"<text x='36' y='{214+i*24}' font-size='17' style='fill:{INK2}'>{l}</text>" for i, l in enumerate(lines))
    big = (f"<text x='{w-36}' y='64' font-size='34' font-weight='800' letter-spacing='-1.2' text-anchor='end' style='fill:{c}'>{proof_big}</text>") if proof_big else ""
    ny, nm = 180, f"x='33' y='180' font-size='54' font-weight='800' letter-spacing='-2.6'"
    tw = len(name) * 30   # rough name width, to spread the bubbles over it
    bubbles = "".join(f"<circle class='b' cx='{36 + tw * f:.0f}' cy='{ny-4}' r='{r}' fill='{c}' style='--d:{d}s;--t:{t}s;--h:-{hh}px'/>"
                      for f, r, d, t, hh in [(.12, 2.5, delay+.6, 2.8, 34), (.38, 2, delay+1.7, 2.4, 28), (.62, 3, delay+1.1, 3.1, 36), (.86, 2, delay+2.3, 2.6, 26)])
    body = f"""
    <defs>
      <linearGradient id='g' x1='0' x2='400' gradientUnits='userSpaceOnUse' spreadMethod='repeat'><stop offset='0' stop-color='{c}'/><stop offset='.5' stop-color='{lite}'/><stop offset='1' stop-color='{c}'/></linearGradient>
      <clipPath id='t'><text {nm}>{name}</text></clipPath>
      <mask id='liq'><g class='fill'>
        <g transform='translate(0 {ny-20})'><path class='wv2' d='{wave(w, 5, 200)}' fill='#fff' fill-opacity='.45'/></g>
        <g transform='translate(0 {ny-15})'><path class='wv' d='{wave(w, 6, 200)}' fill='#fff'/></g>
      </g></mask>
    </defs>
    <rect width='{w}' height='{h}' rx='24' fill='{S1}'/>
    <rect x='.5' y='.5' width='{w-1}' height='{h-1}' rx='23.5' fill='none' stroke='{LINE}'/>
    <g class='pop' style='animation-delay:{delay}s;transform-origin:62px 62px'>{mark(k, 36, 36, 52, c)}</g>
    {big}
    <g class='rise' style='animation-delay:{delay+.1}s'>
      <text class='m' x='36' y='124' font-size='12.5' letter-spacing='2' style='fill:{c}'>{role.upper()}</text>
      <g clip-path='url(#t)'><rect width='{w}' height='{h}' fill='{S2}'/><g mask='url(#liq)'><rect class='hue' width='{w+800}' height='{h}' fill='url(#g)'/></g></g>
      <text {nm} style='fill:none;stroke:#fff;stroke-opacity:.14;stroke-width:1'>{name}</text>
      {bubbles}
      {txt}
    </g>
    <text class='m rise' x='36' y='{h-36}' font-size='13' style='fill:{INK};animation-delay:{delay+.2}s'>{proof}</text>
    """
    write(f"{name}.svg", svg(w, h, body, css, f"{name}: {role}"))


# ---------- the second seat: the same card, quieter (no colour, no liquid) ----------
def side(icon, name, tag, line, w=640, h=132):
    body = f"""
    <rect width='{w}' height='{h}' rx='20' fill='{S1}'/><rect x='.5' y='.5' width='{w-1}' height='{h-1}' rx='19.5' fill='none' stroke='{LINE}'/>
    <g class='rise'>{mark(icon, 28, 28, 40, INK2, tint=False)}
      <text x='84' y='56' font-size='24' font-weight='700' letter-spacing='-.6'>{name}</text>
      <text class='m' x='{w-28}' y='54' font-size='12' letter-spacing='1.6' text-anchor='end' style='fill:{INK3}'>{tag.upper()}</text>
      <text x='28' y='104' font-size='16' style='fill:{INK2}'>{line}</text></g>
    """
    write(f"{name.lower()}.svg", svg(w, h, body, "", f"{name}: {line}"))


# ---------- a section label, transparent so it reads on GitHub light and dark ----------
def label(file, num, text, sub):
    body = (f"<text class='m' x='4' y='30' font-size='13' letter-spacing='2.4' style='fill:#8b8b93'>{num}  ·  {text.upper()}</text>"
            f"<text x='4' y='62' font-size='15' style='fill:#8b8b93'>{sub}</text>")
    write(file, svg(1280, 76, body, "", text))


hero()
card("plorer", "omxplorer", "app · data", ["Ask your data in a sentence: sheets, charts, video", "and documents on one GPU. Every button is a tool", "an agent can call."], "100M rows · a filter to pixels in 30 ms", "30 ms", delay=0)
card("console", "omxconsole", "app · local AI", ["One command turns your GPU into a private,", "OpenAI-compatible model server: the AI", "supplier for every app."], "any model · one endpoint · Mojo + MAX", "1 cmd", delay=.1)
card("core", "omxcore", "the engine", ["SQL on your CPU and your GPU,", "over the files you already have.", "NVIDIA, AMD and Apple Silicon."], "22 TPC-H queries, SF10 · DuckDB 5.08 s", "3.15 s", w=420, h=328, delay=.2)
card("code", "omxcode", "the framework", ["Write an app once in Mojo: native", "on Linux, the web and the Mac,", "and an agent can drive it."], "Linux · Web · Mac · phones next", None, w=420, h=328, delay=.3)
card("qua", "omxqua", "the look", ["Google's solid surfaces, Apple's", "springs, touch first. The look of", "every app here, this page too."], "MIT · phone and web", None, w=420, h=328, delay=.4)
side("layers", "fh-saas", "the SaaS core · Python", "FastHTML for SaaS apps. Login, billing and tenants in plain Python.")
side("note", "PersonalNote", "Python · FastHTML", "A personal notebook with a modern interface and real mind maps.")
side("map", "GitAway", "Python · FastHTML", "Plan a trip, share it, let friends fork it.")
side("house", "Abode", "TypeScript", "One home for all your coding agents, with local voice.")
label("label-apps.svg", "01", "The apps", "What you open. Both run on the GPU you already own.")
label("label-tech.svg", "02", "Under the hood", "Three technologies, all in Mojo, each usable on its own.")
label("label-also.svg", "03", "Also building", "Python and TypeScript, for the web.")
