#!/usr/bin/env python3
"""Search the local automotive LLM wiki.

The script is intentionally dependency-free so OpenCode can call it from the
skill folder without environment setup.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
import urllib.request


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


ROOT = Path(__file__).resolve().parents[1] / "wiki"
WIKI = ROOT
SYNTHESIS_DIRS = ("concepts", "entities", "comparisons", "queries")
RAW_DIR = WIKI / "raw"

LLM_CONFIG = {
    "model": "MiniMax",
    "api_key": "sk-aBQ6pwtdhyp5n3YWSXqoUQ",
    "base_url": "https://llm-gateway.dev.cn-vwa.volkswagen-cea.com/v1",
}


def llm_complete(prompt: str, temperature: float = 0.1) -> str:
    try:
        data = json.dumps(
            {
                "model": LLM_CONFIG["model"],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": 400,
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            LLM_CONFIG["base_url"] + "/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {LLM_CONFIG['api_key']}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8", errors="replace"))
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[LLM error: {e}]"


@dataclass
class Hit:
    path: Path
    rel_path: str
    layer: str
    title: str = ""
    tags: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    score: int = 0
    matches: list[tuple[int, str]] = field(default_factory=list)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def split_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not match:
        return {}, text
    frontmatter = parse_frontmatter(match.group(1))
    return frontmatter, text[match.end() :]


def parse_frontmatter(raw: str) -> dict[str, object]:
    data: dict[str, object] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        data[key] = parse_value(value)
    return data


def parse_value(value: str) -> object:
    if value == "":
        return ""
    if value.startswith("[") and value.endswith("]"):
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return [str(item) for item in parsed]
        except Exception:
            inner = value[1:-1].strip()
            if not inner:
                return []
            return [item.strip().strip("\"'") for item in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def query_terms(query: str) -> list[str]:
    query = query.strip()
    pieces = [piece for piece in re.split(r"[\s,;，；/]+", query) if piece]
    terms: list[str] = []
    if query:
        terms.append(query.casefold())
    for piece in pieces:
        folded = piece.casefold()
        if folded not in terms:
            terms.append(folded)
    return terms


def iter_markdown(search_raw: bool) -> list[tuple[str, Path]]:
    paths: list[tuple[str, Path]] = []
    for dirname in SYNTHESIS_DIRS:
        directory = WIKI / dirname
        if directory.exists():
            paths.extend((dirname, path) for path in sorted(directory.glob("*.md")))
    if search_raw and RAW_DIR.exists():
        for path in sorted(RAW_DIR.glob("**/*.md")):
            if path.name == "text.md":
                sibling = path.parent.parent / (path.parent.name + ".md")
                if sibling.exists():
                    continue
            paths.append(("raw", path))
    return paths


def score_file(path: Path, layer: str, terms: list[str], context: int) -> Hit | None:
    text = read_text(path)
    frontmatter, body = split_frontmatter(text)
    rel_path = path.relative_to(WIKI).as_posix()
    title = str(frontmatter.get("title") or first_heading(body) or (path.parent.name if path.stem == "text" else path.stem))
    tags = as_string_list(frontmatter.get("tags"))
    sources = as_string_list(frontmatter.get("sources"))

    hay_title = title.casefold()
    hay_meta = " ".join(tags + sources + [path.stem, rel_path]).casefold()
    score = 0
    for term in terms:
        if not term:
            continue
        if term in hay_title:
            score += 50
        if term in hay_meta:
            score += 20

    matches: list[tuple[int, str]] = []
    lines = body.splitlines()
    for line_no, line in enumerate(lines, 1):
        folded = line.casefold()
        line_score = 0
        for term in terms:
            if term and term in folded:
                line_score += 10 + min(folded.count(term), 5)
        if line_score:
            score += line_score
            if len(matches) < context:
                matches.append((line_no, clean_line(line)))

    if score == 0:
        return None
    return Hit(
        path=path,
        rel_path=rel_path,
        layer=layer,
        title=title,
        tags=tags,
        sources=sources,
        score=score,
        matches=matches,
    )


def as_string_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str) and value:
        return [value]
    return []


def first_heading(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def clean_line(line: str, width: int = 220) -> str:
    line = re.sub(r"\s+", " ", line).strip()
    if len(line) > width:
        return line[: width - 1].rstrip() + "..."
    return line


def search(query: str, limit: int, context: int, raw_mode: str) -> list[Hit]:
    terms = query_terms(query)
    if not terms:
        return []

    include_raw = raw_mode == "include"
    hits = collect_hits(terms, context, include_raw)

    if raw_mode == "fallback":
        synthesis_hits = [hit for hit in hits if hit.layer != "raw"]
        if len(synthesis_hits) >= limit:
            hits = synthesis_hits
        else:
            raw_hits = collect_hits(terms, context, True)
            raw_only = [hit for hit in raw_hits if hit.layer == "raw"]
            hits = synthesis_hits + raw_only

    hits.sort(key=lambda hit: (-hit.score, hit.layer == "raw", hit.rel_path.casefold()))
    return hits[:limit]


def collect_hits(terms: list[str], context: int, include_raw: bool) -> list[Hit]:
    hits: list[Hit] = []
    for layer, path in iter_markdown(include_raw):
        hit = score_file(path, layer, terms, context)
        if hit is not None:
            hits.append(hit)
    return hits


def print_text_results(hits: list[Hit], show_sources: bool) -> None:
    if not hits:
        print("No matches.")
        return
    for index, hit in enumerate(hits, 1):
        print(f"[{index}] {hit.rel_path}")
        print(f"    title: {hit.title}")
        print(f"    layer: {hit.layer} | score: {hit.score}")
        if hit.tags:
            print(f"    tags: {', '.join(hit.tags)}")
        if show_sources and hit.sources:
            print(f"    sources: {', '.join(hit.sources)}")
        for line_no, line in hit.matches:
            print(f"    line {line_no}: {line}")


def search_semantic(query: str, limit: int = 10, include_raw: bool = True) -> list[Hit]:
    raw_mode = "include" if include_raw else "fallback"
    candidates = search(query, min(limit * 3, 50), 1, raw_mode)
    if not candidates:
        return []

    lines = [f'Query: {query}\n\nCandidates ({len(candidates)} files):\n']
    for i, hit in enumerate(candidates):
        text = read_text(hit.path)
        frontmatter, body = split_frontmatter(text)
        snippet = body[:500].replace("\n", " ").strip()
        lines.append(f"[{i}] {hit.rel_path}\n   title: {hit.title}\n   snippet: {snippet}\n")

    scoring_prompt = "\n".join(lines) + """
