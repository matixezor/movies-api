from sqlalchemy import Float, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "Users"

    ID = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)

    purchases = relationship("Purchase", back_populates="user")


class Purchase(Base):
    __tablename__ = "Purchases"

    ID = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.ID"))
    start_date = Column(String, nullable=False)
    expiry_date = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)

    user = relationship("User", back_populates="purchases")
    movie_list = relationship("MovieList", back_populates="receipt")


class MovieList(Base):
    __tablename__ = "MoviesLists"

    purchase_id = Column(Integer, ForeignKey("Purchases.ID"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("Movies.ID"), primary_key=True)

    receipt = relationship("Purchase", back_populates="movie_list")
    movie = relationship("Movie", back_populates="movie_list")


class Movie(Base):
    __tablename__ = "Movies"

    ID = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True, nullable=False)
    director = Column(String)
    release_year = Column(Integer)
    genre = Column(String, nullable=False)
    rating = Column(Float)
    cost_per_day = Column(Integer, nullable=False)

    movie_list = relationship("MovieList", back_populates="movie")
