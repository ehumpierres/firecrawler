from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from app.exceptions import DatabaseError
from bson.objectid import ObjectId

load_dotenv()

def get_database():
    mongodb_uri = os.getenv('MONGO_URI')
    if not mongodb_uri:
        raise DatabaseError("MONGO_URI environment variable is not set")
    
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

def save_scraping_job(url: str) -> str:
    """Create a new scraping job"""
    result = db.jobs.insert_one({
        "url": url,
        "status": "pending",
        "created_at": datetime.utcnow()
    })
    return str(result.inserted_id)

def get_scraping_job(job_id: str) -> dict:
    """Retrieve a job and its data"""
    return db.jobs.find_one({"_id": ObjectId(job_id)})

def save_structured_data(job_id: str, data: dict, raw: bool = False) -> None:
    """Save data to the job document"""
    update_data = {
        "raw_data" if raw else "processed_data": data,
        "updated_at": datetime.utcnow()
    }
    db.jobs.update_one(
        {"_id": ObjectId(job_id)},
        {"$set": update_data}
    )

def update_job_status(job_id: str, status: str) -> None:
    """Update job status"""
    db.jobs.update_one(
        {"_id": ObjectId(job_id)},
        {
            "$set": {
                "status": status,
                "updated_at": datetime.utcnow()
            }
        }
    )
