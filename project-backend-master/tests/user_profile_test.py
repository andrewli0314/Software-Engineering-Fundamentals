import pytest
import requests
import json
from src import config
from src.helpers import generate_jwt, decode_jwt, encode_jwt
from src.user import user_profile_v1

#####################################################################
user_1 =  {
            "email": "osama2as820sadas02@gmail.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "Osama",
            "name_last": "Almabrouk"
            }
user_1_member = {
    "u_id" : 1,
    "email" : "osama2as820sadas02@gmail.com", 
    "name_first": "Osama",
    "name_last": "Almabrouk",
    "handle_str" : "osamaalmabrouk"
}
#####################################################################
user_2 =  {
            "email": "someemailadress@gmail.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "Osama",
            "name_last": "Almabrouk"
            }
user_2_member = {
    "u_id" : 2,
    "email" : "someemailadress@gmail.com", 
    "name_first": "Osama",
    "name_last": "Almabrouk",
    "handle_str" : "osamaalmabrouk0"
}
#####################################################################
user_3 =  {
            "email": "someemailadressss@gmail.com",
            "password": "Samsoomitoz2132",
            "name_first": "Osama",
            "name_last": "Almabrouk"
            }
user_3_member = {
    "u_id" : 3,
    "email" : "someemailadressss@gmail.com", 
    "name_first": "Osama",
    "name_last": "Almabrouk",
    "handle_str" : "osamaalmabrouk1"
}
#####################################################################
user_4 =  {
            "email": "someemailadresssss@gmail.com",
            "password": "Samsoomitoz2132",
            "name_first": "Osama",
            "name_last": "Almabrouk"
            }
user_4_member = {
    "u_id" : 4,
    "email" : "someemailadresssss@gmail.com", 
    "name_first": "Osama",
    "name_last": "Almabrouk",
    "handle_str" : "osamaalmabrouk2"
}

@pytest.fixture
def clear_users():
    response_del = requests.delete(f"{config.url}clear/v1")
    assert response_del.status_code == 200

#########################################################################
##########################USER_SETHANDLE_TEST############################
#########################################################################
    
def test_profile_sethandle_correct_basic(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']
    handles_1 = {"token": token1, "handle_str": "asd"}
    handles_2 = {'token': token2, 'handle_str': 'asdfghjklpoiuytrewqw'}
    handles_3 = {'token': token3, 'handle_str': 'abcdefg'}
    
    sethandle_1 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_1)
    #print(sethandle_1.content)
    assert sethandle_1.status_code == 200
    sethandle_2 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_2)
    assert sethandle_2.status_code == 200
    sethandle_3 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_3)
    assert sethandle_3.status_code == 200

def test_profile_sethandle_correct_capital(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']
    handles_1 = {'token': token1, 'handle_str': 'ASD'}
    handles_2 = {'token': token2, 'handle_str': 'ASDFGHJKLQWERTYUIOPZ'}
    handles_3 = {'token': token3, 'handle_str': 'ABCDEFG'}
    
    sethandle_1 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_1)
    assert sethandle_1.status_code == 200
    sethandle_2 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_2)
    assert sethandle_2.status_code == 200
    sethandle_3 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_3)
    assert sethandle_3.status_code == 200

def test_profile_sethandle_correct_number(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']
    handles_1 = {'token': token1, 'handle_str': '12234'}
    handles_2 = {'token': token2, 'handle_str': '66666666666666666666'}
    handles_3 = {'token': token3, 'handle_str': '1234567890'}
    
    sethandle_1 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_1)
    assert sethandle_1.status_code == 200
    sethandle_2 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_2)
    assert sethandle_2.status_code == 200
    sethandle_3 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_3)
    assert sethandle_3.status_code == 200
    
def test_profile_sethandle_correct_mix(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']
    handles_1 = {'token': token1, 'handle_str': '1AsD2'}
    handles_2 = {'token': token2, 'handle_str': '1ASdFGHJKLqWERtiOpZ2'}
    handles_3 = {'token': token3, 'handle_str': '1AbCdEfG2'}
    
    sethandle_1 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_1)
    assert sethandle_1.status_code == 200
    sethandle_2 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_2)
    assert sethandle_2.status_code == 200
    sethandle_3 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_3)
    assert sethandle_3.status_code == 200

