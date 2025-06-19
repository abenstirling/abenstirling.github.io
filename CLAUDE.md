# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal website built with Zola, a fast static site generator. The site uses the "no-style-please" theme, which is a minimalist, nearly CSS-free theme that emphasizes content over styling.

## Commands

### Development
- `zola serve` - Start development server with hot reload
- `zola build` - Build the static site (outputs to `public/` directory)
- `zola check` - Validate links and content without building

### Content Management
- Content files are in `content/` directory as Markdown files
- Main site content is in `content/_index.md`
- Each page should have YAML frontmatter with metadata

## Architecture

### Key Directories
- `content/` - Site content in Markdown format
- `templates/` - Custom templates (inherits from theme)
- `static/` - Static assets (images, files)
- `sass/` - Custom Sass/SCSS files
- `public/` - Generated site output (not in git)
- `themes/no-style-please/` - Theme files

### Configuration
- `config.toml` - Main site configuration
- `base_url = "https://abenstirling.com"`
- Theme: "no-style-please" 
- Features enabled: Sass compilation, search index, syntax highlighting

### Theme Features
- Minimalist design with optional dark mode
- Built-in taxonomies: tags, categories, contexts
- Special shortcodes: `hr()` for horizontal rules, `iimg()` for invertible images
- Optional table of contents with `extra.add_toc = true`
- Navigation can be configured in `config.toml` under `[extra]`

### Content Structure
- Pages use standard Zola frontmatter format
- Taxonomies defined in page metadata under `[taxonomies]`
- Author and image metadata supported for SEO
- Twitter card generation enabled by default