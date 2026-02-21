from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app import schemas,models
from app.database import get_db
from passlib.context import CryptContext

router=APIRouter(prefix="/auth",tags=["Authentication"])
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

@router.post("/register",response_model=schemas.UserOut,status_code=status.HTTP_201_CREATED)
def register(user:schemas.UserCreate,db:Session=Depends(get_db)):
	#verifier si l'email exite deja
	existing_user=db.query(models.User).filter(models.User.email==user.email).first()
	if existing_user:
	    raise HTTPException(status_code=400,detail="Email already registered")

	#Hasher le mot de passe
	hashed_password=pwd_context.hash(user.password)

	#Creer l'utilisateur
	db_user=models.User(email=user.email,hashed_password=hashed_password)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)

	return db_user
