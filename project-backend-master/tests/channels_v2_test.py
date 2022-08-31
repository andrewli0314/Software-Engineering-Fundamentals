"""Note to self: Test all functions after finishing the logout function for invalid sessions"""
import pytest
import requests
import json

from requests.sessions import session
from src import config
from src.helpers import encode_jwt, decode_jwt

#users:
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

@pytest.fixture
def clear_and_register_one_user():
    """This will give us one registered user and already logged-in because its token is valid"""
    response_del = requests.delete(f"{config.url}clear/v1")
    assert response_del.status_code == 200
    register1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    assert register1.status_code == 200


@pytest.fixture
def clear_and_register_users():
    """This will give us three registered users and already logged-in because their tokens are valid"""
    response_del = requests.delete(f"{config.url}clear/v1")
    assert response_del.status_code == 200
    register1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    register2 = requests.post(f"{config.url}auth/register/v2", json=user_2)
    register3 = requests.post(f"{config.url}auth/register/v2", json=user_3)
    assert register1.status_code == 200
    assert register2.status_code == 200
    assert register3.status_code == 200

@pytest.fixture
def clear_and_register3_create6():
    """This will give us three registered users and already logged-in because their tokens are valid"""
    response_del = requests.delete(f"{config.url}clear/v1")
    assert response_del.status_code == 200
    register1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    register2 = requests.post(f"{config.url}auth/register/v2", json=user_2)
    register3 = requests.post(f"{config.url}auth/register/v2", json=user_3)
    r1_data = register1.json()
    r2_data = register2.json()
    token1 = r1_data['token']
    token2 = r2_data['token']
    assert register1.status_code == 200
    assert register2.status_code == 200
    assert register3.status_code == 200

    #list of channels:
    channel_1 = {"token": token1,"name": "Channel1","is_public": False}
    channel_2 = {"token": token1,"name": "Channel2","is_public": True}
    channel_3 = {"token": token1,"name": "Channel3","is_public": True}
    channel_4 = {"token": token2,"name": "Channel4","is_public": False}
    channel_5 = {"token": token1,"name": "Channel5","is_public": True}
    channel_6 = {"token": token2,"name": "Channel6","is_public": True}

    #Create 6 channels:
    create_ch1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_ch1.status_code == 200
    create_ch2 = requests.post(f"{config.url}channels/create/v2", json=channel_2)
    assert create_ch2.status_code == 200
    create_ch3 = requests.post(f"{config.url}channels/create/v2", json=channel_3)
    assert create_ch3.status_code == 200
    create_ch4 = requests.post(f"{config.url}channels/create/v2", json=channel_4)
    assert create_ch4.status_code == 200
    create_ch5 = requests.post(f"{config.url}channels/create/v2", json=channel_5)
    assert create_ch5.status_code == 200
    create_ch6 = requests.post(f"{config.url}channels/create/v2", json=channel_6)
    assert create_ch6.status_code == 200

#########################################################################
#########################CHANNELS_CREATE_TEST############################
#########################################################################

# Normal Tests:
def test_create_one_channel(clear_and_register_one_user):
    #we know that users 1, 2, and 3 are registered, a token is made:
    token1 = encode_jwt(1, 0)
    channel_1 = {"token": token1,"name": "UNSW_Discussions","is_public": True}
    create_channel_1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_channel_1.status_code == 200

def test_multiple_channels(clear_and_register_users):
    """Register multiple users, and make 4 channels. Must return 200 Always"""
    token1 = encode_jwt(1, 0)
    token2 = encode_jwt(2, 0)
    token3 = encode_jwt(3, 0)
    channel_1 = {"token": token1,"name": "Channel 1","is_public": True}
    channel_2 = {"token": token2,"name": "Channel 2","is_public": False}
    channel_3 = {"token": token3,"name": "Channel 3","is_public": True}
    channel_4 = {"token": token1,"name": "Channel 4","is_public": True}

    create_channel_1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_channel_1.status_code == 200
    create_channel_1_data = create_channel_1.json()
    assert create_channel_1_data['channel_id'] == 1

    create_channel_2 = requests.post(f"{config.url}channels/create/v2", json=channel_2)
    assert create_channel_2.status_code == 200
    create_channel_2_data = create_channel_2.json()
    assert create_channel_2_data['channel_id'] == 2
    
    create_channel_3 = requests.post(f"{config.url}channels/create/v2", json=channel_3)
    assert create_channel_3.status_code == 200
    create_channel_3_data = create_channel_3.json()
    assert create_channel_3_data['channel_id'] == 3

    create_channel_4 = requests.post(f"{config.url}channels/create/v2", json=channel_4)
    assert create_channel_4.status_code == 200
    create_channel_4_data = create_channel_4.json()
    assert create_channel_4_data['channel_id'] == 4

    
