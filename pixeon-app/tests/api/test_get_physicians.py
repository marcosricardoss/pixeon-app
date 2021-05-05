
def test_get_all_physicians_returning_200_status_code(client, session, access_token):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/physician path is requested 
    THEN check if response is valid
    """
    from app.util import create_physician
    
    physician1 = create_physician('female')   
    physician2 = create_physician('male')       

    response = client.get(f'/api/v1.0/physician',
                            headers={'Authorization': 'Bearer ' + access_token})
    assert response.status_code == 200
    assert len(response.json['physicians']) == 2
    assert response.json['physicians'][0] == physician1.serialize()
    assert response.json['physicians'][1] == physician2.serialize()


def test_get_all_physicians_whitout_access_token_returning_401_status_code(client):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/physician path is requested 
    THEN check if response is valid
    """    
    
    response = client.get('/api/v1.0/physician')
    
    assert response.status_code == 401 