def test_profile_sethandle_wrong_length(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']
    handles_1 = {'token': token1, 'handle_str': 'df'}
    handles_2 = {'token': token2, 'handle_str': 'asdfghjklpoiuytrewqwert'}
    handles_3 = {'token': token3, 'handle_str': ''}
    
    sethandle_1 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_1)
    assert sethandle_1.status_code == 400
    sethandle_2 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_2)
    assert sethandle_2.status_code == 400
    sethandle_3 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_3)
    assert sethandle_3.status_code == 400

def test_profile_sethandle_wrong_notisalnum(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']
    handles_1 = {'token': token1, 'handle_str': '12345!'}
    handles_2 = {'token': token2, 'handle_str': '!@#$%^&'}
    handles_3 = {'token': token3, 'handle_str': '@#$%^1223456'}
    
    sethandle_1 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_1)
    assert sethandle_1.status_code == 400
    sethandle_2 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_2)
    assert sethandle_2.status_code == 400
    sethandle_3 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_3)
    assert sethandle_3.status_code == 400

def test_profile_sethandle_wrong_used(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']
    handles_1 = {'token': token1, 'handle_str': 'asdfg'}
    handles_2 = {'token': token2, 'handle_str': 'Asdfghjk'}
    handles_3_1 = {'token': token3, 'handle_str': 'asdfg'}
    handles_3_2 = {'token': token3, 'handle_str': 'Asdfghjk'}
    
    sethandle_1 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_1)
    assert sethandle_1.status_code == 200
    sethandle_2 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_2)
    assert sethandle_2.status_code == 200
    sethandle_3_1 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_3_1)
    assert sethandle_3_1.status_code == 400
    sethandle_3_2 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_3_2)
    assert sethandle_3_2.status_code == 400
   
def test_profile_sethandle_wrong_mixed(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']
    handles_1 = {'token': token1, 'handle_str': 'asdf-gasdfgtrewqyuio20'}
    handles_2 = {'token': token2, 'handle_str': '!@'}
    handles_3 = {'token': token3, 'handle_str': '1as!@'}
    
    sethandle_1 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_1)
    assert sethandle_1.status_code == 400
    sethandle_2 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_2)
    assert sethandle_2.status_code == 400
    sethandle_3 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_3)
    assert sethandle_3.status_code == 400

def test_profile_sethandle_invalid_token(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json() 
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']  
    token1_invalid = encode_jwt(1,2)    #wrong session
    token2_invalid = encode_jwt(6,0)    #wrong user id
    token3_invalid = encode_jwt(5,1)    #both wrong
    handles_1 = {'token': token1, 'handle_str': 'aaaaaa'}
    handles_2 = {'token': token2, 'handle_str': '111111'}
    handles_3 = {'token': token3, 'handle_str': '111aaa'}
    handles_1_invalid = {'token': token1_invalid, 'handle_str': 'bbbbbb'}
    handles_2_invalid = {'token': token2_invalid, 'handle_str': '222222'}
    handles_3_invalid = {'token': token3_invalid, 'handle_str': '222bbb'}
    
    sethandle_1_1 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_1)
    assert sethandle_1_1.status_code == 200
    sethandle_2_1 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_2)
    assert sethandle_2_1.status_code == 200
    sethandle_3_1 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_3)
    assert sethandle_3_1.status_code == 200
    sethandle_1 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_1_invalid)
    assert sethandle_1.status_code == 403
    sethandle_2 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_2_invalid)
    assert sethandle_2.status_code == 403
    sethandle_3 = requests.put(f'{config.url}user/profile/sethandle/v1', json = handles_3_invalid)
    assert sethandle_3.status_code == 403
    
    
#########################################################################
############################USER_PROFILE_TEST############################
#########################################################################