def test_short_name(clear_and_register_one_user):
    """Tests short channel names"""
    token1 = encode_jwt(1, 0)
    channel_1 = {"token": token1,"name": "","is_public": True}
    create_channel_1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_channel_1.status_code == 400

def test_long_name(clear_and_register_one_user):
    """Tests Long channel names"""
    token1 = encode_jwt(1, 0)
    channel_1 = {"token": token1,"name": "aaaaaaaaaaaaaaaaaaaaa","is_public": True}
    create_channel_1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_channel_1.status_code == 400


def test_invalid_auth_id(clear_and_register_one_user):
    """Expects E403 for an invalid auth_id"""
    token1 = encode_jwt(1, 0)
    token_invalid = encode_jwt(2, 0)
    channel_1 = {"token": token_invalid,"name": "Channel1","is_public": True}
    create_channel_1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_channel_1.status_code == 403

    #create a valid channel to make sure it works
    valid_channel = {"token": token1,"name": "Channel1","is_public": True}
    channel_valid = requests.post(f"{config.url}channels/create/v2", json=valid_channel)
    assert channel_valid.status_code == 200
    channel_valid_data = channel_valid.json()
    assert channel_valid_data['channel_id'] == 1

def test_invalid_session_id(clear_and_register_one_user):
    """Expects E403 for an invalid session"""
    token1 = encode_jwt(1, 0)
    token_invalid = encode_jwt(1, 1)
    channel_1 = {"token": token_invalid,"name": "Channel1","is_public": True}
    create_channel_1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_channel_1.status_code == 403

    #create a valid channel to make sure it works
    valid_channel = {"token": token1,"name": "Channel1","is_public": True}
    channel_valid = requests.post(f"{config.url}channels/create/v2", json=valid_channel)
    assert channel_valid.status_code == 200
    channel_valid_data = channel_valid.json()
    assert channel_valid_data['channel_id'] == 1

def test_ivalid_after_logout(clear_and_register_one_user):
    #login with u1 twice, and assert 403 for logging out w session 0 and 1
    #this way, we have session id's of 0, 1, and 2.
    
    #login1
    u1_login = {"email": "osama2as820sadas02@gmail.com", "password": "dasdasdasdlakmLN"}
    login1 = requests.post(f"{config.url}auth/login/v2", json=u1_login)
    data1 = login1.json()
    assert data1['auth_user_id'] == 1
    assert data1['token'] == encode_jwt(1, 1)
    
    #login2
    login2 = requests.post(f"{config.url}auth/login/v2", json=u1_login)
    data2 = login2.json()
    assert data2['auth_user_id'] == 1
    assert data2['token'] == encode_jwt(1, 2)
    
    #check that no error is returned first:
    token0 = encode_jwt(1,0)
    token1 = data1['token']
    token2 = data2['token']
    channel_1 = {"token": token0,"name": "Channel1","is_public": True}
    create_channel_1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_channel_1.status_code == 200
    channel_2 = {"token": token1,"name": "Channel2","is_public": True}
    create_channel_2 = requests.post(f"{config.url}channels/create/v2", json=channel_2)
    assert create_channel_2.status_code == 200

    channel_3 = {"token": token2,"name": "Channel1","is_public": True}
    create_channel_3 = requests.post(f"{config.url}channels/create/v2", json=channel_3)
    assert create_channel_3.status_code == 200
    #now, logout token 0 and 1, then assert:

    #logout session 0:
    logout0 = {'token': encode_jwt(1,0)}
    requests.post(f"{config.url}auth/logout/v1", json=logout0)
    channel_4 = {"token": encode_jwt(1,0),"name": "Channel4","is_public": True}
    create_channel_4 = requests.post(f"{config.url}channels/create/v2", json=channel_4)
    assert create_channel_4.status_code == 403

    logout1 = {'token': token1}
    requests.post(f"{config.url}auth/logout/v1", json=logout1)
    channel_5 = {"token": token1,"name": "Channel4","is_public": True}
    create_channel_5 = requests.post(f"{config.url}channels/create/v2", json=channel_5)
    assert create_channel_5.status_code == 403

    channel_6 = {"token": token2,"name": "Channel6","is_public": True}
    create_channel_6 = requests.post(f"{config.url}channels/create/v2", json=channel_6)
    assert create_channel_6.status_code == 200
    
