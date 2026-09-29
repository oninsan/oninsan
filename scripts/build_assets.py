"""Build profile artwork with Python, Pillow, and rsvg-convert.

Run: python3 scripts/build_assets.py
Each GIF has a matching static SVG for readers who prefer reduced motion.
Content hashes in filenames prevent GitHub from showing cached artwork.
"""
from pathlib import Path
from io import BytesIO
import math
import subprocess
import hashlib
import re
from PIL import Image

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
ASSETS.mkdir(exist_ok=True)
GREEN, MINT = '#62f6a9', '#b8fbd5'
MANIFEST = {}


def svg(body, height=400, width=1000):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
      <radialGradient id="glow"><stop stop-color="#20c878" stop-opacity=".18"/><stop offset="1" stop-color="#20c878" stop-opacity="0"/></radialGradient>
      <clipPath id="bounds"><rect width="{width}" height="{height}" rx="18"/></clipPath>
      <clipPath id="rain"><rect x="662" y="24" width="306" height="326" rx="16"/></clipPath>
    </defs>
    <rect width="{width}" height="{height}" rx="18" fill="#080f0d"/>
    <g clip-path="url(#bounds)" font-family="DejaVu Sans Mono, monospace">{body}</g></svg>'''


def spark(x, y, color, opacity=1, radius=3):
    return f'''<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius*3}" fill="{color}" opacity="{opacity*.12:.3f}"/>
      <circle cx="{x:.2f}" cy="{y:.2f}" r="{radius}" fill="{color}" opacity="{opacity:.3f}"/>'''


def banner(phase=0, still=False):
    angle=phase*math.tau
    rain=''
    for col in range(14):
        x=672+col*21
        offset=(phase*168+(col*43)%168)%168
        for row in range(24):
            y=22+row*24+offset-168
            char='01{}[];'[(col*7+row*3)%7]
            strength=.08+.12*((row+col)%7)/6
            rain+=f'<text x="{x}" y="{y:.2f}" fill="{GREEN}" font-size="12" opacity="{strength:.3f}">{char}</text>'
    typed='build useful things' if still else 'build useful things'[:min(19,int(phase*65)+1)]
    cursor=1 if still or int(phase*12)%2==0 else .15
    chips=''
    for x,w,label in [(52,78,'Web'),(142,100,'Mobile'),(254,122,'Teaching')]:
        chips+=f'''<rect x="{x}" y="337" width="{w}" height="31" rx="8" fill="#112a1d"/>
          <text x="{x+w/2}" y="358" text-anchor="middle" fill="{MINT}" font-size="14">{label}</text>'''
    return svg(f'''
      <circle cx="813" cy="186" r="236" fill="url(#glow)"/>
      <text x="52" y="64" fill="#829c8d" font-size="17">oninsan<tspan fill="#597165">@github:~$</tspan><tspan fill="{GREEN}"> whoami</tspan></text>
      <text x="47" y="148" fill="#effbf4" font-size="66" font-weight="700" letter-spacing="-3">Niño Abao<tspan fill="{GREEN}">.</tspan></text>
      <text x="52" y="190" fill="#c1d5c9" font-size="21">Web developer / IT instructor</text>
      <text x="52" y="242" fill="{GREEN}" font-size="21">&gt; {typed}</text>
      <rect x="{80+len(typed)*12.64}" y="225" width="9" height="21" rx="1" fill="{GREEN}" opacity="{cursor}"/>
      <text x="52" y="273" fill="#92ad9e" font-size="21">&gt; teach what I learn</text>
      <text x="52" y="310" fill="#799587" font-size="14">Bogo City, Cebu, Philippines</text>
      {chips}
      <g clip-path="url(#rain)">{rain}</g>
      <rect x="710" y="116" width="222" height="137" rx="16" fill="#0a1510" opacity=".9"/>
      <text x="822" y="211" text-anchor="middle" fill="{GREEN}" font-size="96" font-weight="700" letter-spacing="-7">{{n}}</text>
      <text x="822" y="285" text-anchor="middle" fill="#a3c6b1" font-size="15">curiosity.exe</text>
      {spark(917,53,GREEN,.4+.3*math.sin(angle)**2,3)}
      <text x="822" y="328" text-anchor="middle" fill="#557463" font-size="12">build · learn · repeat</text>
    ''')


def toolkit(phase=0, still=False):
    body=''
    files=['index.ts','app.tsx','page.svelte','main.py','api.cs','Dockerfile']
    names=['TypeScript','React','Svelte','Python','dotnet','Docker']
    ext=['.ts','.tsx','.svelte','.py','.cs','>_']
    for i,(filename,name,extension) in enumerate(zip(files,names,ext)):
        x=22+i*161
        active=max(0,math.cos(math.tau*(phase-i/6)))**6
        y=18-2*active
        body+=f'''<rect x="{x}" y="{y}" width="149" height="125" rx="12" fill="#101d16"/>
          <text x="{x+13}" y="{y+24}" fill="#6f9680" font-size="11">{filename}</text>
          <text x="{x+13}" y="{y+68}" fill="{GREEN}" font-size="{24 if extension=='.svelte' else 30}" font-weight="700">{extension}</text>
          <text x="{x+13}" y="{y+103}" fill="#d4e5db" font-size="16">{name}</text>
          {spark(x+126,y+21,GREEN,.2+.6*active,2)}'''
    return svg(body,160)


def hobbies(phase=0, still=False):
    angle=phase*math.tau
    strum=3*math.sin(angle*2)
    icons=[
        f'''<g transform="translate(43 62) rotate({-22+strum} 17 29)">
          <rect x="12" y="-9" width="10" height="13" rx="2"/><path d="M14 4V29M20 4V29"/>
          <path d="M17 29C10 22 2 26 6 34C9 40 2 40 1 48C0 59 9 65 17 65C25 65 34 59 33 48C32 40 25 40 28 34C32 26 24 22 17 29Z"/>
          <circle cx="17" cy="44" r="5"/><path d="M11 56H23M17-7V56" stroke-width="1.3"/></g>
          <path d="M83 64Q{87+strum} 76 83 88M90 59Q{96+strum} 76 90 93" opacity="{.35+.35*math.sin(angle)**2:.2f}"/>''',
        f'''<path d="M380 69L367 82L380 95M410 69L423 82L410 95M402 64L390 100"/>
          {''.join(f'<circle cx="{384+i*11}" cy="116" r="2" stroke="none" fill="{GREEN}" opacity="{.3+.6*math.sin(angle+i*.7)**2}"/>' for i in range(3))}''',
        f'''<g transform="translate(710 63) rotate({6*math.sin(angle)} 18 40)">
          <ellipse cx="18" cy="18" rx="14" ry="18" transform="rotate(-25 18 18)"/><path d="M26 34L36 55"/></g>
          <circle cx="{737+15*math.cos(angle)}" cy="{87-18*abs(math.sin(angle))}" r="4" fill="{GREEN}"/>
          <ellipse cx="{737+15*math.cos(angle)}" cy="129" rx="{7-2*abs(math.sin(angle))}" ry="1.5" fill="{GREEN}" stroke="none" opacity=".2"/>''',
    ]
    body=''
    for i,(x,title,filename,subtitle,icon) in enumerate(zip(
        [16,345,674],['Guitar','Coding','Paddle sports'],
        ['guitar.wav','sideproject.ts','paddle.match'],
        ['Find the rhythm.','Follow the curiosity.','Enjoy the game.'],icons,
    )):
        body+=f'''<rect x="{x}" y="16" width="310" height="157" rx="14" fill="#101d16"/>
          <text x="{x+20}" y="43" fill="#587b66" font-size="12">./{filename}</text>
          <g fill="none" stroke="{GREEN}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icon}</g>
          <text x="{x+100}" y="97" fill="#e5f4eb" font-size="{18 if i==2 else 22}" font-weight="600">{title}</text>
          <text x="{x+20}" y="153" fill="#92ad9e" font-size="15">{subtitle}</text>'''
    return svg(body,190)


def footer(phase=0, still=False):
    cursor=1 if still or int(phase*12)%2==0 else .2
    return svg(f'''
      <text x="500" y="43" text-anchor="middle" fill="#94b8a3" font-size="17">Keep building. Keep learning.</text>
      <text x="483" y="75" text-anchor="middle" fill="{GREEN}" font-size="13">oninsan@github:~$</text>
      <rect x="562" y="64" width="7" height="14" fill="{GREEN}" opacity="{cursor}"/>
    ''',100)


def save_asset(name, payload):
    original = Path(name)
    digest = hashlib.sha256(payload).hexdigest()[:10]
    path = ASSETS / f'{original.stem}-{digest}{original.suffix}'
    path.write_bytes(payload)
    MANIFEST[name] = f'assets/{path.name}'
    return path


def write(name, content):
    return save_asset(name,content.encode('utf-8'))


def update_readme_assets():
    readme = ASSETS.parent / 'README.md'
    pattern = r'assets/([a-z]+)(?:-[0-9a-f]{10})?\.(gif|svg)'
    updated = re.sub(pattern,lambda m: MANIFEST.get(f'{m[1]}.{m[2]}',m[0]),
                     readme.read_text(encoding='utf-8'))
    readme.write_text(updated,encoding='utf-8')
    keep = {Path(path).name for path in MANIFEST.values()}
    stems = '|'.join(sorted({Path(name).stem for name in MANIFEST}))
    generated = re.compile(rf'({stems})(?:-[0-9a-f]{{10}})?\.(gif|svg)')
    for path in ASSETS.iterdir():
        if path.is_file() and generated.fullmatch(path.name) and path.name not in keep:
            path.unlink()


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
    output = BytesIO()
    indexed[0].save(output,format='GIF',save_all=True,append_images=indexed[1:],
        duration=100,loop=0,optimize=True,disposal=1)
    path = save_asset(f'{name}.gif',output.getvalue())
    print(f'{path.name}: {path.stat().st_size:,} bytes',flush=True)


if __name__=='__main__':
    for name,factory,height in [('banner',banner,400),('toolkit',toolkit,160),
                               ('hobbies',hobbies,190),('footer',footer,100)]:
        render_animation(name,factory,height)
    for filename,label,width,color in [
        ('portfolio.svg','Portfolio',110,GREEN),
        ('linkedin.svg','LinkedIn',110,GREEN),
        ('email.svg','Email me',110,GREEN),
        ('projects.svg','Projects',110,GREEN),
    ]:
        write(filename,f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="36" viewBox="0 0 {width} 36">
          <rect width="{width}" height="36" rx="10" fill="#101d16"/>
          <circle cx="16" cy="18" r="3" fill="{color}"/>
          <text x="{width/2+7}" y="22" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" font-weight="600" font-size="12" fill="#d5ebdf">{label}</text>
        </svg>''')
    update_readme_assets()