def test_profile_invalid_token(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json() 
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']  
    token1_invalid = encode_jwt(1,2)    #wrong session
    token2_invalid = encode_jwt(6,0)    #wrong user id
    token3_invalid = encode_jwt(5,1)    #both wrong
    handles_1 = {'token': token1, 'u_id': 2}
    handles_2 = {'token': token2, 'u_id': 1}
    handles_3 = {'token': token3, 'u_id': 3}
    handles_1_invalid = {'token': token1_invalid, 'u_id': 1}
    handles_2_invalid = {'token': token2_invalid, 'u_id': 3}
    handles_3_invalid = {'token': token3_invalid, 'u_id': 2}
    
    profile_1_1 = requests.get(f'{config.url}user/profile/v1', params = handles_1)
    assert profile_1_1.status_code == 200
    profile_2_1 = requests.get(f'{config.url}user/profile/v1', params = handles_2)
    assert profile_2_1.status_code == 200
    profile_3_1 = requests.get(f'{config.url}user/profile/v1', params = handles_3)
    assert profile_3_1.status_code == 200
    profile_1 = requests.get(f'{config.url}user/profile/v1', params = handles_1_invalid)
    assert profile_1.status_code == 403
    profile_2 = requests.get(f'{config.url}user/profile/v1', params = handles_2_invalid)
    assert profile_2.status_code == 403
    profile_3 = requests.get(f'{config.url}user/profile/v1', params = handles_3_invalid)
    assert profile_3.status_code == 403

def test_profile_invalid_uid(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json() 
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']
    handles_1_invalid = {'token': token1, 'u_id': 4}
    handles_2_invalid = {'token': token2, 'u_id': 5}
    handles_3_invalid = {'token': token3, 'u_id': 6}
    
    profile_1 = requests.get(f'{config.url}user/profile/v1', params = handles_1_invalid)
    assert profile_1.status_code == 400
    profile_2 = requests.get(f'{config.url}user/profile/v1', params = handles_2_invalid)
    assert profile_2.status_code == 400
    profile_3 = requests.get(f'{config.url}user/profile/v1', params = handles_3_invalid)
    assert profile_3.status_code == 400

def test_profile_correct(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json() 
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']  
    handles_1 = {'token': token1, 'u_id': 2}
    handles_2 = {'token': token2, 'u_id': 1}
    handles_3 = {'token': token3, 'u_id': 3}
    
    profile_1 = requests.get(f'{config.url}user/profile/v1', params = handles_1)
    assert profile_1.status_code == 200
    data1 = profile_1.json()
    assert data1['user'] == user_2_member
    
    profile_2 = requests.get(f'{config.url}user/profile/v1', params = handles_2)
    assert profile_2.status_code == 200
    data2 = profile_2.json()
    assert data2['user'] == user_1_member
    
    profile_3 = requests.get(f'{config.url}user/profile/v1', params = handles_3)
    assert profile_3.status_code == 200
    data3 = profile_3.json()
    assert data3['user'] == user_3_member


#########################################################################
############################USER_SETNAME_TEST############################
#########################################################################

def test_profile_setname_invalid_token(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json() 
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']  
    token1_invalid = encode_jwt(1,2)    #wrong session
    token2_invalid = encode_jwt(6,0)    #wrong user id
    token3_invalid = encode_jwt(5,1)    #both wrong
    name_1 = {'token': token1, 'name_first': 'aaaaaa', 'name_last': 'bbbb'}
    name_2 = {'token': token2, 'name_first': 'aaaaaa1', 'name_last': 'bbbb1'}
    name_3 = {'token': token3, 'name_first': 'aaaaaa2', 'name_last': 'bbbb2'}
    name_1_invalid = {'token': token1_invalid, 'name_first': 'aaaaaa', 'name_last': 'bbbb'}
    name_2_invalid = {'token': token2_invalid, 'name_first': 'aaaaaa1', 'name_last': 'bbbb1'}
    name_3_invalid = {'token': token3_invalid, 'name_first': 'aaaaaa2', 'name_last': 'bbbb2'}
    
    setname_1_1 = requests.put(f'{config.url}user/profile/setname/v1', json = name_1)
    assert setname_1_1.status_code == 200
    setname_2_1 = requests.put(f'{config.url}user/profile/setname/v1', json = name_2)
    assert setname_2_1.status_code == 200
    setname_3_1 = requests.put(f'{config.url}user/profile/setname/v1', json = name_3)
    assert setname_3_1.status_code == 200
    setname_1 = requests.put(f'{config.url}user/profile/setname/v1', json = name_1_invalid)
    assert setname_1.status_code == 403
    setname_2 = requests.put(f'{config.url}user/profile/setname/v1', json = name_2_invalid)
    assert setname_2.status_code == 403
    setname_3 = requests.put(f'{config.url}user/profile/setname/v1', json = name_3_invalid)
    assert setname_3.status_code == 403

def test_profile_setname_invalid_firstname(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    r1_data = register1.json()
    r2_data = register2.json()
    token1 = r1_data['token']
    token2 = r2_data['token']
    
    # too short
    name_1_invalid = {'token': token1, 'name_first': '', 'name_last': 'bbbb'}
    # too long
    name_2_invalid = {'token': token2, 'name_first': '012345678901234567890123456789012345678901234567891', 'name_last': 'bbbb1'}
    
    setname_1 = requests.put(f'{config.url}user/profile/setname/v1', json = name_1_invalid)
    assert setname_1.status_code == 400
    setname_2 = requests.put(f'{config.url}user/profile/setname/v1', json = name_2_invalid)
    assert setname_2.status_code == 400

##########################NEED INVESTIGAT!!!!################################# 
def test_profile_setname_invalid_lastname(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    r1_data = register1.json()
    r2_data = register2.json()
    token1 = r1_data['token']
    token2 = r2_data['token']
    
    # too short
    name_1_invalid = {'token': token1, 'name_first': 'aa', 'name_last': ''}
    # too long
    name_last = '0123456789012345678901234567890123456789012345678912'
    name_2_invalid = {'token': token2, 'name_first': 'aaa', 'name_last': name_last}
    
    setname_1 = requests.put(f'{config.url}user/profile/setname/v1', json = name_1_invalid)
    assert setname_1.status_code == 400
    setname_2 = requests.put(f'{config.url}user/profile/setname/v1', json = name_2_invalid)
    assert setname_2.status_code == 400
###################################################################################
   
def test_profile_setname_invalid_lastnamee(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    r1_data = register1.json()
    r2_data = register2.json()
    token1 = r1_data['token']
    token2 = r2_data['token']
    handle = {'token': token1, 'u_id':1}
    handles_1_invalid = {'token': token1, 'name_first': 'Aa', 'name_last': 'Bb'}
    handles_2_invalid = {'token': token2, 'name_first': 'aaa1', 'name_last': 'bbb1'}
    
    setname_1 = requests.put(f'{config.url}user/profile/setname/v1', json = handles_1_invalid)
    assert setname_1.status_code == 200
    data = requests.get(f'{config.url}user/profile/v1', params = handle) 
    data1 = data.json()
    assert data1['user'] == {
        "u_id" : 1,
        "email" : "osama2as820sadas02@gmail.com", 
        "name_first": "Aa",
        "name_last": "Bb",
        "handle_str" : "osamaalmabrouk"
        }
    setname_2 = requests.put(f'{config.url}user/profile/setname/v1', json = handles_2_invalid)
    assert setname_2.status_code == 200 

#########################################################################
###########################USER_SETEMAIL_TEST############################
#########################################################################

def test_profile_setemail_invalid_token(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json() 
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']  
    token1_invalid = encode_jwt(1,2)    #wrong session
    token2_invalid = encode_jwt(6,0)    #wrong user id
    token3_invalid = encode_jwt(5,1)    #both wrong
    email_1 = {'token': token1, 'email': '123@gmail.com'}
    email_2 = {'token': token2, 'email': '123@4gmail.com'}
    email_3 = {'token': token3, 'email': '12345abc@gmail.com'}
    email_1_invalid = {'token': token1_invalid, 'email': '123@gmail.com'}
    email_2_invalid = {'token': token2_invalid, 'email': '1234@gmail.com'}
    email_3_invalid = {'token': token3_invalid, 'email': '12345abc@gmail.com'}
    
    setemail_1_1 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_1)
    assert setemail_1_1.status_code == 200
    setemail_2_1 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_2)
    assert setemail_2_1.status_code == 200
    setemail_3_1 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_3)
    assert setemail_3_1.status_code == 200
    setemail_1 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_1_invalid)
    assert setemail_1.status_code == 403
    setemail_2 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_2_invalid)
    assert setemail_2.status_code == 403
    setemail_3 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_3_invalid)
    assert setemail_3.status_code == 403

def test_profile_setemail_invalidemail(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']
    email_1 = {'token': token1, 'email': '12345!'}
    email_2 = {'token': token2, 'email': '123@123'}
    email_3 = {'token': token3, 'email': 'abc.abc'}
    
    setemail_1 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_1)
    assert setemail_1.status_code == 400
    setemail_2 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_2)
    assert setemail_2.status_code == 400
    setemail_3 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_3)
    assert setemail_3.status_code == 400

