from app.exceptions import ScrapingError
from app.schemas import ProductSchema
from firecrawl import FirecrawlApp
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
        # Initialize the FirecrawlApp with API key
        app = FirecrawlApp(api_key=api_key)
        
        # Create scraping configuration using our existing schema
        scrape_config = {
            'formats': ['extract'],
            'extract': {
                'schema': ProductSchema.model_json_schema(),
                'selectors': {
                    'id': '.product-id',
                    'metadata': {
                        'name': '.product-name',
                        'description': '.product-description',
                        'specifications': {
                            'color': '.product-color',
                            'dimensions': '.product-dimensions',
                            'wattage': '.product-wattage',
                            'type': '.product-type',
                            'material': '.product-material'
                        },
                        'category': '.product-category',
                        'price': '.product-price',
                        'sku': '.product-sku'
                    },
                    'image_url': '.product-image'
                }
            }
        }
        
        # Perform the scraping - pass parameters directly, not as config
        result = app.scrape_url(
            url=url,
            formats=['extract'],
            extract={
                'schema': ProductSchema.model_json_schema(),
                'selectors': {
                    'id': '.product-id',
                    'metadata': {
                        'name': '.product-name',
                        'description': '.product-description',
                        'specifications': {
                            'color': '.product-color',
                            'dimensions': '.product-dimensions',
                            'wattage': '.product-wattage',
                            'type': '.product-type',
                            'material': '.product-material'
                        },
                        'category': '.product-category',
                        'price': '.product-price',
                        'sku': '.product-sku'
                    },
                    'image_url': '.product-image'
                }
            }
        )
        
        # Validate and return the data
        return ProductSchema(**result["extract"])
        
    except Exception as e:
        raise ScrapingError(f"Firecrawl API error: {str(e)}")
