
from pydantic import BaseModel,EmailStr,Field
from datetime import date



#creating data transfer object for librarian
class LibrarianDTO(BaseModel):  

    name: str
    password: str
    email: EmailStr
    phonenumber:str
    address: str
    role: str = Field(default="user")
    

#creating data transfer object for Books    
class BooksDTO(BaseModel):  
    ISBN:str
    title:str
    author:str
    category_id:int

                
# Data Transfer Object for Book Category inheriting from BooksDTO
class CategoryDTO(BaseModel):  
    category_name:str
    shelf_no:int
 


#Creating Data Transfer Object for Log Operations
class Log_OperationsDTO(BaseModel):
  
    id:int
    name:str
    title:str
    borrow_date:date
    return_date:date

# Data Transfer Object for User inheriting from LibrarianDTO
class UserDTO(LibrarianDTO):
    status:str
    date_of_reg:date


class SuccessDTO(BaseModel):
    status_code: int
    message: str


class LoginDTO(BaseModel):
    email: str
    password: str

class Config:
    orm_mode = True