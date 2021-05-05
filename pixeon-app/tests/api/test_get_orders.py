import dateutil

def test_get_all_orders_returning_200_status_code(client, session, access_token):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/order path is requested 
    THEN check if response is valid
    """
    
    from app.util import create_physician, create_patient, create_order
    
    physician = create_physician('male')
    patient1 = create_patient('female', 70, 1.70)   
    patient2 = create_patient('male', 70, 1.70)   

    patient1_order = create_order(patient1)
    patient2_order = create_order(patient2)

    response = client.get(f'/api/v1.0/order',
                            headers={'Authorization': 'Bearer ' + access_token})
    
    assert response.status_code == 200
    assert len(response.json['orders']) == 2    
    assert response.json['orders'][0] == patient1_order.serialize()
    assert response.json['orders'][1] == patient2_order.serialize()


def test_get_orders_of_date_range_returning_200_status_code(client, session, access_token):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/order path is requested 
    THEN check if response is valid
    """
    
    from app.util import create_physician, create_patient, create_order
    
    physician = create_physician('male')
    patient1 = create_patient('female', 70, 1.70)   
    patient2 = create_patient('female', 70, 1.70)       

    patient1_order1 = create_order(patient1)
    patient2_order1 = create_order(patient2, dateutil.parser.isoparse("2021-01-01T10:00:00Z"))
    patient2_order2 = create_order(patient2, dateutil.parser.isoparse("2021-01-01T12:00:00Z"))

    uri = "/api/v1.0/order?from_time=2021-01-01T00:00:00Z&to_time=2021-01-01T23:59:59"
    response = client.get(uri,
                          headers={'Authorization': 'Bearer ' + access_token})
    
    assert response.status_code == 200
    assert len(response.json['orders']) == 2   
    assert response.json['orders'][0] == patient2_order1.serialize()
    assert response.json['orders'][1] == patient2_order2.serialize()


def test_get_all_orders_whitout_access_token_returning_401_status_code(client):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/order path is requested 
    THEN check if response is valid
    """    
    
    response = client.get('/api/v1.0/order')
    
    assert response.status_code == 401 