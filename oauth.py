from jose import JWTError,jwt
from datetime import datetime,timedelta
import schemas,database,models
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_acess_token(data:dict):
    to_encode=data.copy()
    
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    
    encode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt
    
    
    
def verify_acess_token(token:str,credential_exception):
    
    try:
        
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        iss:str = payload.get("user_id")
        if iss is None:
            raise credential_exception
        
        id_value = str(iss)
        
        token_data=schemas.TokenData(id=id_value)
        
    except JWTError:
        raise credential_exception
    
    return token_data



def get_current_user(token:str = Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
   
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                       detail=f"Could not validate credential",
                                       headers={"WWW-Authenticate":"Bearer"})
    
    Token= verify_acess_token(token,credential_exception)
    user=db.query(models.User).filter(models.User.id==Token.id).first()
    return user
    

