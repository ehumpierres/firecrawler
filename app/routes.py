from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, AnyHttpUrl
from app.firecrawl_client import scrape_with_firecrawl
from app.claude_client import process_with_claude
from app.mongo_handler import save_scraping_job, save_structured_data, update_job_status, get_scraping_job
from app.exceptions import ScrapingError, ProcessingError, DatabaseError
from app import db

router = APIRouter()

class ScrapeRequest(BaseModel):
    url: str

class ProcessRequest(BaseModel):
    job_id: str

@router.post("/scrape")
async def scrape_url(request: ScrapeRequest):
    try:
        url = request.url
        # Scrape the URL
        scraped_data = scrape_with_firecrawl(url)
        
        # Save to MongoDB
        job_id = save_scraping_job(db, scraped_data)
        
        return {
            "job_id": str(job_id),
            "status": "scraped",
            "message": "Data scraped successfully"
        }
        
    except ScrapingError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process")
async def handle_processing_request(request: ProcessRequest):
    """Second endpoint: Process scraped data with Claude"""
    try:
        # 3. Retrieves the stored raw data from MongoDB
        job_data = get_scraping_job(request.job_id)
        if not job_data:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if job_data.get('status') != "scraped":
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid job status: {job_data.get('status')}. Job must be in 'scraped' state."
            )
        
        # Process with Claude
        structured_data = process_with_claude(job_data.get('raw_data'))
        
        # 4. Saves the processed data back to MongoDB
        save_structured_data(request.job_id, structured_data)
        update_job_status(request.job_id, "completed")
        
        return {
            "job_id": request.job_id,
            "status": "completed",
            "data": structured_data
        }
    
    except ProcessingError as e:
        update_job_status(request.job_id, "processing_failed")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        update_job_status(request.job_id, "processing_failed")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    try:
        db.command('ping')
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500

@router.get("/jobs/{job_id}")
async def get_job_results(job_id: str):
    """Retrieve results for a specific job"""
    try:
        job_data = get_scraping_job(job_id)
        if not job_data:
            raise HTTPException(status_code=404, detail="Job not found")
            
        return {
            "job_id": str(job_data["_id"]),
            "status": job_data["status"],
            "url": job_data["url"],
            "created_at": job_data["created_at"],
            "raw_html": job_data.get("raw_html"),
            "markdown": job_data.get("markdown"),
            "extracted_data": job_data.get("extracted_data"),
            "processed_data": job_data.get("processed_data"),
            "updated_at": job_data.get("updated_at")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs")
async def list_jobs(status: str = None, limit: int = 10):
    """List all jobs with optional status filter"""
    try:
        query = {}
        if status:
            query["status"] = status
            
        jobs = db.jobs.find(query).limit(limit)
        return {
            "jobs": [{
                "job_id": str(job["_id"]),
                "status": job["status"],
                "url": job["url"],
                "created_at": job["created_at"],
                "updated_at": job.get("updated_at")
            } for job in jobs]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
