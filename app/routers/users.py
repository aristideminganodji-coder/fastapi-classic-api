from app import models
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.database import get_db
from app.core.logging import logger
from app.core.security import (
    get_current_active_user,
    get_current_admin_user,
    check_user_permission,
    get_password_hash,
    get_current_user
)

router = APIRouter(prefix="/users", tags=["Users"])

# === 1. ROUTES SPÉCIFIQUES (sans paramètres dynamiques) ===
@router.get("/me", response_model=schemas.UserOut)
def get_my_profile(
    current_user: models.User = Depends(get_current_active_user)
):
    """Profil de l'utilisateur connecté"""
    return current_user

@router.put("/me", response_model=schemas.UserOut)
def update_my_profile(
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Met à jour le profil de l'utilisateur connecté"""
    if user_update.email is not None:
        current_user.email = user_update.email
    
    if user_update.password is not None:
        current_user.hashed_password = get_password_hash(user_update.password)
    
    if user_update.is_active is not None:
        #seul l'utiliateur lui meme peut change desactiver son compte
        current_user.is_active = user_update.is_active
    
    db.commit()
    db.refresh(current_user)
    return current_user

#=== 2. ROUTES ADMINS SEULEMENT ===
@router.get("/admin-only",response_model=List[schemas.UserOut])
def get_all_users_admin(
    db:Session=Depends(get_db),
    current_user:models.User=Depends(get_current_admin_user)
):
    if current_user.role!="admin":
        raise HTTPException(status_code=400,detail="Not authorized")
    #Route test: accessible uniquement aux admins
    return db.query(models.User).all()

@router.put("/{user_id}/role",response_model=schemas.UserOut)
def change_user_role(
    user_id:int,
    new_role:str,
    db:Session=Depends(get_db),
    current_user:models.User=Depends(get_current_admin_user)
):
    #Change le role d'un utilisateur admin(admin seulement)
    if current_user.role!="admin":
        raise HTTPException(status_code=400,detail="Not authorized")
    
    if new_role not in ["user","admin"]:
        raise HTTPException(status_code=400,detail="Role must be 'user' or 'admin'")
    
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    
    user.role=new_role
    db.commit()
    db.refresh(user)
    return user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_account(
    user_id:int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Supprime un utilisateur.
    -Les admins peuvent supprimer n'importe qui
    -Les users normaux ne peuvent supprimer que leur propre compte"""
    #verifier les permissions
    logger.info(f"Tentative de suppression du user {user_id} par {current_user.email}")

    if current_user.role!="admin" and current_user.id!=user_id:
        logger.warning(f"Tentative non autpriser :{current_user.email} tente de supprimer user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
		)
    
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    
    db.delete(current_user)
    db.commit()
    logger.info(f"User {user_id} supprimer par {current_user.email}")
    return None

# === 3. ROUTES DYNAMIQUES (avec paramètres) ===
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db)
):
    """Détail d'un utilisateur par son ID"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# === 4. ROUTES GÉNÉRALES ===
@router.get("/", response_model=List[schemas.UserOut])
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user:models.User=Depends(get_current_user) 
):
    """Liste tous les utilisateurs"""
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users