def test_profile_setemail_wrong_used(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']
    email_1 = {'token': token1, 'email': 'asdfg@gmail.com'}
    email_2 = {'token': token2, 'email': 'Asdfghjk@123.com'}
    email_3_1 = {'token': token3, 'email': 'asdfg@gmail.com'}
    email_3_2 = {'token': token3, 'email': 'Asdfghjk@123.com'}
    
    setemail_1 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_1)
    assert setemail_1.status_code == 200
    setemail_2 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_2)
    assert setemail_2.status_code == 200
    setemail_3_1 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_3_1)
    assert setemail_3_1.status_code == 400
    setemail_3_2 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_3_2)
    assert setemail_3_2.status_code == 400 
    
def test_profile_setemail_correct(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    assert register1.status_code == 200
    assert register2.status_code == 200
    assert register3.status_code == 200
    r1_data = register1.json()
    r2_data = register2.json()
    token1 = r1_data['token']
    token2 = r2_data['token']
    email_1 = {'token': token1, 'email': 'asdfg@gmail.com'}
    email_2 = {'token': token2, 'email': 'Asdfghjk@123.com'}
    user_check = {'token': token1, 'u_id':1}
    
    setemail_1 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_1)
    assert setemail_1.status_code == 200
    setemail_2 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_2)
    assert setemail_2.status_code == 200
    data = requests.get(f'{config.url}user/profile/v1', params = user_check) 
    data1 = data.json()
    assert data1['user'] == {
        "u_id" : 1,
        "email" : "asdfg@gmail.com", 
        "name_first": "Osama",
        "name_last": "Almabrouk",
        "handle_str" : "osamaalmabrouk"
        } 
