import pytest
import requests
import json
from src import config
from src.helpers import generate_jwt, decode_jwt, encode_jwt
#from src.user import user_profile
from src.error import InputError, AccessError
from src.data_store import data_store
import jwt
from src.helpers import hash, generate_jwt, decode_jwt

user_1 =  {
            "email": "osama2as820sadas02@gmail.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "Osama",
            "name_last": "Almabrouk"
            }
user_2 =  {
            "email": "1osama2as820sadas02@gmail.com",
            "password": "1dasdasdasdlakmLN",
            "name_first": "Osama",
            "name_last": "Almabrouk"
            }
user_2_login =  {"email": "1osama2as820sadas02@gmail.com", "password": "1dasdasdasdlakmLN"}
user_3 =  {
            "email": "2osama2as820sadas02@gmail.com",
            "password": "2dasdasdasdlakmLN",
            "name_first": "Osama",
            "name_last": "Almabrouk"
            }
user_4 = {
            "email": "lily.lixin1990@gmail.com",
            "password": "1234asdf",
            "name_first": "Xin",
            "name_last": "Li"
            }
user_4_login = {"email": "lily.lixin1990@gmail.com", "password": "1234asdf"}

@pytest.fixture
def clear_users():
    response_del = requests.delete(f"{config.url}clear/v1")
    assert response_del.status_code == 200

#########################################################################
#########################USER_REMOVE_TESTS###############################
#########################################################################
  
