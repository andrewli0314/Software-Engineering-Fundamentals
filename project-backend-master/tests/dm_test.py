import pytest
import requests
import json
from requests.api import request
from src import config
from src.helpers import encode_jwt, decode_jwt

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
            "name_first": "Andres",
            "name_last": "Iniesta"
            }
user_2_member = {
    "u_id" : 2,
    "email" : "someemailadress@gmail.com", 
    "name_first": "Andres",
    "name_last": "Iniesta",
    "handle_str" : "andresiniesta"
}
#####################################################################
user_3 =  {
            "email": "someemailadressss@gmail.com",
            "password": "Samsoomitoz2132",
            "name_first": "suii",
            "name_last": "suii"
            }
user_3_member = {
    "u_id" : 3,
    "email" : "someemailadressss@gmail.com", 
    "name_first": "suii",
    "name_last": "suii",
    "handle_str" : "suiisuii"
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
def clear_and_register4():
    """This will give us one registered user and already logged-in because its token is valid"""
    response_del = requests.delete(f"{config.url}clear/v1")
    assert response_del.status_code == 200
    register1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    register2 = requests.post(f"{config.url}auth/register/v2", json=user_2)
    register3 = requests.post(f"{config.url}auth/register/v2", json=user_3)
    register4 = requests.post(f"{config.url}auth/register/v2", json=user_4)
    #r1_data = register1.json()
    #r2_data = register2.json()
    #r3_data = register3.json()
    #r4_data = register4.json()
    #token1 = r1_data['token']
    #token2 = r2_data['token']
    #token3 = r3_data['token']
    #token4 = r4_data['token']
    #uid_1 = r1_data['auth_user_id']
    #uid_2 = r2_data['auth_user_id']
    #uid_3 = r3_data['auth_user_id']
    #uid_4 = r4_data['auth_user_id']
    assert register1.status_code == 200
    assert register2.status_code == 200
    assert register3.status_code == 200
    assert register4.status_code == 200

@pytest.fixture
def clear_and_register4creat6():
    """This will give us three registered users and already logged-in because their tokens are valid"""
    response_del = requests.delete(f"{config.url}clear/v1")
    assert response_del.status_code == 200
    register1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    register2 = requests.post(f"{config.url}auth/register/v2", json=user_2)
    register3 = requests.post(f"{config.url}auth/register/v2", json=user_3)
    register4 = requests.post(f"{config.url}auth/register/v2", json=user_4)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()
    r4_data = register4.json()
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']
    token4 = r4_data['token']
    uid_1 = r1_data['auth_user_id']
    uid_2 = r2_data['auth_user_id']
    uid_3 = r3_data['auth_user_id']
    uid_4 = r4_data['auth_user_id']
    assert register1.status_code == 200
    assert register2.status_code == 200
    assert register3.status_code == 200
    assert register4.status_code == 200
    
    #list of users
    users_1 = [uid_1]
    users_2 = [uid_2]
    users_3 = [uid_3]
    users_4 = [uid_1, uid_2]
    users_5 = [uid_2, uid_3]
    users_6 = [uid_4, uid_2, uid_3]
    
    #list of dms:
    dm_1 = {"token": token3,"u_ids": users_1}
    dm_2 = {"token": token1,"u_ids": users_2}
    dm_3 = {"token": token2,"u_ids": users_3}
    dm_4 = {"token": token3,"u_ids": users_4}
    dm_5 = {"token": token4,"u_ids": users_5}
    dm_6 = {"token": token1,"u_ids": users_6}

    #Create 6 dms:
    create_dm1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm1.status_code == 200
    create_dm2 = requests.post(f"{config.url}dm/create/v1", json = dm_2)
    assert create_dm2.status_code == 200
    create_dm3 = requests.post(f"{config.url}dm/create/v1", json = dm_3)
    assert create_dm3.status_code == 200
    create_dm4 = requests.post(f"{config.url}dm/create/v1", json = dm_4)
    assert create_dm4.status_code == 200
    create_dm5 = requests.post(f"{config.url}dm/create/v1", json = dm_5)
    assert create_dm5.status_code == 200
    create_dm6 = requests.post(f"{config.url}dm/create/v1", json = dm_6)
    assert create_dm6.status_code == 200
   
#########################################################################
############################DM_CREATE_TEST###############################
#########################################################################

#Error tests
def test_dm_invalidtoken(clear_and_register4):   
    invalid_user = encode_jwt(5, 0)
    token_1 = {"token": invalid_user,"u_ids": [1,2]}
    create_dm_1 = requests.post(f"{config.url}/dm/create/v1", json = token_1)
    assert create_dm_1.status_code == 403
    
    invalid_session = encode_jwt(1, 2)
    token_2 = {"token": invalid_session,"u_ids": [3]}
    create_dm_2 = requests.post(f"{config.url}/dm/create/v1", json = token_2)
    assert create_dm_2.status_code == 403
    
def test_dm_invaliduser(clear_and_register4):   
    valid_token1 = encode_jwt(1, 0)
    token_1 = {"token": valid_token1,"u_ids": [2,5]}
    create_dm_1 = requests.post(f"{config.url}/dm/create/v1", json = token_1)
    assert create_dm_1.status_code == 400
    
    valid_token2 = encode_jwt(1, 0)
    token_2 = {"token": valid_token2,"u_ids": [5]}
    create_dm_2 = requests.post(f"{config.url}/dm/create/v1", json = token_2)
    assert create_dm_2.status_code == 400 

# should work tests    
def test_onesuer_create_one_dm(clear_and_register4):
    token1 = encode_jwt(2, 0)
    dm_1 = {"token": token1,"u_ids": [1]}
    create_dm_1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm_1.status_code == 200
    
    token2 = encode_jwt(1, 0)
    dm_2 = {"token": token2,"u_ids": [2,3]}
    create_dm_2 = requests.post(f"{config.url}dm/create/v1", json = dm_2)
    assert create_dm_2.status_code == 200

def test_oneuser_multiple_dms(clear_and_register4):   
    token1 = encode_jwt(1, 0)
    token2 = encode_jwt(2, 0)
    token3 = encode_jwt(3, 0)
    token4 = encode_jwt(4, 0)
    
    #list of users
    users_1 = [1]
    users_2 = [2]
    users_3 = [3]
    users_4 = [1, 2]
    users_5 = [2, 3]
    users_6 = [4, 2, 3]
    
    #list of dms:
    dm_1 = {"token": token3,"u_ids": users_1}
    dm_2 = {"token": token1,"u_ids": users_2}
    dm_3 = {"token": token2,"u_ids": users_3}
    dm_4 = {"token": token3,"u_ids": users_4}
    dm_5 = {"token": token4,"u_ids": users_5}
    dm_6 = {"token": token1,"u_ids": users_6}
    
    #Create 6 dms:
    create_dm1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm1.status_code == 200
    create_dm2 = requests.post(f"{config.url}dm/create/v1", json = dm_2)
    assert create_dm2.status_code == 200
    create_dm3 = requests.post(f"{config.url}dm/create/v1", json = dm_3)
    assert create_dm3.status_code == 200
    create_dm4 = requests.post(f"{config.url}dm/create/v1", json = dm_4)
    assert create_dm4.status_code == 200
    create_dm5 = requests.post(f"{config.url}dm/create/v1", json = dm_5)
    assert create_dm5.status_code == 200
    create_dm6 = requests.post(f"{config.url}dm/create/v1", json = dm_6)
    assert create_dm6.status_code == 200


#########################################################################
##############################DM_LIST_TEST###############################
#########################################################################

# Error test
def test_dm_list_invalidtoken(clear_and_register4creat6):   
    invalid_user = encode_jwt(5, 0)
    token_1 = {"token": invalid_user}
    dm_list_1 = requests.get(f"{config.url}dm/list/v1", params = token_1)
    assert dm_list_1.status_code == 403
    
    invalid_session = encode_jwt(1, 2)
    token_2 = {"token": invalid_session}
    dm_list_2 = requests.get(f"{config.url}dm/list/v1", params = token_2)
    assert dm_list_2.status_code == 403

def test_dm_list_one_user(clear_and_register4creat6):   
    u_1 = {"token": encode_jwt(1, 0)}
    
    #Test if it data obtained is true, return dms = { dm_id, name }:
    dm_list_u1 = requests.get(f"{config.url}dm/list/v1", params=u_1)
    assert dm_list_u1.status_code == 200
    data_1 = dm_list_u1.json()
    # channel_id, name
    assert len(data_1['dms']) == 4


#########################################################################
#############################DM_REMOVE_TEST##############################
#########################################################################
# Error test
def test_dm_remove_invalidtoken(clear_and_register4creat6):   
    invalid_user = encode_jwt(5, 0)
    token_1 = {"token": invalid_user, "dm_id": 1}
    dm_remove_1 = requests.delete(f"{config.url}/dm/remove/v1", json = token_1)
    assert dm_remove_1.status_code == 403
    
    invalid_session = encode_jwt(1, 2)
    token_2 = {"token": invalid_session, "dm_id": 2}
    dm_remove_2 = requests.delete(f"{config.url}/dm/remove/v1", json = token_2)
    assert dm_remove_2.status_code == 403

def test_dm_remove_invaliddm(clear_and_register4creat6):   
    user_1 = encode_jwt(1, 0)
    token_1 = {"token": user_1, "dm_id": 8}
    dm_remove_1 = requests.delete(f"{config.url}/dm/remove/v1", json = token_1)
    assert dm_remove_1.status_code == 400
    
    user_2 = encode_jwt(2, 0)
    token_2 = {"token": user_2, "dm_id": 9}
    dm_remove_2 = requests.delete(f"{config.url}/dm/remove/v1", json = token_2)
    assert dm_remove_2.status_code == 400
   

def test_dm_remove_notcreatot(clear_and_register4creat6):   
    user_1 = encode_jwt(1, 0)
    token_1 = {"token": user_1, "dm_id": 1}
    dm_remove_1 = requests.delete(f"{config.url}/dm/remove/v1", json = token_1)
    assert dm_remove_1.status_code == 403
    
    user_2 = encode_jwt(2, 0)
    token_2 = {"token": user_2, "dm_id": 2}
    dm_remove_2 = requests.delete(f"{config.url}/dm/remove/v1", json = token_2)
    assert dm_remove_2.status_code == 403
  
def test_dm_remove_correct(clear_and_register4creat6):   
    # user2 in dm2-6, removed dm2,3,4, dm list should be 5,6 left
    user_1 = encode_jwt(1, 0)
    token_1 = {"token": user_1, "dm_id": 2}
    dm_remove_1 = requests.delete(f"{config.url}/dm/remove/v1", json = token_1)
    assert dm_remove_1.status_code == 200
    
    user_2 = encode_jwt(2, 0)
    token_2 = {"token": user_2, "dm_id": 3}
    dm_remove_2 = requests.delete(f"{config.url}/dm/remove/v1", json = token_2)
    assert dm_remove_2.status_code == 200
    
    user_3 = encode_jwt(3, 0)
    token_3 = {"token": user_3, "dm_id": 4}
    dm_remove_3 = requests.delete(f"{config.url}/dm/remove/v1", json = token_3)
    assert dm_remove_3.status_code == 200
    
    list_token = {"token": user_2}
    u2_list = requests.get(f"{config.url}dm/list/v1", params = list_token)
    assert u2_list.status_code == 200
    data = u2_list.json()
    assert len(data['dms']) == 2
    

#########################################################################
###########################DM_DETAILS_TEST###############################
#########################################################################

def test_dmdetails_invalid_dmid(clear_and_register4creat6):
    user_1 = encode_jwt(1, 0)
    token_1 = {"token": user_1, "dm_id": 15}
    dm_detail_1 = requests.get(f"{config.url}dm/details/v1", params = token_1)
    assert dm_detail_1.status_code == 400

def test_dmdetails_validdmid_usernotmember(clear_and_register4creat6):
    #user4 not in dm1-5, user1 not in dm5,6
    dm1_det = {"token" : encode_jwt(4,0), "dm_id" : 1}
    dm2_det = {"token" : encode_jwt(4,0), "dm_id" : 2}
    dm3_det = {"token" : encode_jwt(4,0), "dm_id" : 3}
    dm4_det = {"token" : encode_jwt(4,0), "dm_id" : 4}
    dm5_det = {"token" : encode_jwt(1,0), "dm_id" : 5}
    dm6_det = {"token" : encode_jwt(1,0), "dm_id" : 6}

    #make requests:
    rdm1_det = requests.get(f"{config.url}dm/details/v1", params = dm1_det)
    rdm2_det = requests.get(f"{config.url}dm/details/v1", params = dm2_det)
    rdm3_det = requests.get(f"{config.url}dm/details/v1", params = dm3_det)
    rdm4_det = requests.get(f"{config.url}dm/details/v1", params = dm4_det)
    rdm5_det = requests.get(f"{config.url}dm/details/v1", params = dm5_det)
    rdm6_det = requests.get(f"{config.url}dm/details/v1", params = dm6_det)    
    #assert requests: have to be 403
    assert rdm1_det.status_code == 403
    assert rdm2_det.status_code == 403
    assert rdm3_det.status_code == 403
    assert rdm4_det.status_code == 403
    assert rdm5_det.status_code == 403
    assert rdm6_det.status_code == 200

#passed
def test_dmdetails_validdmid_invalidtoken(clear_and_register4creat6):
    invalid_user = encode_jwt(5, 0)
    token_1 = {"token": invalid_user, "dm_id": 1}
    dm_detail_1 = requests.get(f"{config.url}dm/list/v1", params = token_1)
    assert dm_detail_1.status_code == 403
    
    invalid_session = encode_jwt(1, 2)
    token_2 = {"token": invalid_session, "dm_id": 2}
    dm_detail_2 = requests.get(f"{config.url}dm/list/v1", params = token_2)
    assert dm_detail_2.status_code == 403


def test_dmdetails_invalid_token_session_id(clear_and_register4creat6):
    #403
    #u1 and 2 asking for their dms with existing session_ids:
    #u1 has dm1246      u2 has dm2-6 : u1 will login 2 times and u2 will login once

    #logins:
    login1 = {"email": "osama2as820sadas02@gmail.com", "password": "dasdasdasdlakmLN"}
    login2 = {"email": "someemailadress@gmail.com", "password": "dasdasdasdlakmLN"}
    
    rlogin1 = requests.post(f"{config.url}auth/login/v2", json = login1)
    rlogin1_data = rlogin1.json()
    assert rlogin1_data['auth_user_id'] == 1
    assert decode_jwt(rlogin1_data['token']) == {'u_id': 1, 'session_id': 1}
    token1_s1 = rlogin1_data['token']

    rlogin12 = requests.post(f"{config.url}auth/login/v2", json = login1)
    rlogin12_data = rlogin12.json()
    assert rlogin12_data['auth_user_id'] == 1
    assert decode_jwt(rlogin12_data['token']) == {'u_id': 1, 'session_id': 2}
    token12_s1 = rlogin12_data['token']

    rlogin2 = requests.post(f"{config.url}auth/login/v2", json = login2)
    rlogin2_data = rlogin2.json()
    assert rlogin2_data['auth_user_id'] == 2
    assert decode_jwt(rlogin2_data['token']) == {'u_id': 2, 'session_id': 1}
    token2_s1 = rlogin2_data['token']
    
    #u1 and u2 will login as well to extend the range of tests.
    dm1_det = {"token" : encode_jwt(1,0), "dm_id" : 1} #200
    dm2_det = {"token" : token1_s1, "dm_id" : 2} #200
    dm3_det = {"token" : encode_jwt(2,0), "dm_id" : 3} #200
    dm4_det = {"token" : token12_s1, "dm_id" :4} #200
    dm5_det = {"token" : token2_s1, "dm_id" : 5} #200
    dm5_det_invalid = {"token" : encode_jwt(1,3), "dm_id" : 5} #403
    dm6_det = {"token" : encode_jwt(1,1), "dm_id" : 6} #200
    dm6_det_invalid = {"token" : encode_jwt(2,2), "dm_id" : 6} #403


    #make a series of details
    rdm1_det = requests.get(f"{config.url}dm/details/v1", params = dm1_det)
    assert rdm1_det.status_code == 200

    rdm2_det = requests.get(f"{config.url}dm/details/v1", params = dm2_det)
    assert rdm2_det.status_code == 200

    rdm3_det = requests.get(f"{config.url}dm/details/v1", params = dm3_det)
    assert rdm3_det.status_code == 200

    rdm4_det = requests.get(f"{config.url}dm/details/v1", params = dm4_det)
    assert rdm4_det.status_code == 200

    rdm5_det = requests.get(f"{config.url}dm/details/v1", params = dm5_det)
    assert rdm5_det.status_code == 200
    
    rdm5_det_invalid = requests.get(f"{config.url}dm/details/v1", params = dm5_det_invalid)
    assert rdm5_det_invalid.status_code == 403
    
    rdm6_det = requests.get(f"{config.url}dm/details/v1", params = dm6_det)
    assert rdm6_det.status_code == 200

    rdm6_det_invalid = requests.get(f"{config.url}dm/details/v1", params = dm6_det_invalid)
    assert rdm6_det_invalid.status_code == 403


def test_dmdetails_basic(clear_and_register4creat6):
    dm1_det = {"token" : encode_jwt(1,0), "dm_id" : 1}
    dm2_det = {"token" : encode_jwt(1,0), "dm_id" : 2}
    dm4_det = {"token" : encode_jwt(2,0), "dm_id" : 4}

    #do the requests and fetch data:
    rdm1_det = requests.get(f"{config.url}dm/details/v1", params = dm1_det)
    assert rdm1_det.status_code == 200
    rdm1_det_data = rdm1_det.json()

    rdm2_det = requests.get(f"{config.url}dm/details/v1", params = dm2_det)
    assert rdm2_det.status_code == 200
    rdm2_det_data = rdm2_det.json()

    rdm4_det = requests.get(f"{config.url}dm/details/v1", params = dm4_det)
    assert rdm4_det.status_code == 200
    rdm4_det_data = rdm4_det.json()

    #now assert the data:
    #{ name, members }
    #assert dm1 details
    assert rdm1_det_data['members'] == [user_1_member, user_3_member]

    #assert dm2 details
    assert rdm2_det_data['members'] == [user_1_member, user_2_member]

    #assert dm4 details
    assert rdm4_det_data['members'] == [user_1_member, user_2_member, user_3_member]


def test_dmdetails_afterleave(clear_and_register4creat6):
    #user1,2,3,4 all in dm6, user3 leaved
    u3_dm6 = {"token" : encode_jwt(3,0), "dm_id" : 6}
    ru3_dm6_leave = requests.post(f"{config.url}dm/leave/v1", json = u3_dm6)
    assert ru3_dm6_leave.status_code == 200

    #get dm6 details:
    dm6_det = {"token" : encode_jwt(1,0), "dm_id" : 6}
    rdm6_det = requests.get(f"{config.url}dm/details/v1", params = dm6_det)
    assert rdm6_det.status_code == 200
    rdm6_det_data = rdm6_det.json()
    assert len(rdm6_det_data['members']) == 3


#########################################################################
##########################DM_LEAVE_TESTS#################################
#########################################################################
def test_dmleave_invalid_token(clear_and_register4creat6):
    """User2 will leave dm1, must return 403"""
    dm1_leave = {'token': encode_jwt(2,1), 'dm_id' : 1}
    request = requests.post(f"{config.url}dm/leave/v1", json = dm1_leave)
    assert request.status_code == 403

    dm1_leave2 = {'token': encode_jwt(7,0), 'dm_id' : 1}
    request2 = requests.post(f"{config.url}dm/leave/v1", json = dm1_leave2)
    assert request2.status_code == 403

def test_dmleave_invalid_dmid(clear_and_register4creat6):
    """Leave dm is 7, must raise 400"""
    dm7_leave = {'token': encode_jwt(1,0), 'dm_id' : 7}
    request = requests.post(f"{config.url}dm/leave/v1", json = dm7_leave)
    assert request.status_code == 400

def test_dmleave_not_member(clear_and_register4creat6):
    "let user3 leave dms 1 and 2, first arg is 200, last must raise 403"
    dm1_leave = {'token': encode_jwt(3,0), 'dm_id' : 1}
    dm3_leave = {'token': encode_jwt(3,0), 'dm_id' : 2}

    leave_dm1 = requests.post(f"{config.url}dm/leave/v1", json = dm1_leave)
    assert leave_dm1.status_code == 200

    leave_dm3 = requests.post(f"{config.url}dm/leave/v1", json = dm3_leave)
    assert leave_dm3.status_code == 403

def test_dm_leave_basic(clear_and_register4creat6):
    """
    - User1 in 1246
    - User2 in 2-6
    - User3 in 13456
    - User4 in 56
    """
    # users 2 and 3 leave dm6
    # user 1 leaves dm4
    # user 4 leaves dm5, who is the creator, dm should work after the leave
    u2_leave_dm6 = {'token': encode_jwt(2,0), 'dm_id': 6}
    u3_leave_dm6 = {'token': encode_jwt(3,0), 'dm_id': 6}
    u1_leave_dm4 = {'token': encode_jwt(1,0), 'dm_id': 4}
    u4_leave_dm5 = {'token': encode_jwt(4,0), 'dm_id': 5}
    
    u2_leave = requests.post(f"{config.url}dm/leave/v1", json = u2_leave_dm6)
    assert u2_leave.status_code == 200
    u3_leave = requests.post(f"{config.url}dm/leave/v1", json = u3_leave_dm6)
    assert u3_leave.status_code == 200
    u1_leave = requests.post(f"{config.url}dm/leave/v1", json = u1_leave_dm4)
    assert u1_leave.status_code == 200
    u4_leave = requests.post(f"{config.url}dm/leave/v1", json = u4_leave_dm5)
    assert u4_leave.status_code == 200
    
    ####################fetch dm details to check#########################
    dm6_det = {"token" : encode_jwt(1,0), "dm_id" : 6}
    dm4_det = {"token" : encode_jwt(3,0), "dm_id" : 4}
    dm5_det = {"token" : encode_jwt(2,0), "dm_id" : 5}
    
    #do the requests and fetch data:
    rdm6_det = requests.get(f"{config.url}dm/details/v1", params = dm6_det)
    assert rdm6_det.status_code == 200
    rdm6_det_data = rdm6_det.json()
    rdm4_det = requests.get(f"{config.url}dm/details/v1", params = dm4_det)
    assert rdm4_det.status_code == 200
    rdm4_det_data = rdm4_det.json()
    rdm5_det = requests.get(f"{config.url}dm/details/v1", params = dm5_det)
    assert rdm4_det.status_code == 200
    rdm5_det_data = rdm5_det.json()
    
    #assert dm6 and dm4 details
    assert len(rdm6_det_data['members']) == 2
    assert len(rdm4_det_data['members']) == 2
    assert len(rdm5_det_data['members']) == 2
    
    #try getting dm data from users who left, must return 403
    dm6_det_invalid = {"token" : encode_jwt(3,0), "dm_id" : 6}
    dm4_det_invalid = {"token" : encode_jwt(1,0), "dm_id" : 4}
    dm5_det_invalid = {"token" : encode_jwt(4,0), "dm_id" : 5}
    rdm6_det = requests.get(f"{config.url}dm/details/v1", params = dm6_det_invalid)
    assert rdm6_det.status_code == 403
    rdm4_det = requests.get(f"{config.url}dm/details/v1", params = dm4_det_invalid)
    assert rdm4_det.status_code == 403
    rdm5_det = requests.get(f"{config.url}dm/details/v1", params = dm5_det_invalid)
    assert rdm5_det.status_code == 403

    
#########################################################################
#########################MESSAGE_SEND_DM#################################
#########################################################################

def test_messagesenddm_invalid_token(clear_and_register4creat6):
    invalid_token = {'token': encode_jwt(1,1), 'dm_id' : 1, 'message': "Hola"}
    rinvalid_token = requests.post(f"{config.url}message/senddm/v1", json = invalid_token)
    assert rinvalid_token.status_code == 403


def test_messagesenddm_invalid_dmid(clear_and_register4creat6):
    invalid_token = {'token': encode_jwt(1,0), 'dm_id' : 7, 'message': "Hola"}
    rinvalid_token = requests.post(f"{config.url}message/senddm/v1", json = invalid_token)
    assert rinvalid_token.status_code == 400

def test_messagesenddm_long_message(clear_and_register4creat6):
    #has 1001 chars.
    long_message = "vSO1Xx3sVDvSanODuMrDsnHqML9mur5GVGHMQbwENoQKVn7L75uiaqyc6G"\
    "GGJDvDzwtl25A8uXJBrkw8Wd1OdQ0axFtkZhtO5CGvDfJTxSNdduH7Ut8uWO3ox9tcqgtv2"\
    "V6bK23AYrj3nNQVCkaeClwaqSdgsUXn3x96nMt8Ck9k5fUdF1M04oHJ8uaNjLKkjwmi8r6EJ"\
    "4WfXKooYsAW8Jxug7XUSOUMW87fUqVarKNxtDpnRymOfYWnkRbSsLRtauqzEbilKqLaQGDPj"\
    "UrQKYZJgbO6EUCmInnovSKFRYnvcn6GRfHqC4px0ChdxN6cs3oxmB9ECi38BCP92885Qzl0IH"\
    "87s5aa3t2m5kYmAjuklhYfsdGkQSuqIEP7CmxDqcFDx6SVb8DJEA9MsVW5LifzpzYqLxU6ZpNQ"\
    "qO2SLegpnKJdwQ7ud9xxaQaW00ocPAVT7zLlwr1tcWuqHZ17dmvwDejtHkmobYM511kT5bKZ2Dr"\
    "UFNHDUmUsPSn5dBN2FH1ZvUCSdng3hFhxe3L0UgElpTZdSeCOQaCZJ5psWCjbaR94xU2ufZROT5"\
    "TwCXgeHjBXWMdM5cYEh7bBfzKRvnbWKof4QMIkrfb6vbjRBptpkfV5lW66CeVqY3EVCGoQymassAs"\
    "9mHnrYmjRxL05NLpQsj5TwGYDonEw4KQcPtugv5q0tB8gPfGFGUZMmaLwuBJj2fXoHcjSPfc8vJWi"\
    "VblSGHpyVFQSLog0xMcMJpeetomITyLKsw2cuc2NKPPEjl4g3gnrNkgL62qeVdGTlXEsaMuwE4O1xi"\
    "QaXKEzUwHU21DHsZLEoictCryufrlk8U2VcZiJJjc23sW55YApnnqDWwTWdlWYjeB5rqpmbisPEPpGz6"\
    "BilRClzlt5uoONDJgUVwxikwzlafidDHzeVb3ypuy4U8PLs9atGqVJqAYsEkvncTKEi1FCNlL6v50vl13"\
    "x94jHmNno5sFAkOf1EKuyWK2NX75bzdhnV99Es"

    #has 1000 chars
    about_right = "vSO1Xx3sVDvSanODuMrDsnHqML9mur5GVGHMQbwENoQKVn7L75uiaqyc6G"\
    "GGJDvDzwtl25A8uXJBrkw8Wd1OdQ0axFtkZhtO5CGvDfJTxSNdduH7Ut8uWO3ox9tcqgtv2"\
    "V6bK23AYrj3nNQVCkaeClwaqSdgsUXn3x96nMt8Ck9k5fUdF1M04oHJ8uaNjLKkjwmi8r6EJ"\
    "4WfXKooYsAW8Jxug7XUSOUMW87fUqVarKNxtDpnRymOfYWnkRbSsLRtauqzEbilKqLaQGDPj"\
    "UrQKYZJgbO6EUCmInnovSKFRYnvcn6GRfHqC4px0ChdxN6cs3oxmB9ECi38BCP92885Qzl0IH"\
    "87s5aa3t2m5kYmAjuklhYfsdGkQSuqIEP7CmxDqcFDx6SVb8DJEA9MsVW5LifzpzYqLxU6ZpNQ"\
    "qO2SLegpnKJdwQ7ud9xxaQaW00ocPAVT7zLlwr1tcWuqHZ17dmvwDejtHkmobYM511kT5bKZ2Dr"\
    "UFNHDUmUsPSn5dBN2FH1ZvUCSdng3hFhxe3L0UgElpTZdSeCOQaCZJ5psWCjbaR94xU2ufZROT5"\
    "TwCXgeHjBXWMdM5cYEh7bBfzKRvnbWKof4QMIkrfb6vbjRBptpkfV5lW66CeVqY3EVCGoQymassAs"\
    "9mHnrYmjRxL05NLpQsj5TwGYDonEw4KQcPtugv5q0tB8gPfGFGUZMmaLwuBJj2fXoHcjSPfc8vJWi"\
    "VblSGHpyVFQSLog0xMcMJpeetomITyLKsw2cuc2NKPPEjl4g3gnrNkgL62qeVdGTlXEsaMuwE4O1xi"\
    "QaXKEzUwHU21DHsZLEoictCryufrlk8U2VcZiJJjc23sW55YApnnqDWwTWdlWYjeB5rqpmbisPEPpGz6"\
    "BilRClzlt5uoONDJgUVwxikwzlafidDHzeVb3ypuy4U8PLs9atGqVJqAYsEkvncTKEi1FCNlL6v50vl13"\
    "x94jHmNno5sFAkOf1EKuyWK2NX75bzdhnV99E"

    qinvalid_message = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': long_message}
    invalid_request = requests.post(f"{config.url}message/senddm/v1", json = qinvalid_message)
    assert invalid_request.status_code == 400

    qvalid_message = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': about_right}
    valid_request = requests.post(f"{config.url}message/senddm/v1", json = qvalid_message)
    assert valid_request.status_code == 200


def test_messagesenddm_not_member(clear_and_register4creat6):
    not_member = {'token': encode_jwt(4,0), 'dm_id' : 1, 'message': "Hola"}
    rinvalid_token = requests.post(f"{config.url}message/senddm/v1", json = not_member)
    assert rinvalid_token.status_code == 403

#########################################################################
#############################DM_MESSAGES#################################
#########################################################################

def test_dmmessages_invalid_token(clear_and_register4creat6):
    invalid_token = {'token':encode_jwt(1,1), 'dm_id':1, 'start':0}
    invalid_r = requests.get(f"{config.url}dm/messages/v1", params = invalid_token)
    assert invalid_r.status_code == 403

def test_dmmessagesend_invalid_dm(clear_and_register4creat6):
    invalid_dm = {'token':encode_jwt(1,0), 'dm_id':7, 'start':0}
    invalid_r = requests.get(f"{config.url}dm/messages/v1", params = invalid_dm)
    assert invalid_r.status_code == 400

def test_dmmessagessend_not_member(clear_and_register4creat6):
    invalid_dm = {'token':encode_jwt(4,0), 'dm_id':1, 'start':0}
    invalid_r = requests.get(f"{config.url}dm/messages/v1", params = invalid_dm)
    assert invalid_r.status_code == 403

def test_dmmessagessend_start_greater_thanlen(clear_and_register4creat6):
    invalid_dm = {'token':encode_jwt(1,0), 'dm_id':2, 'start':10}
    invalid_r = requests.get(f"{config.url}dm/messages/v1", params = invalid_dm)
    assert invalid_r.status_code == 400

def test_dmmessages_normal(clear_and_register4creat6):
    #send 51 messages
    for i in range(1, 52):
        qvalid_message = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': f"{i}ez"}
        valid_request = requests.post(f"{config.url}message/senddm/v1", json = qvalid_message)
        assert valid_request.status_code == 200
    
    valid = {'token':encode_jwt(1,0), 'dm_id':1, 'start':0}
    valid_req = requests.get(f"{config.url}dm/messages/v1", params = valid)
    assert valid_req.status_code == 200
    data = valid_req.json()
    assert len(data['messages']) == 51
    assert data['start'] == 0
    assert data['end'] == 50


def test_dmmessages_end_negative(clear_and_register4creat6):
    #send 51 messages
    for i in range(1, 30):
        qvalid_message = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': f"{i}ez"}
        valid_request = requests.post(f"{config.url}message/senddm/v1", json = qvalid_message)
        assert valid_request.status_code == 200
    
    valid = {'token':encode_jwt(1,0), 'dm_id':1, 'start':0}
    valid_req = requests.get(f"{config.url}dm/messages/v1", params = valid)
    assert valid_req.status_code == 200
    data = valid_req.json()
    assert len(data['messages']) == 29
    assert data['start'] == 0
    assert data['end'] == -1

def test_mentions(clear_and_register4creat6):
    #testing sending message user 1 send a message
    user1_message = {'token': encode_jwt(1,0), 'dm_id' : 6, 'message':"Yall reckon you can do tmrw? @andresiniesta and the amigo @suiisuii"}
    msg_request = requests.post(f"{config.url}message/senddm/v1", json=user1_message)
    assert msg_request.status_code == 200
    msg_data = msg_request.json() #returns {msg:msgid}
    assert msg_data['message_id'] == 1


def test_dmmessages_is_react_true(clear_and_register4creat6):
    #send 51 messages
    for i in range(1, 52):
        qvalid_message = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': f"{i}ez"}
        valid_request = requests.post(f"{config.url}message/senddm/v1", json = qvalid_message)
        assert valid_request.status_code == 200
    #user 1 reacts
    for i in range(1, 52):
        user1_react = {'token': encode_jwt(1,0), 'message_id': i,'react_id': 1}
        user1_reaction = requests.post(f"{config.url}message/react/v1", json=user1_react)
        assert user1_reaction.status_code == 200
        user1_data = user1_reaction.json()
        assert user1_data == {}

    valid = {'token':encode_jwt(1,0), 'dm_id':1, 'start':0}
    valid_req = requests.get(f"{config.url}dm/messages/v1", params = valid)
    assert valid_req.status_code == 200
    data = valid_req.json()
    assert len(data['messages']) == 51
    assert data['start'] == 0
    assert data['end'] == 50

def test_dmmessages_is_react_unreacting(clear_and_register4creat6):
    #send 51 messages
    for i in range(1, 52):
        qvalid_message = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': f"{i}ez"}
        valid_request = requests.post(f"{config.url}message/senddm/v1", json = qvalid_message)
        assert valid_request.status_code == 200
    #user 1 reacts
    for i in range(1, 52):
        user1_react = {'token': encode_jwt(1,0), 'message_id': i,'react_id': 1}
        user1_reaction = requests.post(f"{config.url}message/react/v1", json=user1_react)
        assert user1_reaction.status_code == 200
        user1_data = user1_reaction.json()
        assert user1_data == {}

    valid = {'token':encode_jwt(1,0), 'dm_id':1, 'start':0}
    valid_req = requests.get(f"{config.url}dm/messages/v1", params = valid)
    assert valid_req.status_code == 200
    data = valid_req.json()
    assert len(data['messages']) == 51
    assert data['start'] == 0
    assert data['end'] == 50

    #user 1 unreacts
    for i in range(1, 52):
        user1_react = {'token': encode_jwt(1,0), 'message_id': i,'react_id': 1}
        user1_reaction = requests.post(f"{config.url}message/unreact/v1", json=user1_react)
        assert user1_reaction.status_code == 200
        user1_data = user1_reaction.json()
        assert user1_data == {}
        
    valid = {'token':encode_jwt(1,0), 'dm_id':1, 'start':0}
    valid_req = requests.get(f"{config.url}dm/messages/v1", params = valid)
    assert valid_req.status_code == 200
    data = valid_req.json()
    assert len(data['messages']) == 51
    assert data['start'] == 0
    assert data['end'] == 50