def test_user_profile_uploadphoto(clear_users):

    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    assert register1.status_code == 200
    assert register2.status_code == 200
    assert register3.status_code == 200
    r1_data = register1.json()
    r2_data = register2.json()
    token1 = r1_data['token']
    token2 = r2_data['token']
    email_1 = {'token': token1, 'email': 'asdfg@gmail.com'}
    email_2 = {'token': token2, 'email': 'Asdfghjk@123.com'}
    user_check = {'token': token1, 'u_id':1}
    
    setemail_1 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_1)
    assert setemail_1.status_code == 200
    setemail_2 = requests.put(f'{config.url}user/profile/setemail/v1', json = email_2)
    assert setemail_2.status_code == 200
    data = requests.get(f'{config.url}user/profile/v1', params = user_check) 
    data1 = data.json()
    assert data1['user'] == {
        "u_id" : 1,
        "email" : "asdfg@gmail.com", 
        "name_first": "Osama",
        "name_last": "Almabrouk",
        "handle_str" : "osamaalmabrouk"
        } 

#########################################################################
###########################USERALL_TEST##################################
#########################################################################

def test_userall_invalid_token(clear_users):    
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    assert register1.status_code == 200
    token = {'token':encode_jwt(1,1)}
    invalid_request = requests.get(f'{config.url}users/all/v1', params = token)
    assert invalid_request.status_code == 403


def test_userall(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json = user_3)
    assert register1.status_code == 200
    assert register2.status_code == 200
    assert register3.status_code == 200
    token = {'token':encode_jwt(1,0)}
    valid_request = requests.get(f'{config.url}users/all/v1', params = token)
    assert valid_request.status_code == 200
    data=valid_request.json()
    assert len(data['users']) == 3
    
def test_userall_removed_user(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json=user_2)
    r1_data = register1.json()
    r2_data = register2.json() 
    token1 = r1_data['token']
    uid_2 = r2_data['auth_user_id']
    
    delete_2 = {'token': token1, 'u_id': uid_2}
    userdelete_2 = requests.delete(f'{config.url}admin/user/remove/v1', json=delete_2)
    assert userdelete_2.status_code == 200
    token = {'token':encode_jwt(1,0)}
    valid_request = requests.get(f'{config.url}users/all/v1', params = token)
    assert valid_request.status_code == 200
