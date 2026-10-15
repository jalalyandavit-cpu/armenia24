from pathlib import Path
import json, shutil, html, os, re
from urllib.parse import urlsplit
BASE_PATH=os.environ.get("BASE_PATH", "").strip("/")
BASE_PATH="/"+BASE_PATH if BASE_PATH else ""
if BASE_PATH and (not re.fullmatch(r"/[A-Za-z0-9_/-]+", BASE_PATH) or ".." in BASE_PATH):
    raise ValueError("BASE_PATH must be a safe URL path")
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'dist'
CATS={'politics':'Քաղաքականություն','economy':'Տնտեսություն','society':'Հասարակություն','world':'Աշխարհ','sport':'Սպորտ','video':'Տեսանյութեր'}
articles=json.loads((ROOT/'content/articles.json').read_text())
def esc(s): return html.escape(str(s),quote=True)
for i,a in enumerate(articles):
    a.update(demo=True,status='demo',id=a['slug'],time=f'{12-i//2:02d}:{45 if i%2==0 else 20}',body=a.get('body','Սա ցուցադրական նյութ է, ոչ իրական լուր։ Այն նախատեսված է Armenia24 կայքի ձևավորումն ու հոդվածի կառուցվածքը ներկայացնելու համար։ Նշված թեման չի հաղորդում իրական իրադարձության մասին։\n\nԱյստեղ խմբագիրը կարող է ավելացնել ստուգված տեղեկություններ, աղբյուրների հղումներ, լուսանկարներ և տեսանյութեր։ Իրական հրապարակումից առաջ անհրաժեշտ է ստուգել փաստերը, հեղինակային իրավունքները և հրապարակման ամսաթիվը։'))
    assert a['category'] in CATS
    assert len({x['slug'] for x in articles})==len(articles)
if OUT.exists(): shutil.rmtree(OUT)
shutil.copytree(ROOT/'public',OUT)
nav='<a href="/">Գլխավոր</a>'+''.join(f'<a href="/section/{k}/">{v}</a>' for k,v in CATS.items())
def layout(title,body,description='Armenia24․ հայալեզու լրատվական կայքի ցուցադրական տարբերակ։ Բոլոր նյութերը օրինակներ են։'):
 return f'''<!doctype html><html lang="hy"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Armenia24</title><meta name="description" content="{esc(description)}"><meta name="robots" content="noindex,nofollow"><meta name="site-base" content="{BASE_PATH}/"><meta name="theme-color" content="#142b26"><meta property="og:title" content="{esc(title)} | Armenia24"><meta property="og:description" content="{esc(description)}"><meta property="og:type" content="website"><meta property="og:locale" content="hy_AM"><link rel="icon" href="/assets/favicon.svg"><link rel="stylesheet" href="/style.css"><script src="/app.js" defer></script></head><body><a class="skip" href="#main">Անցնել բովանդակությանը</a><div class="utility"><span>ՀԱՅԱՍՏԱՆԻՑ՝ ԱՇԽԱՐՀԻՆ</span><span>Անկախ հայացք · Հայերեն</span></div><header><a class="logo" href="/" aria-label="Armenia24 գլխավոր">ARMENIA<span>24</span><i></i></a><div class="motto">Լուրեր։ Համատեքստ։<br>Նոր հեռանկար։</div><button id="menu" aria-expanded="false" aria-controls="nav">☰ <span>Բաժիններ</span></button><a class="search-toggle" href="/search/" aria-label="Որոնել">Որոնում ↗</a></header><nav id="nav" aria-label="Հիմնական բաժիններ">{nav}</nav><div class="demo"><b>ՑՈՒՑԱԴՐԱԿԱՆ ՏԱՐԲԵՐԱԿ</b><span>Բոլոր նյութերը օրինակներ են և իրական լուրեր չեն։</span></div><main id="main">{body}</main><footer><a class="logo" href="/">ARMENIA<span>24</span></a><p>Տեղեկատվության նոր հեռանկար։</p><div>{nav}</div><p class="fine">© Armenia24 · Ցուցադրական նախագիծ · Բոլոր նյութերը օրինակներ են։</p></footer></body></html>'''
def save(path,text):
 if path.endswith('.html'):
  text=re.sub(r'(href|src)="/(?!/)', lambda m: m.group(1)+'="'+BASE_PATH+'/', text)
 p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def card(a,n=0):
 return f'''<a class="card" href="/news/{a['slug']}/"><div class="thumb tone{n%4}">{'<img loading="lazy" width="800" height="500" src="'+a['image']+'" alt="'+esc(a['imageAlt'])+'">' if a.get('image') else '<span class="abstract">'+['Ա','24','↗','◉'][n%4]+'</span>'}<span class="sample">ՕՐԻՆԱԿ</span></div><div class="meta">{CATS[a['category']]} <span>· {a['time']}</span></div><h3>{a['title']}</h3><p>{a['excerpt']}</p></a>'''
