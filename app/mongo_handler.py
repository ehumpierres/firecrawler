from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from app.exceptions import DatabaseError

load_dotenv()

def get_database():
    mongodb_uri = os.getenv('MONGODB_URI')
    if not mongodb_uri:
        raise DatabaseError("MONGODB_URI environment variable is not set")
    
    try:
        client = MongoClient(mongodb_uri)
        # Test the connection
        client.admin.command('ping')
        return client.web_scraper_db
    except ConnectionFailure:
        raise DatabaseError("Failed to connect to MongoDB")
    except Exception as e:
        raise DatabaseError(f"MongoDB error: {str(e)}")

# Get database instance
try:
    db = get_database()
except DatabaseError as e:
    print(f"Warning: Database initialization failed: {e}")
    db = None

def save_scraping_job(url):
    """
    Saves the scraping job metadata to the database.
    """
    if not db:
        raise DatabaseError("Database connection not initialized")
    
    try:
        job = {
            "url": url,
            "status": "pending",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        job_id = db.scraping_jobs.insert_one(job).inserted_id
        return str(job_id)
    except OperationFailure as e:
        raise DatabaseError(f"Failed to save scraping job: {str(e)}")

def save_structured_data(job_id, structured_data):
    """
    Saves the structured data to the database.
    """
    if not db:
        raise DatabaseError("Database connection not initialized")
    
    try:
        record = {
            "_id": job_id,
            "id": structured_data.get("id", ""),
            "metadata": structured_data.get("metadata", {}),
            "image_url": structured_data.get("image_url", ""),
            "created_at": datetime.now(timezone.utc)
        }
        db.structured_data.insert_one(record)
    except OperationFailure as e:
        raise DatabaseError(f"Failed to save structured data: {str(e)}")

def update_job_status(job_id, status):
    """
    Updates the status of the scraping job.
    """
    if not db:
        raise DatabaseError("Database connection not initialized")
    
    try:
        db.scraping_jobs.update_one(
            {"_id": job_id},
            {"$set": {"status": status, "updated_at": datetime.now(timezone.utc)}}
        )
    except OperationFailure as e:
        raise DatabaseError(f"Failed to update job status: {str(e)}")
