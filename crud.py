from sqlalchemy.orm import Session
from typing import List

import models
from schemas import MovieCreate, MovieBase, UserUpdate, UserCreate, PurchaseCreate
from utils import get_password_hash


def get_users(db: Session, skip: int, limit: int):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def update_user(db: Session, user_id: int, user: UserUpdate):
    db.query(models.User).filter(models.User.id == user_id).update(user.dict(), synchronize_session=False)
    db.commit()
    return get_user(db, user_id=user_id)


def create_user(db: Session, user: UserCreate):
    user.password = get_password_hash(user.password)
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_movies(db: Session, user_id: int):
    return db.query(models.Movie).\
        join(models.MovieList).\
        join(models.Purchase).\
        filter(models.Purchase.user_id == user_id).all()


def get_purchase_movies(db: Session, purchase_id: int):
    return db.query(models.Movie). \
        join(models.MovieList). \
        join(models.Purchase). \
        filter(models.Purchase.id == purchase_id).all()


def get_purchase(db: Session, purchase_id: int):
    return db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()


def create_purchase(db: Session, purchase: PurchaseCreate, user_id: int, days: int, movies: List[int]):
    db_movies = db.query(models.Movie).filter(models.Movie.id.in_(movies)).all()
    cost = 0

    for db_movie in db_movies:
        cost += days * db_movie.cost_per_day

    db_purchase = models.Purchase(**purchase.dict(), user_id=user_id, cost=cost)
    db_purchase.movie_list = [db_movie for db_movie in db_movies]

    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)

    return db_purchase


def get_purchases(db: Session, skip: int, limit: int):
    return db.query(models.Purchase).offset(skip).limit(limit).all()


def get_purchase_with_user_id(db: Session, purchase_id: int, user_id: int):
    return db.query(models.Purchase). \
        filter(models.Purchase.id == purchase_id, models.Purchase.user_id == user_id).first()


def get_movies(db: Session, skip: int, limit: int):
    return db.query(models.Movie).offset(skip).limit(limit).all()


def create_movies(db: Session, movies: List[MovieCreate]):
    db_movies = [models.Movie(**movie.dict()) for movie in movies]
    db.add_all(db_movies)
    db.commit()
    for movie in db_movies:
        db.refresh(movie)
    return db_movies


def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def get_movie_by_title(db: Session, title: str):
    return db.query(models.Movie).filter(models.Movie.title == title).first()


def update_movie(db: Session, movie_id: int, movie: MovieBase):
    db.query(models.Movie).filter(models.Movie.id == movie_id).update(movie.dict(), synchronize_session=False)
    db.commit()
    return get_movie(db, movie_id=movie_id)


def delete_movie(db: Session, movie_id: int):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).delete(synchronize_session='fetch')
    db.commit()
    return db_movie
