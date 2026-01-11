# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a WordPress-to-GitHub Pages migration project for a Korean lifestyle blog (legoje.com). The site has been converted from WordPress to static HTML hosted on GitHub Pages at `/blog_legoje/`.

## Build Commands

There are no standard build/test/lint tools. The project uses two Python 3 scripts:

```bash
# Extract WordPress backup (.wpress file)
python extract_wpress.py <backup.wpress> <output_dir>

# Build static site from extracted WordPress files
python build_static_site.py
```

**Build workflow:**
1. Extract WordPress backup with `extract_wpress.py`
2. Run `build_static_site.py` to generate the `docs/` folder for GitHub Pages
3. Commit and push `docs/` to deploy

## Architecture

```
blog_legoje/
├── build_static_site.py    # Main build script - generates docs/ from WordPress export
├── extract_wpress.py       # Extracts All-in-One WP Migration .wpress backups
└── docs/                   # GitHub Pages output (deployed content)
    ├── index.html
    ├── .nojekyll           # Disables Jekyll processing
    ├── wp-content/         # WordPress assets (uploads, themes, cache)
    └── [blog posts]/       # ~150 post directories, each with index.html
```

**Key build script behaviors:**
- Rewrites hardcoded `legoje.com` links to `/blog_legoje/` paths
- Removes `-optimized` image suffixes from paths (WordPress optimization artifacts)
- Bundles CSS/JS from WP Fast Cache minified files
- Creates 404.html and .nojekyll

## Technical Notes

- **No external dependencies** - Python standard library only
- **Hardcoded paths** - Scripts contain absolute paths that need updating for different environments
- **Comments in Korean** - Docstrings and comments are written in Korean
- **Regex-based HTML manipulation** - Link rewriting uses regex patterns, not DOM parsing
- **Original stack:** WordPress 6.8.3, GeneratePress theme, WP Fast Cache, Rank Math SEO