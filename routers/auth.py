from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import database,schemas,models,utils,oauth


router=APIRouter(tags=['Authentication'])

#response_model=schemas.Token
@router.post('/login',response_model=schemas.TokenM)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    
    user=db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials.")
        
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials.")
    
    acess_token=oauth.create_acess_token(data={"user_id":user.id})
    
    return {"acess_token":acess_token,"token_type":'bearer'}    