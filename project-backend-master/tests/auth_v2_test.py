import pytest
import requests
from src import config
from src.helpers import generate_jwt, decode_jwt, encode_jwt

#Users_list:
user_1 =  {
            "email": "osama2as820sadas02@gmail.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "Osama",
            "name_last": "Almabrouk"
            }
user_2 =  {
            "email": "someemailadress@gmail.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "Osama",
            "name_last": "Almabrouk"
            }
user_3 =  {
            "email": "someemailadressss@gmail.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "Osama",
            "name_last": "Almabrouk"
            }

user_4 = {
            "email": "someemailadresssses@gmail.com",
            "password": "dasdasdasdlaasdaskmLN",
            "name_first": "SAMSOMITOOOOOOOS",
            "name_last": "BSHBKBFKJBWEFKJ@!@!RKJkjbskfbdkkjbksjdbfsdf@!"
            }

email_invalid =  {
            "email": "someemailadressss.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "Osama",
            "name_last": "Almabrouk"
            }

short_password =  {
            "email": "someemailadressss@gmail.com",
            "password": "s23f8",
            "name_first": "Osama",
            "name_last": "Almabrouk"
            }
short_first =  {
            "email": "someemailadressss@gmail.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "",
            "name_last": "Almabrouk"
            }

short_last =  {
            "email": "someemailadressss@gmail.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "Osama",
            "name_last": ""
            }

long_first =  {
            "email": "someemailadressss@gmail.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "OSEJKLRTEROSEJKLRTEROSEJKLRTEROSEJKLRTEROSEJKLRTERte",
            "name_last": "Almabrouk"
            }

long_last =  {
            "email": "someemailadressss@gmail.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "Osama",
            "name_last": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab"
            }

@pytest.fixture
def clear_users():
    response_del = requests.delete(f"{config.url}clear/v1")
    assert response_del.status_code == 200

#########################################################################
#########################AUTH_REGISTER_TESTS#############################
#########################################################################
def test_auth_register(clear_users):
    """Tests register for one user only"""
    #Post request
    response = requests.post(f"{config.url}auth/register/v2", json=user_1)
    response_data = response.json()
    assert response_data['auth_user_id'] == 1
    assert decode_jwt(response_data['token']) == {'u_id': 1, 'session_id': 0}

    response4 = requests.post(f"{config.url}auth/register/v2", json=user_4)
    response4_data = response4.json()
    assert response4_data['auth_user_id'] == 2
    assert decode_jwt(response4_data['token']) == {'u_id': 2, 'session_id': 0}

def test_auth_register2(clear_users):
    """Registers Three users and asserts their return types"""
    response_1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    response_data_1 = response_1.json()
    assert response_1.status_code == 200
    assert response_data_1['auth_user_id'] == 1
    assert decode_jwt(response_data_1['token']) == {'u_id': 1, 'session_id': 0}

    response_2 = requests.post(f"{config.url}auth/register/v2", json=user_2)
    response_data_2 = response_2.json()
    assert response_2.status_code == 200
    assert response_data_2['auth_user_id'] == 2
    assert decode_jwt(response_data_2['token']) == {'u_id': 2, 'session_id': 0}

    response_3 = requests.post(f"{config.url}auth/register/v2", json=user_3)
    response_data_3 = response_3.json()
    assert response_3.status_code == 200
    assert response_data_3['auth_user_id'] == 3
    assert decode_jwt(response_data_3['token']) == {'u_id': 3, 'session_id': 0}

def test_invalid_email(clear_users):
    """Tests invalid inputs"""
    #Invalid Email
    response_1 = requests.post(f"{config.url}auth/register/v2", json=email_invalid)
    assert response_1.status_code == 400

def test_email_already_used(clear_users):
    """Tests if it registers an already used email"""
    response_1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    assert response_1.status_code == 200

    response_2 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    assert response_2.status_code == 400

def test_short_password(clear_users):
    response_1 = requests.post(f"{config.url}auth/register/v2", json=short_password)
    assert response_1.status_code == 400

def test_short_name_first_last(clear_users):
    response_1 = requests.post(f"{config.url}auth/register/v2", json=short_first)
    assert response_1.status_code == 400
    response_2 = requests.post(f"{config.url}auth/register/v2", json=short_last)
    assert response_2.status_code == 400

def test_long_name_first_last(clear_users):
    response_1 = requests.post(f"{config.url}auth/register/v2", json=long_first)
    assert response_1.status_code == 400
    response_2 = requests.post(f"{config.url}auth/register/v2", json=long_last)
    assert response_2.status_code == 400
#########################################################################
#########################AUTH_REGISTER_TESTS#############################
#########################################################################




#########################################################################
#########################AUTH_LOGIN_TESTS################################
#########################################################################
user_1_login = {"email": "osama2as820sadas02@gmail.com", "password": "dasdasdasdlakmLN"}
invalid_user_email = {"email": "osama2as820sadas012@gmail.com", "password": "dasdasdasdlakmLN"}
user_1_invalid_password = {"email": "osama2as820sadas02@gmail.com", "password": "asdasdasdlakmLN"}
user_2_login =  {"email": "someemailadress@gmail.com", "password": "dasdasdasdlakmLN"}
user_3_login =  {"email": "someemailadressss@gmail.com", "password": "dasdasdasdlakmLN"}
def test_auth_login(clear_users):
    #Register a user
    response = requests.post(f"{config.url}auth/register/v2", json=user_1)
    assert response.status_code == 200
    #login 10 times:
    for i in range(1,11):
        response_login = requests.post(f"{config.url}auth/login/v2", json=user_1_login)
        response_login_data = response_login.json()
        assert response_login_data['auth_user_id'] == 1
        assert decode_jwt(response_login_data['token']) == {'u_id': 1, 'session_id': i}