#########################################################################
#########################CHANNELS_CREATE_TEST############################
#########################################################################


#########################################################################
#########################CHANNELS_LIST_TEST##############################
#########################################################################
def test_channels_list_one_user(clear_and_register3_create6):
    u_1 = {"token": encode_jwt(1, 0)}
    u_2 = {"token": encode_jwt(2, 0)}
    u_3 = {"token": encode_jwt(3, 0)}

    #Test if it data obtained is true:
    channels_list_1 = requests.get(f"{config.url}channels/list/v2", params=u_1)
    assert channels_list_1.status_code == 200
    data_1 = channels_list_1.json()
    # channel_id, name
    assert data_1['channels'] == [
        {'channel_id':1, 'name':'Channel1'},
        {'channel_id':2, 'name':'Channel2'},  
        {'channel_id':3, 'name':'Channel3'}, 
        {'channel_id':5, 'name':'Channel5'}, 
        ]
    

    channels_list_2 = requests.get(f"{config.url}channels/list/v2", params=u_2)
    assert channels_list_2.status_code == 200
    data_2 = channels_list_2.json()
    # channel_id, name
    assert data_2['channels'] == [
        {'channel_id':4, 'name':'Channel4'},
        {'channel_id':6, 'name':'Channel6'},  
        ]


    channels_list_3 = requests.get(f"{config.url}channels/list/v2", params=u_3)
    assert channels_list_3.status_code == 200
    data_3 = channels_list_3.json()
    assert data_3['channels'] == []

def test_channels_invalid_token(clear_and_register_one_user):
    token1 = encode_jwt(1, 0)
    token_invalid = encode_jwt(1,1)
    channel_1 = {"token": token1,"name": "UNSW_Discussions","is_public": True}
    create_channel_1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_channel_1.status_code == 200

    #Checking phase, has to return a list
    u_1 = {"token" : token1}
    list_true = requests.get(f"{config.url}channels/list/v2", params=u_1)
    assert list_true.status_code == 200
    list_data = list_true.json()
    assert list_data['channels'] == [{'channel_id':1, 'name':'UNSW_Discussions'}]
    
    #checking #2, has to raise 403
    u_invalid = {"token":token_invalid}
    list_false = requests.get(f"{config.url}channels/list/v2", params=u_invalid)
    assert list_false.status_code == 403

def test_channels_list_and_join(clear_and_register3_create6):
    u_1 = {"token": encode_jwt(1, 0)}

    #join channels 4, and 6:
    u1_ch4 = {"token" : encode_jwt(1,0), "channel_id" : 4}
    u1_ch6 = {"token" : encode_jwt(1,0), "channel_id" : 6}
    ru1_ch4 = requests.post(f"{config.url}channel/join/v2", json=u1_ch4)
    assert ru1_ch4.status_code == 200
    ru1_ch6 = requests.post(f"{config.url}channel/join/v2", json=u1_ch6)
    assert ru1_ch6.status_code == 200
    #Test if it data obtained is true:
    channels_list_1 = requests.get(f"{config.url}channels/list/v2", params=u_1)
    assert channels_list_1.status_code == 200
    data_1 = channels_list_1.json()
    # channel_id, name
    assert data_1['channels'] == [
        {'channel_id':1, 'name':'Channel1'},
        {'channel_id':2, 'name':'Channel2'},  
        {'channel_id':3, 'name':'Channel3'}, 
        {'channel_id':4, 'name':'Channel4'},
        {'channel_id':5, 'name':'Channel5'},
        {'channel_id':6, 'name':'Channel6'}, 
        ]

