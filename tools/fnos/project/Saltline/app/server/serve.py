#!/usr/bin/env python3
"""Minimal static HTTP server for Saltline."""
import os
import socketserver
from http.server import SimpleHTTPRequestHandler


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main() -> None:
    port = int(os.environ.get("SALTLINE_PORT", "59940"))
    bind = os.environ.get("SALTLINE_BIND", "0.0.0.0")
    root = os.environ.get("SALTLINE_WWW")
    if not root or not os.path.isfile(os.path.join(root, "index.html")):
        raise SystemExit("Saltline www directory is missing index.html")
    os.chdir(root)
    with ReusableTCPServer((bind, port), SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    main()
