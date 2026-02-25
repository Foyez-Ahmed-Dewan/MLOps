from database import engine, Base, get_db
from models import Student
from sqlalchemy.orm import Session

# create table
Base.metadata.create_all(bind=engine)

# fastapi
from fastapi import FastAPI, Depends

app = FastAPI()

# add new student
@app.post("/add_student")
def create_student(name: str, email: str, age : int, db : Session = Depends(get_db)):
    new_student = Student(name = name, email = email, age = age)
    db.add(new_student)
    db.commit()
    # db.flush()
    db.refresh(new_student)
    print(f"New student {name}, id {new_student.id}")
    return new_student

# get all student
@app.get("/get_all/")
def get_all_stu(db : Session = Depends(get_db)):
    return db.query(Student).all()

# get student by id
@app.get("/get_stu/{stu_id}")
def get_stu(stu_id : int, db : Session = Depends(get_db)):
    info = db.query(Student).filter(Student.id == stu_id).first()
    return info 

# update student age
@app.put("/update_info/{stu_id}")
def update_info(stu_id : int, new_age : int, db : Session=Depends(get_db)):
    user = db.query(Student).filter(Student.id == stu_id).first()
    
    if not user:
        return {"message" : "no user found"}
    
    user.age = new_age
    
    db.commit()
    db.refresh(user)
    
    return user 


# delete user
@app.delete("/users/{stu_id}")
def delete_user(stu_id : int, db : Session = Depends(get_db)):
    user = db.query(Student).filter(Student.id == stu_id).first()
    
    if not user: 
        return {"error" : "Student not found"}
    
    db.delete(user)
    db.commit()
    
    return {"message" : "Student deleted"}