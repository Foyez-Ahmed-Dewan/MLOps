from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello():
    return {'message' : 'Welcome abroad!'}

## logging middleware

# store logs in a file
import logging 
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log",
    maxBytes=5_000_000, # 5MB
    backupCount=3  # keep last 3 backups
)

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler],
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@app.middleware('http')
async def log_middleware(request, call_next):
    import time 
    start = time.time()
    
    client_ip = request.client.host
    method = request.method
    path = request.url.path 
    
    response = await call_next(request)
    
    process_time = time.time() - start 
    
    logger.info(
        f"IP = {client_ip}, METHOD = {method} PATH = {path}"
        f"STATUS = {response.status_code} TIME = {process_time:.4f}s"
    )
    
    return response
    

