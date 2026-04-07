from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    #base de donne
    DATABASE_URL:str=os.getenv("DATABASE_URL","postgresql://fastapi_user:password123@localhost/fastapi_classic")

    #JWT config
    SECRET_KEY:str=os.getenv("SECRET_KEY","e7078263cdef5fe2223d400fd2b0cdbfe9ad7a199a82f760c3642654799dd591")
    ALGORITHM:str=os.getenv("ALGORITHM","HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES:int=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","30"))

    class Config:
        env_file=".env"
        case_sensitive=True

settings=Settings()