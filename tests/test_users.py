from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal

from config import test_password, test_login
from schemas import User
import crud
import models
from utils import get_db

from main import app


client = TestClient(app)
payload = {'username': test_login, 'password': test_password}
token = client.post('/token', data=payload)
token = token.json()
token = {'Authorization': f"Bearer {token['access_token']}"}


def test_read_self_user():
    response = client.get('/users/me', headers=token)
    assert response.status_code == 200
    db: Session = SessionLocal()
    user: User = db.query(models.User).filter(models.User.email == test_login).first()
    print(user.password)
    assert response.json() == user.__dict__
    db.close()





