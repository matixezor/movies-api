from fastapi import APIRouter, HTTPException, Depends, status, Path
from sqlalchemy.orm import Session
from typing import List
from datetime import date

import crud
from schemas import User, UserBase, PurchaseMovie, UserPurchase, UserUpdate, UserMovie, PurchaseCreate
from utils import get_db, admin_text_desc, get_user, get_date


router = APIRouter()


@router.get(
    '/',
    summary='Read users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    description=admin_text_desc
)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@router.get(
    '/{user_id}',
    summary='Read User information',
    response_model=User,
    status_code=status.HTTP_200_OK,
    description=admin_text_desc
)
def read_user(user: User = Depends(get_user)):
    return user


@router.put(
    '/{user_id}',
    summary='Modify User information',
    response_model=User,
    status_code=status.HTTP_200_OK,
    description=admin_text_desc
)
def modify_user(updated_user: UserUpdate, user: User = Depends(get_user), db: Session = Depends(get_db)):
    user_db = crud.get_user_by_email(db, updated_user.email)
    if user_db.ID != user.ID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already taken!')
    return crud.update_user(db, user_id=user.ID, user=updated_user)


@router.get(
    '/{user_id}/purchases',
    summary='Read User purchases',
    response_model=UserPurchase,
    status_code=status.HTTP_200_OK,
    description=admin_text_desc
)
def read_user_purchases(user: UserBase = Depends(get_user)):
    return user


@router.post(
    '/{user_id}/purchases',
    summary='Create User purchase',
    response_model=PurchaseMovie,
    status_code=status.HTTP_200_OK,
    description=admin_text_desc
)
def create_purchase(
        purchase: PurchaseCreate,
        movies: List[int],
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    days = (purchase.expiry_date-purchase.start_date).days + 1
    return crud.create_purchase(db, purchase=purchase, user_id=user.ID, days=days, movies=movies)


@router.get(
    '/{user_id}/purchases/{purchase_id}',
    summary='Read User purchase with full info',
    response_model=PurchaseMovie,
    status_code=status.HTTP_200_OK,
    description=admin_text_desc
)
def read_user_purchase(
        user: User = Depends(get_user),
        purchase_id: int = Path(..., ge=1),
        db: Session = Depends(get_db)
):
    db_purchase = crud.get_purchase_with_user_id(db, purchase_id=purchase_id, user_id=user.ID)
    if not db_purchase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Purchase for given user not found')
    return db_purchase


@router.get(
    '/{user_id}/movies',
    summary='Read User movies',
    response_model=List[UserMovie],
    status_code=status.HTTP_200_OK,
    description=admin_text_desc
)
def read_user_movies(user: User = Depends(get_user), db: Session = Depends(get_db)):
    db_movies = crud.get_user_movies(db, user_id=user.ID)
    if not db_movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movies not found')
    for movie in db_movies:
        movie.expired = True if get_date(movie.purchase.expiry_date) < date.today() else False
    return db_movies
