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
        
        # Basic call with just the URL
        result = app.scrape_url(url)
        
        return {
            "url": url,
            "raw_html": result.get('html', ''),
            "markdown": result.get('markdown', ''),
            "status": "scraped"
        }
        
    except Exception as e:
        raise ScrapingError(f"Firecrawl API error: {str(e)}")
