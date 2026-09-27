"""Rebuild profile artwork with Python, Pillow, and rsvg-convert.

Run from any directory: python3 scripts/build_assets.py
Artwork is self-contained; no remote image or stats services are required.
"""

from pathlib import Path
from io import BytesIO
import math
import subprocess
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)


def svg(body, height=360, width=1000):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
      <linearGradient id="accent" x1="0" y1="1" x2="1" y2="0"><stop stop-color="#22d3ee"/><stop offset=".5" stop-color="#a78bfa"/><stop offset="1" stop-color="#f472b6"/></linearGradient>
      <radialGradient id="glow"><stop stop-color="#7c3aed" stop-opacity=".32"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>
      <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" stroke="#b6b6ff" stroke-opacity=".045" fill="none"/></pattern>
    </defs>
    <rect width="{width}" height="{height}" rx="18" fill="#0c1020"/>
    <rect width="{width}" height="{height}" rx="18" fill="url(#grid)"/>
    <g font-family="DejaVu Sans, Arial, sans-serif">{body}</g>
    </svg>'''


def banner(phase=0):
    angle = phase * math.tau - .7
    x, y = 810 + 119 * math.cos(angle), 173 + 119 * math.sin(angle)
    return svg(f'''
      <circle cx="795" cy="170" r="235" fill="url(#glow)"/>
      <path d="M40 35H960" stroke="url(#accent)" stroke-width="2"/>
      <text x="48" y="73" fill="#a5aeca" font-size="13" letter-spacing="3">ONINSAN / CEBU, PHILIPPINES</text>
      <text x="44" y="156" fill="#f5f7ff" font-size="66" font-weight="700" letter-spacing="-2">Niño Abao<tspan fill="#22d3ee">.</tspan></text>
      <text x="48" y="198" fill="#c5b4ff" font-size="19" letter-spacing="1">WEB DEVELOPER / IT INSTRUCTOR</text>
      <text x="48" y="246" fill="#d8dfef" font-size="22">Build with purpose. Teach with clarity.</text>
      <rect x="48" y="278" width="78" height="29" rx="14" fill="#123442" stroke="#255663"/>
      <text x="87" y="297" text-anchor="middle" fill="#7ee7f7" font-size="12" font-weight="700">BUILD</text>
      <rect x="135" y="278" width="80" height="29" rx="14" fill="#262044" stroke="#403467"/>
      <text x="175" y="297" text-anchor="middle" fill="#c7b7ff" font-size="12" font-weight="700">TEACH</text>
      <rect x="224" y="278" width="91" height="29" rx="14" fill="#342039" stroke="#62344d"/>
      <text x="269" y="297" text-anchor="middle" fill="#f5afd4" font-size="12" font-weight="700">EXPLORE</text>
      <circle cx="810" cy="173" r="119" fill="none" stroke="#8374bd" stroke-opacity=".25"/>
      <circle cx="810" cy="173" r="95" fill="none" stroke="#a78bfa" stroke-opacity=".20" stroke-dasharray="3 9"/>
      <circle cx="{x:.2f}" cy="{y:.2f}" r="12" fill="#22d3ee" opacity=".12"/>
      <circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="#67e8f9"/>
      <rect x="684" y="108" width="252" height="145" rx="13" fill="#15192d" stroke="#4c426d"/>
      <path d="M684 139H936" stroke="#36344f"/>
      <circle cx="701" cy="124" r="3.5" fill="#f472b6"/><circle cx="714" cy="124" r="3.5" fill="#a78bfa"/><circle cx="727" cy="124" r="3.5" fill="#22d3ee"/>
      <g font-family="DejaVu Sans Mono, monospace" font-size="15">
      <text x="703" y="173" fill="#a78bfa">const <tspan fill="#e4e8f7">mindset = {{</tspan></text>
      <text x="717" y="198" fill="#9caac4">  build: <tspan fill="#67e8f9">'useful',</tspan></text>
      <text x="717" y="222" fill="#9caac4">  learn: <tspan fill="#f5afd4">'always'</tspan></text>
      <text x="703" y="243" fill="#e4e8f7">}};</text>
      </g>
      <text x="810" y="319" text-anchor="middle" fill="#8d96b1" font-size="12" letter-spacing="2">CURIOUS BY DEFAULT</text>
    ''')


def write(name, content):
    (ASSETS / name).write_text(content, encoding="utf-8")


write("banner.svg", banner())
frames = []
for i in range(36):
    png = subprocess.run(
        ["rsvg-convert", "--width", "1000", "--height", "360"],
        input=banner(i / 36).encode(), capture_output=True, check=True,
    ).stdout
    frames.append(Image.open(BytesIO(png)).convert("RGB"))
palette = frames[0].quantize(colors=128)
frames = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
frames[0].save(ASSETS / "banner.gif", save_all=True, append_images=frames[1:],
               duration=100, loop=0, optimize=True, disposal=1)

for filename, label, width, color in [
    ("portfolio.svg", "PORTFOLIO SOURCE", 186, "#a78bfa"),
    ("linkedin.svg", "LINKEDIN", 118, "#67e8f9"),
    ("email.svg", "EMAIL ME", 118, "#f5afd4"),
    ("projects.svg", "REPOSITORIES", 155, "#a78bfa"),
]:
    write(filename, f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="36" viewBox="0 0 {width} 36">
      <rect x=".5" y=".5" width="{width - 1}" height="35" rx="8" fill="#15192d" stroke="#454261"/>
      <circle cx="17" cy="18" r="3" fill="{color}"/>
      <text x="{width / 2 + 7}" y="22" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-weight="600" font-size="11" letter-spacing=".8" fill="#e8ecff">{label}</text>
    </svg>''')

