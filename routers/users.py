from typing import List
from datetime import date

from fastapi import APIRouter, HTTPException, Depends, status, Path
from sqlalchemy.orm import Session

import crud
from schemas import User, UserBase, Movie, Purchase, UserPurchase, UserMovie
from utils import get_db, get_admin, get_current_user, admin_text_desc, get_user, get_password_hash

router = APIRouter()


@router.get('/me', summary='Read info of yourself', response_model=User, status_code=status.HTTP_200_OK)
def read_self_user(user: User = Depends(get_current_user)):
    return user


@router.get(
    '/me/purchases',
    summary='Read info about your purchases',
    response_model=UserPurchase,
    status_code=status.HTTP_200_OK
)
def read_self_purchases(user: User = Depends(get_current_user)):
    return user


@router.get(
    '/me/purchases/{purchase_id}',
    summary='Read full info about your purchase',
    response_model=Purchase,
    status_code=status.HTTP_200_OK
)
def read_self_purchase(
        purchase_id: int = Path(..., ge=1),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_purchase = crud.get_purchase_with_user_id(db, purchase_id=purchase_id, user_id=user.ID)
    if not db_purchase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Purchase not found')
    return db_purchase


@router.get('/me/movies', summary='Read your movies', response_model=List[UserMovie], status_code=status.HTTP_200_OK)
def read_self_movies(user: UserBase = Depends(get_current_user), db: Session = Depends(get_db)):
    db_movies = crud.get_user_movies(db, user_id=user.ID)
    if not db_movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User movies not found')
    for movie in db_movies:
        year, month, day = (int(x) for x in movie.purchase.expiry_date.split('-'))
        movie.expired = True if date(year, month, day) < date.today() else False
    return db_movies


@router.get(
    '/',
    summary='Read users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_admin)],
    description=admin_text_desc
)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@router.get(
    '/{user_id}',
    summary='Read User information',
    response_model=User,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_admin)],
    description=admin_text_desc
)
def read_user(user: User = Depends(get_user)):
    return user


@router.get(
    '/{user_id}/purchases',
    summary='Read User purchases',
    response_model=UserPurchase,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_admin)],
    description=admin_text_desc
)
def read_user_purchases(user: UserBase = Depends(get_user)):
    return user


@router.get(
    '/{user_id}/purchases/{purchase_id}',
    summary='Read User purchase with full info',
    response_model=Purchase,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_admin)],
    description=admin_text_desc
)
def read_user_purchase(
        user_id: int = Path(..., ge=1),
        purchase_id: int = Path(..., ge=1),
        db: Session = Depends(get_db)
):
    db_purchase = crud.get_purchase_with_user_id(db, purchase_id=purchase_id, user_id=user_id)
    if not db_purchase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Purchase for given user not found')
    return db_purchase


@router.get(
    '/{user_id}/movies',
    summary='Read User movies',
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_admin)],
    description=admin_text_desc
)
def read_user_movies(user: UserBase = Depends(get_user), db: Session = Depends(get_db)):
    db_movies = crud.get_user_movies(db, user_id=user.ID)
    if not db_movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movies not found')
    return db_movies
