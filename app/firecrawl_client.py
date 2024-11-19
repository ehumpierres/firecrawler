from app.exceptions import ScrapingError
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_with_firecrawl(url):
    api_key = os.getenv('FIRECRAWL_API_KEY')
    if not api_key:
        raise ScrapingError("FIRECRAWL_API_KEY environment variable is not set")
        
    try:
        response = requests.post(
            "https://api.firecrawl.dev/v1/scrape",
            json={"url": url},
            headers={"Authorization": f"Bearer {api_key}"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ScrapingError(f"Firecrawl API error: {str(e)}")
