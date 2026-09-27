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


def svg(body, height=360, width=1000):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
      <linearGradient id="accent" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="0"><stop stop-color="#22d3ee"/><stop offset=".5" stop-color="#a78bfa"/><stop offset="1" stop-color="#f472b6"/></linearGradient>
      <radialGradient id="glow"><stop stop-color="#7c3aed" stop-opacity=".45"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>
      <radialGradient id="cyan-glow"><stop stop-color="#22d3ee" stop-opacity=".22"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></radialGradient>
      <clipPath id="bounds"><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="18"/></clipPath>
    </defs>
    <rect width="{width}" height="{height}" rx="18" fill="#0c1020"/>
    <g clip-path="url(#bounds)">
    <g font-family="DejaVu Sans, Arial, sans-serif">{body}</g></g></svg>'''


def spark(x, y, color, opacity=1, radius=3):
    return f'''<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius*3}" fill="{color}" opacity="{opacity*.13:.3f}"/>
      <circle cx="{x:.2f}" cy="{y:.2f}" r="{radius}" fill="{color}" opacity="{opacity:.3f}"/>'''


def banner(phase=0, still=False):
    angle = phase * math.tau
    particles = ''.join(
        spark(x+5*math.sin(angle+i),y+4*math.cos(angle+i),color,
              .25+.2*math.sin(angle+i)**2,radius)
        for i,(x,y,color,radius) in enumerate([
            (618,69,PURPLE,1.4),(964,231,CYAN,1.5),(686,302,PINK,1.4),
            (915,57,PURPLE,1.6),(573,306,CYAN,1.2),
        ])
    )
    orbit = spark(808+139*math.cos(angle-.7),173+112*math.sin(angle-.7),CYAN,.75,3)
    typed = "'useful'" if still else "'useful'"[:min(8,int(phase*40)+1)]
    cursor_opacity = 1 if still or int(phase*12)%2==0 else .25
    float_y = 2*math.sin(angle)
    chips = ''
    for i,(x,w,label,bg,color) in enumerate([(52,80,'Build','#12303b',CYAN),(143,82,'Teach','#26203d',PURPLE),(236,94,'Explore','#302034',PINK)]):
        chips += f'''<rect x="{x}" y="274" width="{w}" height="32" rx="16" fill="{bg}"/>
          <text x="{x+w/2}" y="295" text-anchor="middle" fill="{color}" font-size="14">{label}</text>'''
    return svg(f'''
      <circle cx="804" cy="166" r="245" fill="url(#glow)" opacity=".75"/>
      <circle cx="120" cy="360" r="240" fill="url(#cyan-glow)" opacity=".32"/>
      {particles}
      <text x="52" y="67" fill="#9ba7c1" font-size="15">oninsan · Cebu, Philippines</text>
      <text x="48" y="148" fill="#f5f7ff" font-size="70" font-weight="700" letter-spacing="-2">Niño Abao<tspan fill="{CYAN}">.</tspan></text>
      <text x="52" y="191" fill="{PURPLE}" font-size="22">Web developer / IT instructor</text>
      <text x="52" y="238" fill="#d8dfef" font-size="21">Build with purpose. Teach with clarity.</text>
      {chips}
      {orbit}
      <g transform="translate(0 {float_y:.2f})">
      <rect x="666" y="101" width="286" height="175" rx="18" fill="#080c1c" opacity=".35"/>
      <rect x="666" y="93" width="286" height="175" rx="18" fill="#171a2f"/>
      <rect x="666" y="93" width="286" height="175" rx="18" fill="url(#glow)" opacity=".13"/>
      <circle cx="689" cy="115" r="3.5" fill="#f472b6"/><circle cx="703" cy="115" r="3.5" fill="#a78bfa"/><circle cx="717" cy="115" r="3.5" fill="#22d3ee"/>
      <text x="757" y="119" fill="#8f9ab7" font-size="12">~/oninsan</text>
      <g font-family="DejaVu Sans Mono, monospace" font-size="17">
      <text x="688" y="158" fill="#a78bfa">const <tspan fill="#e4e8f7">mindset = {{</tspan></text>
      <text x="708" y="185" fill="#a4afc7">build: <tspan fill="{CYAN}">{typed}</tspan><tspan fill="#dce3f2">,</tspan></text>
      <rect x="{710+(8+len(typed))*10.24}" y="171" width="6" height="17" rx="1" fill="{CYAN}" opacity="{cursor_opacity}"/>
      <text x="708" y="212" fill="#a4afc7">learn: <tspan fill="{PINK}">'always'</tspan></text>
      <text x="688" y="239" fill="#e4e8f7">}};</text>
      </g></g>
      <text x="809" y="307" text-anchor="middle" fill="#a5aec7" font-size="14">Curious by default</text>
    ''')


def toolkit(phase=0, still=False):
    body = ''
    names = ['TypeScript', 'React', 'Svelte', 'Python', 'dotnet', 'Docker']
    colors = [CYAN, CYAN, '#f9a68c', '#f9d784', PURPLE, CYAN]
    categories = ['Language', 'Frontend', 'Frontend', 'Backend', 'Backend', 'Tooling']
    for i, (name, color) in enumerate(zip(names,colors)):
        x = 24 + i*161
        active = max(0, math.cos(math.tau*(phase-i/6)))**6
        y = 20 - active*3
        body += f'''<rect x="{x}" y="{y}" width="147" height="78" rx="12" fill="#161b30"/>
          <text x="{x+14}" y="{y+26}" fill="#9aa8c3" font-size="12">{categories[i]}</text>
          <text x="{x+14}" y="{y+57}" fill="#eef2ff" font-size="19" font-weight="600">{name}</text>
          {spark(x+124,y+22,color,.35+active*.65,2.5)}'''
    return svg(body,118)


def hobbies(phase=0, still=False):
    a = phase*math.tau
    strum = 3*math.sin(a*2)
    code_cursor = .4+.6*math.sin(a)**2
    ball_x, ball_y = 737+15*math.cos(a), 51-18*abs(math.sin(a))
    icons = [
        f'''<g transform="translate(43 32) rotate({-22+strum} 17 29)">
        <rect x="12" y="-9" width="10" height="13" rx="2"/><path d="M14 4V29M20 4V29"/>
        <path d="M17 29C10 22 2 26 6 34C9 40 2 40 1 48C0 59 9 65 17 65C25 65 34 59 33 48C32 40 25 40 28 34C32 26 24 22 17 29Z"/>
        <circle cx="17" cy="44" r="5"/><path d="M11 56H23M17-7V56" stroke-width="1.3"/></g>
        <path d="M83 34Q{87+strum} 46 83 58M90 29Q{96+strum} 46 90 63" opacity="{.35+.45*math.sin(a)**2:.2f}"/>''',
        f'''<path d="M380 35L367 48L380 61M410 35L423 48L410 61M402 30L390 66"/>
        <circle cx="384" cy="82" r="2" stroke="none" fill="{CYAN}" opacity="{code_cursor}"/>
        <circle cx="395" cy="82" r="2" stroke="none" fill="{CYAN}" opacity="{.4+.6*math.sin(a+.7)**2}"/>
        <circle cx="406" cy="82" r="2" stroke="none" fill="{CYAN}" opacity="{.4+.6*math.sin(a+1.4)**2}"/>''',
        f'''<g transform="translate(710 27) rotate({6*math.sin(a)} 18 40)"><ellipse cx="18" cy="18" rx="14" ry="18" transform="rotate(-25 18 18)"/><path d="M26 34L36 55"/></g>
        <circle cx="{ball_x}" cy="{ball_y}" r="5" fill="{PINK}"/>
        <ellipse cx="{ball_x}" cy="93" rx="{7-2*abs(math.sin(a))}" ry="1.5" fill="{PINK}" stroke="none" opacity=".2"/>''',
    ]
    body=''
    for i,(x,title,subtitle,color,icon) in enumerate(zip(
        [16,345,674],['Guitar','Coding','Paddle sports'],
        ['A little rhythm.','One more idea.','Time to play.'],[PURPLE,CYAN,PINK],icons,
    )):
        body+=f'''<rect x="{x}" y="16" width="310" height="103" rx="14" fill="#161b30"/>
          <g fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icon}</g>
          <text x="{x+96}" y="59" fill="#f0f3ff" font-size="21" font-weight="600">{title}</text>
          <text x="{x+96}" y="87" fill="#a6b0ca" font-size="16">{subtitle}</text>'''
    return svg(body,135)


def footer(phase=0, still=False):
    dots=''.join(spark(472+i*28,23,color,.3+.5*math.sin(phase*math.tau-i*.7)**2,2.5)
                 for i,color in enumerate([CYAN,PURPLE,PINK]))
    return svg(f'''{dots}<text x="500" y="60" text-anchor="middle" fill="#b3bed7" font-size="16">Build with purpose. Teach with clarity.</text>''',84)


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
    for name,factory,height in [('banner',banner,360),('toolkit',toolkit,118),
                               ('hobbies',hobbies,135),('footer',footer,84)]:
        render_animation(name,factory,height)
    for filename,label,width,color in [
        ('portfolio.svg','Portfolio',110,PURPLE),
        ('linkedin.svg','LinkedIn',110,CYAN),
        ('email.svg','Email me',110,PINK),
        ('projects.svg','Projects',110,PURPLE),
    ]:
        write(filename,f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="36" viewBox="0 0 {width} 36">
          <rect width="{width}" height="36" rx="10" fill="#171c30"/>
          <circle cx="16" cy="18" r="3" fill="{color}"/>
          <text x="{width/2+7}" y="22" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-weight="600" font-size="12" fill="#e8ecff">{label}</text>
        </svg>''')
