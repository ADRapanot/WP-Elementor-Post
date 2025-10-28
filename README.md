# WP Elementor Post — README

This project publishes posts to WordPress with Elementor components and Ultimate FAQ items. It includes utilities to:

- Publish articles with an Elementor Table of Contents.
- Publish Elementor Accordion FAQ items and FAQ schema.

This README explains configuration and how to run the included scripts.

## Files of interest

- `wordpress_service.py` — low-level HTTP client and helpers for interacting with the WP REST API.
- `publish_elementor_widgets.py` — example scripts demonstrating usage.

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
