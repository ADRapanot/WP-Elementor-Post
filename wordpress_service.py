"""
WordPress service for publishing articles.
"""
import json
import logging
from typing import Optional, List
from datetime import datetime

import httpx

from models.content import PublishedArticle


class WordPressService:
    """WordPress service for publishing articles."""
    
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,  # Application password
        timeout: int = 60
        , cookies: dict = None
    ):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.logger = logging.getLogger(__name__)
        
        self.api_url = f"{self.base_url}/wp-json/wp/v2"
        
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            auth=(self.username, self.password),
            headers={"Content-Type": "application/json"}
        )

        # If cookies were provided (for example copied from browser), set them
        if cookies:
            try:
                for k, v in cookies.items():
                    self.client.cookies.set(k, v)
                self.logger.info("Initialized client with provided cookies")
            except Exception:
                self.logger.warning("Failed to set provided cookies on client")

    async def _request_json(self, method: str, url: str, **kwargs):
        """Helper to make an HTTP request and parse JSON with improved error logging.

        Args:
            method: HTTP method name on the client (e.g., 'get', 'post')
            url: Full URL to call
            **kwargs: forwarded to client method

        Returns:
            Parsed JSON response

        Raises:
            httpx.HTTPStatusError or ValueError with helpful logs if non-JSON
        """
        try:
            client_method = getattr(self.client, method.lower())
        except Exception as e:
            raise ValueError(f"Invalid HTTP method: {method}") from e

        # If client has no cookies, try to load from .wp_cookies.json in repo root
        try:
            has_cookies = bool(getattr(self.client, 'cookies', None) and len(self.client.cookies.keys()) > 0)
        except Exception:
            has_cookies = False

        if not has_cookies:
            try:
                # Prefer wp_config.json via config.py (if present)
                from config import get_config
                cfg = get_config()
                raw = cfg.get('cookies') if isinstance(cfg, dict) else None
                if not raw:
                    # Fall back to .wp_cookies.json for backward compatibility
                    import json as _json
                    from pathlib import Path
                    p = Path(__file__).resolve().parent / '.wp_cookies.json'
                    if p.exists():
                        raw = _json.loads(p.read_text())

                if isinstance(raw, dict):
                    for k, v in raw.items():
                        try:
                            self.client.cookies.set(k, v)
                        except Exception:
                            pass
                    self.logger.debug(f"Loaded {len(raw)} cookies from configuration")
            except Exception:
                pass

        response = await client_method(url, **kwargs)
        try:
            response.raise_for_status()
        except Exception as e:
            # Log body for easier debugging
            self.logger.error(f"HTTP error {response.status_code} for {url}: {response.text[:500]}")
            raise

        try:
            return response.json()
        except Exception:
            # Response was not JSON — log and raise
            body_preview = response.text[:1000] if response.text else "<empty>"
            self.logger.error(f"Expected JSON from {url} but got: {body_preview}")
            raise ValueError(f"Non-JSON response from {url}")

    async def login_with_credentials(self) -> bool:
        """Attempt a form-based login to obtain WordPress session cookies.

        This posts to /wp-login.php with the configured username/password and
        stores any returned cookies on the AsyncClient for subsequent requests.

        Returns True if a wordpress_logged_in cookie was obtained.
        """
        login_url = f"{self.base_url}/wp-login.php"
        try:
            # Fetch the login page first (some sites set test cookies or nonces)
            resp = await self.client.get(login_url)
            resp.raise_for_status()

            data = {
                "log": self.username,
                "pwd": self.password,
                "wp-submit": "Log In",
                "redirect_to": f"{self.base_url}/wp-admin/",
                "testcookie": "1"
            }

            headers = {"Content-Type": "application/x-www-form-urlencoded", "Referer": login_url}

            resp2 = await self.client.post(login_url, data=data, headers=headers)
            # Update client's cookie jar with any cookies received
            try:
                self.client.cookies.update(resp2.cookies)
            except Exception:
                # Fallback: iterate and set
                for k, v in resp2.cookies.items():
                    try:
                        self.client.cookies.set(k, v)
                    except Exception:
                        pass

            # Look for wordpress_logged_in_ cookie
            cookie_keys = list(self.client.cookies.keys())
            if not cookie_keys: return False
            return True

        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            return False
    
    async def _get_category_id(self, category_name: str) -> Optional[int]:
        """Get category ID by name, create if doesn't exist."""
        try:
            response = await self.client.get(
                f"{self.api_url}/categories",
                params={"search": category_name}
            )
            response.raise_for_status()
            
            categories = response.json()
            
            for category in categories:
                if category["name"].lower() == category_name.lower():
                    return category["id"]
            
            # Create new category
            self.logger.info(f"Creating new category: {category_name}")
            create_response = await self.client.post(
                f"{self.api_url}/categories",
                json={"name": category_name}
            )
            create_response.raise_for_status()
            
            return create_response.json()["id"]
            
        except Exception as e:
            self.logger.error(f"Error with category '{category_name}': {e}")
            return None
    
    async def _get_tag_ids(self, tag_names: List[str]) -> List[int]:
        """Get tag IDs by names, create if don't exist."""
        tag_ids = []
        
        for tag_name in tag_names:
            try:
                response = await self.client.get(
                    f"{self.api_url}/tags",
                    params={"search": tag_name}
                )
                response.raise_for_status()
                
                tags = response.json()
                
                tag_id = None
                for tag in tags:
                    if tag["name"].lower() == tag_name.lower():
                        tag_id = tag["id"]
                        break
                
                if tag_id is None:
                    self.logger.info(f"Creating new tag: {tag_name}")
                    create_response = await self.client.post(
                        f"{self.api_url}/tags",
                        json={"name": tag_name}
                    )
                    create_response.raise_for_status()
                    tag_id = create_response.json()["id"]
                
                if tag_id:
                    tag_ids.append(tag_id)
                    
            except Exception as e:
                self.logger.error(f"Error with tag '{tag_name}': {e}")
                continue
        
        return tag_ids
    
    async def publish_article(
        self,
        title: str,
        content: str,
        status: str = "publish",
        categories: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        publish_date: Optional[str] = None,
        meta_description: Optional[str] = None,
        excerpt: Optional[str] = None
    ) -> PublishedArticle:
        """
        Publish an article to WordPress.

        Args:
            title: Article title
            content: Article content (HTML)
            status: Publication status (draft, publish, private)
            categories: List of category names
            tags: List of tag names
            publish_date: Scheduled publish date
            meta_description: SEO meta description for AIOSEO
            excerpt: WordPress excerpt

        Returns:
            Published article information
        """
        self.logger.info(f"Publishing article: {title}")
        
        try:
            post_data = {
                "title": title,
                "content": content,
                "status": status
            }
            
            # Add categories
            if categories:
                category_ids = []
                for cat in categories:
                    cat_id = await self._get_category_id(cat)
                    if cat_id:
                        category_ids.append(cat_id)
                if category_ids:
                    post_data["categories"] = category_ids
            
            # Add tags
            if tags:
                tag_ids = await self._get_tag_ids(tags)
                if tag_ids:
                    post_data["tags"] = tag_ids

            # Add scheduled publish date if provided
            if publish_date:
                post_data["date"] = publish_date
                self.logger.info(f"Scheduling article for: {publish_date}")

            # Add excerpt if provided
            if excerpt:
                post_data["excerpt"] = excerpt
                self.logger.info(f"Adding excerpt: {excerpt[:100]}...")
            faq_data = [  # Your dynamic FAQs
                {'title': 'What is Python?', 'content': 'A high-level language.'},
                {'title': 'How do I install?', 'content': 'pip install requests.'},
            ]
            meta = {'faq_json': json.dumps(faq_data), '_elementor_data': json.dumps(faq_data)}
            post_data["meta"] = meta
            response = await self.client.post(
                f"{self.api_url}/posts",
                json=post_data
            )
            response.raise_for_status()

            post_response = response.json()

            post_id = post_response["id"]

            # Handle AIOSEO meta description if provided
            if meta_description:
                await self._update_aioseo_meta(post_id, meta_description)

            post_url = post_response.get("link", f"{self.base_url}/?p={post_id}")
            post_title = post_response.get("title", {}).get("rendered", title)
            post_status = post_response.get("status", status)

            self.logger.info(f"Successfully published: {post_url}")

            
            return PublishedArticle(
                post_id=post_id,
                url=post_url,
                title=post_title,
                status=post_status,
                meta=meta,
                published_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"WordPress publishing error: {e}")
            raise

    async def _update_aioseo_meta(self, post_id: int, meta_description: str):
        """Update AIOSEO meta description for a post."""
        try:
            # AIOSEO stores data in a custom post meta field
            response = await self.client.post(
                f"{self.api_url}/posts/{post_id}",
                json={
                    "meta": {
                        "_aioseo_description": meta_description
                    }
                }
            )
            response.raise_for_status()
            self.logger.info(f"Updated AIOSEO meta description for post {post_id}")
        except Exception as e:
            self.logger.error(f"Error updating AIOSEO meta: {e}")
   
    async def publish_elementor_widgets_meta(self, content_html:  str, faq_items: List[dict]) :
        """Fixed test function with proper vertical layout structure"""
        
        toc_title = "Table of Contents"
        elementor_data = [
            # SECTION 1: Table of Contents
            {
                "id": "section_toc",
                "elType": "section",
                "settings": {
                    "layout": "boxed",
                    "content_width": {"unit": "px", "size": 1140},
                    "gap": "default",
                    "padding": {
                        "unit": "px",
                        "top": "40",
                        "right": "20",
                        "bottom": "40",
                        "left": "20",
                        "isLinked": False
                    }
                },
                "elements": [
                    {
                        "id": "column_toc",
                        "elType": "column",
                        "settings": {
                            "_column_size": 100,
                            "_inline_size": None
                        },
                        "elements": [
                            {
                                "id": "widget_toc",
                                "elType": "widget",
                                "widgetType": "table-of-contents",
                                "settings": {
                                    "title": toc_title,
                                    "_css_classes": "custom-toc-black",
                                    "custom_css": "selector .elementor-toc__header-title { color: #000000 !important; }",
                                    "title_typography_typography": "custom",
                                    "title_typography_color": "#000000" ,
                                    "hierarchical_view": "yes",
                                    "headings_by_tags": ["h2", "h3"],
                                    "container": "",
                                    "exclude_headings_by_selector": "",
                                    "marker_view": "numbers",
                                    "icon": {"value": "", "library": ""},
                                    "collapse_subitems": "no",
                                    "minimized_on": "mobile",
                                    
                                },
                                "elements": []
                            }
                        ]
                    }
                ]
            },
            
            # SECTION 2: Main Content
            {
                "id": "section_content",
                "elType": "section",
                "settings": {
                    "layout": "boxed",
                    "content_width": {"unit": "px", "size": 1140},
                    "gap": "default",
                    "padding": {
                        "unit": "px",
                        "top": "40",
                        "right": "20",
                        "bottom": "40",
                        "left": "20",
                        "isLinked": False
                    }
                },
                "elements": [
                    {
                        "id": "column_content",
                        "elType": "column",
                        "settings": {
                            "_column_size": 100,
                            "_inline_size": None
                        },
                        "elements": [
                            {
                                "id": "widget_text",
                                "elType": "widget",
                                "widgetType": "text-editor",
                                "settings": {
                                    "editor": content_html
                                },
                                "elements": []
                            }
                        ]
                    }
                ]
            },
            
            # SECTION 3: FAQ
            {
                "id": "section_faq",
                "elType": "section",
                "settings": {
                    "layout": "boxed",
                    "content_width": {"unit": "px", "size": 1140},
                    "gap": "default",
                    "padding": {
                        "unit": "px",
                        "top": "40",
                        "right": "20",
                        "bottom": "40",
                        "left": "20",
                        "isLinked": False
                    },
                    "background_background": "classic",
                    "background_color": "#F8F9FA"
                },
                "elements": [
                    {
                        "id": "column_faq",
                        "elType": "column",
                        "settings": {
                            "_column_size": 100,
                            "_inline_size": None
                        },
                        "elements": [
                            # FAQ Heading
                            {
                                "id": "widget_faq_heading",
                                "elType": "widget",
                                "widgetType": "heading",
                                "settings": {
                                    "title": "FAQ",
                                    "header_size": "h2",
                                    "title_color": "#1D53DD",
                                    "align": "center",
                                    "align_tablet": "center",
                                    "align_mobile": "center"
                                },
                                "elements": []
                            },
                            # FAQ Accordion
                            {
                                "id": "widget_faq",
                                "elType": "widget",
                                "widgetType": "accordion",
                                "settings": {
                                    "faq_schema": "yes",
                                    "tabs": [
                                        {
                                            "_id": f"faq_{i+1}",
                                            "tab_title": item["question"],
                                            "tab_content": f"<p>{item['answer']}</p>"
                                        }
                                        for i, item in enumerate(faq_items)
                                    ],
                                    "icon": "fa fa-caret-right",
                                    "icon_active": "fa fa-caret-down",
                                    "icon_align": "right",
                                    "title_color": "#1D53DD",
                                    "title_hover_color": "#1D53DD",
                                    "title_active_color": "#1D53DD",
                                    "title_typography_typography": "custom",
                                    "title_typography_font_weight": "bold",
                                    "title_typography_font_weight_tablet": "bold",
                                    "active_title_typography_font_weight": "bold",
                                    "active_title_typography_font_weight_tablet": "bold",
                                    "icon_color": "#1D53DD",
                                    "icon_hover_color": "#1D53DD",
                                    "icon_active_color": "#1D53DD",
                                    "border_width": {
                                        "unit": "px",
                                        "top": "1",
                                        "right": "0",
                                        "bottom": "1",
                                        "left": "0",
                                        "isLinked": False
                                    },
                                    "border_color": "#E5E5E5"
                                },
                                "elements": []
                            }
                        ]
                    }
                ]
            }
        ]
        # Prepare payload with FAQ Schema and publish status
        payload = {
            "title": "Test: Properly Structured Layout",
            "status": "draft",
            "content": "",
            "meta": {
                "_elementor_data": json.dumps(elementor_data, ensure_ascii=False),  # Prevent ASCII encoding issues
                "_elementor_edit_mode": "builder",
                "_elementor_version": "3.22.2",
                "_elementor_css": "",  # Clear cached CSS
            }
        }
        # Create the post
        res = await self.client.post(
            f"{self.api_url}/posts",
            json=payload
        )
        res.raise_for_status()
        data = res.json() 

        # Clean up to regenerate post css
        await self.client.post(
            f"{self.api_url}/posts/{data["id"]}",
            json={
                "meta": {
                    "_elementor_css": "",  # Clear cached CSS
                    "_elementor_edit_mode": "builder"
                }
            }
        )
        # Set status to publish
        res = await self.client.post(
           f"{self.api_url}/posts/{data["id"]}",
            json={"status": "publish"}
        )
        data = res.json()
        print("Post created:", data.get("link"))
        print("Layout should now display vertically with proper spacing!")
        return data


    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
