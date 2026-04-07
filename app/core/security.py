from datetime import datetime,timedelta,timezone
from jose import JWTError,jwt
from typing import Optional,Dict
from app.core.config import settings
from passlib.context import CryptContext
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

#Configuration du context de hachage
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

#configuration OAuth2
#Indiquer a fastapi ou chercher le token(dans le header Authorization)
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

#Fonction pour le mot de passe
def verify_password(plain_password:str,hashed_password:str)->bool:
    #verifie si le mot de passe correspond au hash
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password:str)->str:
    #hash du mot de passe avec bcrypt
    return pwd_context.hash(password)

#Fonction pour les JWT
def create_access_token(data:Dict,expires_delta:Optional[timedelta]=None)->str:
    #creer un jwt avec les donnees fournis
    to_encode=data.copy()
    #ajout de l'expiration
    if expires_delta:
        expire=datetime.now(timezone.utc)+expires_delta
    else:
        expire=datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    #creation du token
    encode_jwt=jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return encode_jwt

def verify_token(token:str)->Optional[Dict]:
    #verifie la validite du token et retourne son contenu
    try:
        payload=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
    
#Dependances pour les routes protegees
async def get_current_user(
        token:str=Depends(oauth2_scheme),
        db:Session=Depends(get_db)
):
    """Recuperer l'utilisateur courant a partir du token JWT
    A utiliser comme dependance dans les routes protegees"""
    #Creer un exception en cas d'echec
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"www-Authenticate":"Bearer"}
    )

    #verifier le token
    payload=verify_token(token)
    if payload is None:
        raise credentials_exception
    
    #Extraire l'email du token
    email=payload.get("sub")
    user_id=payload.get("user_id")

    if email is None or user_id is None:
        raise credentials_exception
    
    #chercher l'utilisateur dans la base
    user=db.query(models.User).filter(models.User.email==email).first()

    if user is None:
        raise create_access_token
    
    return user

async def get_current_active_user(
        current_user=Depends(get_current_user)
):
    #verifier que l'utilisateur est actif
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Inactive user")
    return current_user

#creer les dependances des roles
async def get_current_admin_user(
        current_user:models.User=Depends(get_current_active_user)
):
    """
    Verifier que l'utilisateur est un admin
    A utiliser pour les routes reservees aux administrateurs
    """
    if current_user.role!="admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions, Admin role required."
        )
    return current_user

def check_user_permission(
        requested_user_id:int,
        current_user:models.user
):
    """
    Verifier si l'utilisateur a le droit de modifier/supprimer un compte.
    - Les admins peuvent tout faire
    - Les users normaux ne peuvent agir que sur leur propre compte
    """
    if current_user.role!="admin" and current_user.id!=requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action on another user"
        )
    return True