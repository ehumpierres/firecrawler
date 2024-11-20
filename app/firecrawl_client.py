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
        # Initialize the FirecrawlApp with API key
        app = FirecrawlApp(api_key=api_key)
        
        # Ensure URL is a string
        url_str = str(url)
        
        # Simple scrape request following the SDK example
        result = app.scrape_url(url_str)
        
        print(f"Raw response: {result}")  # Debug print
        
        return {
            "url": url_str,
            "raw_html": result.get('html', ''),
            "markdown": result.get('markdown', ''),
            "status": "scraped"
        }
        
    except Exception as e:
        raise ScrapingError(f"Firecrawl API error: {str(e)}")
