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
    ID: int


class UserMovie(Movie):
    expired: Optional[bool] = None


class PurchaseBase(BaseModel):
    ID: int
    start_date: date
    expiry_date: date
    cost: int

    class Config:
        orm_mode = True


class Purchase(PurchaseBase):
    movie_list: List[MovieBase] = []


class UserBase(BaseModel):
    ID: int
    email: str

    class Config:
        orm_mode = True


class User(UserBase):
    name: str
    surname: str
    phone: Optional[str] = None
    address: Optional[str] = None
    is_admin: bool


class UserPurchase(UserBase):
    purchases: List[PurchaseBase] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
