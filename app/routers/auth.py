from fastapi import APIRouter,Depends,HTTPException,status
from app import models,schemas
from app.database import get_db
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.security import verify_password,get_password_hash,create_access_token,get_current_admin_user
from app.core.config import settings
from app.core.logging import logger
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter(prefix="/auth",tags=['Authentication'])

@router.post("/register",response_model=schemas.UserOut,status_code=status.HTTP_201_CREATED)
def register(user:schemas.UserCreate,db:Session=Depends(get_db)):
    #inscription d'un nouveau utilisateur
    #verifier si l'utilisateur existe deja
    existing_user=db.query(models.User).filter(models.User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    
    hashed_password=get_password_hash(user.password)

    #creer l'utilisateur avec le role "user" par defaut
    db_user=models.User(
        email=user.email,
        hashed_password=hashed_password,
        role="user"#par default tout le monde est un "user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

#route pour la creation d'admin
@router.post("/create-admin",response_model=schemas.UserOut)
def create_admin(
    user:schemas.UserCreate,
    db:Session=Depends(get_db)
):
    #Creer un utilisateur avec un role admin
    existing_user=db.query(models.User).filter(models.User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registere")
    
    hashed_password=get_password_hash(user.password)

    db_user=models.User(
        email=user.email,
        hashed_password=hashed_password,
        role="admin" # role admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/login",response_model=schemas.Token)
def login(
    form_data:OAuth2PasswordRequestForm=Depends(),
    db:Session=Depends(get_db)
):
    logger.info(f"Tentative de connexion pour {form_data.username}")
    #chercher l'utilisateur
    db_user=db.query(models.User).filter(
        models.User.email==form_data.username
    ).first()

    #verification
    if not db_user:
        logger.warning(f"Echec:email{form_data.username} inexistant")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    
    if not verify_password(form_data.password,db_user.hashed_password):
        logger.warning(f"Echec:mot de passe incorrect pour {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    
    if not db_user.is_active:
        logger.warning(f"Echec: compte inactif pour {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Compte inactif"
        )
    
    #creation du token
    access_token_expires=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data={
        "sub":db_user.email,
        "user_id":db_user.id,
        "role":db_user.role
    }

    access_token=create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )
    logger.info(f"Connexion reussie pour {db_user.email} (id:{db_user.id},role:{db_user.role})")

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }