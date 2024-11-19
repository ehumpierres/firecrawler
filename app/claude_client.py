import requests
import os
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Dict

load_dotenv()

class RateLimiter:
    def __init__(self, tokens_per_minute: int = 36000):
        self.tokens_per_minute = tokens_per_minute
        self.tokens_available = tokens_per_minute
        self.last_updated = datetime.now()
    
    def update_tokens(self):
        now = datetime.now()
        time_passed = now - self.last_updated
        tokens_to_add = (time_passed.total_seconds() / 60.0) * self.tokens_per_minute
        self.tokens_available = min(
            self.tokens_per_minute,
            self.tokens_available + tokens_to_add
        )
        self.last_updated = now
    
    def can_process(self, tokens_needed: int) -> bool:
        self.update_tokens()
        if self.tokens_available >= tokens_needed:
            self.tokens_available -= tokens_needed
            return True
        return False
    
    def wait_time_seconds(self, tokens_needed: int) -> float:
        if self.tokens_available >= tokens_needed:
            return 0
        tokens_required = tokens_needed - self.tokens_available
        return (tokens_required / self.tokens_per_minute) * 60

# Create a global rate limiter instance with conservative limit
rate_limiter = RateLimiter()

def estimate_tokens(data: Dict) -> int:
    # Rough estimation of tokens in the data
    # You might want to adjust this based on your specific use case
    return len(str(data)) // 4  # Rough estimate: 4 characters per token

def process_with_claude(scraped_data):
    """
    Sends scraped data to the Claude.ai API for processing and structures it
    into the specified JSON schema with conservative rate limiting.
    """
    api_key = os.getenv('CLAUDE_API_KEY')
    if not api_key:
        raise ValueError("CLAUDE_API_KEY environment variable is not set")
    
    # Estimate tokens needed for this request
    estimated_tokens = estimate_tokens(scraped_data)
    
    # Check if we need to wait
    wait_time = rate_limiter.wait_time_seconds(estimated_tokens)
    if wait_time > 0:
        time.sleep(wait_time)
    
    # Process only if we have enough tokens
    if not rate_limiter.can_process(estimated_tokens):
        raise Exception("Rate limit exceeded. Please try again later.")
        
    response = requests.post(
        "https://api.anthropic.com/v1",
        json={"data": scraped_data},
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()

    # Process Claude response to match the desired JSON schema
    processed_data = response.json()

    structured_data = {
        "id": processed_data.get("id", ""),
        "metadata": {
            "name": processed_data.get("name", ""),
            "description": processed_data.get("description", ""),
            "specifications": {
                "color": processed_data.get("specifications", {}).get("color", ""),
                "dimensions": processed_data.get("specifications", {}).get("dimensions", ""),
                "wattage": processed_data.get("specifications", {}).get("wattage", ""),
                "type": processed_data.get("specifications", {}).get("type", ""),
            },
            "category": processed_data.get("category", ""),
            "price": processed_data.get("price", 0.0),
            "sku": processed_data.get("sku", "")
        },
        "image_url": processed_data.get("image_url", "")
    }
    return structured_data