a=articles[0]
hero=f'''<div class="section-head"><h1>Օրվա պատկերը</h1><span>ARMENIA24 / ԴԵՄՈ</span></div><div class="lead-grid"><a class="hero" href="/news/{a['slug']}/"><img src="{a['image']}" width="1200" height="800" fetchpriority="high" alt="{a['imageAlt']}"><div class="hero-shade"><span class="pill">ՀԱՍԱՐԱԿՈՒԹՅՈՒՆ · ՕՐԻՆԱԿ</span><h2>{a['title']}</h2><p>{a['excerpt']}</p><span>Կարդալ նյութը ↗</span><small class="image-note">ԱԲ-ով ստեղծված ցուցադրական պատկեր</small></div></a><aside><div class="aside-head"><h2>Վերջին նյութերը</h2><span class="dot"></span></div><p class="muted">Ցուցադրական լրահոս</p>{''.join(f'<a class="latest" href="/news/{x["slug"]}/"><time>{x["time"]}</time><div><small>{CATS[x["category"]]} · ՕՐԻՆԱԿ</small><h3>{x["title"]}</h3></div></a>' for x in articles[1:5])}<a class="text-link" href="/search/">Բոլոր նյութերը →</a></aside></div>'''
body=hero+'<div class="section-head"><h2>Ուշադրության կենտրոնում</h2><span>ԸՆՏՐՎԱԾ ՆՅՈՒԹԵՐ</span></div><div class="cards">'+''.join(card(a,i) for i,a in enumerate(articles[1:4]))+'</div>'
body+='''<section class="video-banner"><div><span class="eyebrow">ՏԵՍԱՆՅՈՒԹԵՐ / ՕՐԻՆԱԿ</span><h2>Պատմություններ՝<br>նոր տեսանկյունից։</h2><p>Տեսապատմությունների համար նախատեսված տարածք։</p><a class="light-button" href="/section/video/">Դիտել բաժինը ↗</a></div><div class="play-art" aria-hidden="true">▷</div></section>'''
for k in ['society','economy','politics','world','sport']:
 if k=='politics': body+='<div class="topic-grid">'
 body+=f'<section><div class="section-head"><h2>{CATS[k]}</h2><a href="/section/{k}/">Բոլոր նյութերը ↗</a></div><div class="cards">'+''.join(card(a,i+1) for i,a in enumerate(articles) if a['category']==k)+'</div></section>'
body+='</div>'
save('index.html',layout('Գլխավոր',body))
for k,v in CATS.items(): save(f'section/{k}/index.html',layout(v,f'<div class="section-head"><h1>{v}</h1><span>ՑՈՒՑԱԴՐԱԿԱՆ ՆՅՈՒԹԵՐ</span></div><div class="cards">'+''.join(card(a,i) for i,a in enumerate(articles) if a['category']==k)+'</div>'))
for a in articles:
 body=f'<article class="article"><a class="text-link" href="/section/{a["category"]}/">← {CATS[a["category"]]}</a><p class="eyebrow">ՕՐԻՆԱԿ · ՑՈՒՑԱԴՐԱԿԱՆ ՆՅՈՒԹ</p><h1>{a["title"]}</h1><p class="intro">{a["excerpt"]}</p><p class="muted">Armenia24 · Դեմո խմբագրություն</p>'
 if a.get('image'): body+=f'<figure><img src="{a["image"]}" width="1200" height="800" alt="{a["imageAlt"]}"><figcaption>ԱԲ-ով ստեղծված պատկեր․ իրական իրադարձության լուսանկար չէ։</figcaption></figure>'
 if a['category']=='video': body+='<div class="video-placeholder">▷<p>Տեսանյութ դեռ կցված չէ։ Սա տեսանյութի էջի օրինակ է։</p></div>'
 body+=''.join('<p>'+esc(p)+'</p>' for p in a['body'].split('\n\n'))+'<a class="text-link" href="/">Վերադառնալ գլխավոր էջ →</a></article>'
 save(f'news/{a["slug"]}/index.html',layout(a['title']+' — օրինակ',body,a['excerpt']))
save('search/index.html',layout('Որոնում','<div class="section-head"><h1>Որոնում</h1></div><form id="search-form" role="search"><label for="query">Որոնել ցուցադրական նյութերում</label><div class="search-row"><input id="query" name="q" type="search" placeholder="Մուտքագրեք բանալի բառ…"><button>Որոնել →</button></div></form><p id="result-count" role="status"></p><div id="results" class="cards"></div>'))
save('404.html',layout('Էջը չի գտնվել','<div class="article"><h1>404 · Էջը չի գտնվել</h1><p>Հնարավոր է՝ հղումը փոխվել է։</p><a href="/">Գլխավոր էջ →</a></div>'))
save('data.json',json.dumps([{**a, **({'image': BASE_PATH+a['image']} if a.get('image','').startswith('/') else {})} for a in articles],ensure_ascii=False))
save('.nojekyll','')
save('build-config.json',json.dumps({'basePath':BASE_PATH}))
save('robots.txt','User-agent: *\nDisallow: /\n')
print(f'Built {len(articles)} articles, {len(CATS)} sections. Demo indexing disabled.')
