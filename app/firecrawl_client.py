from firecrawl import FirecrawlApp
from app.exceptions import ScrapingError
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_with_firecrawl(url: str):
    """
    Scrape product data using Firecrawl API
    """
    api_key = os.getenv('FIRECRAWL_API_KEY')
    if not api_key:
        raise ScrapingError("FIRECRAWL_API_KEY environment variable is not set")
    
    try:
        app = FirecrawlApp(api_key=api_key)
        
        # Match the API builder structure
        payload = {
            "url": url,
            "formats": ["extract", "markdown"],
            "onlyMainContent": True,
            "extract": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": { "type": "string" },
                        "description": { "type": "string" },
                        "color": { "type": "string" },
                        "width_diameter": { "type": "string" },
                        "height": { "type": "string" },
                        "wattage": { "type": "string" },
                        "product_type": { "type": "string" },
                        "material": { "type": "string" },
                        "price": { "type": "string" },
                        "sku": { "type": "string" },
                        "image_url": { "type": "string" }
                    }
                }
            },
            "actions": [
                {
                    "type": "scroll",
                    "direction": "down"
                }
            ]
        }
        
        result = app.scrape_url(url, payload)
        
        return {
            "url": url,
            "raw_html": result.get('html', ''),
            "markdown": result.get('markdown', ''),
            "extracted_data": result.get('extract', {}),
            "status": "scraped"
        }
        
    except Exception as e:
        raise ScrapingError(f"Firecrawl API error: {str(e)}")
