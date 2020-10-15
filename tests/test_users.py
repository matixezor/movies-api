from fastapi.testclient import TestClient

from .test_utils import override_get_db, get_token

from config import test_admin_password, test_admin_username, test_password, test_username
from main import app
from utils import get_db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

admin_token = get_token(test_admin_username, test_admin_password, client)
token = get_token(test_username, test_password, client)


def test_read_self_user():
    response = client.get('/users/me', headers=admin_token)
    assert response.status_code == 200
    assert response.json() == {
                                'ID': 1,
                                'email': 'test_mail',
                                'name': 'test_name',
                                'surname': 'test_surname',
                                'phone': 'test_phone',
                                'address': 'test_address',
                                'is_admin': 1
                            }


def test_read_self_user_bad_token():
    response = client.get('/users/me', headers={'Authorization': 'Bearer 12345'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_self_purchases():
    response = client.get('/users/me/purchases', headers=admin_token)
    assert response.status_code == 200
    assert response.json() == {
                                'ID': 1,
                                'email': 'test_mail',
                                'purchases': [
                                    {
                                        'ID': 1,
                                         'start_date': '2020-10-03',
                                         'expiry_date': '2020-10-09',
                                         'cost': 66
                                     },
                                    {
                                        'ID': 2,
                                        'start_date': '2020-10-14',
                                        'expiry_date': '2020-11-15',
                                        'cost': 198
                                    }
                                ]
                            }


def test_read_self_purchases_bad_token():
    response = client.get('/users/me/purchases', headers={'Authorization': 'Bearer 12345'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_self_purchase():
    response = client.get('/users/me/purchases/2', headers=admin_token)
    assert response.status_code == 200
    assert response.json() == {
                                'ID': 2,
                                'start_date': '2020-10-14',
                                'expiry_date': '2020-11-15',
                                'cost': 198,
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
    response = client.get('/users/me/purchases/2', headers={'Authorization': 'Bearer 12345'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_self_movies():
    response = client.get('/users/me/movies', headers=admin_token)
    assert response.status_code == 200
    assert response.json() == [
                                {
                                    'title': 'Project Power',
                                    'genre': 'Fantasy',
                                    'director': 'Henry Joost',
                                    'release_year': 2020, 'rating': 6.0,
                                    'cost_per_day': 5,
                                    'ID': 2,
                                    'expired': True
                                },
                                {
                                    'title': '#Alive',
                                    'genre': 'Horror',
                                    'director': 'Il Cho',
                                    'release_year': 2020,
                                    'rating': 6.2,
                                    'cost_per_day': 6,
                                    'ID': 3,
                                    'expired': True
                                },
                                {
                                    'title': 'Venom',
                                    'genre': 'Action',
                                    'director': 'Ruben Fleischer',
                                    'release_year': None,
                                    'rating': 6.7,
                                    'cost_per_day': 6,
                                    'ID': 5,
                                    'expired': False
                                }
                            ]


def test_read_self_movies_bad_token():
    response = client.get('/users/me/movies', headers={'Authorization': 'Bearer 12345'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_users():
    response = client.get('/users', headers=admin_token)
    assert response.status_code == 200
    assert response.json() == [
                                {
                                    'ID': 1,
                                    'email': 'test_mail',
                                    'name': 'test_name',
                                    'surname': 'test_surname',
                                    'phone': 'test_phone',
                                    'address': 'test_address',
                                    'is_admin': True
                                },
                                {
                                    'ID': 2,
                                    'email': 'test_1',
                                    'name': 'test_2',
                                    'surname': 'test_3',
                                    'phone': 'test_4',
                                    'address': 'test_5',
                                    'is_admin': False
                                }
                            ]


def test_read_users_insufficient_permission():
    response = client.get('/users', headers=token)
    assert response.status_code == 403
    assert response.json() == {'detail': 'Insufficient permissions'}


def test_read_users_bad_token():
    response = client.get('/users', headers={'Authorization': 'Bearer 1234'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_users_skip_first():
    response = client.get('/users/?skip=1', headers=admin_token)
    assert response.status_code == 200
    assert response.json() == [
                                {
                                    'ID': 2,
                                    'email': 'test_1',
                                    'name': 'test_2',
                                    'surname': 'test_3',
                                    'phone': 'test_4',
                                    'address': 'test_5',
                                    'is_admin': False
                                }
                            ]


def test_read_users_limit_one():
    response = client.get('/users/?limit=1', headers=admin_token)
    assert response.status_code == 200
    assert response.json() == [
                                {
                                    'ID': 1,
                                    'email': 'test_mail',
                                    'name': 'test_name',
                                    'surname': 'test_surname',
                                    'phone': 'test_phone',
                                    'address': 'test_address',
                                    'is_admin': True
                                }
                            ]


def test_read_users_skip_all():
    response = client.get('/users/?skip=2', headers=admin_token)
    assert response.status_code == 200
    assert response.json() == []


def test_read_user():
    response = client.get('/users/2', headers=admin_token)
    assert response.status_code == 200
    assert response.json() == {
                                'ID': 2,
                                'email': 'test_1',
                                'name': 'test_2',
                                'surname': 'test_3',
                                'phone': 'test_4',
                                'address': 'test_5',
                                'is_admin': False
                            }


def test_read_nonexistent_user():
    response = client.get('/users/3', headers=admin_token)
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_read_user_bad_token():
    response = client.get('/users/1', headers={'Authorization': 'Bearer 1234'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_user_insufficient_permission():
    response = client.get('/users/1', headers=token)
    assert response.status_code == 403
    assert response.json() == {'detail': 'Insufficient permissions'}


def test_read_user_purchases():
    response = client.get('/users/1/purchases', headers=admin_token)
    assert response.status_code == 200
    assert response.json() == {
                                'ID': 1,
                                'email': 'test_mail',
                                'purchases': [
                                    {
                                        'ID': 1,
                                        'start_date': '2020-10-03',
                                        'expiry_date': '2020-10-09',
                                        'cost': 66
                                    },
                                    {
                                        'ID': 2, 'start_date': '2020-10-14', 'expiry_date': '2020-11-15', 'cost': 198
                                    }
                                ]
                            }


def test_read_nonexistent_user_purchases():
    response = client.get('/users/3/purchases', headers=admin_token)
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_read_user_id_le_one():
    response = client.get('/users/0/purchases', headers=admin_token)
    assert response.status_code == 422
    assert response.json() == {
                                'detail':
                                    [
                                        {
                                            'loc': ['path', 'user_id'],
                                            'msg': 'ensure this value is greater than or equal to 1',
                                            'type': 'value_error.number.not_ge',
                                            'ctx': {'limit_value': 1}
                                        }
                                    ]
                            }


def test_read_user_purchase():
    response = client.get('/users/1/purchases/1', headers=admin_token)
    assert response.status_code == 200
    assert response.json() == {
                                'ID': 1,
                                'start_date': '2020-10-03',
                                'expiry_date': '2020-10-09',
                                'cost': 66,
                                'movie_list': [
                                    {
                                        'title': 'Project Power',
                                        'genre': 'Fantasy',
                                        'director': 'Henry Joost',
                                        'release_year': 2020,
                                        'rating': 6.0,
                                        'cost_per_day': 5
                                    },
                                    {
                                        'title': '#Alive',
                                        'genre': 'Horror',
                                        'director': 'Il Cho',
                                        'release_year': 2020,
                                        'rating': 6.2,
                                        'cost_per_day': 6
                                    }
                                ]
                            }


def test_read_nonexistent_user_purchase():
    response = client.get('/users/5/purchases/1', headers=admin_token)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Purchase for given user not found'}


def test_read_user_nonexistent_purchase():
    response = client.get('/users/2/purchases/1', headers=admin_token)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Purchase for given user not found'}


def test_read_user_movies():
    response = client.get('/users/2/movies', headers=admin_token)
    assert response.status_code == 200
    assert response.json() == [
                                {
                                    'title': '#Alive',
                                    'genre': 'Horror',
                                    'director': 'Il Cho',
                                    'release_year': 2020,
                                    'rating': 6.2,
                                    'cost_per_day': 6,
                                    'ID': 3
                                }
                            ]


def test_read_nonexistent_user_movies():
    response = client.get('/users/3/movies', headers=admin_token)
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
