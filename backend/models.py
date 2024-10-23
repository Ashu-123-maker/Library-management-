from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, ForeignKey,func
from sqlalchemy.orm import sessionmaker,declarative_base,relationship
from datetime import datetime
URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/Library_management"
# Creating an Engine  which establishes a connection to the database
engine = create_engine(URL)
Base = declarative_base()

#creating librarian table which inherits from Base class
class Librarian(Base):
    __tablename__ = 'Librarian'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phonenumber = Column(String, nullable=False)  
    address = Column(String, nullable=False)
    role= Column(String, nullable=False)
    password=Column(String,nullable=False)
    children = relationship("Log_Operations", back_populates="parent")


class Books(Base):
    __tablename__ = 'Books'
    ISBN = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('Category.category_id'), nullable=False)
    Category = relationship("Category", back_populates="Books")


#Creating the Log_Operations Which inherits from Base class
class Log_Operations(Base):
    __tablename__ = 'Log_Operations'
    log_id=Column(Integer,primary_key=True)
    id= Column(Integer, ForeignKey('Librarian.id'), nullable=False)
    name = Column(String, nullable=False)
    title=Column(String,nullable=False)
    borrow_date = Column(Date, default=func.now(), nullable=False)
    return_date = Column(Date , nullable=False)
    parent = relationship("Librarian", back_populates="children")

#Creating the Log_Operations Which inherits from Base class

class Category(Base):
    __tablename__ = 'Category'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False ,unique=True)
    shelf_no = Column(Integer)
    Books = relationship("Books", back_populates="Category")

#Creating all tables
Base.metadata.create_all(engine)


#creating a session to perform operations
Session = sessionmaker(bind=engine)
session = Session()

