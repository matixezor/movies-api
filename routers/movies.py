from fastapi import APIRouter, Depends, status, Path, HTTPException, Query, Response
from typing import List
from schemas import Movie, MovieCreate, MovieBase

from sqlalchemy.orm import Session
import crud
from utils import get_db, get_admin, admin_text_desc


router = APIRouter()


@router.get('/', response_model=List[Movie], summary='Read movies', status_code=status.HTTP_200_OK)
def read_movies(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1), db: Session = Depends(get_db)):
    """
    Read movies.\n
    Optional query parameters:
    - **skip**: how many records to skip
    - **limit**: how many records to read
    """
    return crud.get_movies(db, skip=skip, limit=limit)


@router.post(
    '/',
    response_model=List[Movie],
    summary='Create movies',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_admin)]
)
def create_movies(movies: List[MovieCreate], db: Session = Depends(get_db)):
    """
    Create movies with all information:
    - **title**: required
    - **genre**: required
    - **director**: optional
    - **release_year**: optional
    - **rating**: required
    - **cost_per_day**: required
    """
    for movie in movies:
        if crud.get_movie_by_title(db, title=movie.title):
            movies.remove(movie)
    return crud.create_movies(db, movies=movies)


@router.get('/{movie_id}', response_model=Movie, summary='Read movie', status_code=status.HTTP_200_OK)
def read_movie(movie_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """
    Read movie. Path param **movie_id** must be greater or equal 1
    """
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if not db_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movie not found')
    return db_movie


@router.put(
    '/{movie_id}',
    response_model=Movie,
    summary='Modify movie',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_admin)]
)
def update_movie(movie: MovieBase, movie_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """
    Modify movie with given information:
    - **title**: required
    - **genre**: required
    - **director**: optional
    - **release_year**: optional
    - **rating**: required
    - **cost_per_day**: required
    """
    db_movie = crud.update_movie(db, movie_id=movie_id, movie=movie)
    if not db_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movie not found')
    return db_movie
