
def test_get_all_patients_returning_200_status_code(client, session, access_token):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/patient path is requested 
    THEN check if response is valid
    """
    from app.util import create_patient
    
    patient1 = create_patient('female', 70, 1.70)   
    patient2 = create_patient('male', 70, 1.70)       

    response = client.get(f'/api/v1.0/patient',
                            headers={'Authorization': 'Bearer ' + access_token})
    assert response.status_code == 200
    assert len(response.json['patients']) == 2
    assert response.json['patients'][0] == patient1.serialize()
    assert response.json['patients'][1] == patient2.serialize()


def test_get_all_patients_whitout_access_token_returning_401_status_code(client):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/patient path is requested 
    THEN check if response is valid
    """    
    
    response = client.get('/api/v1.0/patient')
    
    assert response.status_code == 401 