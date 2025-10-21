"""
Test script for ElementorWordPressService's publish_ufaq_items function
"""
import asyncio
from elementor_wordpress_service import ElementorWordPressService

# Try to import cookies from use_cookies.py if you stored them there
try:
    from use_cookies import cookies as _COOKIES  # type: ignore
except Exception:
    _COOKIES = None

async def test_publish_ufaq():
    # Initialize the service
    wp_service = ElementorWordPressService(
        base_url="", # example https://www.idsexpress.net
        username="", # example aaa@a.com
        password="", # Application password
        cookies=_COOKIES
    )
    
    try:
        # Test FAQ items
        faq_items = [
            {
                "question": "What is Ultimate FAQ?",
                "answer": "Ultimate FAQ is a WordPress plugin that helps you create and manage FAQs on your website."
            },
            {
                "question": "How does the FAQ schema work?",
                "answer": "The FAQ schema is automatically added using JSON-LD format, which helps search engines understand and display your FAQs in search results."
            },
            {
                "question": "Can I categorize FAQs?",
                "answer": "Yes, FAQs can be organized into categories for better organization and display."
            }
        ]
        
        print("Publishing FAQ items...")
        # Try publishing to the "test-faqs" category
        faq_ids = await wp_service.publish_ufaq_items(
            questions=faq_items,
            faq_category_slug="test-faqs",
            status="draft"  # Using draft for testing
        )
        
        print(f"\nSuccessfully published {len(faq_ids)} FAQ items:")
        print(f"FAQ IDs: {faq_ids}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await wp_service.close()

if __name__ == "__main__":
    asyncio.run(test_publish_ufaq())