from typing import Optional, List
from pydantic import BaseModel


class Movie(BaseModel):
    title: str
    genre: str
    director: Optional[str] = None
    release_year: Optional[str] = None
    rating: float
    cost: int


class Purchase(BaseModel):
    id: int
    start_date: str
    expiry_date: str
    cost: int
    movies: List[Movie] = []

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    surname: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    purchases: List[Purchase] = []

    class Config:
        orm_mode = True
