"""
Test script for ElementorWordPressService
"""
import asyncio
from elementor_wordpress_service import ElementorWordPressService


async def main():
    # Initialize the service
    wp_service = ElementorWordPressService(
        base_url="https://www.idsexpress.net", # example https://www.idsexpress.net
        username="idsexpress@aol.com", # example aaa@a.com
        password="0rVg v8lQ Uo1s wIBA eyPo taCu", # Application password
        cookies=None
    )
    await wp_service.login_with_credentials()
    try:
        # Example article content with headings for TOC
        content = """
        <h2>Introduction</h2>
        <p>This is the introduction section of our article.</p>
        
        <h2>Main Topic</h2>
        <p>Here's our main topic discussion.</p>
        
        <h3>Subtopic 1</h3>
        <p>Details about subtopic 1.</p>
        
        <h3>Subtopic 2</h3>
        <p>Details about subtopic 2.</p>
        
        <h2>Conclusion</h2>
        <p>This is the conclusion of our article.</p>
        """
        
        # Example FAQ items
        faq_items = [
            {
                "question": "What is this article about?",
                "answer": "This article discusses important topics with examples."
            },
            {
                "question": "How can I learn more?",
                "answer": "You can check our other articles or contact us."
            }
        ]
        
        # Basic TOC settings for testing
        toc_settings = {
            "title": "In This Article"
        }
        
        # Basic FAQ settings for testing
        faq_settings = {
            "faq_schema": "yes"
        }
        
        # Publish article with Elementor components
        result = await wp_service.publish_elementor_article(
            title="Test Article with Elementor Components",
            content=content,
            faq_items=faq_items,
            include_toc=True,
            toc_settings=toc_settings,
            status="draft",  # Set to "draft" for testing
            tags=[],
            meta_description="Test article with Elementor components"
        )
        
        print(f"Article published successfully!")
        print(f"URL: {result.url}")
        print(f"Status: {result.status}")
        
    finally:
        await wp_service.close()

if __name__ == "__main__":
    asyncio.run(main())