toolkit = ''
for x, name, color, number in [
    (24, "TypeScript", "#67e8f9", "01"), (185, "React", "#67e8f9", "02"),
    (346, "Svelte", "#f9a68c", "03"), (507, "Python", "#f9d784", "04"),
    (668, ".NET", "#c5b4ff", "05"), (829, "Docker", "#67e8f9", "06"),
]:
    toolkit += f'''<rect x="{x}" y="20" width="147" height="72" rx="10" fill="#161b30" stroke="#343c55"/>
      <text x="{x + 14}" y="43" fill="{color}" font-size="11" letter-spacing="2">{number} /</text>
      <text x="{x + 14}" y="73" fill="#eef2ff" font-size="19" font-weight="600">{name}</text>'''
write("toolkit.svg", svg(toolkit, 112))

icons = [
    '<g transform="translate(42 40) rotate(-25 17 20)"><ellipse cx="17" cy="29" rx="13" ry="14"/><ellipse cx="17" cy="17" rx="10" ry="9"/><path d="M14 14V-5H20V14M14-5V-14H20V-5"/><circle cx="17" cy="23" r="3"/><path d="M17-5V34"/></g>',
    '<path d="M380 35L367 48L380 61M410 35L423 48L410 61M402 30L390 66"/>',
    '<g transform="translate(710 27)"><ellipse cx="18" cy="18" rx="14" ry="18" transform="rotate(-25 18 18)"/><path d="M26 34L36 55"/><circle cx="58" cy="14" r="6"/></g>',
]
hobbies = ''
for x, title, subtitle, color, icon in zip(
    [16, 345, 674], ["Guitar", "Coding", "Paddle sports"],
    ["A little rhythm.", "One more idea.", "Time to play."],
    ["#c5b4ff", "#67e8f9", "#f5afd4"], icons,
):
    hobbies += f'''<rect x="{x}" y="16" width="310" height="103" rx="12" fill="#161b30" stroke="#363b55"/>
      <g fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icon}</g>
      <text x="{x + 92}" y="59" fill="#f0f3ff" font-size="21" font-weight="600">{title}</text>
      <text x="{x + 92}" y="87" fill="#a6b0ca" font-size="16">{subtitle}</text>'''
write("hobbies.svg", svg(hobbies, 135))
write("footer.svg", svg('''<path d="M26 20H974" stroke="url(#accent)"/>
  <text x="500" y="50" text-anchor="middle" fill="#a5b0cb" font-size="12" letter-spacing="2">BUILD WITH PURPOSE. TEACH WITH CLARITY.</text>''', 72))
print(f"Built 8 SVG assets and banner.gif ({(ASSETS / 'banner.gif').stat().st_size:,} bytes)")
