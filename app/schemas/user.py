from typing import Optional 
from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
	email: EmailStr
	password: str

class UserOut(BaseModel):
	id:int
	email:EmailStr
	is_active:bool

class UserInDB(UserOut):
	hashed_password:str

class UserUpdate(BaseModel):
	email:Optional[EmailStr]=None
	password:Optional[str]=None
	is_active:Optional[bool]=None
