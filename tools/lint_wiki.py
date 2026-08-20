#!/usr/bin/env python3
"""Lint the local automotive LLM wiki.

Checks are intentionally conservative and dependency-free:
- required frontmatter on synthesis pages
- allowed tags from SCHEMA.md
- sources paths that exist
- broken wikilinks
- index coverage for synthesis pages
- raw document SHA-256 drift
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


ROOT = Path(r"C:\Users\T1UKLL7\Desktop\Workstation\employee agent\_archive_llm_wiki")
WIKI = ROOT
SYNTHESIS_DIRS = ("concepts", "entities", "comparisons", "queries")
REQUIRED_SYNTHESIS_KEYS = {
    "title",
    "created",
    "updated",
    "type",
    "tags",
    "sources",
    "aliases",
    "related",
    "confidence",
}


@dataclass
class Issue:
    severity: str
    path: str
    message: str


@dataclass
class LintResult:
    checked_files: int = 0
    issues: list[Issue] = field(default_factory=list)

    def add(self, severity: str, path: Path | str, message: str) -> None:
        rel = str(path)
        if isinstance(path, Path):
            try:
                rel = path.relative_to(WIKI).as_posix()
            except ValueError:
                rel = path.as_posix()
        self.issues.append(Issue(severity, rel, message))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def split_frontmatter(text: str) -> tuple[dict[str, object], str, str]:
    if not text.startswith("---"):
        return {}, "", text
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not match:
        return {}, "", text
    raw_frontmatter = match.group(1)
    return parse_frontmatter(raw_frontmatter), raw_frontmatter, text[match.end() :]


def parse_frontmatter(raw: str) -> dict[str, object]:
    data: dict[str, object] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = parse_value(value.strip())
    return data


def parse_value(value: str) -> object:
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


def as_string_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str) and value:
        return [value]
    return []


def synthesis_pages() -> list[Path]:
    pages: list[Path] = []
    for dirname in SYNTHESIS_DIRS:
        directory = WIKI / dirname
        if directory.exists():
            pages.extend(sorted(directory.glob("*.md")))
    return pages


def raw_pages() -> list[Path]:
    directory = WIKI / "raw" / "documents"
    if not directory.exists():
        return []
    return sorted(directory.glob("*.md"))


def allowed_tags() -> set[str]:
    schema = WIKI / "SCHEMA.md"
    if not schema.exists():
        return set()
    text = read_text(schema)
    tags: set[str] = set()
    in_taxonomy = False
    for line in text.splitlines():
        if line.strip() == "## Tag Taxonomy":
            in_taxonomy = True
            continue
        if in_taxonomy and line.startswith("## "):
            break
        if in_taxonomy and line.strip().startswith("- "):
            tags.add(line.strip()[2:].strip())
    return tags


def wiki_targets(pages: list[Path]) -> set[str]:
    targets = {page.stem.casefold() for page in pages}
    root_pages = ["SCHEMA.md", "index.md", "log.md", "README.md", "AGENTS.md"]
    for name in root_pages:
        path = WIKI / name
        if path.exists():
            targets.add(path.stem.casefold())
    return targets


def extract_wikilinks(text: str) -> list[str]:
    links = []
    for match in re.finditer(r"\[\[([^\]]+)\]\]", text):
        target = match.group(1).split("|", 1)[0].strip()
        if target:
            links.append(target)
    return links


def normalize_link_target(target: str) -> str:
    target = target.split("#", 1)[0].strip()
    target = target.replace("\\", "/").rstrip("/")
    if "/" in target:
        target = target.rsplit("/", 1)[-1]
    if target.endswith(".md"):
        target = target[:-3]
    return target.casefold()


def lint_synthesis(result: LintResult, pages: list[Path], tags: set[str]) -> None:
    targets = wiki_targets(pages)
    index_text = read_text(WIKI / "index.md") if (WIKI / "index.md").exists() else ""
    for page in pages:
        result.checked_files += 1
        text = read_text(page)
        frontmatter, _, body = split_frontmatter(text)
        if not frontmatter:
            result.add("error", page, "missing or malformed frontmatter")
            continue
        missing = sorted(REQUIRED_SYNTHESIS_KEYS - set(frontmatter))
        if missing:
            result.add("warning", page, f"missing frontmatter keys: {', '.join(missing)}")
        page_type = str(frontmatter.get("type", ""))
        if page_type and page_type not in {"entity", "concept", "comparison", "query"}:
            result.add("warning", page, f"unknown page type: {page_type}")
        for tag in as_string_list(frontmatter.get("tags")):
            if tags and tag not in tags:
                result.add("warning", page, f"tag not in SCHEMA taxonomy: {tag}")
        for source in as_string_list(frontmatter.get("sources")):
            source_path = (WIKI / source).resolve()
            try:
                source_path.relative_to(WIKI.resolve())
            except ValueError:
                result.add("error", page, f"source escapes wiki root: {source}")
                continue
            if not source_path.exists():
                result.add("error", page, f"source does not exist: {source}")
        for link in extract_wikilinks(body):
            normalized = normalize_link_target(link)
            if normalized and normalized not in targets:
                result.add("warning", page, f"broken wikilink: [[{link}]]")
        if f"[[{page.stem}" not in index_text:
            result.add("warning", page, "page is not listed in index.md")


def lint_raw_checksums(result: LintResult) -> None:
    for page in raw_pages():
        result.checked_files += 1
        text = read_text(page)
        frontmatter, _, body = split_frontmatter(text)
        expected = str(frontmatter.get("sha256", "")).strip()
        if not expected:
            result.add("warning", page, "raw document missing sha256")
            continue
        actual = hashlib.sha256(body.strip().encode("utf-8")).hexdigest()
        if actual != expected:
            result.add("warning", page, f"raw sha256 drift: expected {expected}, got {actual}")


def to_json(result: LintResult) -> str:
    payload = {
        "checked_files": result.checked_files,
        "issue_count": len(result.issues),
        "issues": [issue.__dict__ for issue in result.issues],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def print_text(result: LintResult) -> None:
    print(f"Checked files: {result.checked_files}")
    print(f"Issues: {len(result.issues)}")
    for issue in result.issues:
        print(f"[{issue.severity}] {issue.path}: {issue.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint the automotive LLM wiki.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument(
        "--no-raw-checksum",
        action="store_true",
        help="Skip raw document checksum drift checks.",
    )
    args = parser.parse_args()

    result = LintResult()
    if not WIKI.exists():
        result.add("error", WIKI, "wiki directory does not exist")
    else:
        pages = synthesis_pages()
        lint_synthesis(result, pages, allowed_tags())
        if not args.no_raw_checksum:
            lint_raw_checksums(result)

    if args.json:
        print(to_json(result))
    else:
        print_text(result)
    return 1 if any(issue.severity == "error" for issue in result.issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
