from fastapi import FastAPI

import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import FastAPI,HTTPException,status,Response,Depends

from typing import List
from sqlalchemy.orm import Session
from database import engine,get_db
import models,schemas






models.Base.metadata.create_all(bind=engine)
app=FastAPI()



        
        
        


        

@app.get("/")
def get_index():
    return{"Data":"Sucessfully Tested."}


# @app.get("/sqlpost")
# def test_post(db:Session=Depends(get_db)):
#     posts=db.query(models.Post).all()
#     return{"data":posts}


@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
    postss=db.query(models.Post).all()
    #print(postss)
    return postss



@app.post("/post",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db:Session=Depends(get_db)):  
    new_post=models.Post(
        **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #print(new_post) 
    return new_post

@app.get("/posts/{ids}")
def get_post(ids:int,db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==ids).first()
    #print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{ids} was not found")
    return post




@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):    
    post=db.query(models.Post).filter(models.Post.id==id)  
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)





@app.put("/post/{id}")
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    posts=post_query.first()
    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} doesn't exist")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()



