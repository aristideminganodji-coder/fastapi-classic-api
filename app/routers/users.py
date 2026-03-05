from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app import schemas,models
from app.database import get_db
from app.routers.auth import pwd_context

router=APIRouter(prefix="/users",tags=["Users"])

#GET/users/
@router.get("/",response_model=list[schemas.UserOut])
def read_users(skip:int=0,limit=100,db:Session=Depends(get_db)):
	users=db.query(models.User).offset(skip).limit(limit).all()
	return users

#GET/users/{id}
@router.get("/{user_id}",response_model=schemas.UserOut)
def read_user(user_id:int,db:Session=Depends(get_db)):
	user=db.query(models.User).filter(models.User.id==user_id).first()
	if not user:
	    raise HTTPException(status_code=404,detail="User not found")
	return user

#PUT/users/{id}
@router.put("/{user_id}",response_model=schemas.UserOut)
def update_user(user_id:int,user_update:schemas.UserUpdate,db:Session=Depends(get_db)):
	user=db.query(models.User).filter(models.User.id==user_id).first()
	if not user:
	    raise HTTPException(status_code=404,detail="User not found")

	#Mise a jour des champs fournis
	if user_update.email:
	    user.email=user_update.email
	if user_update.password:
	    user.hashed_password=pwd_context.hash(user_update.password)
	if user_update.is_active is not None:
	    user.is_active=user_update.is_active

	db.commit()
	db.refresh(user)
	return user

#DELETE/users/{id}
@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int,db:Session=Depends(get_db)):
	user=db.query(models.User).filter(models.User.id==user_id).first()
	if not user:
	    raise HTTPException(status_code=404,detail="User not found")


	db.delete(user)
	db.commit()
	return None #204 No  Content
