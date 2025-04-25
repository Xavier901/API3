from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from fastapi.middleware.cors import CORSMiddleware
from database import engine,get_db
import models,schemas,utils
from routers import post,user,auth


#models.Base.metadata.create_all(bind=engine)
app=FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)       
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def get_index():
    return{"Data":"Sucessfully Tested."}


# @app.get("/sqlpost")
# def test_post(db:Session=Depends(get_db)):
#     posts=db.query(models.Post).all()
#     return{"data":posts}




 