You are a semantic search relevance scorer.
For each candidate [0] to [N], output a JSON array scoring how relevant the file is to the query.
Score: 0=irrelevant, 1=slight match, 2=moderate match, 3=highly relevant, 4=perfect match.
Return ONLY a JSON array of integers in order, e.g.: [3, 1, 4, 0, 2]
Consider: intent matching, topic relevance, and conceptual overlap (not just keyword matches).
"""
    raw_scores = llm_complete(scoring_prompt, temperature=0.1)
    try:
        scores = json.loads(raw_scores)
    except Exception:
        scores = [hit.score for hit in candidates]

    scored = []
    for i, hit in enumerate(candidates):
        score = scores[i] if i < len(scores) else 0
        hit.score = int(score) * 50
        hit.layer = "semantic"
        scored.append(hit)

    scored.sort(key=lambda h: h.score, reverse=True)
    return scored[:limit]


def to_jsonable(hit: Hit) -> dict[str, object]:
    return {
        "path": hit.rel_path,
        "layer": hit.layer,
        "title": hit.title,
        "tags": hit.tags,
        "sources": hit.sources,
        "score": hit.score,
        "matches": [{"line": line_no, "text": line} for line_no, line in hit.matches],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the automotive LLM wiki.")
    parser.add_argument("query", nargs="+", help="Search query words or phrase.")
    parser.add_argument("--limit", type=int, default=12, help="Maximum results.")
    parser.add_argument("--context", type=int, default=3, help="Matching lines per result.")
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Search raw documents together with synthesis pages.",
    )
    parser.add_argument(
        "--no-raw-fallback",
        action="store_true",
        help="Search only synthesis pages unless --raw is supplied.",
    )
    parser.add_argument(
        "--semantic",
        action="store_true",
        help="Use LLM semantic reranking (best relevance, slower).",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON results.")
    parser.add_argument(
        "--sources",
        action="store_true",
        help="Show source paths in text output.",
    )
    args = parser.parse_args()

    if not WIKI.exists():
        print(f"Wiki directory not found: {WIKI}", file=sys.stderr)
        return 2

    raw_mode = "include" if args.raw else "none" if args.no_raw_fallback else "fallback"
    query_str = " ".join(args.query)
    if args.semantic:
        hits = search_semantic(query_str, max(args.limit, 1), args.raw)
    else:
        hits = search(query_str, max(args.limit, 1), max(args.context, 0), raw_mode)

    if args.json:
        print(json.dumps([to_jsonable(hit) for hit in hits], ensure_ascii=False, indent=2))
    else:
        print_text_results(hits, args.sources)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
