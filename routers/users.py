from fastapi import APIRouter

from schemas import User

users = {
    '1': {
        'name': 'Mateusz',
        'surname': 'Romański',
        'email': 'mat@int.pl',
        'phone': None,
        'address': 'Pruszcz'
    }
}


router = APIRouter()


@router.get("/{user_id}", response_model=User)
def read_users(user_id: str):
    return users.get(user_id)
