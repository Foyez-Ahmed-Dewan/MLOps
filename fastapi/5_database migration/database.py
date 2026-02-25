from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from sqlalchemy.engine import URL

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="password",   # raw password here
    host="172.29.0.1",
    port=3306,
    database="db_mig"
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# db session
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()