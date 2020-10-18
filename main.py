from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from routers import users, movies, me, purchases
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import Token
from utils import get_db, authenticate_user, create_access_token, get_current_user, get_admin
from schemas import UserCreate, User
from crud import get_user_by_email, create_user


app = FastAPI()


@app.post('/token', response_model=Token, tags=['token'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    **IMPORTANT!!**\n
    Instead of **username** use **email** address!!
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )

    return {'access_token': access_token, 'token_type': 'bearer'}


@app.post('/register', response_model=User, status_code=status.HTTP_201_CREATED, tags=['register'])
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
    return create_user(db, user=user)


app.include_router(me.router, prefix='/me', tags=['me'], dependencies=[Depends(get_current_user)])
app.include_router(users.router, prefix='/users', tags=['users'], dependencies=[Depends(get_admin)])
app.include_router(purchases.router, prefix='/purchases', tags=['purchases'], dependencies=[Depends(get_current_user)])
app.include_router(movies.router, prefix='/movies', tags=['movies'])
