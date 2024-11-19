class ScrapingError(Exception):
    """Raised when there's an error during web scraping"""
    pass

class ProcessingError(Exception):
    """Raised when there's an error during Claude processing"""
    pass

class DatabaseError(Exception):
    """Raised when there's an error with MongoDB operations"""
    pass 