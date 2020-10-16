from fastapi.testclient import TestClient

from config import test_admin_password, test_admin_username, test_password, test_username
from main import app
from utils import get_db
from .test_helpers import override_get_db, get_token

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

admin_token = get_token(test_admin_username, test_admin_password, client)
token = get_token(test_username, test_password, client)


def test_read_movies():
    response = client.get('/movies')
    assert response.status_code == 200
    assert response.json() == [
        {'title': 'Joker', 'genre': 'Crime', 'director': 'Todd Phillips', 'release_year': 2019, 'rating': 8.5,
         'cost_per_day': 7, 'ID': 1},
        {'title': 'Project Power', 'genre': 'Fantasy', 'director': 'Henry Joost', 'release_year': 2020, 'rating': 6.0,
         'cost_per_day': 5, 'ID': 2},
        {'title': '#Alive', 'genre': 'Horror', 'director': 'Il Cho', 'release_year': 2020, 'rating': 6.2,
         'cost_per_day': 6, 'ID': 3},
        {'title': 'Enola Holmes', 'genre': 'Adventure', 'director': 'Harry Bradbeer', 'release_year': 2020,
         'rating': 6.7, 'cost_per_day': 8, 'ID': 4},
        {'title': 'Venom', 'genre': 'Action', 'director': 'Ruben Fleischer', 'release_year': None, 'rating': 6.7,
         'cost_per_day': 6, 'ID': 5},
        {'title': 'Aquaman', 'genre': 'Action', 'director': 'James Wan', 'release_year': 2018, 'rating': 6.7,
         'cost_per_day': 56, 'ID': 6},
        {'title': 'Interstellar', 'genre': 'Sci-fi', 'director': 'Christopher Nolan', 'release_year': None,
         'rating': 8.6, 'cost_per_day': 4, 'ID': 7}
    ]


def test_read_movies_wrong_skip_and_limit_values():
    response = client.get('/movies/?skip=-1&limit=0')
    assert response.status_code == 422
    assert response.json() == {
                                'detail': [
                                    {
                                        'loc': ['query', 'skip'],
                                         'msg': 'ensure this value is greater than or equal to 0',
                                         'type': 'value_error.number.not_ge', 'ctx': {'limit_value': 0}
                                     },
                                    {
                                        'loc': ['query', 'limit'],
                                        'msg': 'ensure this value is greater than or equal to 1',
                                        'type': 'value_error.number.not_ge',
                                        'ctx': {'limit_value': 1}
                                    }
                                ]
                            }


def test_read_movies_skip_and_limit():
    response = client.get('/movies/?skip=1&limit=2')
    assert response.status_code == 200
    assert response.json() == [
                                {
                                    'title': 'Project Power',
                                    'genre': 'Fantasy',
                                    'director': 'Henry Joost',
                                    'release_year': 2020,
                                    'rating': 6.0,
                                    'cost_per_day': 5,
                                    'ID': 2
                                },
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


def test_read_movie():
    response = client.get('/movies/1')
    assert response.status_code == 200
    assert response.json() == {
                                'title': 'Joker',
                                'genre': 'Crime',
                                'director': 'Todd Phillips',
                                'release_year': 2019,
                                'rating': 8.5,
                                'cost_per_day': 7,
                                'ID': 1
                            }


def test_read_nonexistent_movie():
    response = client.get('/movies/30')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Movie not found'}


def test_read_movie_id_lt_one():
    response = client.get('/movies/0')
    assert response.status_code == 422
    assert response.json() == {
                                'detail': [
                                    {
                                        'loc': ['path', 'movie_id'],
                                        'msg': 'ensure this value is greater than or equal to 1',
                                        'type': 'value_error.number.not_ge', 'ctx': {'limit_value': 1}
                                    }
                                ]
                            }


# def test_create_movie():
#     data = [
#         {'title': 'string', 'genre': 'string', 'director': 'string', 'release_year': 0, 'rating': 0, 'cost_per_day': 0}
#     ]
#     response = client.post('/movies/', headers=admin_token, json=data)
#
#     assert response.status_code == 201
#     data = response.json()
#     assert data == [
#                                 {
#                                     'title': 'string',
#                                     'genre': 'string',
#                                     'director': 'string',
#                                     'release_year': 0,
#                                     'rating': 0.0,
#                                     'cost_per_day':0,
#                                     'ID': 8
#                                 }
#                             ]
#
#     movie_id = data['id']
#
#     response = client.get(f'/movies/{movie_id}')
#     assert response.status_code == 200
#     assert data == response.json()


# @pytest.fixture(scope='module')
# def test_create_movie_invalid_title_and_rating():
#     data = [
#         {'title': 'title', 'genre': 'string', 'director': 'string', 'release_year': 0, 'rating': '123', 'cost_per_day': 0}
#     ]
#     response = client.post('/movies/', headers=admin_token, json=data)
#     print(response.status_code)
#     print(response.json())
#     assert response.status_code == 400
