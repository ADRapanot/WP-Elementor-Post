"""
Example script that demonstrates using browser cookies with the ElementorWordPressService.

Usage:
  - Export cookies from Chrome (see README.md)
  - Fill the `cookies` dict below and run with the project's python venv:
      ./.venv-macos/bin/python use_cookies.py

This script is intentionally minimal and for local/manual runs only. Do not commit secret cookie values.
"""
import asyncio
import os
import json
from elementor_wordpress_service import ElementorWordPressService


def load_chrome_cookies(domain: str) -> dict:
    """Attempt to load cookies for `domain` from Chrome's cookie store.

    Requires `browser-cookie3` to be installed and access to the local Chrome profile.
    Returns a dict of cookie_name -> cookie_value.
    """
    try:
        import browser_cookie3
    except Exception:
        print("browser_cookie3 not installed; install via requirements.txt to auto-load cookies")
        return {}

    cookies = {}
    try:
        cj = browser_cookie3.chrome(domain_name=domain)
        for cookie in cj:
            cookies[cookie.name] = cookie.value
    except Exception as e:
        print(f"Failed to read Chrome cookies: {e}")

    return cookies


async def main():
    # Paste or load your cookies here (example keys shown)
    cookies = {
    }

    # Optionally load cookies from an environment variable with JSON content
    env_cookies = os.environ.get('WP_COOKIES_JSON')
    if env_cookies:
        try:
            cookies = json.loads(env_cookies)
        except Exception:
            print("Failed to parse WP_COOKIES_JSON; ignoring")

    # Optionally auto-load Chrome cookies (set AUTO_LOAD_CHROME_COOKIES=1 and DOMAIN)
    if os.environ.get('AUTO_LOAD_CHROME_COOKIES') == '1':
        domain = os.environ.get('AUTO_LOAD_DOMAIN', 'www.idsexpress.net')
        print(f"Attempting to load Chrome cookies for domain: {domain}")
        chrome_cookies = load_chrome_cookies(domain)
        if chrome_cookies:
            cookies.update(chrome_cookies)
            # Print loaded cookie names (mask values)
            print("Loaded cookies:", {k: ('<redacted>' if len(v) > 0 else '<empty>') for k, v in chrome_cookies.items()})

    svc = ElementorWordPressService(
        base_url="https://www.idsexpress.net",
        username="idsexpress@aol.com",
        password="0rVg v8lQ Uo1s wIBA eyPo taCu",
        cookies=cookies
    )

    try:
        faq_items = [
            {"question": "What is this test?", "answer": "Testing cookies-based auth."}
        ]

        # Optional debug: fetch categories endpoint to see what the server returns with cookies
        try:
            from wordpress_service import WordPressService
            tmp = WordPressService(base_url="https://www.idsexpress.net", username="", password="", cookies=cookies)
            # try a direct call to categories to inspect response
            try:
                try:
                    data = await tmp._request_json('get', f"{tmp.api_url}/categories", params={"slug": "test-faqs"})
                    print('Probe categories (JSON):', data)
                except Exception as e:
                    print('Probe categories error:', e)
            finally:
                await tmp.close()
        except Exception:
            # ignore probe errors; proceed with publishing
            pass

        print("Publishing FAQ items with provided cookies...")
        ids = await svc.publish_ufaq_items(questions=faq_items, faq_category_slug="", status="draft")
        print("Published FAQ IDs:", ids)
    except Exception as e:
        print("Error:", e)
    finally:
        await svc.close()


if __name__ == '__main__':
    asyncio.run(main())
