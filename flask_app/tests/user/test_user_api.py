from app import app

user = 'test'
password = 'testtest'

def test_create_user():
    response = app.test_client().post('http://localhost:5000/api/v1/user',
                            json={'username': user,
                                  'password': password}
                         )
    assert response.status_code == 201
