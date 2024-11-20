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
        
        # Ensure URL is a string
        url_str = str(url)
        
        # Get both HTML and Markdown
        response = app.scrape_url(
            url_str,
            params={'formats': ['markdown', 'html']}
        )
        
        # Extract data from the nested structure
        if response.get('success') and 'data' in response:
            data = response['data']
            return {
                "url": url_str,
                "raw_html": data.get('html', ''),
                "markdown": data.get('markdown', ''),
                "metadata": data.get('metadata', {}),  # Also storing metadata
                "status": "scraped"
            }
        else:
            raise ScrapingError("Failed to get valid response from Firecrawl")
        
    except Exception as e:
        raise ScrapingError(f"Firecrawl API error: {str(e)}")
