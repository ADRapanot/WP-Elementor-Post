import asyncio
from wordpress_service import WordPressService


wp_service = WordPressService(
        base_url="https://www.idsexpress.net", # example https://www.idsexpress.net
        username="idsexpress@aol.com", # example aaa@a.com
        password="xwPl Ma5g 1HRK 7PxW IY9N T2ti", # Application password
        cookies=None
    )
async def publish():
    await wp_service.login_with_credentials()

    try: 
        await wp_service.publish_elementor_widgets_meta()   
    except Exception as e:
        print(f"Error publishing Elementor widgets meta: {e}")
    finally:
        await wp_service.close()            
    



if __name__ == "__main__":
    asyncio.run(publish())