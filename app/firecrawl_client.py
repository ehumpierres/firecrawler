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
                    "name": "name",
                    "description": "description",
                    "color": "color",
                    "width_diameter": "Width/Dia",
                    "height": "Height",
                    "wattage": "wattage",
                    "type": "Type",
                    "material": "material",
                    "price": "List Price",
                    "sku": "SKU",
                    "image_url": "image_url"
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
