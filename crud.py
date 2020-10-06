from sqlalchemy.orm import Session

from typing import List

import models
from schemas import Movie


def get_users(db: Session, skip: int, limit: int):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.ID == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_movies(db: Session, user_id: int):
    return db.query(models.Movie).\
        join(models.MovieList).\
        join(models.Purchase).\
        filter(models.Purchase.user_id == user_id).all()


def get_purchase_movies(db: Session, purchase_id: int):
    return db.query(models.Movie). \
        join(models.MovieList). \
        join(models.Purchase). \
        filter(models.Purchase.ID == purchase_id).all()


def get_purchase(db: Session, purchase_id: int):
    return db.query(models.Purchase).filter(models.Purchase.ID == purchase_id).first()


def get_movies(db: Session, skip: int, limit: int):
    return db.query(models.Movie).offset(skip).limit(limit).all()


def create_movies(db:Session, movies: List[Movie]):
    db_movies = [models.Movie(**movie.dict()) for movie in movies]
    db.add_all(db_movies)
    db.commit()
    for movie in db_movies:
        db.refresh(movie)
    return db_movies


def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.ID == movie_id).first()
