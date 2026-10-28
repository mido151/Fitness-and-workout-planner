"""Phase 2 QA runner: axe-core scan (WCAG 2.1 A/AA + best practice), horizontal overflow
check and full-page screenshots for every page at 375, 768 and 1280 px.
Setup: cd tests/qa && npm install && pip install playwright && python3 -m playwright install chromium
Run:   python3 qa.py ../../frontend ./out   (results in out/report.json + PNGs)
"""
import json, os, sys
from playwright.sync_api import sync_playwright

front, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
pages = sys.argv[3:] or sorted(f for f in os.listdir(front) if f.endswith('.html'))
os.makedirs(out, exist_ok=True)
AXE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_modules/axe-core/axe.min.js')).read()
WIDTHS = [375, 768, 1280]
proxy = os.environ.get('HTTPS_PROXY')
report = {}

with sync_playwright() as p:
    b = p.chromium.launch(proxy={'server': proxy} if proxy else None)
    ctx = b.new_context(ignore_https_errors=True)
    # Fonts are served from local npm copies so screenshots match a normal browser even offline
    NM = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_modules')
    FONTS = {'sym.woff2': NM + '/material-symbols/material-symbols-outlined.woff2',
             'inter.woff2': NM + '/@fontsource-variable/inter/files/inter-latin-wght-normal.woff2',
             'outfit.woff2': NM + '/@fontsource-variable/outfit/files/outfit-latin-wght-normal.woff2'}
    CSS = ('@font-face{font-family:"Material Symbols Outlined";font-style:normal;font-weight:100 700;src:url(https://localfonts.test/sym.woff2) format("woff2")}'
           '.material-symbols-outlined{font-family:"Material Symbols Outlined";font-weight:normal;font-style:normal;font-size:24px;line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-feature-settings:"liga";-webkit-font-smoothing:antialiased}'
           '@font-face{font-family:"Inter";font-weight:100 900;src:url(https://localfonts.test/inter.woff2) format("woff2")}'
           '@font-face{font-family:"Outfit";font-weight:100 900;src:url(https://localfonts.test/outfit.woff2) format("woff2")}')
    ctx.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(status=200, content_type='text/css', body=CSS))
    # The Tailwind Play CDN cannot load offline; for pages still on it, inject the built css/output.css
    # instead (this is how the page will look once it is switched to the build).
    ctx.route('https://cdn.tailwindcss.com/**', lambda r: r.fulfill(status=200, content_type='text/javascript',
              body="document.head.insertAdjacentHTML('beforeend','<link rel=\"stylesheet\" href=\"css/output.css\">')"))
    ctx.route('https://fonts.gstatic.com/**', lambda r: r.fulfill(status=204, body=''))
    ctx.route('https://localfonts.test/**', lambda r: r.fulfill(status=200, content_type='font/woff2', headers={'Access-Control-Allow-Origin': '*'}, body=open(FONTS[r.request.url.rsplit('/', 1)[1]], 'rb').read()))
    for page_name in pages:
        report[page_name] = {}
        for w in WIDTHS:
            pg = ctx.new_page(); pg.set_viewport_size({'width': w, 'height': 900})
            pg.goto('file://' + os.path.join(front, page_name), wait_until='load', timeout=60000)
            try:
                pg.evaluate("document.fonts.ready.then(() => 1)")
            except Exception:
                pass
            pg.wait_for_timeout(400)
            info = pg.evaluate("""() => {
              const de = document.documentElement;
              const over = [];
              for (const el of document.querySelectorAll('body *')) {
                const r = el.getBoundingClientRect();
                if (r.width && r.right > de.clientWidth + 1) {
                  // ignore children of horizontally scrollable containers and hidden decorative glows
                  let p = el.parentElement, skip = false;
                  while (p) { const s = getComputedStyle(p); if (/(auto|scroll|hidden)/.test(s.overflowX) || s.position === 'fixed' && s.pointerEvents === 'none') { skip = true; break; } p = p.parentElement; }
                  if (!skip) over.push(el.tagName + '.' + (el.className.baseVal ?? el.className).toString().slice(0, 60));
                }
              }
              return { scrollW: de.scrollWidth, clientW: de.clientWidth, over: over.slice(0, 8),
                       cdn: !!document.querySelector('script[src*="cdn.tailwindcss"]'),
                       css: !!document.querySelector('link[href="css/output.css"]'),
                       iconsLoaded: [...document.fonts].some(f => f.family.includes('Material') && f.status === 'loaded') };
            }""")
            pg.screenshot(path=os.path.join(out, f"{page_name[:-5]}-{w}.png"), full_page=True)
            if w == 1280 or w == 375:
                pg.add_script_tag(content=AXE)
                res = pg.evaluate("""async () => {
                  const r = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice'] } });
                  return r.violations.map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length,
                    sample: v.nodes.slice(0, 3).map(n => n.target.join(' ') + ' :: ' + (n.any[0]?.message || n.all[0]?.message || n.none[0]?.message || '').slice(0, 140)) }));
                }""")
                info['axe'] = res
            report[page_name][w] = info
            pg.close()
    b.close()

json.dump(report, open(os.path.join(out, 'report.json'), 'w'), indent=1)
for page_name, ws in report.items():
    print('==', page_name)
    for w, i in ws.items():
        line = f"  {w}px overflow={i['scrollW']>i['clientW']} ({i['scrollW']}/{i['clientW']}) cdn={i['cdn']} css={i['css']} icons={i['iconsLoaded']}"
        if i['over']: line += ' over=' + ', '.join(i['over'][:3])
        print(line)
        for v in i.get('axe', []):
            print(f"     axe {v['impact']:9} {v['id']} x{v['n']}  {v['sample'][0][:150]}")
