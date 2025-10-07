#!/usr/bin/env python3
"""Serve the AI learning site on http://localhost:8000/.

This helper script starts a simple HTTP server rooted at the repository
so you can visit the site without manually running python -m http.server.
"""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import argparse
import contextlib
import os
import socket
import sys
import webbrowser


def find_available_port(preferred: int) -> int:
    """Return the preferred port if free, otherwise pick an ephemeral port."""
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("", preferred))
        except OSError:
            sock.bind(("", 0))
        return sock.getsockname()[1]


def serve(directory: Path, port: int, open_browser: bool) -> None:
    os.chdir(directory)
    handler = SimpleHTTPRequestHandler
    httpd = ThreadingHTTPServer(("", port), handler)

    url = f"http://localhost:{port}/index.html"
    print(f"Serving {directory} at {url}")
    if open_browser:
        try:
            webbrowser.open(url)
        except Exception as exc:  # pragma: no cover - best effort
            print(f"Failed to open browser automatically: {exc}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        httpd.server_close()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Serve the AI Learning Lab site.")
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind (default: 8000)."
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not attempt to open a browser automatically.",
    )
    args = parser.parse_args(argv)

    project_root = Path(__file__).resolve().parent
    port = find_available_port(args.port)
    serve(project_root, port, not args.no_browser)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
