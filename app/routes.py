from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.firecrawl_client import scrape_with_firecrawl
from app.claude_client import process_with_claude
from app.mongo_handler import save_scraping_job, save_structured_data, update_job_status
from app.exceptions import ScrapingError, ProcessingError, DatabaseError

router = APIRouter()

class ScrapeRequest(BaseModel):
    url: HttpUrl

@router.post("/scrape")
async def handle_scraping_request(request: ScrapeRequest):
    try:
        job_id = save_scraping_job(str(request.url))
    except Exception as e:
        raise DatabaseError(f"Failed to create scraping job: {str(e)}")

    try:
        scraped_data = scrape_with_firecrawl(str(request.url))
    except Exception as e:
        update_job_status(job_id, "failed")
        raise ScrapingError(f"Failed to scrape URL: {str(e)}")

    try:
        structured_data = process_with_claude(scraped_data)
    except Exception as e:
        update_job_status(job_id, "failed")
        raise ProcessingError(f"Failed to process with Claude: {str(e)}")

    try:
        save_structured_data(job_id, structured_data)
        update_job_status(job_id, "completed")
        return {"job_id": job_id, "status": "completed"}
    except Exception as e:
        update_job_status(job_id, "failed")
        raise DatabaseError(f"Failed to save structured data: {str(e)}")

@router.get("/health")
async def health_check():
    try:
        # Check MongoDB connection
        db.scraping_jobs.find_one()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