#########################################################################
###########################UPLOADPHOTO_TEST##############################
#########################################################################
def test_uploadphoto_invalid_token(clear_users):    
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    assert register1.status_code == 200
    
    photo = {'token':encode_jwt(1,1), 'img_url':"https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg", 'x_start': 10, 'y_start': 10, 'x_end': 200, 'y_end': 200}
    invalid_request = requests.post(f'{config.url}user/profile/uploadphoto/v1', json = photo)
    assert invalid_request.status_code == 403

def test_uploadphoto_invalid_url(clear_users):    
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    assert register1.status_code == 200
    
    photo = {'token':encode_jwt(1,0), 'img_url':"https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191", 'x_start': 10, 'y_start': 10, 'x_end': 200, 'y_end': 200}
    invalid_request = requests.post(f'{config.url}user/profile/uploadphoto/v1', json = photo)
    assert invalid_request.status_code == 400
    
def test_uploadphoto_notjpg(clear_users):    
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    assert register1.status_code == 200
    
    photo = {'token':encode_jwt(1,0), 'img_url':"https://i0.wp.com/www.printmag.com/wp-content/uploads/2021/02/4cbe8d_f1ed2800a49649848102c68fc5a66e53mv2.gif", 'x_start': 10, 'y_start': 10, 'x_end': 200, 'y_end': 200}
    invalid_request = requests.post(f'{config.url}user/profile/uploadphoto/v1', json = photo)
    assert invalid_request.status_code == 400

def test_uploadphoto_invalid_size(clear_users):    
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    assert register1.status_code == 200
    
    photo = {'token':encode_jwt(1,0), 'img_url':"https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg", 'x_start':-1, 'y_start': 10, 'x_end': 200, 'y_end': 200}
    invalid_request = requests.post(f'{config.url}user/profile/uploadphoto/v1', json = photo)
    assert invalid_request.status_code == 400
    photo2 = {'token':encode_jwt(1,0), 'img_url':"https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg", 'x_start':300, 'y_start': 10, 'x_end': 200, 'y_end': 200}
    invalid_request2 = requests.post(f'{config.url}user/profile/uploadphoto/v1', json = photo2)
    assert invalid_request2.status_code == 400
    photo3 = {'token':encode_jwt(1,0), 'img_url':"https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg", 'x_start':10, 'y_start': -1, 'x_end': 200, 'y_end': 200}
    invalid_request3 = requests.post(f'{config.url}user/profile/uploadphoto/v1', json = photo3)
    assert invalid_request3.status_code == 400
    photo4 = {'token':encode_jwt(1,0), 'img_url':"https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg", 'x_start':10, 'y_start': 300, 'x_end': 200, 'y_end': 200}
    invalid_request4 = requests.post(f'{config.url}user/profile/uploadphoto/v1', json = photo4)
    assert invalid_request4.status_code == 400
'''   
def test_uploadphoto_basic(clear_users):    
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    assert register1.status_code == 200
    
    photo = {'token':encode_jwt(1,0), 'img_url':"https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg", 'x_start': 10, 'y_start': 10, 'x_end': 200, 'y_end': 200}
    valid_request = requests.post(f'{config.url}user/profile/uploadphoto/v1', json = photo)
    assert valid_request.status_code == 200
'''

#########################################################################
###########################USERSTATS_TEST################################
#########################################################################

def test_userstats_invalid_token(clear_users):    
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    assert register1.status_code == 200
    token = {'token':encode_jwt(1,1)}
    invalid_request = requests.get(f'{config.url}/user/stats/v1', params = token)
    assert invalid_request.status_code == 403

def test_userstats_didnotdoanything(clear_users):    
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    assert register1.status_code == 200
    token = {'token':encode_jwt(1,0)}
    valid_request = requests.get(f'{config.url}/user/stats/v1', params = token)
    assert valid_request.status_code == 200
    
