#!/usr/bin/env python3
"""
CSV-to-Obsidian Converter for UI/UX Pro Max

Converts all CSV databases into Obsidian-compatible Markdown notes
with YAML frontmatter for Dataview queries, wikilinks, and tags.

Usage:
    python3 scripts/csv_to_obsidian.py --output "/path/to/vault/Skills/UI-UX-Pro-Max"
    python3 scripts/csv_to_obsidian.py --output "./obsidian-output"  # local preview
"""

import argparse
import csv
import os
import re
import shutil
from pathlib import Path

SRC_DATA = Path(__file__).resolve().parent.parent / "src" / "ui-ux-pro-max" / "data"
SRC_SCRIPTS = Path(__file__).resolve().parent.parent / "src" / "ui-ux-pro-max" / "scripts"

DOMAIN_FOLDERS = {
    "styles": ("01 - Styles", "style"),
    "colors": ("02 - Colors", "color"),
    "typography": ("03 - Typography", "typography"),
    "ux-guidelines": ("04 - UX Guidelines", "ux"),
    "charts": ("05 - Charts", "chart"),
    "landing": ("06 - Landing Pages", "landing"),
    "products": ("07 - Products", "product"),
    "icons": ("08 - Icons", "icon"),
    "ui-reasoning": ("09 - Reasoning Rules", "reasoning"),
    "react-performance": ("10 - React Performance", "react"),
    "web-interface": ("11 - Web Interface", "web"),
}


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name[:100]


