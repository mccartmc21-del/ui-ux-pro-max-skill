# Obsidian Integration Plan for UI/UX Pro Max

**For:** michael.mccarthy@hearst.com
**Target Vault:** Hearst (Google Drive)
**Date:** 2026-02-25

---

## Repository Summary

UI/UX Pro Max (Antigravity Kit) is an AI-powered design intelligence toolkit containing:

| Asset | Count | Format |
|-------|-------|--------|
| UI Styles | 67 | CSV with AI prompts, CSS keywords, checklists |
| Color Palettes | 96 | CSV with hex codes by product type |
| Font Pairings | 57 | CSV with Google Fonts imports + Tailwind config |
| UX Guidelines | 99 | CSV with Do/Don't + code examples |
| Chart Types | 25 | CSV with library recommendations |
| Landing Page Patterns | varies | CSV with section orders + CTA strategies |
| Product Type Guides | 100+ | CSV with style/color/layout recs per industry |
| Stack Guidelines | 13 stacks | CSV (React, Next.js, Vue, Svelte, Flutter, etc.) |
| Reasoning Rules | 100 | CSV for AI design system generation |

It also includes a **Python search engine** (BM25 + regex, zero dependencies) and a **Design System Generator** that synthesizes multi-domain recommendations.

---

## Recommended Obsidian Integration Strategies

### Strategy 1: Reference Vault (Low Effort, High Value)

Copy the skill content and CSV databases directly into your Obsidian vault as Markdown notes, organized into a dedicated folder structure.

**Proposed vault structure:**

```
Hearst/
└── Skills/
    └── UI-UX-Pro-Max/
        ├── 00 - Index.md              ← Master index with links to all sections
        ├── 01 - Styles/
        │   ├── _Styles Index.md       ← Table of all 67 styles
        │   ├── Minimalism.md          ← Individual style notes (one per style)
        │   ├── Glassmorphism.md
        │   ├── Brutalism.md
        │   └── ...
        ├── 02 - Colors/
        │   ├── _Colors Index.md       ← All 96 palettes in a table
        │   ├── SaaS General.md        ← Individual palette notes
        │   ├── E-commerce.md
        │   └── ...
        ├── 03 - Typography/
        │   ├── _Typography Index.md   ← All 57 pairings
        │   ├── Classic Elegant.md
        │   ├── Modern Professional.md
        │   └── ...
        ├── 04 - UX Guidelines/
        │   ├── _UX Index.md
        │   ├── Animation.md           ← Grouped by category
        │   ├── Accessibility.md
        │   └── ...
        ├── 05 - Charts/
        │   ├── _Charts Index.md
        │   └── ...
        ├── 06 - Landing Pages/
        │   ├── _Landing Index.md
        │   └── ...
        ├── 07 - Products/
        │   ├── _Products Index.md
        │   └── ...
        ├── 08 - Stacks/
        │   ├── React.md
        │   ├── Next.js.md
        │   ├── Vue.md
        │   └── ...
        ├── 09 - Reasoning Rules/
        │   └── _Reasoning Index.md    ← 100 industry-specific rules
        ├── Workflow.md                ← The skill workflow (from SKILL.md)
        └── Checklists.md             ← Pre-delivery + implementation checklists
```

