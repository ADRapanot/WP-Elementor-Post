"""Configuration loader for WP Elementor project.

This module loads `wp_config.json` from the repository root and exposes a `get_config()` function.
"""
import json
from pathlib import Path

_config = None

def get_config():
    global _config
    if _config is None:
        p = Path(__file__).resolve().parent / 'config.json'
        if p.exists():
            try:
                _config = json.loads(p.read_text())
            except Exception:
                _config = {}
        else:
            _config = {}
    return _config




