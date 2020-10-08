from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn

from routers import users, movies
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy.orm import Session
from schemas import Token

from utils import get_db, authenticate_user, create_access_token, get_current_user


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


app.include_router(users.router, prefix='/users', tags=['users'], dependencies=[Depends(get_current_user)])
app.include_router(movies.router, prefix='/movies', tags=['movies'])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
