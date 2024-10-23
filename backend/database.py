from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/Library_management"
# Creating an Engine  which establishes a connection to the database
engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency function that will be used to get a new database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
