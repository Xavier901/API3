from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

    
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode=True
  
class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True
    
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:UserOut
    
    class Config:
        orm_mode=True
        
        
class UserCreate(BaseModel):
    email:EmailStr
    password:str
    

        
        
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class TokenM(BaseModel):
    acess_token:str
    token_type:str
    
class TokenData(BaseModel):
    #id: str
    id:Optional[str]=None 