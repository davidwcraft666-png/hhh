#!/usr/bin/env python3
"""Command line tool to fetch and summarize information from a webpage."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from pathlib import Path
from html.parser import HTMLParser
from typing import Dict, List
from urllib.parse import urlparse
from urllib.request import url2pathname


class WebInfoParser(HTMLParser):
    """Lightweight HTML parser that extracts simple page information."""

    def __init__(self) -> None:
        super().__init__()
        self.title: str | None = None
        self.description: str | None = None
        self.headings: List[str] = []
        self.paragraphs: List[str] = []
        self._stack: List[dict] = []

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        attrs_dict = {name.lower(): (value or "") for name, value in attrs}

        if tag == "meta":
            name = attrs_dict.get("name", "").lower()
            if name == "description" and not self.description:
                content = attrs_dict.get("content", "").strip()
                if content:
                    self.description = content
            return

        if tag == "title" and self.title is None:
            self._stack.append({"tag": tag, "buffer": []})
            return

        if tag in {"h1", "h2", "h3"} and len(self.headings) < 10:
            self._stack.append({"tag": tag, "buffer": []})
            return

        if tag == "p" and len(self.paragraphs) < 5:
            self._stack.append({"tag": tag, "buffer": []})

    def handle_endtag(self, tag: str) -> None:
        if not self._stack:
            return

        current = self._stack[-1]
        if current["tag"] != tag:
            return

        self._stack.pop()
        text = "".join(current["buffer"]).strip()
        if not text:
            return

        if tag == "title" and self.title is None:
            self.title = text
        elif tag in {"h1", "h2", "h3"}:
            self.headings.append(f"{tag.upper()}: {text}")
        elif tag == "p":
            self.paragraphs.append(text)

    def handle_data(self, data: str) -> None:
        if not self._stack:
            return
        self._stack[-1]["buffer"].append(data)

    def get_info(self) -> Dict[str, str]:
        info: Dict[str, str] = {}
        if self.title:
            info["title"] = self.title
        if self.description:
            info["description"] = self.description
        if self.headings:
            info["headings"] = "\n".join(self.headings)
        if self.paragraphs:
            info["paragraphs"] = "\n".join(self.paragraphs)
        return info


def _read_local_file(path: Path) -> str:
    """Read HTML content from a local file, handling encoding issues gracefully."""

    if not path.exists():
        raise FileNotFoundError(f"本地文件不存在: {path}")

    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="ignore")


def fetch_html(source: str, timeout: int = 10) -> str:
    """Fetch raw HTML from the given URL or local file path."""

    parsed = urlparse(source)

    if parsed.scheme in {"http", "https"}:
        request = urllib.request.Request(source, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            encoding = response.headers.get_content_charset() or "utf-8"
            raw = response.read()
            try:
                return raw.decode(encoding, errors="ignore")
            except LookupError:
                return raw.decode("utf-8", errors="ignore")

    if parsed.scheme in {"", "file"}:
        if parsed.scheme == "file":
            path = Path(url2pathname(parsed.path))
        else:
            path = Path(source)
        return _read_local_file(path)

    raise ValueError("仅支持 HTTP/HTTPS 地址或本地文件路径。")


def parse_html(html: str) -> Dict[str, str]:
    """Parse relevant information from HTML using a lightweight parser."""

    parser = WebInfoParser()
    parser.feed(html)
    parser.close()
    return parser.get_info()


def format_info(info: Dict[str, str]) -> str:
    """Format the extracted information as a readable string."""
    if not info:
        return "未能从页面中提取到信息。"

    sections = []
    for key, title in [
        ("title", "页面标题"),
        ("description", "页面描述"),
        ("headings", "主要标题"),
        ("paragraphs", "示例段落"),
    ]:
        value = info.get(key)
        if value:
            sections.append(f"{title}:\n{value}\n")

    return "\n".join(sections)


def prompt_local_fallback() -> str | None:
    """Ask for a local HTML file path when remote fetching fails."""

    try:
        alternative = input(
            "请输入已保存的本地 HTML 文件路径（直接回车取消）: "
        ).strip()
    except EOFError:
        return None

    return alternative or None


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="抓取网页信息并打印页面中的标题、描述和部分文本内容。"
    )
    parser.add_argument("url", nargs="?", help="要抓取的网页地址或本地 HTML 文件路径")
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="请求超时时间（秒），默认 10 秒。",
    )
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    url = args.url
    if not url:
        url = input("请输入要抓取的网页地址: ").strip()

    if not url:
        print("未提供有效的网址。", file=sys.stderr)
        return 1

    source = url

    while True:
        try:
            html = fetch_html(source, timeout=args.timeout)
            info = parse_html(html)
            print(format_info(info))
            return 0
        except urllib.error.HTTPError as exc:
            print(
                "抓取网页失败: HTTP {code} {reason}. 如果这是由于网络限制导致的 403 错误，"
                "可以先在可访问网络的环境下载页面 HTML 保存为本地文件，然后使用本脚本"
                "读取该文件。".format(code=exc.code, reason=exc.reason),
                file=sys.stderr,
            )
        except urllib.error.URLError as exc:
            print(
                f"抓取网页失败: {exc}. 如果是因为网络限制导致无法访问目标网站，可先"
                "下载网页到本地文件后再使用本脚本解析。",
                file=sys.stderr,
            )
        except (FileNotFoundError, PermissionError) as exc:
            print(f"读取本地文件失败: {exc}", file=sys.stderr)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1

        alternative = prompt_local_fallback()
        if not alternative:
            return 1

        source = alternative


if __name__ == "__main__":
    sys.exit(main())