def test_channels_list_invite(clear_and_register3_create6):
    #user 1 invites user 3, then user 3 joins another channel
    u1_ch2_u2 = {"token" : encode_jwt(1,0), "channel_id" : 2, "u_id":3}
    ru1_ch2_u2 = requests.post(f"{config.url}channel/invite/v2", json=u1_ch2_u2)
    assert ru1_ch2_u2.status_code == 200

    #ch3 joins ch6
    u3_ch6 = {"token" : encode_jwt(3,0), "channel_id" : 6}
    ru3_ch6 = requests.post(f"{config.url}channel/join/v2", json=u3_ch6)
    assert ru3_ch6.status_code == 200

    #check channels_list:
    u_3 = {"token" : encode_jwt(3,0)}
    channels_list_3 = requests.get(f"{config.url}channels/list/v2", params=u_3)
    assert channels_list_3.status_code == 200
    data = channels_list_3.json()
    # channel_id, name
    assert data['channels'] == [
        {'channel_id':2, 'name':'Channel2'},  
        {'channel_id':6, 'name':'Channel6'}, 
        ]

    #join channel 5
    u3_ch5 = {"token" : encode_jwt(3,0), "channel_id" : 5}
    ru3_ch5 = requests.post(f"{config.url}channel/join/v2", json=u3_ch5)
    assert ru3_ch5.status_code == 200

    #check again
    channels_list_3 = requests.get(f"{config.url}channels/list/v2", params=u_3)
    assert channels_list_3.status_code == 200
    data = channels_list_3.json()
    # channel_id, name
    assert data['channels'] == [
        {'channel_id':2, 'name':'Channel2'},  
        {'channel_id':5, 'name':'Channel5'},  
        {'channel_id':6, 'name':'Channel6'}, 
        ]
#########################################################################
#########################CHANNELS_LIST_TEST##############################
#########################################################################


#########################################################################
######################CHANNELS_LISTALL_TEST##############################
#########################################################################
def test_listall_all_users(clear_and_register3_create6):
    u_1 = {"token": encode_jwt(1, 0)}
    u_2 = {"token": encode_jwt(2, 0)}
    u_3 = {"token": encode_jwt(3, 0)}
    all_channels = [
        {'channel_id':1, 'name':'Channel1'},
        {'channel_id':2, 'name':'Channel2'},  
        {'channel_id':3, 'name':'Channel3'}, 
        {'channel_id':4, 'name':'Channel4'}, 
        {'channel_id':5, 'name':'Channel5'}, 
        {'channel_id':6, 'name':'Channel6'}, 
        ]
    #Test if it data obtained is true:
    channels_list_1 = requests.get(f"{config.url}channels/listall/v2", params=u_1)
    assert channels_list_1.status_code == 200
    data_1 = channels_list_1.json()
    # channel_id, name
    assert data_1['channels'] == all_channels
    
    channels_list_2 = requests.get(f"{config.url}channels/listall/v2", params=u_2)
    assert channels_list_2.status_code == 200
    data_2 = channels_list_2.json()
    # channel_id, name
    assert data_2['channels'] == all_channels

    channels_list_3 = requests.get(f"{config.url}channels/listall/v2", params=u_3)
    assert channels_list_3.status_code == 200
    data_3 = channels_list_3.json()
    assert data_3['channels'] == all_channels

def test_invalid_token(clear_and_register_one_user):
    token1 = encode_jwt(1, 0)
    token_invalid = encode_jwt(1,1)
    channel_1 = {"token": token1,"name": "UNSW_Discussions","is_public": True}
    create_channel_1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_channel_1.status_code == 200

    #Checking phase, has to return a list
    u_1 = {"token" : token1}
    list_true = requests.get(f"{config.url}channels/listall/v2", params=u_1)
    assert list_true.status_code == 200
    list_data = list_true.json()
    assert list_data['channels'] == [{'channel_id':1, 'name':'UNSW_Discussions'}]
    
    #checking #2, has to raise 403
    u_invalid = {"token":token_invalid}
    list_false = requests.get(f"{config.url}channels/listall/v2", params=u_invalid)
    assert list_false.status_code == 403

#########################################################################
######################CHANNELS_LISTALL_TEST##############################
#########################################################################

