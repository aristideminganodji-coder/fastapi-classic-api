from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    #Schema pour la reponse contenant le token
    access_token:str
    token_type:str

class TokenData(BaseModel):
    #schema pour les donnes contenus dans le token
    email:Optional[str]=None
    user_id:Optional[int]=None