import os
import json
import uuid
import dateutil

def test_user_login_with_correct_credentials_returning_200_status_code(client, session, access_token):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/exam path is requested 
    THEN check if response is valid
    """

    from app.model import User
    from app.model import UserRepository

    user_repository = UserRepository()
    user = User()
    user.public_id = uuid.uuid1().hex
    user.username = "test"
    user.password = "*test*"
    user_repository.save(user)

    data = {
        "username": "test",
        "password": "*test*"
    }

    response = client.post('/api/v1.0/auth/login', 
                            data=json.dumps(data),
                            content_type='application/json')

    assert response.status_code == 200

def test_user_login_with_incorrect_credentials_returning_200_status_code(client, session, access_token):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/exam path is requested 
    THEN check if response is valid
    """

    data = {
        "username": "xxxxxxxxxx",
        "password": "xxxxxxxxxx"
    }

    response = client.post('/api/v1.0/auth/login', 
                            data=json.dumps(data),
                            content_type='application/json')

    assert response.status_code == 401    
    