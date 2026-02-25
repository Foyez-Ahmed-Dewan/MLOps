from fastapi import FastAPI, Depends, HTTPException, Request
import time

app = FastAPI()


# Database dependency
def get_db():
    print("Opening DB connection")
    db = {"connection": "active"}
    try:
        yield db
    finally:
        print("Closing DB connection")


# Authentication dependency
def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    
    if token != "secret-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return {"username": "foyez"}


# Dependency inside dependency
def get_user_db(
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    print("User validated and DB ready")
    return {"db": db, "user": user}


# Route
@app.get("/dashboard")
def dashboard(context = Depends(get_user_db)):
    return {
        "message": "Welcome",
        "user": context["user"],
        "db_status": context["db"]["connection"]
    }
