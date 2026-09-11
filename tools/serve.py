#!/usr/bin/env python3
"""Static server for local preview. `python3 tools/serve.py [port]` then open
http://localhost:8123/ . Exists because `python3 -m http.server` calls
os.getcwd() at import time, which the synced CloudStorage path rejects."""
import os, sys, functools, http.server, socketserver

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8123

Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
    print(f"serving {ROOT} at http://localhost:{PORT}/", flush=True)
    httpd.serve_forever()
