import os
import uuid

import requests
from dotenv import load_dotenv

from ..users.schemas import RegisterUser

load_dotenv('.env')

API_URL = os.environ['API_URL']
SUPERUSER_USERNAME = os.environ['SUPERUSER_USERNAME']
SUPERUSER_PASSWORD = os.environ['SUPERUSER_PASSWORD']

def get_random_string(length: int = 10):
    return uuid.uuid4().hex[:length]

def get_mock_user(username=None, password=None, fingerprint=None, referrer_id):
    return RegisterUser(
        username=get_random_string(10) if username is None else username,
        password=get_random_string(10) if password is None else password,
        fingerprint=get_random_string(16) if fingerprint is None else fingerprint,
        referrer_id=referrer_id
    )

def test_superuser_exists():
    r = requests.get(
        API_URL+'/users/auth/token',
        data={
            'username': 
        }
    )

def test_register_user():
    r = requests.post(
        API_URL+'/users/register',
        data={
            'username': 'testuser',
            'password': '12345678',
            'fingerprint': '12345678'
        },
        verify=False
    )
    
    assert r.status_code == 200

def test_register_user_with_referrer():


    r = requests.post(
        API_URL+'/users/register',
        data={
            'username': 'testuser',
            'password': '12345678',
            'fingerprint': '12345678'
        },
        verify=False
    )
    
    assert r.status_code == 200