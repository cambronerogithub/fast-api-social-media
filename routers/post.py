import models
from typing import List, Optional
from database import engine, get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import schemas
from sqlalchemy import func
from sqlalchemy.orm import Session
import oauth2

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed!")
#         print(f"Error is: {error}")
#         time.sleep(2)


@router.get('/profile/{id}', response_model=List[schemas.Post])
def get_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    profile_query = db.query(models.User).filter(models.User.id == id)
    profile = profile_query.first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The profile with the id: {id} does not exist in our database')

    
    posts = db.query(models.Post).filter(models.Post.owner_id == id).all()
    return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_specific_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # specific_post = cursor.fetchone()
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(models.Post.id == id).group_by(models.Post.id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post with the id: {id} does not exist in our database')

    return post


# @router.get('/', response_model=List[schemas.Post])
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    print(f"limit: {limit}")
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(f"current_user: {current_user.email}")
    new_post = models.Post(owner_id=current_user.id, **dict(post))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post



@router.delete("/{id}")
def delete_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"We did not find any post with the id: {id}")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return f"The post with the id: {id} has been deleted"

@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_updated = post_query.first()
    
    if post_updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"We did not find any post with the id: {id}")
    
    if post_updated.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(dict(updated_post), synchronize_session = False)
    
    db.commit()
    
    return post_query.first()