"""Inject logo texture + flare layout into the template -> self-contained visual.html"""
import base64, json, sys
tex = base64.b64encode(open('src/logo_tex.png', 'rb').read()).decode()
def T(x, y):  # reference-image px -> logo texture uv
    return [round((248 + (x - 223.7) / 812.3 * 3600) / 4096, 5), round((197.25 + (y - 530) / 142 * 629.5) / 1024, 5)]
# x, y (ref px), size, colour, phase  -- positions of the sparkles in the brand artwork
fl = [(248, 535, .8, 0, 0.0), (625, 525, 1.25, 1, 1.3), (637, 668, 1.35, 0, 2.9),
      (920, 532, .85, 1, 4.1), (432, 665, .6, 1, 5.2), (995, 660, .8, 0, 0.7)]
flares = [T(x, y) + [s, c, p] for x, y, s, c, p in fl]
html = open('src/visual.template.html').read().replace('__LOGO_TEX__', 'data:image/png;base64,' + tex).replace('__FLARES__', json.dumps(flares))
open(sys.argv[1] if len(sys.argv) > 1 else 'visual.html', 'w').write(html)
