from fastapi import APIRouter, HTTPException, Depends, status, Path
from sqlalchemy.orm import Session
from typing import List
from datetime import date

import crud
from schemas import User, UserBase, UserAdminCreate, PurchaseMovie, UserPurchase, UserUpdate, UserMovie, PurchaseCreate
from utils import get_db, get_user, get_date


router = APIRouter()


@router.get(
    '/',
    summary='Read users',
    response_model=List[User],
    status_code=status.HTTP_200_OK
)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Read Users.\n
    Optional query parameters:
    - **skip**: how many records to skip
    - **limit**: how many records to read
    """
    return crud.get_users(db, skip=skip, limit=limit)


@router.post(
    '/',
    summary='Create user',
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserAdminCreate, db: Session = Depends(get_db)):
    """
    Create user with all the information:
    - **email**: required
    - **name**: required
    - **surname**: required
    - **phone**: optional
    - **address**: optional
    - **password**: required
    - **is_admin**: optional, false by default
    """
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
    return crud.create_user(db, user=user)


@router.get(
    '/{user_id}',
    summary='Read User information',
    response_model=User,
    status_code=status.HTTP_200_OK
)
def read_user(user: User = Depends(get_user)):
    """
    Read user
    """
    return user


@router.put(
    '/{user_id}',
    summary='Modify User information',
    response_model=User,
    status_code=status.HTTP_200_OK
)
def modify_user(updated_user: UserUpdate, user: User = Depends(get_user), db: Session = Depends(get_db)):
    """
    Modify user with given information:
    - **email**: required
    - **name**: required
    - **phone**: optional
    - **address*: optional
    """
    user_db = crud.get_user_by_email(db, updated_user.email)
    if user_db.id != user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already taken!')
    return crud.update_user(db, user_id=user.id, user=updated_user)


@router.get(
    '/{user_id}/purchases',
    summary='Read User purchases',
    response_model=UserPurchase,
    status_code=status.HTTP_200_OK
)
def read_user_purchases(user: UserBase = Depends(get_user)):
    """
    Get purchases of user.
    """
    return user


@router.post(
    '/{user_id}/purchases',
    summary='Create User purchase',
    response_model=PurchaseMovie,
    status_code=status.HTTP_200_OK
)
def create_purchase(
        purchase: PurchaseCreate,
        movies: List[int],
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    """
    Create purchase for user with all the information:
    - **purchase**:

        * **start_date**: format 'YYYY-MM-DD'
        * **expiry_date**: format 'YYYY-MM-DD'
    - **movies**: list containing movie ids
    """
    days = (purchase.expiry_date-purchase.start_date).days + 1
    return crud.create_purchase(db, purchase=purchase, user_id=user.id, days=days, movies=movies)


@router.get(
    '/{user_id}/purchases/{purchase_id}',
    summary='Read User purchase with full info',
    response_model=PurchaseMovie,
    status_code=status.HTTP_200_OK
)
def read_user_purchase(
        user: User = Depends(get_user),
        purchase_id: int = Path(..., ge=1),
        db: Session = Depends(get_db)
):
    """
    Get purchase of user. Path param **purchase_id** must be greater or equal 1
    """
    db_purchase = crud.get_purchase_with_user_id(db, purchase_id=purchase_id, user_id=user.id)
    if not db_purchase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Purchase for given user not found')
    return db_purchase


@router.get(
    '/{user_id}/movies',
    summary='Read User movies',
    response_model=List[UserMovie],
    status_code=status.HTTP_200_OK
)
def read_user_movies(user: User = Depends(get_user), db: Session = Depends(get_db)):
    """
    Read movies of user
    """
    db_movies = crud.get_user_movies(db, user_id=user.id)
    if not db_movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movies not found')
    for movie in db_movies:
        movie.expired = True if get_date(movie.purchase.expiry_date) < date.today() else False
    return db_movies
