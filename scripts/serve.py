"""Local-only preview; rebuild before serving. No deployment."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import runpy
from functools import partial
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'scripts/build.py'))
class Handler(SimpleHTTPRequestHandler):
    def send_error(self, code, message=None, explain=None):
        if code==404:
            content=(ROOT/'dist/404.html').read_bytes();self.send_response(404);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(content)
        else: super().send_error(code,message,explain)
print('Armenia24 local preview: http://localhost:4173',flush=True)
ThreadingHTTPServer(('127.0.0.1',4173),partial(Handler,directory=str(ROOT/'dist'))).serve_forever()