def test_auth_login_multiple_users(clear_users):
    #register three users
    register1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    register2 = requests.post(f"{config.url}auth/register/v2", json=user_2)
    register3 = requests.post(f"{config.url}auth/register/v2", json=user_3)
    assert register1.status_code == 200
    assert register2.status_code == 200
    assert register3.status_code == 200

    # login in order 1, 2, 3 5 times
    for i in range(1,6):
        response_login1 = requests.post(f"{config.url}auth/login/v2", json=user_1_login)
        response_login2 = requests.post(f"{config.url}auth/login/v2", json=user_2_login)
        response_login3 = requests.post(f"{config.url}auth/login/v2", json=user_3_login)
        response_login_data1 = response_login1.json()
        response_login_data2 = response_login2.json()
        response_login_data3 = response_login3.json()
        assert response_login_data1['auth_user_id'] == 1
        assert response_login_data2['auth_user_id'] == 2
        assert response_login_data3['auth_user_id'] == 3
        assert decode_jwt(response_login_data1['token']) == {'u_id': 1, 'session_id': i}
        assert decode_jwt(response_login_data2['token']) == {'u_id': 2, 'session_id': i}
        assert decode_jwt(response_login_data3['token']) == {'u_id': 3, 'session_id': i}

    # login in order 3, 1, 5 5 more times
    for i in range(6,11):
        response_login3 = requests.post(f"{config.url}auth/login/v2", json=user_3_login)
        response_login1 = requests.post(f"{config.url}auth/login/v2", json=user_1_login)
        response_login2 = requests.post(f"{config.url}auth/login/v2", json=user_2_login)
        response_login_data3 = response_login3.json()
        response_login_data1 = response_login1.json()
        response_login_data2 = response_login2.json()
        assert response_login_data3['auth_user_id'] == 3
        assert response_login_data1['auth_user_id'] == 1
        assert response_login_data2['auth_user_id'] == 2
        assert decode_jwt(response_login_data3['token']) == {'u_id': 3, 'session_id': i}
        assert decode_jwt(response_login_data1['token']) == {'u_id': 1, 'session_id': i}
        assert decode_jwt(response_login_data2['token']) == {'u_id': 2, 'session_id': i}



#Check for Errors:
def test_invalid_email_login(clear_users):
    register1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    assert register1.status_code == 200
    response_login1 = requests.post(f"{config.url}auth/login/v2", json=invalid_user_email)
    assert response_login1.status_code == 400

def test_invalid_password(clear_users):
    register1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    assert register1.status_code == 200
    response_login1 = requests.post(f"{config.url}auth/login/v2", json=user_1_invalid_password)
    assert response_login1.status_code == 400
    #Check if it doesn't add any session id with invalid attempts:
    response_login = requests.post(f"{config.url}auth/login/v2", json=user_1_login)
    response_login_data = response_login.json()
    assert response_login_data['auth_user_id'] == 1
    assert decode_jwt(response_login_data['token']) == {'u_id': 1, 'session_id': 1}

#########################################################################
#########################AUTH_LOGIN_TESTS################################
#########################################################################

#########################################################################
#########################AUTH_LOGOUT_TESTS###############################
#########################################################################

#ACER when token passed is invalid:
    #register and logout twice, error must be at second one:

def test_logout_twice(clear_users):
    #register user 1
    response_1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    response_data_1 = response_1.json()
    assert response_1.status_code == 200
    assert response_data_1['auth_user_id'] == 1
    assert decode_jwt(response_data_1['token']) == {'u_id': 1, 'session_id': 0}

    token0 = response_data_1['token']
    #logout user1:
    logout1 = {'token': token0}
    rlogout1 = requests.post(f"{config.url}auth/logout/v1", json=logout1)
    assert rlogout1.status_code == 200

    rlogout2 = requests.post(f"{config.url}auth/logout/v1", json=logout1)
    assert rlogout2.status_code == 403

def test_invalid_token(clear_users):
    #register user 1
    response_1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    response_data_1 = response_1.json()
    assert response_1.status_code == 200
    assert response_data_1['auth_user_id'] == 1
    assert decode_jwt(response_data_1['token']) == {'u_id': 1, 'session_id': 0}

    #logout w session 1:
    token1 = encode_jwt(1,1)
    #logout user1:
    logout1 = {'token': token1}
    rlogout1 = requests.post(f"{config.url}auth/logout/v1", json=logout1)
    assert rlogout1.status_code == 403

    #login and check that it acc works:
    response_login1 = requests.post(f"{config.url}auth/login/v2", json=user_1_login)
    response_login_data1 = response_login1.json()
    assert response_login_data1['auth_user_id'] == 1
    assert decode_jwt(response_login_data1['token']) == {'u_id': 1, 'session_id': 1}


def test_logout_user3(clear_users):
    response_1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    assert response_1.status_code == 200

    response_2 = requests.post(f"{config.url}auth/register/v2", json=user_2)
    assert response_2.status_code == 200

    response_3 = requests.post(f"{config.url}auth/register/v2", json=user_3)
    response_data_3 = response_3.json()
    assert response_3.status_code == 200

    #logout user3:
    logout3 = {'token': response_data_3['token']}
    rlogout3 = requests.post(f"{config.url}auth/logout/v1", json=logout3)
    assert rlogout3.status_code == 200
    
#########################################################################
#########################AUTH_LOGOUT_TESTS###############################
#########################################################################