def test_userstats_twochannels(clear_users):    
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    assert register1.status_code == 200
    r1_data = register1.json()
    token1 = r1_data['token']
    channel_1 = {"token": token1,"name": "Channel1","is_public": False}
    create_ch1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_ch1.status_code == 200
    token = {'token':encode_jwt(1,0)}
    valid_request1 = requests.get(f'{config.url}/user/stats/v1', params = token)
    assert valid_request1.status_code == 200
    
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    assert register2.status_code == 200
    r2_data = register2.json()
    token2 = r2_data['token']
    channel_2 = {"token": token2,"name": "Channel2","is_public": False}
    create_ch2 = requests.post(f"{config.url}channels/create/v2", json=channel_2)
    assert create_ch2.status_code == 200
    
    valid_request2 = requests.get(f'{config.url}/user/stats/v1', params = token)
    assert valid_request2.status_code == 200
    
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 1, 'message':"hey guys"}
    msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
    assert msg_request.status_code == 200
    
    valid_request3 = requests.get(f'{config.url}/user/stats/v1', params = token)
    assert valid_request3.status_code == 200

def test_userstats_dms(clear_users):    
    register1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    register2 = requests.post(f"{config.url}auth/register/v2", json=user_2)
    
    r1_data = register1.json()
    r2_data = register2.json()
    
    token1 = r1_data['token']
    #token2 = r2_data['token']
    
    #uid_1 = r1_data['auth_user_id']
    uid_2 = r2_data['auth_user_id']
    
    dm_1 = {"token": token1,"u_ids": [uid_2]}
    
    create_dm1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm1.status_code == 200
    
    valid_message = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': "hello"}
    valid_request = requests.post(f"{config.url}message/senddm/v1", json = valid_message)
    assert valid_request.status_code == 200
    
    token = {'token':encode_jwt(1,0)}
    valid_request1 = requests.get(f'{config.url}/user/stats/v1', params = token)
    assert valid_request1.status_code == 200

#########################################################################
###########################USERsSTATS_TEST################################
#########################################################################

def test_usersstats_invalid_token(clear_users):    
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    assert register1.status_code == 200
    token = {'token':encode_jwt(1,1)}
    invalid_request = requests.get(f'{config.url}/users/stats/v1', params = token)
    assert invalid_request.status_code == 403
    
def test_usersstats_didnotdoanything(clear_users):    
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    assert register1.status_code == 200
    token = {'token':encode_jwt(1,0)}
    valid_request = requests.get(f'{config.url}/users/stats/v1', params = token)
    assert valid_request.status_code == 200
    
def test_usersstats_twochannels(clear_users):    
    register1 = requests.post(f'{config.url}auth/register/v2', json = user_1)
    assert register1.status_code == 200
    r1_data = register1.json()
    token1 = r1_data['token']
    channel_1 = {"token": token1,"name": "Channel1","is_public": False}
    create_ch1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_ch1.status_code == 200
    token = {'token':encode_jwt(1,0)}
    valid_request1 = requests.get(f'{config.url}/users/stats/v1', params = token)
    assert valid_request1.status_code == 200
    
    register2 = requests.post(f'{config.url}auth/register/v2', json = user_2)
    assert register2.status_code == 200
    r2_data = register2.json()
    token2 = r2_data['token']
    channel_2 = {"token": token2,"name": "Channel2","is_public": False}
    create_ch2 = requests.post(f"{config.url}channels/create/v2", json=channel_2)
    assert create_ch2.status_code == 200
    
    valid_request2 = requests.get(f'{config.url}/users/stats/v1', params = token)
    assert valid_request2.status_code == 200
    
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 1, 'message':"hey guys"}
    msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
    assert msg_request.status_code == 200
    
    valid_request3 = requests.get(f'{config.url}/users/stats/v1', params = token)
    assert valid_request3.status_code == 200

def test_usersstats_dms(clear_users):    
    register1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    register2 = requests.post(f"{config.url}auth/register/v2", json=user_2)
    
    r1_data = register1.json()
    r2_data = register2.json()
    
    token1 = r1_data['token']
    #token2 = r2_data['token']
    
    #uid_1 = r1_data['auth_user_id']
    uid_2 = r2_data['auth_user_id']
    
    dm_1 = {"token": token1,"u_ids": [uid_2]}
    
    create_dm1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm1.status_code == 200
    
    valid_message = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': "hello"}
    valid_request = requests.post(f"{config.url}message/senddm/v1", json = valid_message)
    assert valid_request.status_code == 200
    
    token = {'token':encode_jwt(1,0)}
    valid_request1 = requests.get(f'{config.url}/users/stats/v1', params = token)
    assert valid_request1.status_code == 200
