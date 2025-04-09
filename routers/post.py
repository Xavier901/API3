from fastapi import FastAPI,HTTPException,status,Response,Depends,APIRouter
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List

import models,schemas
from database import get_db


router=APIRouter()

@router.get("/posts",response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
    postss=db.query(models.Post).all()
    #print(postss)
    return postss



@router.post("/post",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db:Session=Depends(get_db)):  
    new_post=models.Post(
        **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #print(new_post) 
    return new_post

@router.get("/posts/{ids}")
def get_post(ids:int,db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==ids).first()
    #print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{ids} was not found")
    return post




@router.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):    
    post=db.query(models.Post).filter(models.Post.id==id)  
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.put("/post/{id}")
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    posts=post_query.first()
    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} doesn't exist")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
