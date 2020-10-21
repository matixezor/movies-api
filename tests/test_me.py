from fastapi.testclient import TestClient

from .test_helpers import override_get_db, get_token

from config import test_admin_password, test_admin_username
from main import app
from utils import get_db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

token = get_token(test_admin_username, test_admin_password, client)


def test_read_self_user():
    response = client.get('/me', headers=token)
    assert response.status_code == 200
    assert response.json() == {
                                'id': 1,
                                'email': 'test_mail',
                                'name': 'test_name',
                                'surname': 'test_surname',
                                'phone': 'test_phone',
                                'address': 'test_address',
                                'is_admin': 1
                            }


def test_read_self_user_bad_token():
    response = client.get('/me', headers={'Authorization': 'Bearer 12345'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_self_purchases():
    response = client.get('/me/purchases', headers=token)
    assert response.status_code == 200
    assert response.json() == {
                                'email': 'test_mail',
                                'id': 1,
                                'purchases': [
                                    {
                                        'start_date': '2020-10-03',
                                        'expiry_date': '2020-10-09',
                                        'cost': 66,
                                        'id': 1,
                                        'user_id': 1
                                    },
                                    {
                                        'start_date': '2020-10-14',
                                        'expiry_date': '2020-11-15',
                                        'cost': 198,
                                        'id': 2,
                                        'user_id': 1
                                    }
                                ]
                            }


def test_read_self_purchases_bad_token():
    response = client.get('/me/purchases', headers={'Authorization': 'Bearer 12345'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_self_purchase():
    response = client.get('/me/purchases/2', headers=token)
    assert response.status_code == 200
    assert response.json() == {
                                'start_date': '2020-10-14',
                                'expiry_date': '2020-11-15',
                                'cost': 198,
                                'id': 2,
                                'user_id': 1,
                                'movie_list': [
                                    {
                                        'title': 'Venom',
                                        'genre': 'Action',
                                        'director': 'Ruben Fleischer',
                                        'release_year': None,
                                        'rating': 6.7,
                                        'cost_per_day': 6
                                    }
                                ]
                            }


def test_read_self_purchase_bad_token():
    response = client.get('/me/purchases/2', headers={'Authorization': 'Bearer 12345'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_self_movies():
    response = client.get('/me/movies', headers=token)
    assert response.status_code == 200
    assert response.json() == [
                                {
                                    'title': 'Project Power',
                                    'genre': 'Fantasy',
                                    'director': 'Henry Joost',
                                    'release_year': 2020, 'rating': 6.0,
                                    'cost_per_day': 5,
                                    'id': 2,
                                    'expired': True
                                },
                                {
                                    'title': '#Alive',
                                    'genre': 'Horror',
                                    'director': 'Il Cho',
                                    'release_year': 2020,
                                    'rating': 6.2,
                                    'cost_per_day': 6,
                                    'id': 3,
                                    'expired': True
                                },
                                {
                                    'title': 'Venom',
                                    'genre': 'Action',
                                    'director': 'Ruben Fleischer',
                                    'release_year': None,
                                    'rating': 6.7,
                                    'cost_per_day': 6,
                                    'id': 5,
                                    'expired': False
                                }
                            ]


def test_read_self_movies_bad_token():
    response = client.get('/me/movies', headers={'Authorization': 'Bearer 12345'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}
