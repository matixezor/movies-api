from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn

from typing import Optional
import crud
from passlib.context import CryptContext
from routers import users, movies
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from schemas import Token, TokenData

from utils import get_db, verify_password, get_password_hash, get_current_user, authenticate_user, create_access_token


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


# def verify_password(plain_password: str, hashed_password: str):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password: str):
#     return pwd_context.hash(password)
#
#
# def authenticate_user(email: str, password: str, db: Session):
#     user = crud.get_user_by_email(db, email=email)
#     if not user:
#         return False
#     if not verify_password(password, user.password):
#         return False
#     return user
#
#
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         token_data = TokenData(email=email)
#     except JWTError:
#         raise credentials_exception
#     user = crud.get_user_by_email(db, email=token_data.email)
#     if user is None:
#         raise credentials_exception
#     return user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    **IMPORTANT!!**\n
    Instead of **username** use your **email** address value!!
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


app.include_router(users.router, prefix='/users', tags=['users'], dependencies=[Depends(get_current_user)])
app.include_router(movies.router, prefix='/movies', tags=['movies'])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