def test_user_remove_correct_basic(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json=user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json=user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    uid_2 = r2_data['auth_user_id']
    uid_3 = r3_data['auth_user_id']
    
    delete_2 = {'token': token1, 'u_id': uid_2}
    delete_3 = {'token': token1, 'u_id': uid_3} 
    userdelete_2 = requests.delete(f'{config.url}admin/user/remove/v1', json=delete_2)
    assert userdelete_2.status_code == 200
    userdelete_3 = requests.delete(f'{config.url}admin/user/remove/v1', json=delete_3)
    assert userdelete_3.status_code == 200


# user been removed cannot do anything
def test_user_remove_afterremove(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json=user_2)
    r1_data = register1.json()
    r2_data = register2.json()
    token1 = r1_data['token']
    token2 = r2_data['token']
    uid_2 = r2_data['auth_user_id']
    #print(uid_2)
    delete_2 = {'token': token1, 'u_id': uid_2}
    userdelete_2 = requests.delete(f'{config.url}admin/user/remove/v1', json=delete_2)
    assert userdelete_2.status_code == 200
    
    response_login = requests.post(f"{config.url}auth/login/v2", json=user_2_login)
    assert response_login.status_code == 400
    
    channel_1 = {"token": token2,"name": "UNSW_Discussions","is_public": True}
    create_channel_1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_channel_1.status_code == 403
    dm_1 = {"token": token2,"u_ids": [1]}
    create_dm_1 = requests.post(f"{config.url}dm/create/v1", json=dm_1)
    assert create_dm_1.status_code == 403

#test after implement of userpermission
def test_user_remove_correct_globle(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json=user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json=user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    #token2 = r2_data['token']
    #token3 = r3_data['token']
    #uid_1 = r1_data['auth_user_id']
    uid_2 = r2_data['auth_user_id']
    uid_3 = r3_data['auth_user_id']
    
    permission_2 = {'token':token1, 'u_id': uid_2, 'permission_id': 1}
    permission_3 = {'token':token1, 'u_id': uid_3, 'permission_id': 1}
    change_2 = requests.post(f'{config.url}admin/userpermission/change/v1', json=permission_2)
    assert change_2 .status_code == 200
    change_3 = requests.post(f'{config.url}admin/userpermission/change/v1', json=permission_3)
    assert change_3 .status_code == 200
    
    delete_2 = {'token': token1, 'u_id': uid_2}
    delete_3 = {'token': token1, 'u_id': uid_3}   
    userdelete_2 = requests.delete(f'{config.url}admin/user/remove/v1', json=delete_2)
    assert userdelete_2 .status_code == 200
    userdelete_3 = requests.delete(f'{config.url}admin/user/remove/v1', json=delete_3)
    assert userdelete_3.status_code == 200
    '''
    assert user_profile(uid_2) = {
                'u_id': uid_2,
                'email': r2_data['email'],
                'name_first': 'Removed',
                'name_last': 'user',
                'handle_str': r2_data['handle_str']
        }
    assert user_profile(uid_3) = {
                'u_id': uid_3,
                'email': r3_data['email'],
                'name_first': 'Removed',
                'name_last': 'user',
                'handle_str': r3_data['handle_str']
        }
    '''
   
def test_user_remove_wrong_notglobleuser(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json=user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json=user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token2 = r2_data['token']
    token3 = r3_data['token']
    uid_1 = r1_data['auth_user_id']
    uid_2 = r2_data['auth_user_id']
    uid_3 = r3_data['auth_user_id']
    delete_1 = {'token': token2, 'u_id': uid_1}
    delete_2 = {'token': token3, 'u_id': uid_2}
    delete_3 = {'token': token3, 'u_id': uid_3}
    
    userdelete_1 = requests.delete(f'{config.url}admin/user/remove/v1', json=delete_1)
    assert userdelete_1.status_code == 403
    userdelete_2 = requests.delete(f'{config.url}admin/user/remove/v1', json=delete_2)
    assert userdelete_2.status_code == 403
    userdelete_3 = requests.delete(f'{config.url}admin/user/remove/v1', json=delete_3)
    assert userdelete_3.status_code == 403   

def test_user_remove_wrong_notvaliduser(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    r1_data = register1.json()  
    token1 = r1_data['token']
    uid_2 = 4
    uid_3 = 5
    delete_2 = {'token': token1, 'u_id': uid_2}
    delete_3 = {'token': token1, 'u_id': uid_3}
    
    userdelete_2 = requests.delete(f'{config.url}admin/user/remove/v1', json=delete_2)
    assert userdelete_2.status_code == 400
    userdelete_3 = requests.delete(f'{config.url}admin/user/remove/v1', json=delete_3)
    assert userdelete_3.status_code == 400

def test_user_remove_wrong_onlyglobleuser(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    r1_data = register1.json() 
    token1 = r1_data['token']
    uid_1 = r1_data['auth_user_id']
    delete_1 = {'token': token1, 'u_id': uid_1}
    
    userdelete_1 = requests.delete(f'{config.url}admin/user/remove/v1', json=delete_1)
    assert userdelete_1 .status_code == 400 
    
def test_user_remove_correct_channelmember(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json=user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json=user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    token2 = r2_data['token']
    uid_2 = r2_data['auth_user_id']
    uid_3 = r3_data['auth_user_id']
    
    channel_1 = {"token": token1,"name": "Channel1","is_public": True}
    create_ch1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_ch1.status_code == 200
    
    ch1_u2 = {"token" : encode_jwt(1,0), "channel_id": 1, "u_id":2}
    added_ch1_u2 = requests.post(f"{config.url}channel/invite/v2", json=ch1_u2)
    assert added_ch1_u2.status_code == 200
    ch1_u3 = {"token" : encode_jwt(1,0), "channel_id": 1, "u_id":3}
    added_ch1_u3 = requests.post(f"{config.url}channel/invite/v2", json=ch1_u3)
    assert added_ch1_u3.status_code == 200
    
    ch1_send = {'token': token2, 'channel_id': 1, 'message': "hello"}
    message_2 = requests.post(f"{config.url}message/send/v1", json=ch1_send)
    assert message_2.status_code == 200
    
    delete_2 = {'token': token1, 'u_id': uid_2}
    delete_3 = {'token': token1, 'u_id': uid_3}   
    userdelete_2 = requests.delete(f'{config.url}admin/user/remove/v1', json=delete_2)
    assert userdelete_2 .status_code == 200
    userdelete_3 = requests.delete(f'{config.url}admin/user/remove/v1', json=delete_3)
    assert userdelete_3.status_code == 200


def test_user_remove_invalid_token(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json=user_2)
    assert register1.status_code == 200
    assert register2.status_code == 200
    invalid_session = {'token': encode_jwt(1,1), 'u_id': 2}
    invalid_id = {'token': encode_jwt(3,0), 'u_id': 2}   

    rinvalid_session = requests.delete(f'{config.url}admin/user/remove/v1', json=invalid_session)
    assert rinvalid_session .status_code == 403
    rinvalid_id = requests.delete(f'{config.url}admin/user/remove/v1', json=invalid_id)
    assert rinvalid_id.status_code == 403

def test_user_remove_all(clear_users):
    #register 3 users:
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json=user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json=user_3)
    assert register1.status_code == 200
    assert register2.status_code == 200
    assert register3.status_code == 200
    #make 2 channels:
    channel_1 = {"token": encode_jwt(1,0),"name": "Channel1","is_public": True}
    create_ch1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_ch1.status_code == 200

    channel_2 = {"token": encode_jwt(2,0),"name": "Channel2","is_public": False}
    create_ch2 = requests.post(f"{config.url}channels/create/v2", json=channel_2)
    assert create_ch2.status_code == 200
    
    ch1_u2 = {"token" : encode_jwt(1,0), "channel_id": 1, "u_id":2}
    added_ch1_u2 = requests.post(f"{config.url}channel/invite/v2", json=ch1_u2)
    assert added_ch1_u2.status_code == 200
    ch1_u3 = {"token" : encode_jwt(1,0), "channel_id": 1, "u_id":3}
    added_ch1_u3 = requests.post(f"{config.url}channel/invite/v2", json=ch1_u3)
    assert added_ch1_u3.status_code == 200

    u1_ch2 = {"token" : encode_jwt(1,0), "channel_id" : 2}
    ru1_ch2 = requests.post(f"{config.url}channel/join/v2", json=u1_ch2)
    assert ru1_ch2.status_code == 200

    #make 2 dms: one by user3 and one by user1 - all members
    dm1 = {'token':encode_jwt(1,0), 'u_ids':[2,3]}
    dm2 = {'token':encode_jwt(2,0), 'u_ids':[1]}

    dm1_create = requests.post(f"{config.url}dm/create/v1", json=dm1)
    assert dm1_create.status_code == 200
    dm1_data = dm1_create.json()
    assert dm1_data['dm_id'] == 1

    dm2_create = requests.post(f"{config.url}dm/create/v1", json=dm2)
    assert dm2_create.status_code == 200
    dm2_data = dm2_create.json()
    assert dm2_data['dm_id'] == 2

    
    #message in 1 channel and one in each dm (all by user2)
    user2_message = {'token': encode_jwt(2,0), 'channel_id' : 1, 'message':"hey guys"}
    msg_request2 = requests.post(f"{config.url}message/send/v1", json=user2_message)
    assert msg_request2.status_code == 200
    msg_data2 = msg_request2.json()
    assert msg_data2['message_id'] == 1

    dm_msg1 = {'token': encode_jwt(2,0), 'dm_id' : 1, 'message': 'yoo'}
    rdm_msg1 = requests.post(f"{config.url}message/senddm/v1", json=dm_msg1)
    assert rdm_msg1.status_code == 200
    dm_d1 = rdm_msg1.json()
    assert dm_d1['message_id'] == 2

    dm_msg2 = {'token': encode_jwt(2,0), 'dm_id' : 2, 'message': 'ayee'}
    rdm_msg2 = requests.post(f"{config.url}message/senddm/v1", json=dm_msg2)
    assert rdm_msg2.status_code == 200
    dm_d2 = rdm_msg2.json()
    assert dm_d2['message_id'] == 3
   
    #message in 1 channel and one in each dm (user1)
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 1, 'message':"hey guys"}
    msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
    assert msg_request.status_code == 200
    msg_data = msg_request.json()
    assert msg_data['message_id'] == 4

    dm2_msg1 = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': 'yoo'}
    rdm2_msg1 = requests.post(f"{config.url}message/senddm/v1", json=dm2_msg1)
    assert rdm2_msg1.status_code == 200
    dm2_d1 = rdm2_msg1.json()
    assert dm2_d1['message_id'] == 5

    dm2_msg2 = {'token': encode_jwt(1,0), 'dm_id' : 2, 'message': 'ayee'}
    rdm2_msg2 = requests.post(f"{config.url}message/senddm/v1", json=dm2_msg2)
    assert rdm2_msg2.status_code == 200
    dm2_d2 = rdm2_msg2.json()
    assert dm2_d2['message_id'] == 6

    #ask user1 to remove user2
    valid_remove = {'token': encode_jwt(1,0), 'u_id': 2}   
    request_remove = requests.delete(f'{config.url}admin/user/remove/v1', json=valid_remove)
    assert request_remove .status_code == 200

    valid_remove2 = {'token': encode_jwt(1,0), 'u_id': 3}   
    request_remove2 = requests.delete(f'{config.url}admin/user/remove/v1', json=valid_remove2)
    assert request_remove2 .status_code == 200



#########################################################################
########################USERPERMISSION_TESTS#############################
#########################################################################
##### result been tested in functions as white box test and it works#####

def test_userpermission_correct_basic_p1(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json=user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json=user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    uid_2 = r2_data['auth_user_id']
    uid_3 = r3_data['auth_user_id']
    
    permission_2 = {'token': token1, 'u_id': uid_2, 'permission_id':1}
    permission_3 = {'token': token1, 'u_id': uid_3, 'permission_id':1} 
    changepermission_2 = requests.post(f'{config.url}admin/userpermission/change/v1', json=permission_2)
    assert changepermission_2.status_code == 200
    changepermission_3 = requests.post(f'{config.url}admin/userpermission/change/v1', json=permission_3)
    assert changepermission_3.status_code == 200
    

def test_userpermission_correct_basic_p2(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json=user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json=user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    uid_2 = r2_data['auth_user_id']
    uid_3 = r3_data['auth_user_id']
    
    permission_2_1 = {'token': token1, 'u_id': uid_2, 'permission_id':1}
    permission_3_1 = {'token': token1, 'u_id': uid_3, 'permission_id':1} 
    changepermission_2_1 = requests.post(f'{config.url}admin/userpermission/change/v1', json=permission_2_1)
    assert changepermission_2_1.status_code == 200
    changepermission_3_1 = requests.post(f'{config.url}admin/userpermission/change/v1', json=permission_3_1)
    assert changepermission_3_1.status_code == 200
    
    permission_2_2 = {'token': token1, 'u_id': uid_2, 'permission_id':2}
    permission_3_2 = {'token': token1, 'u_id': uid_3, 'permission_id':2}
    changepermission_2_2 = requests.post(f'{config.url}admin/userpermission/change/v1', json=permission_2_2)
    assert changepermission_2_2.status_code == 200
    changepermission_3_2 = requests.post(f'{config.url}admin/userpermission/change/v1', json=permission_3_2)
    assert changepermission_3_2.status_code == 200

    
def test_userpermission_wrong_onlyglobaluser(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    r1_data = register1.json()  
    token1 = r1_data['token']
    uid_1 = r1_data['auth_user_id']
    permission_1_1 = {'token': token1, 'u_id': uid_1, 'permission_id':1}
    permission_1_2 = {'token': token1, 'u_id': uid_1, 'permission_id':2}
    
    changepermission_1_1 = requests.post(f'{config.url}admin/user/remove/v1', json=permission_1_1)
    assert changepermission_1_1.status_code == 405
    changepermission_1_2 = requests.post(f'{config.url}admin/user/remove/v1', json=permission_1_2)
    assert changepermission_1_2.status_code == 405


def test_userpermission_wrong_notvaliduser(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    r1_data = register1.json()  
    token1 = r1_data['token']
    uid_2 = 4
    uid_3 = 5
    permission_2 = {'token': token1, 'u_id': uid_2, 'permission_id':1}
    permission_3 = {'token': token1, 'u_id': uid_3, 'permission_id':2}
    
    changepermission_2 = requests.post(f'{config.url}admin/user/remove/v1', json=permission_2)
    assert changepermission_2.status_code == 405
    changepermission_3 = requests.post(f'{config.url}admin/user/remove/v1', json=permission_3)
    assert changepermission_3.status_code == 405


def test_userpermission_wrong_notglobaluser(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json=user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json=user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token2 = r2_data['token']
    token3 = r3_data['token']
    uid_1 = r1_data['auth_user_id']
    uid_2 = r2_data['auth_user_id']
    
    permission_2to1 = {'token': token2, 'u_id': uid_1, 'permission_id':1}
    permission_3to2 = {'token': token3, 'u_id': uid_2, 'permission_id':2} 
    changepermission_2to1 = requests.post(f'{config.url}admin/userpermission/change/v1', json=permission_2to1)
    assert changepermission_2to1.status_code == 403
    changepermission_3to2 = requests.post(f'{config.url}admin/userpermission/change/v1', json=permission_3to2)
    assert changepermission_3to2.status_code == 403
    
    
def test_userpermission_wrong_invalidpermissionid(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json=user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json=user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()   
    token1 = r1_data['token']
    uid_2 = r2_data['auth_user_id']
    uid_3 = r3_data['auth_user_id']
    
    permission_2 = {'token': token1, 'u_id': uid_2, 'permission_id':3}
    permission_3 = {'token': token1, 'u_id': uid_3, 'permission_id':0} 
    changepermission_2 = requests.post(f'{config.url}admin/userpermission/change/v1', json=permission_2)
    assert changepermission_2.status_code == 400
    changepermission_3 = requests.post(f'{config.url}admin/userpermission/change/v1', json=permission_3)
    assert changepermission_3.status_code == 400


def test_invalid_token(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    register2 = requests.post(f'{config.url}auth/register/v2', json=user_2)
    register3 = requests.post(f'{config.url}auth/register/v2', json=user_3)
    assert register1.status_code == 200
    assert register2.status_code == 200
    assert register3.status_code == 200
    token1 = encode_jwt(1,1)
    token4 = encode_jwt(4,0)
    
    invalid_sessionid = {'token': token1, 'u_id': 2, 'permission_id':3}
    invalid_authid = {'token': token4, 'u_id': 3, 'permission_id':0} 
    changepermission_2 = requests.post(f'{config.url}admin/userpermission/change/v1', json=invalid_sessionid)
    assert changepermission_2.status_code == 403
    changepermission_3 = requests.post(f'{config.url}admin/userpermission/change/v1', json=invalid_authid)
    assert changepermission_3.status_code == 403


def test_userpermission_uid_onlyglobal(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    assert register1.status_code == 200
    token1 = encode_jwt(1,0)
    invalid_request = {'token': token1, 'u_id': 1, 'permission_id':2}
    changepermission_1 = requests.post(f'{config.url}admin/userpermission/change/v1', json=invalid_request)
    assert changepermission_1.status_code == 400
    register2 = requests.post(f'{config.url}auth/register/v2', json=user_2)
    assert register2.status_code == 200
    change_to_admin = {'token': encode_jwt(1,0), 'u_id': 2, 'permission_id':1}
    changepermission_2 = requests.post(f'{config.url}admin/userpermission/change/v1', json=change_to_admin)
    assert changepermission_2.status_code == 200


    invalid_authid = {'token': encode_jwt(1,0), 'u_id': 1, 'permission_id':2}
    changepermission_3 = requests.post(f'{config.url}admin/userpermission/change/v1', json=invalid_authid)
    assert changepermission_3.status_code == 200

def test_userpermission_invalid_uid(clear_users):
    register1 = requests.post(f'{config.url}auth/register/v2', json=user_1)
    assert register1.status_code == 200
    token1 = encode_jwt(1,0)
    invalid_request = {'token': token1, 'u_id': 2, 'permission_id':2}
    changepermission_1 = requests.post(f'{config.url}admin/userpermission/change/v1', json=invalid_request)
    assert changepermission_1.status_code == 400

#########################################################################
######################PASSWORDRESET_REQUEST_TESTS########################
#########################################################################

def test_passwordreset_request_basic(clear_users):
    register4 = requests.post(f'{config.url}auth/register/v2', json=user_4)
    assert register4.status_code == 200
    
    email = user_4['email']
    email = {'email': email}
    pw_request = requests.post(f'{config.url}auth/passwordreset/request/v1', json=email)
    assert pw_request.status_code == 200
    
def test_passwordreset_request_wrongfomat(clear_users):
    register4 = requests.post(f'{config.url}auth/register/v2', json=user_4)
    assert register4.status_code == 200
    
    email = 'a123!asd'
    email = {'email': email}
    pw_request = requests.post(f'{config.url}auth/passwordreset/request/v1', json=email)
    assert pw_request.status_code == 400

# no error raised due to security/privacy concern, should not send email to entered email address
def test_passwordreset_request_invalidemail(clear_users):
    register4 = requests.post(f'{config.url}auth/register/v2', json=user_4)
    assert register4.status_code == 200
    
    email = '1457055131@qq.com'
    email = {'email': email}
    pw_request = requests.post(f'{config.url}auth/passwordreset/request/v1', json=email)
    assert pw_request.status_code == 200

def test_passwordreset_request_logout(clear_users):
    register4 = requests.post(f'{config.url}auth/register/v2', json=user_4)
    assert register4.status_code == 200
    #data = register4.json()   
    #token = data['token']
    
    response_login = requests.post(f"{config.url}auth/login/v2", json=user_4_login)
    assert response_login.status_code == 200
    data = response_login.json()   
    token = data['token']
    
    email = user_4['email']
    email = {'email': email}
    pw_request2 = requests.post(f'{config.url}auth/passwordreset/request/v1', json=email)
    assert pw_request2.status_code == 200
    
    # invalid token, should not be able to create channel without login
    channel_1 = {"token": token,"name": "UNSW_Discussions","is_public": True}
    create_channel_1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_channel_1.status_code == 403
    
    response_login2 = requests.post(f"{config.url}auth/login/v2", json=user_4_login)
    assert response_login2.status_code == 200
    #data = response_login2.json()   
    #token = data['token']

#########################################################################
#######################PASSWORDRESET_RESET_TESTS#########################
#########################################################################
  
def test_passwordreset_reset_invalidpw(clear_users):
    register4 = requests.post(f'{config.url}auth/register/v2', json=user_4)
    assert register4.status_code == 200
    
    email = user_4['email']
    email = {'email': email}
    pw_request = requests.post(f'{config.url}auth/passwordreset/request/v1', json=email)
    assert pw_request.status_code == 200
    
    reset = {'reset_code': 123, 'new_password': '789'}
    pw_reset = requests.post(f'{config.url}auth/passwordreset/reset/v1', json=reset)
    assert pw_reset.status_code == 400
      
def test_passwordreset_reset_wongresetcode(clear_users):
    register4 = requests.post(f'{config.url}auth/register/v2', json=user_4)
    assert register4.status_code == 200
    
    email = user_4['email']
    email = {'email': email}
    pw_request = requests.post(f'{config.url}auth/passwordreset/request/v1', json=email)
    assert pw_request.status_code == 200
    
    reset = {'reset_code': 13, 'new_password': '789poiu'}
    pw_reset = requests.post(f'{config.url}auth/passwordreset/reset/v1', json=reset)
    assert pw_reset.status_code == 400

#########################################################################
#######################PASSWORDRESET_RESET_TESTS#########################
#########################################################################

