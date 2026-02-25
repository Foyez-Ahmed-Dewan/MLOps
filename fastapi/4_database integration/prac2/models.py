from sqlalchemy import Column, String, Integer 
from database import Base

class Student(Base):
    __tablename__ = "student_info"
    
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(50))
    email = Column(String(50), unique = True, index = True)
    age = Column(Integer)