from fastapi import APIRouter

from schemas import Movie


router = APIRouter()


@router.get("/{movie_id}", response_model=Movie)
def read_users(movie_id: str):
    return users.get(movie_id)