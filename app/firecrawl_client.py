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
        
        # Perform the scraping with minimal params first
        result = app.scrape_url(
            url,
            params={'formats': ['markdown', 'html']}  # Simplified to match documentation example
        )
        
        # Validate and return the data
        return ProductSchema(**result)
        
    except Exception as e:
        raise ScrapingError(f"Firecrawl API error: {str(e)}")
