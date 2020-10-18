from sqlalchemy import Float, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "Users"

    ID = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)
    is_admin = Column(Boolean, default=False)

    purchases = relationship("Purchase", back_populates="user")


class Purchase(Base):
    __tablename__ = "Purchases"

    ID = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.ID"))
    start_date = Column(String, nullable=False)
    expiry_date = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)

    user = relationship("User", back_populates="purchases")
    movie_list = relationship("Movie", secondary="MoviesLists", back_populates="purchase")


class MovieList(Base):
    __tablename__ = "MoviesLists"

    purchase_id = Column(Integer, ForeignKey("Purchases.ID"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("Movies.ID"), primary_key=True)


class Movie(Base):
    __tablename__ = "Movies"

    ID = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    director = Column(String)
    release_year = Column(Integer)
    genre = Column(String, nullable=False)
    rating = Column(Float)
    cost_per_day = Column(Integer, nullable=False)

    purchase = relationship("Purchase", secondary="MoviesLists", back_populates="movie_list", uselist=False)
