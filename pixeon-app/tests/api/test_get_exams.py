import dateutil

def test_get_all_exams_returning_200_status_code(client, session, access_token):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/exam path is requested 
    THEN check if response is valid
    """
    
    from app.util import create_physician, create_patient, create_order, create_exam
    
    physician1 = create_physician('male')
    physician2 = create_physician('male')
    
    patient1 = create_patient('female', 70, 1.70)   
    patient2 = create_patient('male', 70, 1.70)   

    patient1_order = create_order(patient1)
    patient2_order = create_order(patient2)

    exam1 = create_exam(physician1, patient1_order)
    exam2 = create_exam(physician2, patient2_order)

    response = client.get(f'/api/v1.0/exam',
                            headers={'Authorization': 'Bearer ' + access_token})

    assert response.status_code == 200
    assert len(response.json['exams']) == 2    
    assert response.json['exams'][0] == exam1.serialize()
    assert response.json['exams'][1] == exam2.serialize()


def test_get_exams_by_patient_id_returning_200_status_code(client, session, access_token):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/exam path is requested 
    THEN check if response is valid
    """
    
    from app.util import create_physician, create_patient, create_order, create_exam
    
    physician1 = create_physician('male')
    physician2 = create_physician('male')
    
    patient1 = create_patient('female', 70, 1.70)   
    patient2 = create_patient('male', 70, 1.70)   

    patient1_order = create_order(patient1)
    patient2_order = create_order(patient2)

    exam1 = create_exam(physician1, patient1_order)
    exam2 = create_exam(physician2, patient2_order) # exam from patient selected
    exam3 = create_exam(physician2, patient2_order) # exam from patient selected

    response = client.get(f'/api/v1.0/exam?patient_id={patient2.public_id}',
                            headers={'Authorization': 'Bearer ' + access_token})

    assert response.status_code == 200
    assert len(response.json['exams']) == 2    
    assert response.json['exams'][0] == exam2.serialize()
    assert response.json['exams'][1] == exam3.serialize()


def test_get_exams_by_physician_id_returning_200_status_code(client, session, access_token):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/exam path is requested 
    THEN check if response is valid
    """
    
    from app.util import create_physician, create_patient, create_order, create_exam
    
    physician1 = create_physician('male')
    physician2 = create_physician('male')
    
    patient1 = create_patient('female', 70, 1.70)   
    patient2 = create_patient('male', 70, 1.70)   

    patient1_order = create_order(patient1)
    patient2_order = create_order(patient2)

    exam1 = create_exam(physician1, patient1_order)
    exam2 = create_exam(physician2, patient2_order) # exam from physician selected
    exam3 = create_exam(physician2, patient2_order) # exam from physician selected

    response = client.get(f'/api/v1.0/exam?physician_id={physician2.public_id}',
                            headers={'Authorization': 'Bearer ' + access_token})

    assert response.status_code == 200
    assert len(response.json['exams']) == 2    
    assert response.json['exams'][0] == exam2.serialize()
    assert response.json['exams'][1] == exam3.serialize()    


def test_get_exams_from_patients_by_bmi_returning_200_status_code(client, session, access_token):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/exam path is requested 
    THEN check if response is valid
    """
    
    from app.util import create_physician, create_patient, create_order, create_exam
    
    physician1 = create_physician('male')
    physician2 = create_physician('male')
    
    patient1 = create_patient('female', 70, 1.70) # normal BMI
    patient2 = create_patient('male', 100, 1.70) # not normal BMI

    patient1_order = create_order(patient1)
    patient2_order = create_order(patient2)

    # Exame from patient with normal BMI
    exam1 = create_exam(physician1, patient1_order)
    # Exames from patient with not normal BMI
    exam2 = create_exam(physician2, patient2_order)
    exam3 = create_exam(physician2, patient2_order)

    # Request for normal BMI

    response = client.get(f'/api/v1.0/exam?bmi=normal',
                            headers={'Authorization': 'Bearer ' + access_token})

    assert response.status_code == 200
    assert len(response.json['exams']) == 1    
    assert response.json['exams'][0] == exam1.serialize()    

    # Request for not normal BMI

    response = client.get(f'/api/v1.0/exam?bmi=not%20normal',
                            headers={'Authorization': 'Bearer ' + access_token})

    assert response.status_code == 200
    assert len(response.json['exams']) == 2
    assert response.json['exams'][0] == exam2.serialize()    
    assert response.json['exams'][1] == exam3.serialize()    


def test_get_all_exams_whitout_access_token_returning_401_status_code(client):
    """
    GIVEN a Flask application
    WHEN the GET /api/v1.0/exam path is requested 
    THEN check if response is valid
    """    
    
    response = client.get('/api/v1.0/exam')
    
    assert response.status_code == 401 