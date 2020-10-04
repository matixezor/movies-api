from fastapi import APIRouter, HTTPException, Depends, status, Path

from typing import List

from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(user_id: int = Path(..., ge=1), db: Session = Depends(get_db)) -> schemas.User:
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.get("/{user_id}", summary="Read User information", response_model=schemas.User, status_code=status.HTTP_200_OK)
def read_user(user: schemas.User = Depends(get_user)):
    return user


@router.get(
    "/{user_id}/purchases",
    summary="Read User purchases",
    response_model=schemas.UserPurchase,
    status_code=status.HTTP_200_OK
)
def read_user_purchases(user: schemas.UserBase = Depends(get_user)):
    return user


@router.get(
    "/{user_id}/purchases/{purchase_id}",
    summary="Read User purchase with movies",
    response_model=schemas.Purchase,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_user)]
)
def read_user_purchase_movies(purchase_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    db_purchase = crud.get_purchase(db, purchase_id=purchase_id)
    if not db_purchase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")
    db_purchase_movies = crud.get_purchase_movies(db, purchase_id=purchase_id)
    db_purchase.movie_list = db_purchase_movies
    return db_purchase


@router.get(
    "/{user_id}/movies",
    summary="Read User movies",
    response_model=List[schemas.Movie],
    status_code=status.HTTP_200_OK
)
def read_user_movies(user: schemas.UserBase = Depends(get_user), db: Session = Depends(get_db)):
    db_movies = crud.get_user_movies(db, user_id=user.ID)
    return db_movies
