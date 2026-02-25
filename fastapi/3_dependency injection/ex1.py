from fastapi import FastAPI, Depends

app = FastAPI()

# dependency 
def get_db():
    print("Opening database connection")
    db = "DB_CONNECTION_OBJECT"
    try:
        yield db
    finally:
        print("Closing database connection")
        
# routes that depends on db
@app.get('/')
async def read_root(db = Depends(get_db)):
    print("Using: ", db)
    return {"message" : "Hello World"}

#### Execution FLOW
# Opening database connection
# Using: DB_CONNECTION_OBJECT
# "message" : "Hello World"
# Closing database connection
