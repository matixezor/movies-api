from typing import Optional, List
from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str

    class Config:
        orm_mode = True


class Movie(MovieBase):
    genre: str
    director: Optional[str] = None
    release_year: Optional[str] = None
    rating: float
    cost_per_day: int


class PurchaseBase(BaseModel):
    ID: int
    start_date: str
    expiry_date: str
    cost: int

    class Config:
        orm_mode = True


class Purchase(PurchaseBase):
    movie_list: List[Movie] = []


class UserBase(BaseModel):
    ID: int
    email: str

    class Config:
        orm_mode = True


class User(UserBase):
    name: str
    surname: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None


class UserPurchase(UserBase):
    purchases: List[PurchaseBase] = []
