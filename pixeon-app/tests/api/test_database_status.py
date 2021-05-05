import os
import json
import uuid
import dateutil

def test_check_database_status_returning_200_status_code(client, access_token):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/status path is requested 
    THEN check if response is valid
    """

    response = client.get(f'/api/v1.0/status',
                            headers={'Authorization': 'Bearer ' + access_token})
    assert response.status_code == 200


def test_check_database_status_returning_503_status_code(client, access_token, mocker):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/status path is requested 
    THEN check if response is valid
    """    
    
    mocker.patch.dict(os.environ, {"DATABASE_URL": "xxxxxxxxxxxxxxxxxx"})
    response = client.get(f'/api/v1.0/status',
                                headers={'Authorization': 'Bearer ' + access_token})
    assert response.status_code == 503

    
def test_check_database_status_returning_401_status_code(client):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/status path is requested 
    THEN check if response is valid
    """

    response = client.get(f'/api/v1.0/status')
    assert response.status_code == 401 