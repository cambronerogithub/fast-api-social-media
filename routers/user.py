
import models as models
from database import engine, get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import schemas
from sqlalchemy.orm import Session
import utils, oauth2

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/{id}", response_model=schemas.UserOut)
def create_user(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The user with the id: {id} does not exist")
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    user_validation = db.query(models.User).filter(models.User.email == user.email).first()
    print(f"post_updated {user}")
    if user_validation != None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"The email: {user_validation.email} has been registered before")
    
    #hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    print(f"user: {user}")
    
    new_user = models.User(** dict(user))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get('/')
def get_user(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).all()
    return user
