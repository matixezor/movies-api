from fastapi import APIRouter, Depends, status, Path, HTTPException
from typing import List
from schemas import Movie

from sqlalchemy.orm import Session
import crud
from utils import get_db

router = APIRouter()


@router.get("/", response_model=List[Movie], summary="Read movies", status_code=status.HTTP_200_OK)
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_movies(db, skip=skip, limit=limit)


@router.post("/", response_model=List[Movie], summary="Post movies", status_code=status.HTTP_201_CREATED)
def create_movies(movies: List[Movie], db: Session = Depends(get_db)):
    return crud.create_movies(db, movies=movies)


@router.get("/{movie_id}", response_model=Movie, summary="Read movie", status_code=status.HTTP_200_OK)
def read_movie(movie_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if not db_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return db_movie
