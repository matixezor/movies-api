from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.ID == user_id).first()


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


def get_purchase(db:Session, purchase_id: int):
    return db.query(models.Purchase).filter(models.Purchase.ID == purchase_id).first()

