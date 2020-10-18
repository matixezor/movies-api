from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.orm import Session

import crud
from schemas import User, Purchase, PurchaseMovie, PurchaseCreate
from utils import get_db, get_current_user, get_admin


router = APIRouter()


@router.get('/', summary='Read purchases', response_model=List[Purchase], dependencies=[Depends(get_admin)])
def read_purchases(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1), db: Session = Depends(get_db)):
    return crud.get_purchases(db, skip=skip, limit=limit)


@router.post('/', summary='Create purchase', response_model=PurchaseMovie)
def create_purchase(
        purchase: PurchaseCreate,
        movies: List[int],
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    days = (purchase.expiry_date-purchase.start_date).days + 1
    return crud.create_purchase(db, purchase=purchase, user_id=user.ID, days=days, movies=movies)
