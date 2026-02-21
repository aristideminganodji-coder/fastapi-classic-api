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
