from database import engine, Base, get_db
from models import User
from sqlalchemy.orm import Session

# this creates 'users' table in MySQL
Base.metadata.create_all(bind=engine)

# to drop table
# Base.metadata.drop_all(bind=engine)

# fastapi
from fastapi import FastAPI, Depends

app = FastAPI()

# routes
## create user
@app.post("/users/")
def create_user(name : str, email : str, db : Session = Depends(get_db)):
    new_user = User(naame=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# get all user
@app.get("/users/")
def get_users(db : Session = Depends(get_db)):
    return db.query(User).all()

# get single user
@app.get("/users/{user_id}")
def get_user(user_id : int, db : Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()

# update user
@app.put("/users/{user_id}")
def update_user(user_id : int, name : str, email : str, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user: 
        return {"error" : "User not found"}
    
    user.naame = name 
    user.email = email
    
    db.commit()
    db.refresh(user)
    
    return user 


# delete user
@app.delete("/users/{user_id}")
def delete_user(user_id : int, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user: 
        return {"error" : "User not found"}
    
    db.delete(user)
    db.commit()
    
    return {"message" : "user deleted"}

