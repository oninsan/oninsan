"""Build profile artwork with Python, Pillow, and rsvg-convert.

Run: python3 scripts/build_assets.py
Each GIF has a matching static SVG for readers who prefer reduced motion.
"""
from pathlib import Path
from io import BytesIO
import math
import subprocess
from PIL import Image

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
ASSETS.mkdir(exist_ok=True)
CYAN, PURPLE, PINK = '#67e8f9', '#c5b4ff', '#f5afd4'


def svg(body, height=380, width=1000):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
      <linearGradient id="accent" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="0"><stop stop-color="#22d3ee"/><stop offset=".5" stop-color="#a78bfa"/><stop offset="1" stop-color="#f472b6"/></linearGradient>
      <radialGradient id="glow"><stop stop-color="#7c3aed" stop-opacity=".45"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>
      <radialGradient id="cyan-glow"><stop stop-color="#22d3ee" stop-opacity=".22"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></radialGradient>
      <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" stroke="#b6b6ff" stroke-opacity=".045" fill="none"/></pattern>
      <clipPath id="bounds"><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="18"/></clipPath>
    </defs>
    <rect width="{width}" height="{height}" rx="18" fill="#0c1020"/>
    <g clip-path="url(#bounds)"><rect width="{width}" height="{height}" fill="url(#grid)"/>
    <g font-family="DejaVu Sans, Arial, sans-serif">{body}</g></g></svg>'''


def spark(x, y, color, opacity=1, radius=3):
    return f'''<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius*3}" fill="{color}" opacity="{opacity*.13:.3f}"/>
      <circle cx="{x:.2f}" cy="{y:.2f}" r="{radius}" fill="{color}" opacity="{opacity:.3f}"/>'''


def banner(phase=0, still=False):
    angle = phase * math.tau
    pulse = .6 + .4 * math.sin(angle)**2
    particles = ''
    for i in range(19):
        t = (phase + i / 19) % 1
        x = (i * 97 + 30 * math.sin(angle+i)) % 1000
        y = 380 - t * 380
        particles += spark(x, y, [CYAN, PURPLE, PINK][i % 3], .15+.2*math.sin(t*math.pi), 1.3)
    orbital = ''
    for i, color in enumerate([CYAN, PINK]):
        for tail in range(10):
            a = angle + i*math.pi - tail*.045
            x, y = 809+139*math.cos(a), 174+121*math.sin(a)
            orbital += spark(x, y, color, (1-tail/11)*.85, 3.5 if tail==0 else 1.8)
    typed = "'something useful'" if still else "'something useful'"[:min(18, int(phase*36)+1)]
    cursor = 716 + len(typed)*9.04
    cursor_opacity = 1 if still or int(phase*12) % 2 == 0 else .2
    chips = ''
    for i,(x,w,label,bg,color) in enumerate([(48,79,'Build','#123442',CYAN),(139,82,'Teach','#262044',PURPLE),(233,96,'Explore','#342039',PINK)]):
        chips += f'''<rect x="{x}" y="286" width="{w}" height="31" rx="15" fill="{bg}" stroke="{color}" stroke-opacity="{.35+.15*math.sin(angle+i):.2f}"/>
          <text x="{x+w/2}" y="307" text-anchor="middle" fill="{color}" font-size="14">{label}</text>'''
    wave = ''
    for i, color in enumerate([CYAN, PURPLE, PINK]):
        points = ' '.join(f'{x},{351+4*math.sin(x/65+angle+i*.9):.2f}' for x in range(42,959,8))
        wave += f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="1" opacity=".22"/>'
    return svg(f'''
      <circle cx="{770+25*math.sin(angle):.2f}" cy="170" r="255" fill="url(#glow)" opacity="{pulse:.2f}"/>
      <circle cx="{270+60*math.cos(angle):.2f}" cy="350" r="220" fill="url(#cyan-glow)"/>
      {particles}
      <rect x="1" y="1" width="998" height="378" rx="18" stroke="url(#accent)" stroke-opacity=".45" fill="none"/>
      <path d="M48 35H952" stroke="url(#accent)" stroke-width="2" opacity=".65"/>
      {spark(48+phase*904,35,CYAN,.85,3)}
      <text x="48" y="76" fill="#a5aeca" font-size="16">oninsan / Cebu, Philippines</text>
      <text x="44" y="158" fill="#f5f7ff" font-size="70" font-weight="700" letter-spacing="-2">Niño Abao<tspan fill="{CYAN}">.</tspan></text>
      <path d="M48 173H406" stroke="url(#accent)" stroke-width="2" opacity=".7"/>
      <text x="48" y="209" fill="{PURPLE}" font-size="22">Web developer / IT instructor</text>
      <text x="48" y="253" fill="#d8dfef" font-size="22">Build with purpose. Teach with clarity.</text>
      {chips}
      <ellipse cx="809" cy="174" rx="139" ry="121" fill="none" stroke="#a78bfa" stroke-opacity=".25"/>
      <ellipse cx="809" cy="174" rx="116" ry="98" fill="none" stroke="#a78bfa" stroke-opacity=".25" stroke-dasharray="3 9" stroke-dashoffset="{-phase*96}"/>
      <g transform="translate(0 {3*math.sin(angle):.2f})">
      <rect x="679" y="104" width="260" height="160" rx="13" fill="#15192d" stroke="url(#accent)" stroke-opacity=".75"/>
      <path d="M679 137H939" stroke="#36344f"/>
      <circle cx="696" cy="121" r="3.5" fill="#f472b6"/><circle cx="709" cy="121" r="3.5" fill="#a78bfa"/><circle cx="722" cy="121" r="3.5" fill="#22d3ee"/>
      <text x="749" y="125" fill="#8793b2" font-size="12">~/oninsan</text>
      <g font-family="DejaVu Sans Mono, monospace" font-size="15">
      <text x="698" y="169" fill="#a78bfa">build<tspan fill="#e4e8f7">(</tspan></text>
      <text x="716" y="195" fill="{CYAN}">{typed}</text>
      <rect x="{cursor}" y="183" width="7" height="16" fill="{CYAN}" opacity="{cursor_opacity}"/>
      <text x="698" y="221" fill="#e4e8f7">);</text>
      <text x="698" y="247" fill="#9caac4">// learn. teach. repeat.</text>
      </g></g>
      {orbital}
      <text x="809" y="312" text-anchor="middle" fill="#a5aec7" font-size="14">Curious by default</text>
      {wave}
    ''')


def toolkit(phase=0, still=False):
    body = ''
    names = ['TypeScript', 'React', 'Svelte', 'Python', 'dotnet', 'Docker']
    colors = [CYAN, CYAN, '#f9a68c', '#f9d784', PURPLE, CYAN]
    for i, (name, color) in enumerate(zip(names,colors)):
        x = 24 + i*161
        active = max(0, math.cos(math.tau*(phase-i/6)))**6
        y = 20 - active*3
        body += f'''<rect x="{x}" y="{y}" width="147" height="78" rx="10" fill="#161b30" stroke="{color}" stroke-opacity="{.15+active*.65:.2f}"/>
          <text x="{x+14}" y="{y+24}" fill="{color}" font-size="11">0{i+1} /</text>
          <text x="{x+14}" y="{y+53}" fill="#eef2ff" font-size="19" font-weight="600">{name}</text>
          <path d="M{x+14} {y+66}H{x+133}" stroke="{color}" stroke-opacity=".2" stroke-width="2"/>
          <path d="M{x+14} {y+66}H{x+14+119*active}" stroke="{color}" stroke-width="2"/>'''
        if name == 'React':
            body += f'<g transform="translate({x+123} {y+22}) rotate({phase*360})" fill="none" stroke="{CYAN}" stroke-width=".8" opacity=".7">'
            body += ''.join(f'<ellipse rx="10" ry="3.5" transform="rotate({a})"/>' for a in [0,60,120])+'</g>'
        elif name == 'Docker':
            body += f'<path d="M{x+103} {y+25}Q{x+110} {y+19+2*math.sin(phase*math.tau)} {x+119} {y+25}T{x+135} {y+25}" fill="none" stroke="{color}" opacity=".7"/>'
    return svg(body,118)


def hobbies(phase=0, still=False):
    a = phase*math.tau
    strum = 3*math.sin(a*2)
    code_cursor = .4+.6*math.sin(a)**2
    ball_x, ball_y = 756+26*math.cos(a), 55-19*abs(math.sin(a))
    icons = [
        f'''<g transform="translate(42 40) rotate({-25+strum} 17 20)"><ellipse cx="17" cy="29" rx="13" ry="14"/><ellipse cx="17" cy="17" rx="10" ry="9"/><path d="M14 14V-5H20V14M14-5V-14H20V-5"/><circle cx="17" cy="23" r="3"/><path d="M17-5V34"/></g>
        <path d="M83 34Q{87+strum} 46 83 58M90 29Q{96+strum} 46 90 63" opacity="{.35+.45*math.sin(a)**2:.2f}"/>''',
        f'''<path d="M380 35L367 48L380 61M410 35L423 48L410 61M402 30L390 66"/>
        <path d="M374 83H410" stroke-opacity=".3"/><path d="M374 83H{374+36*(.5+.5*math.sin(a))}"/>
        <rect x="416" y="76" width="4" height="13" stroke="none" fill="{CYAN}" opacity="{code_cursor}"/>''',
        f'''<g transform="translate(710 27) rotate({6*math.sin(a)} 18 40)"><ellipse cx="18" cy="18" rx="14" ry="18" transform="rotate(-25 18 18)"/><path d="M26 34L36 55"/></g>
        <circle cx="{ball_x}" cy="{ball_y}" r="5" fill="{PINK}"/>
        <ellipse cx="{ball_x}" cy="93" rx="{7-2*abs(math.sin(a))}" ry="1.5" fill="{PINK}" stroke="none" opacity=".2"/>''',
    ]
    body=''
    for i,(x,title,subtitle,color,icon) in enumerate(zip(
        [16,345,674],['Guitar','Coding','Paddle sports'],
        ['A little rhythm.','One more idea.','Time to play.'],[PURPLE,CYAN,PINK],icons,
    )):
        pulse=.2+.15*math.sin(a+i)**2
        body+=f'''<rect x="{x}" y="16" width="310" height="103" rx="12" fill="#161b30" stroke="{color}" stroke-opacity="{pulse}"/>
          <g fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icon}</g>
          <text x="{x+96}" y="59" fill="#f0f3ff" font-size="21" font-weight="600">{title}</text>
          <text x="{x+96}" y="87" fill="#a6b0ca" font-size="16">{subtitle}</text>'''
    return svg(body,135)


def footer(phase=0, still=False):
    wave=''
    for i,color in enumerate([CYAN,PURPLE,PINK]):
        points=' '.join(f'{x},{24+7*math.sin(x/90+phase*math.tau+i*.8):.2f}' for x in range(26,975,6))
        wave+=f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="1.3" opacity=".5"/>'
    return svg(f'''{wave}<text x="500" y="67" text-anchor="middle" fill="#b3bed7" font-size="16">Build with purpose. Teach with clarity.</text>''',91)


def write(name, content):
    (ASSETS/name).write_text(content,encoding='utf-8')


def render_animation(name, factory, height, count=48):
    write(f'{name}.svg',factory(0,still=True))
    frames=[]
    for i in range(count):
        png=subprocess.run(['rsvg-convert','--width','1000','--height',str(height)],
            input=factory(i/count).encode(),capture_output=True,check=True).stdout
        frames.append(Image.open(BytesIO(png)).convert('RGB'))
    # Sample several phases so every animated color is in the shared palette.
    samples=Image.new('RGB',(1000,height*4))
    for j,i in enumerate([0,count//4,count//2,count*3//4]):
        samples.paste(frames[i],(0,height*j))
    palette=samples.quantize(colors=256)
    indexed=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    indexed[0].save(ASSETS/f'{name}.gif',save_all=True,append_images=indexed[1:],
        duration=100,loop=0,optimize=True,disposal=1)
    print(f'{name}.gif: {(ASSETS/f"{name}.gif").stat().st_size:,} bytes',flush=True)


if __name__=='__main__':
    for name,factory,height in [('banner',banner,380),('toolkit',toolkit,118),
                               ('hobbies',hobbies,135),('footer',footer,91)]:
        render_animation(name,factory,height)
    for filename,label,width,color in [
        ('portfolio.svg','Portfolio source',159,PURPLE),
        ('linkedin.svg','LinkedIn',106,CYAN),
        ('email.svg','Email me',106,PINK),
        ('projects.svg','Repositories',136,PURPLE),
    ]:
        write(filename,f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="36" viewBox="0 0 {width} 36">
          <rect x=".5" y=".5" width="{width-1}" height="35" rx="8" fill="#15192d" stroke="#454261"/>
          <circle cx="16" cy="18" r="3" fill="{color}"/>
          <text x="{width/2+7}" y="22" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-weight="600" font-size="12" fill="#e8ecff">{label}</text>
        </svg>''')
