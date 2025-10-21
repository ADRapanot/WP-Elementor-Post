"""
Extended WordPress service with Elementor Pro support.
"""
import json
from typing import List, Dict, Optional, Union
from wordpress_service import WordPressService


class ElementorWordPressService(WordPressService):
    """WordPress service with Elementor support for publishing articles."""

    async def publish_ufaq_items(
        self,
        questions: List[Dict[str, str]],
        faq_category_slug: str = "",  # Default category slug
        status: str = "publish"
    ) -> List[int]:
        """Publish FAQs to Ultimate FAQ's CPT in a simple, robust way.

        Behavior:
        - Look up category ID by slug if provided (uses _request_json).
        - Post each FAQ to the ufaq endpoint via _request_json and collect returned IDs.
        - Logs and continues on errors per-item.

        Returns a list of created FAQ IDs.
        """
        self.logger.info("Publishing FAQs to Ultimate FAQ CPT (simple path)")
        faq_ids: List[int] = []

        # Resolve category ID if a slug is given
        category_id: Optional[int] = None
        if faq_category_slug:
            try:
                categories = await self._request_json('get', f"{self.api_url}/categories", params={"slug": faq_category_slug})
                if categories and isinstance(categories, list):
                    category_id = categories[0].get('id')
            except Exception as e:
                self.logger.warning(f"Could not resolve category slug '{faq_category_slug}': {e}")
        print(category_id)
        # Post each FAQ
        for q in questions:
            question = q.get('question') or ''
            answer = q.get('answer') or ''

            payload = {
                'title': question,
                'content': answer,
                'status': status,
            }
            if category_id:
                payload['categories'] = [category_id]

            try:
                resp = await self._request_json('post', f"{self.api_url}/ufaq", json=payload)
                if isinstance(resp, dict) and resp.get('id'):
                    faq_ids.append(resp['id'])
                    self.logger.info(f"Published FAQ '{question}' -> ID {resp['id']}")
                else:
                    self.logger.warning(f"FAQ created but no id returned for question '{question}'; resp={resp}")
            except Exception as e:
                self.logger.error(f"Failed to publish FAQ '{question}': {e}")
                # continue with next item
                continue
        print(faq_ids)
        return faq_ids
    async def create_elementor_toc(self, settings: Optional[Dict] = None) -> str:
        """
        Create Elementor Pro Table of Contents section with advanced features.
        
        Args:
            settings: Optional TOC settings dictionary
            
        Returns:
            Elementor-compatible TOC section HTML
        """
        default_settings = {
            'title': 'Table of Contents',
            'hierarchical_view': 'yes',
            'collapse_subitems': 'yes'
        }
        
        toc_settings = {**default_settings, **(settings or {})}
        
        # Convert settings to Elementor format (widget_data left for potential future use)
        widget_data = {
            "id": "table-of-contents",
            "elType": "widget",
            "settings": toc_settings,
            "elements": []
        }

        # Determine template id from configuration if available
        try:
            from config import get_config
            cfg = get_config()
            template_id = cfg.get('elementor_template_id', 1425) if isinstance(cfg, dict) else 1425
        except Exception:
            template_id = 1425

        # Embed settings as a JSON string so shortcode parsing isn't confused by double quotes
        try:
            settings_json = json.dumps(toc_settings)
            return f"[elementor-template id=\"{template_id}\" settings='{settings_json}']"
        except Exception:
            return f"[elementor-template id=\"{template_id}\"]"

    async def publish_elementor_article(
        self,
        title: str,
        content: str,
        faq_items: Optional[List[Dict[str, str]]] = None,
        include_toc: bool = False,
        toc_settings: Optional[Dict] = None,
        **kwargs
    ):
        """
        Publish an article with Elementor components.

        Args:
            title: Article title
            content: Main article content (HTML)
            faq_items: Optional list of FAQ items (question/answer pairs)
            include_toc: Whether to include Table of Contents
            toc_settings: Optional TOC settings
            **kwargs: Additional arguments passed to publish_article
        """
        full_content = []
        
        # Prepare the content sections
        content_parts = []
        
        if include_toc:
            toc_section = await self.create_elementor_toc(toc_settings)
            content_parts.append(toc_section)
        
        
        # Add main content
        content_parts.append(content)
        
        # Add FAQ section if provided
        # If faq_items not provided, create a simple FAQ pair from the title (short Q/A)
        if not faq_items:
            # Simple heuristic: ask "What is {title}?" and use a short answer
            short_question = f"What is {title.split(':')[0].strip()}?"
            short_answer = f"{title} — an overview and details are in this article."
            faq_items = [{"question": short_question, "answer": short_answer}]

        # Publish FAQ items and insert shortcode + JSON-LD schema
        if faq_items:
            faq_ids = await self.publish_ufaq_items(
                questions=faq_items,
                faq_category_slug="test",
                status=kwargs.get('status', 'publish')  # Match post status
            )
            if faq_ids:
                faq_shortcode = f'[ultimate-faqs include_category_ids="{",".join(map(str, faq_ids))}"]'
                content_parts.append(faq_shortcode)

                # Add FAQ Schema (JSON-LD for SEO)
                try:
                    faq_schema = {
                        "@context": "https://schema.org",
                        "@type": "FAQPage",
                        "mainEntity": [
                            {
                                "@type": "Question",
                                "name": item["question"],
                                "acceptedAnswer": {
                                    "@type": "Answer",
                                    "text": item["answer"]
                                }
                            }
                            for item in faq_items
                        ]
                    }
                    content_parts.append(f'<script type="application/ld+json">{json.dumps(faq_schema)}</script>')
                except Exception as e:
                    self.logger.error(f"Failed to build FAQ schema: {e}")

        # Join all content parts
        content_with_widgets = "\n\n".join(content_parts)
        
        # Wrap everything in the page template shortcode
        final_content = f'\n{content_with_widgets}\n'
        self.logger.debug(f"Final post content length: {len(final_content)}")

        # Publish using parent class method
        return await super().publish_article(
            title=title,
            content=final_content,
            **kwargs
        )