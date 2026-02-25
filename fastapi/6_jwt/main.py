from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User
from auth import hash_password, verify_password, create_access_token, decode_access_token

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# oauth2 schema
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# signup route
@app.post("/signup")
def signup(email: str, password: str, db : Session = Depends(get_db)):
    # check if user already exist or not?
    exist = db.query(User).filter(User.email == email).first()
    
    if exist:
        raise HTTPException(status_code=400, detail="User already exists")
    # if user doesn't exist yet, add him/her
    hashed_pw = hash_password(password)
    
    user = User(email=email, password_hash = hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"message" : "user created"}

# login route
@app.post("/login")
def login(
    form_data : OAuth2PasswordRequestForm = Depends(), 
    db : Session = Depends(get_db)
):
    # check if credential is valid or not
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # if valid, create a token
    token = create_access_token({"sub" : str(user.id)})
    
    return {"access_token" : token, "token_type" : "bearer"}

# protected route
@app.get("/profile")
def profile(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_access_token(token)
    
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return {"id" : user.id, "email" : user.email}


