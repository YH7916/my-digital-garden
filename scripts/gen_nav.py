#!/usr/bin/env python3
"""
Auto-generate nav in zensical.toml by scanning docs/.
Run: python scripts/gen_nav.py
"""
import re
from pathlib import Path

DOCS_DIR = Path("docs")
TOML_PATH = Path("zensical.toml")

# Top-level tabs: (directory or file, tab label)
TOP_LEVEL = [
    ("index.md",  "🏠 首页"),
    ("Research",  "🔬 科研"),
    ("Career",    "💼 实习"),
    ("Dev",       "🧩 算法"),
    ("Diary",     "✍️ 随笔"),
    ("Notes",     "📚 课程笔记"),
]

# Display names for subdirectories (add here when you create new subsections)
SUB_LABELS = {
    "TinyML":       "TinyML",
    "Internship":   "实习经历",
    "Interview":    "面试复盘",
    "更古早的说说":  "更古早的说说",
    "大物":         "大物",
    "概统":         "概统",
}

# Files/dirs to skip entirely
SKIP = {"index.md", ".pages", ".obsidian", ".trash", "assets", "stylesheets"}


def scan(dir_path: Path, prefix: str) -> list:
    """Recursively build nav entries for a directory.
    index.md is listed first; navigation.indexes promotes it to the section title.
    """
    entries = []
    index = dir_path / "index.md"
    if index.exists():
        entries.append(f"{prefix}/index.md")
    subdirs, files = [], []
    for item in sorted(dir_path.iterdir()):
        if item.name.startswith(".") or item.name in SKIP:
            continue
        if item.is_dir():
            subdirs.append(item)
        elif item.is_file() and item.suffix == ".md" and item.name != "index.md":
            files.append(item)

    for f in files:
        entries.append(f"{prefix}/{f.name}")

    for d in subdirs:
        label = SUB_LABELS.get(d.name, d.name)
        children = scan(d, f"{prefix}/{d.name}")
        entries.append({label: children})

    return entries


def to_toml(items, depth=1) -> str:
    pad = "    " * depth
    lines = []
    for item in items:
        if isinstance(item, str):
            lines.append(f'{pad}"{item}",')
        else:
            for label, value in item.items():
                if isinstance(value, str):
                    lines.append(f'{pad}{{ "{label}" = "{value}" }},')
                else:
                    inner = to_toml(value, depth + 1)
                    lines.append(f'{pad}{{ "{label}" = [')
                    lines.append(inner)
                    lines.append(f'{pad}]}},')
    return "\n".join(lines)


nav_entries = []
for path, label in TOP_LEVEL:
    target = DOCS_DIR / path
    if target.is_file():
        nav_entries.append({label: path})
    elif target.is_dir():
        children = scan(target, path)
        nav_entries.append({label: children})

nav_block = "nav = [\n" + to_toml(nav_entries) + "\n]"

original = TOML_PATH.read_text(encoding="utf-8")
updated = re.sub(
    r"^nav = \[.*?^\]",
    nav_block,
    original,
    flags=re.MULTILINE | re.DOTALL,
)
TOML_PATH.write_text(updated, encoding="utf-8")
print("nav updated in zensical.toml")
