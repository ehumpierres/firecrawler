from app.exceptions import ScrapingError
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
        
        # Get both HTML and Markdown
        result = app.scrape_url(
            url,
            params={'formats': ['markdown', 'html']}
        )
        
        # Return data structure with both formats
        return {
            "url": url,
            "raw_html": result.get('html', ''),
            "markdown": result.get('markdown', ''),
            "status": "scraped"
        }
        
    except Exception as e:
        raise ScrapingError(f"Firecrawl API error: {str(e)}")
