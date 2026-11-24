"""도트 아이콘을 SVG CSS 변수로 만들어 index.html의 <style id="px"> 블록에 넣는다. python build_css.py"""
import importlib.util, pathlib, re
from urllib.parse import quote
here = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location('icons', here/'icons.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def svg(name):
    g = m.I[name]; L = len(g[0]); rects = []
    for y,row in enumerate(g):
        x = 0
        while x < L:
            ch = row[x]
            if ch == '.': x += 1; continue
            x2 = x
            while x2+1 < L and row[x2+1] == ch: x2 += 1
            rects.append(f"<rect x='{x}' y='{y}' width='{x2-x+1}' height='1' fill='{m.PAL[ch]}'/>"); x = x2+1
    s = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {L} {L}' shape-rendering='crispEdges'>" + ''.join(rects) + "</svg>"
    return 'url("data:image/svg+xml,' + quote(s, safe="/:=' ") + '")'
css = '<style id="px">\n/* 도트 아이콘 — 원본 tools/icons.py, python tools/build_css.py 로 다시 붙임 */\n:root{\n' + \
      '\n'.join(f'  --px-{n}:{svg(n)};' for n in m.I) + '\n}\n' + \
      '.px{display:inline-block;width:1em;height:1em;background-size:contain;background-repeat:no-repeat;background-position:center;image-rendering:pixelated;vertical-align:-0.12em;flex:none}\n' + \
      '\n'.join(f'.px-{n}{{background-image:var(--px-{n})}}' for n in m.I) + '\n</style>'
p = here.parent/'index.html'; s = p.read_text(encoding='utf8')
if '<style id="px">' in s: s = re.sub(r'<style id="px">.*?</style>', lambda _: css, s, flags=re.S)
else: s = s.replace('</head>', css + '\n</head>', 1)
p.write_text(s, encoding='utf8'); print('ok', len(m.I))
