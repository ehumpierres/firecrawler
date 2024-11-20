from app.exceptions import ScrapingError
from app.schemas import ProductSchema
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_with_firecrawl(url):
    api_key = os.getenv('FIRECRAWL_API_KEY')
    if not api_key:
        raise ScrapingError("FIRECRAWL_API_KEY environment variable is not set")
        
    # Define the extraction schema based on our ProductSchema
    request_body = {
        "url": url,  # URL from the function parameter
        "formats": ["extract"],
        "extract": {
            "schema": {
                "product": {
                    "container": ".product-container",
                    "fields": {
                        "id": ".product-id",
                        "metadata": {
                            "name": ".product-name",
                            "description": ".product-description",
                            "specifications": {
                                "color": ".product-color",
                                "dimensions": ".product-dimensions",
                                "wattage": ".product-wattage",
                                "type": ".product-type",
                                "material": ".product-material"
                            },
                            "category": ".product-category",
                            "price": ".product-price",
                            "sku": ".product-sku"
                        },
                        "image_url": ".product-image"
                    }
                }
            }
        }
    }
        
    try:
        response = requests.post(
            "https://api.firecrawl.dev/scrape",
            json=request_body,  # Send the complete request body
            headers={"Authorization": f"Bearer {api_key}"}
        )
        response.raise_for_status()
        
        # Validate response against our schema
        data = response.json()
        return ProductSchema(**data["extract"])
    except requests.exceptions.RequestException as e:
        raise ScrapingError(f"Firecrawl API error: {str(e)}")
