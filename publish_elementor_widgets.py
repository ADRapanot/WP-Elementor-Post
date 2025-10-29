import asyncio
from wordpress_service import WordPressService


wp_service = WordPressService(
        base_url="https://www.idsexpress.net", # example https://www.idsexpress.net
        username="idsexpress@aol.com", # example aaa@a.com
        password="xwPl Ma5g 1HRK 7PxW IY9N T2ti", # Application password
        cookies=None
    )
async def publish():
    try:
        await wp_service.login_with_credentials()
    except Exception as e:
        print(f"Login failed: {e}")
        return
    
    
    await wp_service.login_with_credentials()
    content_html = """
        <h2>Introduction</h2>
        <p>This is the intro section.</p>
        <h2>Topic A</h2>
        <p>Details about topic A.</p>
        <h3>Subtopic A-1</h3>
        <p>Extra info.</p>
    """

    faq_items = [
        {"question": "What is an email lookup tool?", "answer": "An email lookup tool finds and verifies professional email addresses from online sources."},
        {"question": "Is it legal to find emails online?", "answer": "Yes, as long as you use them for legitimate business purposes and follow GDPR or CAN-SPAN rules."},
        {"question": "What's the most accurate way to find emails?", "answer": "Using Email verifier tools like LeadsScraper.io ensures higher accuracy than manual guessing."},
    ]
    try: 
        await wp_service.publish_elementor_widgets_meta(content_html, faq_items)   
    except Exception as e:
        print(f"Error publishing Elementor widgets meta: {e}")
    finally:
        await wp_service.close()            
    



if __name__ == "__main__":
    asyncio.run(publish())