def yaml_safe(value: str) -> str:
    if not value:
        return '""'
    if any(c in value for c in (':', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`', '"', "'")):
        return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return value


def split_keywords(text: str) -> list:
    if not text:
        return []
    return [k.strip() for k in re.split(r'[,;]', text) if k.strip()]


def make_frontmatter(fields: dict) -> str:
    lines = ["---"]
    for key, value in fields.items():
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {yaml_safe(item)}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        else:
            lines.append(f"{key}: {yaml_safe(str(value))}")
    lines.append("---")
    return "\n".join(lines)


# ── Converters per domain ──────────────────────────────────────────────

def convert_styles(rows: list, out_dir: Path):
    index_lines = [
        "# UI Styles Index\n",
        "#uiux/style\n",
        "| Style | Type | Complexity | Performance | Accessibility | Best For |",
        "|-------|------|-----------|-------------|---------------|----------|",
    ]
    for row in rows:
        name = row.get("Style Category", "").strip()
        if not name:
            continue
        fname = sanitize_filename(name)
        fm = make_frontmatter({
            "type": "style",
            "category": row.get("Type", ""),
            "keywords": split_keywords(row.get("Keywords", "")),
            "primary_colors": row.get("Primary Colors", ""),
            "secondary_colors": row.get("Secondary Colors", ""),
            "best_for": split_keywords(row.get("Best For", "")),
            "do_not_use_for": split_keywords(row.get("Do Not Use For", "")),
            "light_mode": "✓" in row.get("Light Mode ✓", ""),
            "dark_mode": "✓" in row.get("Dark Mode ✓", ""),
            "performance": row.get("Performance", "").replace("⚡ ", "").replace("⚠ ", "").replace("❌ ", ""),
            "accessibility": row.get("Accessibility", "").replace("✓ ", "").replace("⚠ ", ""),
            "mobile_friendly": row.get("Mobile-Friendly", ""),
            "complexity": row.get("Complexity", ""),
            "framework_compatibility": row.get("Framework Compatibility", ""),
            "era": row.get("Era/Origin", ""),
            "tags": ["uiux/style"],
        })
        body = f"\n# {name}\n\n"
        body += f"**Type:** {row.get('Type', '')}\n"
        body += f"**Complexity:** {row.get('Complexity', '')}\n"
        body += f"**Era:** {row.get('Era/Origin', '')}\n\n"
        body += "## Effects & Animation\n\n"
        body += f"{row.get('Effects & Animation', '')}\n\n"
        body += "## AI Prompt\n\n"
        body += f"> {row.get('AI Prompt Keywords', '')}\n\n"
        body += "## CSS / Technical Keywords\n\n"
        body += f"`{row.get('CSS/Technical Keywords', '')}`\n\n"
        body += "## Implementation Checklist\n\n"
        for item in row.get("Implementation Checklist", "").split("☐"):
            item = item.strip().rstrip(",").strip()
            if item:
                body += f"- [ ] {item}\n"
        body += "\n## Design System Variables\n\n"
        body += f"```css\n{row.get('Design System Variables', '')}\n```\n"
        (out_dir / f"{fname}.md").write_text(fm + body, encoding="utf-8")
        perf = row.get("Performance", "")
        acc = row.get("Accessibility", "")
        best = row.get("Best For", "")[:40]
        index_lines.append(f"| [[{fname}]] | {row.get('Type','')} | {row.get('Complexity','')} | {perf} | {acc} | {best} |")
    (out_dir / "_Styles Index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def convert_colors(rows: list, out_dir: Path):
    index_lines = [
        "# Color Palettes Index\n",
        "#uiux/color\n",
        "| Product Type | Primary | Secondary | CTA | Background | Text |",
        "|-------------|---------|-----------|-----|------------|------|",
    ]
    for row in rows:
        name = row.get("Product Type", "").strip()
        if not name:
            continue
        fname = sanitize_filename(name)
        fm = make_frontmatter({
            "type": "color",
            "product_type": name,
            "primary": row.get("Primary (Hex)", ""),
            "secondary": row.get("Secondary (Hex)", ""),
            "cta": row.get("CTA (Hex)", ""),
            "background": row.get("Background (Hex)", ""),
            "text_color": row.get("Text (Hex)", ""),
            "border": row.get("Border (Hex)", ""),
            "tags": ["uiux/color"],
        })
        body = f"\n# {name} - Color Palette\n\n"
        body += "| Role | Hex |\n|------|-----|\n"
        body += f"| Primary | `{row.get('Primary (Hex)', '')}` |\n"
        body += f"| Secondary | `{row.get('Secondary (Hex)', '')}` |\n"
        body += f"| CTA | `{row.get('CTA (Hex)', '')}` |\n"
        body += f"| Background | `{row.get('Background (Hex)', '')}` |\n"
        body += f"| Text | `{row.get('Text (Hex)', '')}` |\n"
        body += f"| Border | `{row.get('Border (Hex)', '')}` |\n\n"
        body += f"**Notes:** {row.get('Notes', '')}\n"
        (out_dir / f"{fname}.md").write_text(fm + body, encoding="utf-8")
        index_lines.append(
            f"| [[{fname}]] | `{row.get('Primary (Hex)','')}` | `{row.get('Secondary (Hex)','')}` | `{row.get('CTA (Hex)','')}` | `{row.get('Background (Hex)','')}` | `{row.get('Text (Hex)','')}` |"
        )
    (out_dir / "_Colors Index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def convert_typography(rows: list, out_dir: Path):
    index_lines = [
        "# Typography Index\n",
        "#uiux/typography\n",
        "| Pairing | Category | Heading | Body | Mood |",
        "|---------|----------|---------|------|------|",
    ]
    for row in rows:
        name = row.get("Font Pairing Name", "").strip()
        if not name:
            continue
        fname = sanitize_filename(name)
        fm = make_frontmatter({
            "type": "typography",
            "category": row.get("Category", ""),
            "heading_font": row.get("Heading Font", ""),
            "body_font": row.get("Body Font", ""),
            "keywords": split_keywords(row.get("Mood/Style Keywords", "")),
            "best_for": split_keywords(row.get("Best For", "")),
            "tags": ["uiux/typography"],
        })
        body = f"\n# {name}\n\n"
        body += f"**Category:** {row.get('Category', '')}\n"
        body += f"**Heading:** {row.get('Heading Font', '')}\n"
        body += f"**Body:** {row.get('Body Font', '')}\n\n"
        body += f"**Mood:** {row.get('Mood/Style Keywords', '')}\n"
        body += f"**Best For:** {row.get('Best For', '')}\n\n"
        body += "## Google Fonts\n\n"
        body += f"[Preview on Google Fonts]({row.get('Google Fonts URL', '')})\n\n"
        body += "## CSS Import\n\n"
        body += f"```css\n{row.get('CSS Import', '')}\n```\n\n"
        body += "## Tailwind Config\n\n"
        body += f"```js\n{row.get('Tailwind Config', '')}\n```\n\n"
        if row.get("Notes"):
            body += f"**Notes:** {row.get('Notes', '')}\n"
        (out_dir / f"{fname}.md").write_text(fm + body, encoding="utf-8")
        mood = row.get("Mood/Style Keywords", "")[:30]
        index_lines.append(
            f"| [[{fname}]] | {row.get('Category','')} | {row.get('Heading Font','')} | {row.get('Body Font','')} | {mood} |"
        )
    (out_dir / "_Typography Index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def convert_ux_guidelines(rows: list, out_dir: Path):
    index_lines = [
        "# UX Guidelines Index\n",
        "#uiux/ux\n",
        "| Issue | Category | Platform | Severity |",
        "|-------|----------|----------|----------|",
    ]
    for row in rows:
        issue = row.get("Issue", "").strip()
        if not issue:
            continue
        category = row.get("Category", "")
        fname = sanitize_filename(f"{category} - {issue}")
        fm = make_frontmatter({
            "type": "ux-guideline",
            "category": category,
            "platform": row.get("Platform", ""),
            "severity": row.get("Severity", ""),
            "tags": ["uiux/ux"],
        })
        body = f"\n# {issue}\n\n"
        body += f"**Category:** {category}\n"
        body += f"**Platform:** {row.get('Platform', '')}\n"
        body += f"**Severity:** {row.get('Severity', '')}\n\n"
        body += f"{row.get('Description', '')}\n\n"
        body += "## Do\n\n"
        body += f"{row.get('Do', '')}\n\n"
        body += "## Don't\n\n"
        dont_val = row.get("Don't", "")
        body += f"{dont_val}\n\n"
        good_code = row.get("Code Example Good", "")
        bad_code = row.get("Code Example Bad", "")
        if good_code:
            body += "## Good Example\n\n"
            body += f"```\n{good_code}\n```\n\n"
        if bad_code:
            body += "## Bad Example\n\n"
            body += f"```\n{bad_code}\n```\n"
        (out_dir / f"{fname}.md").write_text(fm + body, encoding="utf-8")
        index_lines.append(f"| [[{fname}]] | {category} | {row.get('Platform','')} | {row.get('Severity','')} |")
    (out_dir / "_UX Index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def convert_charts(rows: list, out_dir: Path):
    index_lines = [
        "# Charts Index\n",
        "#uiux/chart\n",
        "| Data Type | Best Chart | Library | Interactive |",
        "|-----------|------------|---------|-------------|",
    ]
    for row in rows:
        name = row.get("Data Type", "").strip()
        if not name:
            continue
        fname = sanitize_filename(name)
        fm = make_frontmatter({
            "type": "chart",
            "keywords": split_keywords(row.get("Keywords", "")),
            "best_chart": row.get("Best Chart Type", ""),
            "library": row.get("Library Recommendation", ""),
            "tags": ["uiux/chart"],
        })
        body = f"\n# {name}\n\n"
        body += f"**Best Chart Type:** {row.get('Best Chart Type', '')}\n"
        body += f"**Secondary Options:** {row.get('Secondary Options', '')}\n\n"
        body += f"**Color Guidance:** {row.get('Color Guidance', '')}\n"
        body += f"**Performance:** {row.get('Performance Impact', '')}\n"
        body += f"**Accessibility:** {row.get('Accessibility Notes', '')}\n\n"
        body += f"**Recommended Library:** {row.get('Library Recommendation', '')}\n"
        body += f"**Interactive Level:** {row.get('Interactive Level', '')}\n"
        (out_dir / f"{fname}.md").write_text(fm + body, encoding="utf-8")
        index_lines.append(
            f"| [[{fname}]] | {row.get('Best Chart Type','')} | {row.get('Library Recommendation','')} | {row.get('Interactive Level','')} |"
        )
    (out_dir / "_Charts Index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def convert_landing(rows: list, out_dir: Path):
    index_lines = [
        "# Landing Page Patterns Index\n",
        "#uiux/landing\n",
        "| Pattern | CTA Placement | Conversion |",
        "|---------|---------------|------------|",
    ]
    for row in rows:
        name = row.get("Pattern Name", "").strip()
        if not name:
            continue
        fname = sanitize_filename(name)
        fm = make_frontmatter({
            "type": "landing",
            "keywords": split_keywords(row.get("Keywords", "")),
            "tags": ["uiux/landing"],
        })
        body = f"\n# {name}\n\n"
        body += "## Section Order\n\n"
        for section in row.get("Section Order", "").split(","):
            section = section.strip()
            if section:
                body += f"1. {section}\n"
        body += f"\n**CTA Placement:** {row.get('Primary CTA Placement', '')}\n"
        body += f"**Color Strategy:** {row.get('Color Strategy', '')}\n"
        body += f"**Effects:** {row.get('Recommended Effects', '')}\n\n"
        body += "## Conversion Optimization\n\n"
        body += f"{row.get('Conversion Optimization', '')}\n"
        (out_dir / f"{fname}.md").write_text(fm + body, encoding="utf-8")
        conv = row.get("Conversion Optimization", "")[:50]
        index_lines.append(f"| [[{fname}]] | {row.get('Primary CTA Placement','')} | {conv} |")
    (out_dir / "_Landing Index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def convert_products(rows: list, out_dir: Path):
    index_lines = [
        "# Product Types Index\n",
        "#uiux/product\n",
        "| Product Type | Primary Style | Landing Pattern | Color Focus |",
        "|-------------|---------------|-----------------|-------------|",
    ]
    for row in rows:
        name = row.get("Product Type", "").strip()
        if not name:
            continue
        fname = sanitize_filename(name)
        fm = make_frontmatter({
            "type": "product",
            "keywords": split_keywords(row.get("Keywords", "")),
            "primary_style": row.get("Primary Style Recommendation", ""),
            "secondary_styles": split_keywords(row.get("Secondary Styles", "")),
            "landing_pattern": row.get("Landing Page Pattern", ""),
            "color_focus": row.get("Color Palette Focus", ""),
            "tags": ["uiux/product"],
        })
        body = f"\n# {name}\n\n"
        body += f"**Primary Style:** {row.get('Primary Style Recommendation', '')}\n"
        body += f"**Secondary Styles:** {row.get('Secondary Styles', '')}\n\n"
        body += f"**Landing Page Pattern:** {row.get('Landing Page Pattern', '')}\n"
        body += f"**Dashboard Style:** {row.get('Dashboard Style (if applicable)', '')}\n"
        body += f"**Color Focus:** {row.get('Color Palette Focus', '')}\n\n"
        body += "## Key Considerations\n\n"
        body += f"{row.get('Key Considerations', '')}\n"
        (out_dir / f"{fname}.md").write_text(fm + body, encoding="utf-8")
        index_lines.append(
            f"| [[{fname}]] | {row.get('Primary Style Recommendation','')} | {row.get('Landing Page Pattern','')} | {row.get('Color Palette Focus','')} |"
        )
    (out_dir / "_Products Index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def convert_icons(rows: list, out_dir: Path):
    index_lines = [
        "# Icons Index\n",
        "#uiux/icon\n",
        "| Icon | Category | Library | Best For |",
        "|------|----------|---------|----------|",
    ]
    for row in rows:
        name = row.get("Icon Name", "").strip()
        if not name:
            continue
        category = row.get("Category", "")
        fname = sanitize_filename(f"{category} - {name}")
        fm = make_frontmatter({
            "type": "icon",
            "category": category,
            "library": row.get("Library", ""),
            "keywords": split_keywords(row.get("Keywords", "")),
            "style": row.get("Style", ""),
            "tags": ["uiux/icon"],
        })
        body = f"\n# {name}\n\n"
        body += f"**Category:** {category}\n"
        body += f"**Library:** {row.get('Library', '')}\n"
        body += f"**Style:** {row.get('Style', '')}\n"
        body += f"**Best For:** {row.get('Best For', '')}\n\n"
        body += "## Import\n\n"
        body += f"```jsx\n{row.get('Import Code', '')}\n```\n\n"
        body += "## Usage\n\n"
        body += f"```jsx\n{row.get('Usage', '')}\n```\n"
        (out_dir / f"{fname}.md").write_text(fm + body, encoding="utf-8")
        index_lines.append(f"| [[{fname}]] | {category} | {row.get('Library','')} | {row.get('Best For','')[:40]} |")
    (out_dir / "_Icons Index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def convert_reasoning(rows: list, out_dir: Path):
    index_lines = [
        "# UI Reasoning Rules Index\n",
        "#uiux/reasoning\n",
        "| UI Category | Pattern | Style Priority | Severity |",
        "|-------------|---------|---------------|----------|",
    ]
    for row in rows:
        category = row.get("UI_Category", "").strip()
        if not category:
            continue
        fname = sanitize_filename(f"Rule - {category}")
        fm = make_frontmatter({
            "type": "reasoning",
            "ui_category": category,
            "pattern": row.get("Recommended_Pattern", ""),
            "style_priority": row.get("Style_Priority", ""),
            "severity": row.get("Severity", ""),
            "tags": ["uiux/reasoning"],
        })
        body = f"\n# {category}\n\n"
        body += f"**Recommended Pattern:** {row.get('Recommended_Pattern', '')}\n"
        body += f"**Style Priority:** {row.get('Style_Priority', '')}\n"
        body += f"**Color Mood:** {row.get('Color_Mood', '')}\n"
        body += f"**Typography Mood:** {row.get('Typography_Mood', '')}\n"
        body += f"**Key Effects:** {row.get('Key_Effects', '')}\n\n"
        body += "## Decision Rules\n\n"
        body += f"```json\n{row.get('Decision_Rules', '')}\n```\n\n"
        body += "## Anti-Patterns\n\n"
        body += f"{row.get('Anti_Patterns', '')}\n"
        (out_dir / f"{fname}.md").write_text(fm + body, encoding="utf-8")
        index_lines.append(
            f"| [[{fname}]] | {row.get('Recommended_Pattern','')} | {row.get('Style_Priority','')} | {row.get('Severity','')} |"
        )
    (out_dir / "_Reasoning Index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def convert_generic(rows: list, out_dir: Path, csv_name: str, tag: str):
    """Fallback converter for CSVs without a specialized handler."""
    if not rows:
        return
    headers = list(rows[0].keys())
    name_col = headers[1] if len(headers) > 1 else headers[0]
    index_lines = [
        f"# {csv_name.replace('-', ' ').title()} Index\n",
        f"#uiux/{tag}\n",
        "| " + " | ".join(headers[:5]) + " |",
        "|" + "|".join(["-----"] * min(len(headers), 5)) + "|",
    ]
    for row in rows:
        name = row.get(name_col, "").strip()
        if not name:
            continue
        fname = sanitize_filename(name)
        fm = make_frontmatter({
            "type": tag,
            "tags": [f"uiux/{tag}"],
        })
        body = f"\n# {name}\n\n"
        for h in headers:
            if h == "No":
                continue
            body += f"**{h}:** {row.get(h, '')}\n\n"
        (out_dir / f"{fname}.md").write_text(fm + body, encoding="utf-8")
        cols = [row.get(h, "")[:40] for h in headers[:5]]
        index_lines.append("| " + " | ".join(cols) + " |")
    (out_dir / f"_{csv_name.replace('-',' ').title()} Index.md").write_text(
        "\n".join(index_lines) + "\n", encoding="utf-8"
    )


def convert_stacks(stacks_dir: Path, out_dir: Path):
    """Convert stack CSVs into Obsidian notes."""
    out_dir.mkdir(parents=True, exist_ok=True)
    index_lines = [
        "# Stack Guidelines Index\n",
        "#uiux/stack\n",
        "Each stack file contains framework-specific best practices.\n",
    ]
    for csv_file in sorted(stacks_dir.glob("*.csv")):
        stack_name = csv_file.stem
        rows = list(csv.DictReader(open(csv_file, encoding="utf-8")))
        if not rows:
            continue
        display_name = stack_name.replace("-", " ").title()
        fname = sanitize_filename(display_name)

        fm = make_frontmatter({
            "type": "stack",
            "stack": stack_name,
            "guideline_count": len(rows),
            "tags": ["uiux/stack"],
        })
        body = f"\n# {display_name} Guidelines\n\n"
        body += f"**{len(rows)} guidelines**\n\n"
        headers = list(rows[0].keys())
        for row in rows:
            title_col = next((h for h in headers if h.lower() in ("guideline", "category", "issue")), headers[1] if len(headers) > 1 else headers[0])
            title = row.get(title_col, "Untitled")
            body += f"## {title}\n\n"
            for h in headers:
                if h == "No":
                    continue
                val = (row.get(h) or "").strip()
                if not val:
                    continue
                if h.lower() in ("code good", "code_good"):
                    body += f"**Good:**\n```\n{val}\n```\n\n"
                elif h.lower() in ("code bad", "code_bad"):
                    body += f"**Bad:**\n```\n{val}\n```\n\n"
                elif h == title_col:
                    continue
                else:
                    body += f"**{h}:** {val}\n\n"
            body += "---\n\n"
        (out_dir / f"{fname}.md").write_text(fm + body, encoding="utf-8")
        index_lines.append(f"- [[{fname}]] ({len(rows)} guidelines)")
    (out_dir / "_Stacks Index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


CONVERTERS = {
    "styles": convert_styles,
    "colors": convert_colors,
    "typography": convert_typography,
    "ux-guidelines": convert_ux_guidelines,
    "charts": convert_charts,
    "landing": convert_landing,
    "products": convert_products,
    "icons": convert_icons,
    "ui-reasoning": convert_reasoning,
}


def create_master_index(out_dir: Path, stats: dict):
    content = "# UI/UX Pro Max - Design Intelligence\n\n"
    content += "#uiux\n\n"
    content += "AI-powered design intelligence toolkit. Searchable databases of styles, colors, fonts, charts, and UX guidelines.\n\n"
    content += "## Quick Stats\n\n"
    content += "| Domain | Count |\n|--------|-------|\n"
    for domain, count in stats.items():
        content += f"| {domain} | {count} |\n"
    content += "\n## Sections\n\n"
    for csv_name, (folder, _) in sorted(DOMAIN_FOLDERS.items(), key=lambda x: x[1][0]):
        content += f"- [[{folder}/_{''.join(w.title() for w in csv_name.replace('-', ' ').split())} Index|{folder}]]\n"
    content += "- [[08 - Stacks/_Stacks Index|08 - Stacks]]\n\n"
    content += "## Search Engine\n\n"
    content += "The `_engine/` folder contains the Python search engine for AI assistants:\n\n"
    content += "```bash\npython3 _engine/scripts/search.py \"<query>\" --domain <domain>\npython3 _engine/scripts/search.py \"<query>\" --design-system -p \"Project Name\"\n```\n\n"
    content += "## Dataview Queries\n\n"
    content += "### All Styles by Complexity\n\n"
    content += "```dataview\nTABLE keywords, performance, complexity\nFROM #uiux/style\nSORT complexity ASC\n```\n\n"
    content += "### Color Palettes for SaaS\n\n"
    content += '```dataview\nTABLE primary, secondary, cta\nFROM #uiux/color\nWHERE contains(product_type, "SaaS")\n```\n\n'
    content += "### High-Severity UX Issues\n\n"
    content += '```dataview\nTABLE category, platform, severity\nFROM #uiux/ux\nWHERE severity = "High"\nSORT category ASC\n```\n'
    (out_dir / "00 - Index.md").write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Convert UI/UX Pro Max CSVs to Obsidian Markdown")
    parser.add_argument("--output", "-o", required=True, help="Output directory for Obsidian notes")
    parser.add_argument("--include-engine", action="store_true", default=True,
                        help="Copy Python search engine to _engine/ (default: true)")
    args = parser.parse_args()

    out_root = Path(args.output).resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    stats = {}

    for csv_name, (folder, tag) in DOMAIN_FOLDERS.items():
        csv_path = SRC_DATA / f"{csv_name}.csv"
        if not csv_path.exists():
            print(f"  Skipping {csv_name} (not found)")
            continue
        folder_path = out_root / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        with open(csv_path, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        converter = CONVERTERS.get(csv_name, lambda r, d: convert_generic(r, d, csv_name, tag))
        converter(rows, folder_path)
        stats[folder] = len(rows)
        print(f"  {folder}: {len(rows)} notes")

    stacks_dir = SRC_DATA / "stacks"
    if stacks_dir.exists():
        stacks_out = out_root / "08 - Stacks"
        convert_stacks(stacks_dir, stacks_out)
        stack_count = len(list(stacks_dir.glob("*.csv")))
        stats["08 - Stacks"] = stack_count
        print(f"  08 - Stacks: {stack_count} stack files")

    create_master_index(out_root, stats)
    print(f"  00 - Index.md created")

    if args.include_engine:
        engine_dir = out_root / "_engine"
        if engine_dir.exists():
            shutil.rmtree(engine_dir)
        engine_scripts = engine_dir / "scripts"
        engine_data = engine_dir / "data"
        shutil.copytree(SRC_SCRIPTS, engine_scripts)
        shutil.copytree(SRC_DATA, engine_data)
        print(f"  _engine/ copied (scripts + data)")

    # Copy workflow file
    skill_content = Path(__file__).resolve().parent.parent / "src" / "ui-ux-pro-max" / "templates" / "base" / "skill-content.md"
    if skill_content.exists():
        content = skill_content.read_text(encoding="utf-8")
        content = content.replace("{{TITLE}}", "UI/UX Pro Max Workflow")
        content = content.replace("{{DESCRIPTION}}", "Design intelligence workflow for AI assistants and human reference.")
        content = content.replace("{{SCRIPT_PATH}}", "_engine/scripts/search.py")
        content = content.replace("{{SKILL_OR_WORKFLOW}}", "Workflow")
        content = content.replace("{{QUICK_REFERENCE}}", "")
        (out_root / "Workflow.md").write_text(content, encoding="utf-8")
        print(f"  Workflow.md created")

    print(f"\nDone! {sum(stats.values())} total entries written to {out_root}")
    print(f"Open in Obsidian and install the Dataview plugin for dynamic queries.")


if __name__ == "__main__":
    main()
