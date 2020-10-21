from datetime import date
from typing import Optional, List
from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    genre: str
    director: Optional[str] = None
    release_year: Optional[int] = None
    rating: float
    cost_per_day: int

    class Config:
        orm_mode = True


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int


class UserMovie(Movie):
    expired: Optional[bool] = None


class PurchaseBase(BaseModel):
    start_date: date
    expiry_date: date

    class Config:
        orm_mode = True


class Purchase(PurchaseBase):
    cost: int
    id: int
    user_id: int


class PurchaseMovie(Purchase):
    movie_list: List[MovieCreate] = []


class PurchaseCreate(PurchaseBase):
    pass


class UserBase(BaseModel):
    email: str

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    name: str
    surname: str
    phone: Optional[str] = None
    address: Optional[str] = None


class User(UserUpdate):
    is_admin: bool
    id: int


class UserCreate(UserUpdate):
    password: str


class UserAdminCreate(UserCreate):
    is_admin: Optional[bool] = None


class UserPurchase(UserBase):
    id: int
    purchases: List[Purchase] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
