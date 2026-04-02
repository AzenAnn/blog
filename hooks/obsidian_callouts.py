from __future__ import annotations

import re

CALLOUT_START_RE = re.compile(
    r"^(?P<indent>[ \t]{0,3})>\s*\[!(?P<kind>[A-Za-z][A-Za-z0-9_-]*)\](?P<fold>[+-])?\s*(?P<title>.*)$"
)
BLOCKQUOTE_RE = re.compile(r"^(?P<indent>[ \t]{0,3})>\s?(?P<content>.*)$")
FENCE_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<fence>`{3,}|~{3,}).*$")

CALLOUT_ALIASES = {
    "abstract": "abstract",
    "summary": "abstract",
    "tldr": "abstract",
    "note": "note",
    "info": "info",
    "todo": "info",
    "tip": "tip",
    "hint": "tip",
    "important": "tip",
    "success": "success",
    "check": "success",
    "done": "success",
    "question": "question",
    "help": "question",
    "faq": "question",
    "warning": "warning",
    "caution": "warning",
    "attention": "warning",
    "failure": "failure",
    "fail": "failure",
    "missing": "failure",
    "danger": "danger",
    "error": "danger",
    "bug": "bug",
    "example": "example",
    "quote": "quote",
    "cite": "quote",
}


def on_page_markdown(markdown: str, **kwargs) -> str:
    return _convert_obsidian_callouts(markdown)


def _convert_obsidian_callouts(markdown: str) -> str:
    lines = markdown.splitlines()
    converted: list[str] = []
    trailing_newline = markdown.endswith("\n")
    fence_char: str | None = None
    fence_len = 0
    i = 0

    while i < len(lines):
        line = lines[i]
        fence_match = FENCE_RE.match(line)

        if fence_char is not None:
            converted.append(line)
            if fence_match:
                fence = fence_match.group("fence")
                if fence[0] == fence_char and len(fence) >= fence_len:
                    fence_char = None
                    fence_len = 0
            i += 1
            continue

        if fence_match:
            fence = fence_match.group("fence")
            fence_char = fence[0]
            fence_len = len(fence)
            converted.append(line)
            i += 1
            continue

        callout_match = CALLOUT_START_RE.match(line)
        if not callout_match:
            converted.append(line)
            i += 1
            continue

        indent = callout_match.group("indent")
        kind = _normalize_kind(callout_match.group("kind"))
        fold = callout_match.group("fold")
        title = callout_match.group("title").strip()

        marker = "!!!"
        if fold == "+":
            marker = "???+"
        elif fold == "-":
            marker = "???"

        if title:
            escaped_title = title.replace("\\", "\\\\").replace('"', '\\"')
            converted.append(f'{indent}{marker} {kind} "{escaped_title}"')
        else:
            converted.append(f"{indent}{marker} {kind}")

        i += 1
        body_lines: list[str] = []
        while i < len(lines):
            blockquote_match = BLOCKQUOTE_RE.match(lines[i])
            if not blockquote_match:
                break
            body_lines.append(blockquote_match.group("content"))
            i += 1

        if not body_lines:
            converted.append(f"{indent}    ")
            continue

        for body_line in body_lines:
            if body_line:
                converted.append(f"{indent}    {body_line}")
            else:
                converted.append("")

    result = "\n".join(converted)
    if trailing_newline:
        result += "\n"
    return result


def _normalize_kind(kind: str) -> str:
    return CALLOUT_ALIASES.get(kind.lower(), "note")