**Why this works well:**
- Obsidian's full-text search replaces the BM25 engine for human lookup
- Wikilinks (`[[Glassmorphism]]`) create a connected knowledge graph
- Tags (#style, #color, #typography) enable Dataview queries
- Each note can have YAML frontmatter for structured metadata
- Compatible with Google Drive sync (just Markdown files)

### Strategy 2: Dataview-Powered Database (Medium Effort, Highest Value)

Convert CSVs into Markdown notes with YAML frontmatter, then use the Dataview plugin to create dynamic dashboards.

**Example style note (`Glassmorphism.md`):**

```yaml
---
type: style
category: General
keywords:
  - frosted glass
  - transparent
  - blurred background
  - layered
primary_colors: "rgba(255,255,255,0.1-0.3)"
effects: "backdrop blur (10-20px), subtle border"
best_for:
  - Modern SaaS
  - financial dashboards
  - high-end corporate
light_mode: true
dark_mode: true
performance: Good
accessibility: "Ensure 4.5:1"
complexity: Medium
---

# Glassmorphism

## AI Prompt
> Design a glassmorphic interface with frosted glass effect...

## CSS Keywords
`backdrop-filter: blur(15px)`, `background: rgba(255,255,255,0.15)`...

## Implementation Checklist
- [ ] Backdrop-filter blur 10-20px
- [ ] Translucent white 15-30% opacity
- [ ] Subtle border 1px light
- [ ] Vibrant background verified
- [ ] Text contrast 4.5:1 checked
```

**Example Dataview query (in an index note):**

```dataview
TABLE keywords, performance, accessibility
FROM "Skills/UI-UX-Pro-Max/01 - Styles"
WHERE type = "style" AND performance = "Excellent"
SORT complexity ASC
```

### Strategy 3: Hybrid (Scripts + Vault)

Keep the Python search engine alongside the vault for AI-assistant usage, while the Markdown notes serve as the human-readable reference.

**Proposed setup:**

```
Hearst/
├── Skills/
│   └── UI-UX-Pro-Max/
│       ├── (Markdown notes as in Strategy 1 or 2)
│       └── _engine/
│           ├── scripts/          ← search.py, core.py, design_system.py
│           └── data/             ← Original CSVs (source of truth)
```

This way:
- You can run `python3 _engine/scripts/search.py "query" --domain style` from a terminal
- Obsidian displays the human-friendly Markdown notes
- AI assistants (Cursor, Claude Code) can use the search engine directly
- Updates to CSVs can be re-converted to Markdown via a script

---

## Recommended Approach for Hearst Vault

**I recommend Strategy 2 (Dataview-Powered)** for the following reasons:

1. **Hearst editorial context** - Your team likely needs to reference design guidelines during content/product work. Dataview tables make this instant.

2. **Google Drive compatibility** - Pure Markdown files sync perfectly with Google Drive. No binary files, no database issues.

3. **Cross-team sharing** - Other team members with Obsidian can open the same vault from Google Drive and get the same experience.

4. **AI assistant integration** - You can still point Cursor/Claude Code to the `_engine/` subfolder for automated design system generation while the Markdown notes serve as human reference.

5. **Maintenance** - A conversion script (provided below) can regenerate Markdown from CSVs whenever the upstream repo updates.

---

## Implementation Steps

### Step 1: Set Up the Folder Structure

In your Google Drive Obsidian vault (`Hearst`), create:

```
Skills/UI-UX-Pro-Max/
```

### Step 2: Run the CSV-to-Obsidian Converter

A conversion script (`scripts/csv_to_obsidian.py`) has been added to this repo. Run it with:

```bash
python3 scripts/csv_to_obsidian.py --output "/path/to/Google Drive/Hearst/Skills/UI-UX-Pro-Max"
```

This will:
- Read all CSVs from `src/ui-ux-pro-max/data/`
- Generate individual Markdown notes with YAML frontmatter
- Create index files with Dataview-compatible tables
- Copy the search engine scripts to `_engine/`

### Step 3: Install Recommended Obsidian Plugins

| Plugin | Purpose |
|--------|---------|
| **Dataview** | Query and filter design data with SQL-like syntax |
| **Templater** | Create new style/color/typography notes from templates |
| **Kanban** | Track design system implementation progress |
| **Style Settings** | Customize vault appearance per-project |
| **Excalidraw** | Wireframe and sketch alongside reference data |

### Step 4: Configure Tags and Links

The converter generates these tags automatically:

- `#uiux/style` - All style entries
- `#uiux/color` - All color palettes
- `#uiux/typography` - All font pairings
- `#uiux/ux` - UX guidelines
- `#uiux/chart` - Chart types
- `#uiux/landing` - Landing page patterns
- `#uiux/product` - Product type guides
- `#uiux/stack` - Stack-specific guidelines

### Step 5: Sync Strategy

Since your vault is on Google Drive:

1. **Upstream updates**: When UI/UX Pro Max releases a new version, pull changes and re-run the converter
2. **Personal additions**: Add your own notes alongside the generated ones (the converter won't overwrite files with a `custom: true` frontmatter field)
3. **Team sharing**: Other Hearst team members can access the vault via shared Google Drive folder

---

## Keeping the AI Skill Active

To use this as an AI coding skill in your projects (separate from Obsidian), you can still run:

```bash
npx uipro-cli init --ai cursor   # For Cursor projects
npx uipro-cli init --ai claude   # For Claude Code projects
```

This installs the skill files directly into your project's `.cursor/` or `.claude/` folder. The Obsidian vault is complementary -- it's your human-readable, searchable, cross-linked reference library.

---

## File Locations Reference

| What | Where |
|------|-------|
| Source CSVs | `src/ui-ux-pro-max/data/*.csv` |
| Search engine | `src/ui-ux-pro-max/scripts/` |
| Obsidian converter | `scripts/csv_to_obsidian.py` |
| Obsidian output | `Google Drive/Hearst/Skills/UI-UX-Pro-Max/` |
| AI skill (Cursor) | `.cursor/skills/ui-ux-pro-max/` |
| AI skill (Claude) | `.claude/skills/ui-ux-pro-max/` |
