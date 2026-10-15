from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
ROOT=Path(__file__).resolve().parents[1]; dist=ROOT/'dist'
class Check(HTMLParser):
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  for key in ('href','src'):
   url=attrs.get(key,'')
   if not url or url.startswith('#') or urlsplit(url).scheme: continue
   path=dist/unquote(urlsplit(url).path).lstrip('/')
   if str(urlsplit(url).path).endswith('/'): path=path/'index.html'
   assert path.exists(),f'Broken reference {url} in {self.page}'
  if tag=='html': assert attrs.get('lang')=='hy'
  if tag=='img': assert attrs.get('alt'),f'Missing image alt in {self.page}'
parser=Check()
for path in dist.rglob('*.html'):
 parser.page=path;source=path.read_text();parser.feed(source)
 assert 'noindex,nofollow' in source
 assert 'ՑՈՒՑԱԴՐԱԿԱՆ' in source or 'Ցուցադրական' in source
assert len(json.loads((dist/'data.json').read_text()))==8
print('PASS: all generated HTML, internal links, assets, Armenian language, demo labels and indexing protection.')
