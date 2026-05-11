# middleware.py
import logging
import time
from fastapi import Request, Response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def log_requests(request: Request, call_next):
    """
    Middleware to log request details, including method, path, and processing time.
    """
    request_id = id(request)
    start_time = time.time()
    
    # Log the incoming request
    logger.info(f"[{request_id}] {request.method} {request.url.path} - Started")
    
    # Process the request
    response: Response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Add a custom header with the process time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log the completed request
    logger.info(f"[{request_id}] {request.method} {request.url.path} - Completed in {process_time:.4f}s with status {response.status_code}")
    
    return response