# WP Elementor Post — README

This project publishes posts to WordPress with Elementor components and Ultimate FAQ items. It includes utilities to:

- Publish articles with an Elementor Table of Contents shortcode.
- Publish Elementor Accordion FAQ items (CPT `ufaq`) and insert an FAQ shortcode and JSON-LD schema.
- Use browser cookies to bypass WAF (Incapsula) challenges for testing.

This README explains configuration, cookie handling, and how to run the included scripts.

## Files of interest

- `wordpress_service.py` — low-level HTTP client and helpers for interacting with the WP REST API.
- `publish_elementor_widgets.py` — example scripts demonstrating usage.
- `config.json` — configuration file for Elementor template id.

## Configuration (wp_config.json)

Create or edit `config.json` at the repo root. Example format:

{
"elementor_template_id": 1425
}

- `elementor_template_id` (optional): the Elementor template id used for the TOC shortcode (defaults to `1425`).

## Running locally (macOS)

1. Create a macOS venv (the repo includes a Windows-style `.venv`; use `.venv-macos` in examples):

```bash
python3 -m venv .venv-macos
```

2. Install dependencies:

```bash
./.venv-macos/bin/python -m pip install -r requirements.txt
```

3. Run the example publisher:

```bash
./.venv-macos/bin/python publish_elementor_widgets.py
```
