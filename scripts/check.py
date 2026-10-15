from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
dist=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'dist'
base=json.loads((dist/'build-config.json').read_text())['basePath']
def local_path(url):
    path=unquote(urlsplit(url).path)
    assert path.startswith(base+'/'), f'URL escapes deployment base {base}: {url}'
    return dist/path[len(base)+1:]
class Check(HTMLParser):
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  for key in ('href','src'):
   url=attrs.get(key,'')
   if not url or url.startswith('#') or urlsplit(url).scheme: continue
   path=local_path(url)
   if urlsplit(url).path.endswith('/'): path=path/'index.html'
   assert path.exists(),f'Broken reference {url} in {self.page}'
  if tag=='html': assert attrs.get('lang')=='hy'
  if tag=='img': assert attrs.get('alt'),f'Missing image alt in {self.page}'
parser=Check()
pages=[dist/'index.html',dist/'404.html',*(dist/'news').rglob('*.html'),*(dist/'section').rglob('*.html'),*(dist/'search').rglob('*.html')]
for path in pages:
 parser.page=path;source=path.read_text();parser.feed(source)
 assert 'noindex,nofollow' in source
 assert 'ՑՈՒՑԱԴՐԱԿԱՆ' in source or 'Ցուցադրական' in source
 assert f'name="site-base" content="{base}/"' in source
for url in re.findall(r'url\([\'"]?([^\)\'\"]+)',(dist/'style.css').read_text()):
 assert not url.startswith('/'),f'Root-relative CSS URL: {url}'
 assert (dist/url).exists(),f'Missing CSS asset: {url}'
articles=json.loads((dist/'data.json').read_text());assert len(articles)==8
for article in articles:
 if article.get('image'): assert local_path(article['image']).exists()
assert (dist/'.nojekyll').exists()
print(f'PASS: {len(pages)} pages, links, CSS fonts, images, Armenian language, demo labels; base={base or "/"}.')
