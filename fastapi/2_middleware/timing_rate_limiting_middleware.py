from fastapi import FastAPI, Request
from pydantic import BaseModel
import time

app = FastAPI()


# timing middleware measures amount of time taken by each request to process
@app.middleware("http")
async def add_process_time_header(request, call_next):
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Request to {request.url.path} took {process_time} seconds")
    return response


# rate limit middleware control request frequency
from fastapi.responses import JSONResponse

# store timestamps of requests per IP
requests_log = {}

RATE_LIMIT = 5 # number of requests
RATE_TIME = 10 # time window(seconds)

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()
    
    # create key if the user is new
    if client_ip not in requests_log:
        requests_log[client_ip] = []
    
    # remove timestamps older than RATE_TIME
    requests_log[client_ip] = [
        t for t in requests_log[client_ip] if current_time - t < RATE_TIME
    ]

    # check limit
    if len(requests_log[client_ip]) >= RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={"message": "Too many requests, slow down!"}
        )

    # record this request
    requests_log[client_ip].append(time.time())

    # continue normal request processing
    response = await call_next(request)
    
    return response


        
@app.get("/test/")
async def test():
    return {"message" : "Request successful"}