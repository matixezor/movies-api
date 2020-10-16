from fastapi import APIRouter, HTTPException, Depends, status, Path
from typing import List
from sqlalchemy.orm import Session
from datetime import date

import crud
from schemas import User, UserBase, Purchase, UserPurchase, UserMovie
from utils import get_db, get_current_user


router = APIRouter()


@router.get('/', summary='Read info of yourself', response_model=User, status_code=status.HTTP_200_OK)
def read_self_user(user: User = Depends(get_current_user)):
    return user


@router.get(
    '/purchases',
    summary='Read info about your purchases',
    response_model=UserPurchase,
    status_code=status.HTTP_200_OK
)
def read_self_purchases(user: User = Depends(get_current_user)):
    return user


@router.get(
    '/purchases/{purchase_id}',
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


@router.get('/movies', summary='Read your movies', response_model=List[UserMovie], status_code=status.HTTP_200_OK)
def read_self_movies(user: UserBase = Depends(get_current_user), db: Session = Depends(get_db)):
    db_movies = crud.get_user_movies(db, user_id=user.ID)
    if not db_movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User movies not found')

    for movie in db_movies:
        year, month, day = (int(x) for x in movie.purchase.expiry_date.split('-'))
        movie.expired = True if date(year, month, day) < date.today() else False

    return db_movies
