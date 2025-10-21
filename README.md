# WP Elementor Post — README

This project publishes posts to WordPress with Elementor components and Ultimate FAQ items. It includes utilities to:

- Publish articles with an Elementor Table of Contents shortcode.
- Publish Ultimate FAQ items (CPT `ufaq`) and insert an FAQ shortcode and JSON-LD schema.
- Use browser cookies to bypass WAF (Incapsula) challenges for testing.

This README explains configuration, cookie handling, and how to run the included scripts.

## Files of interest

- `elementor_wordpress_service.py` — high-level service that composes Elementor/FAQ content and calls the base WordPress service.
- `wordpress_service.py` — low-level HTTP client and helpers for interacting with the WP REST API.
- `use_cookies.py` — example script that demonstrates loading cookies from Chrome or env and publishing FAQs.
- `test_elementor_service.py`, `test_ufaq_items.py` — example scripts demonstrating usage.
- `wp_config.json` — configuration file for cookies and Elementor template id.
- `.wp_cookies.json` — legacy cookie file (supported fallback).

## Configuration (wp_config.json)

Create or edit `wp_config.json` at the repo root. Example format:

{
"cookies": {
"wordpress*logged_in_abcd1234": "<cookie_value>",
"incap_ses*...": "<cookie*value>",
"visid_incap*...": "<cookie_value>"
},
"elementor_template_id": 1425
}

- `cookies` (optional): key/value pairs copied from your browser session. These are used automatically by the internal request helper if the client has no cookies.
- `elementor_template_id` (optional): the Elementor template id used for the TOC shortcode (defaults to `1425`).

Security note: `wp_config.json` contains secrets. Add it to `.gitignore` or keep cookie values in an environment variable for improved safety. See next section.

## Cookie options

1. Use `wp_config.json` (recommended for quick local testing): paste cookie name/value pairs.
2. Or create `.wp_cookies.json` as a fallback (older approach supported).
3. Or set the `WP_COOKIES_JSON` environment variable with a JSON string containing the cookies.
4. Or use `use_cookies.py` with auto-loading enabled to read cookies from your Chrome profile (requires `browser-cookie3` installed in your venv).

Example (env var):

```bash
export WP_COOKIES_JSON='{"wordpress_logged_in_abcd1234":"<value>", "incap_ses_...":"<value>"}'
./.venv-macos/bin/python use_cookies.py
```

## Running locally (macOS)

1. Create a macOS venv (the repo includes a Windows-style `.venv`; use `.venv-macos` in examples):

```bash
python3 -m venv .venv-macos
```

2. Install dependencies:

```bash
./.venv-macos/bin/python -m pip install -r requirements.txt
```

3. Run the example publisher (uses cookies from `wp_config.json` or `.wp_cookies.json` automatically if present):

```bash
./.venv-macos/bin/python test_elementor_service.py
```

Or run the cookie helper script which can auto-load Chrome cookies:

```bash
AUTO_LOAD_CHROME_COOKIES=1 AUTO_LOAD_DOMAIN=www.idsexpress.net ./.venv-macos/bin/python use_cookies.py
```

## How the code uses cookies

- `wordpress_service._request_json` will attempt to load cookies from `wp_config.json` (`config.get_config()`) when the client has no cookies set. This ensures requests like category lookups and FAQ creation use the same browser session cookies that work in Chrome.
- `use_cookies.py` also demonstrates explicit cookie usage and probing behavior used to prime WAF/session state.

## Troubleshooting

- If requests return an HTML page with an Incapsula iframe, the WAF is blocking API requests. Ensure cookies in `wp_config.json` match a real logged-in browser session that has passed the Incapsula challenge (copy all `incap_ses_*` and `visid_incap_*` cookies if present).
- If cookies expire, refresh them by re-logging in via Chrome and updating `wp_config.json`.

## Next steps you may want

- Add `wp_config.json` to `.gitignore`.
- Add a CLI flag to point to a custom config path.
- Convert example scripts to pytest tests using mocked HTTP (respx) for CI.

If you want, I can make any of the above changes now — which one should I do first?
