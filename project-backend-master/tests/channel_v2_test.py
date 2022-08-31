"""Note to self: Test all functions after finishing the logout function for invalid sessions"""
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

#user1 has 1-p, 2, 3, and 5
#user2 has 4-p, 6
#user3 has nada
#aim: make user1 has access to all channels, 2 to 2-6, 3 to 2,3,5,6
u1_ch4 = {"token" : encode_jwt(1,0), "channel_id" : 4}
u1_ch6 = {"token" : encode_jwt(1,0), "channel_id" : 6}
u2_ch2 = {"token" : encode_jwt(2,0), "channel_id" : 2}
u2_ch3 = {"token" : encode_jwt(2,0), "channel_id" : 3}
u2_ch5 = {"token" : encode_jwt(2,0), "channel_id" : 5}
u3_ch2 = {"token" : encode_jwt(3,0), "channel_id" : 2}
u3_ch3 = {"token" : encode_jwt(3,0), "channel_id" : 3}
u3_ch5 = {"token" : encode_jwt(3,0), "channel_id" : 5}
u3_ch6 = {"token" : encode_jwt(3,0), "channel_id" : 6}

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
###########################CHANNEL_JOIN_TEST#############################
#########################################################################


def test_invalid_channel(clear_and_register3_create6):
    """u_id 1 wants to join ch_is 7, which is not available"""
    invalid_channel = {"token" : encode_jwt(1,0), "channel_id" : 7}
    request = requests.post(f"{config.url}channel/join/v2", json=invalid_channel)
    assert request.status_code == 400


def test_already_member(clear_and_register3_create6):
    """u_id wants to join ch_id 2, and he is already a member"""
    already_member = {"token" : encode_jwt(1,0), "channel_id" : 2}
    request = requests.post(f"{config.url}channel/join/v2", json=already_member)
    assert request.status_code == 400


def test_channel_priv_notamember_notglobal(clear_and_register3_create6):
    """u_id 2 wants to join ch_id 1 when its priv, and they're not a member not a global owner"""
    long_error = {"token" : encode_jwt(2,0), "channel_id" : 1}
    long_error2 = {"token" : encode_jwt(3,0), "channel_id" : 1}
    request = requests.post(f"{config.url}channel/join/v2", json=long_error)
    assert request.status_code == 403

    request2 = requests.post(f"{config.url}channel/join/v2", json=long_error2)
    assert request2.status_code == 403


def test_channel_join(clear_and_register3_create6):
    """Should not return any error"""
    valid_input = {"token" : encode_jwt(2,0), "channel_id" : 2}
    request = requests.post(f"{config.url}channel/join/v2", json=valid_input)
    assert request.status_code == 200

def test_channel_join_all_users(clear_and_register3_create6):
    """Test to see if all users are able to join"""
    #testing user1
    ru1_ch4 = requests.post(f"{config.url}channel/join/v2", json=u1_ch4)
    assert ru1_ch4.status_code == 200
    ru1_ch6 = requests.post(f"{config.url}channel/join/v2", json=u1_ch6)
    assert ru1_ch6.status_code == 200

    #testing user2
    ru2_ch2 = requests.post(f"{config.url}channel/join/v2", json=u2_ch2)
    assert ru2_ch2.status_code == 200
    ru2_ch3 = requests.post(f"{config.url}channel/join/v2", json=u2_ch3)
    assert ru2_ch3.status_code == 200
    ru2_ch5 = requests.post(f"{config.url}channel/join/v2", json=u2_ch5)
    assert ru2_ch5.status_code == 200

    #testing user3
    ru3_ch2 = requests.post(f"{config.url}channel/join/v2", json=u3_ch2)
    assert ru3_ch2.status_code == 200
    ru3_ch3 = requests.post(f"{config.url}channel/join/v2", json=u3_ch3)
    assert ru3_ch3.status_code == 200
    ru3_ch5 = requests.post(f"{config.url}channel/join/v2", json=u3_ch5)
    assert ru3_ch5.status_code == 200
    ru3_ch6 = requests.post(f"{config.url}channel/join/v2", json=u3_ch6)
    assert ru3_ch6.status_code == 200


def test_join_multiple_session_id(clear_and_register3_create6):
    """user 3 will have 3 sessions: 0-2, and will join using them; should return 200"""
    #Session1
    user_3_login = {"email": "someemailadressss@gmail.com", "password": "Samsoomitoz2132"}
    u3_session1 = requests.post(f"{config.url}auth/login/v2", json=user_3_login)
    u3_session1_data = u3_session1.json()
    assert u3_session1_data['auth_user_id'] == 3
    assert decode_jwt(u3_session1_data['token']) == {'u_id': 3, 'session_id': 1}

    #Session2
    u3_session2 = requests.post(f"{config.url}auth/login/v2", json=user_3_login)
    u3_session2_data = u3_session2.json()
    assert u3_session2_data['auth_user_id'] == 3
    assert decode_jwt(u3_session2_data['token']) == {'u_id': 3, 'session_id': 2}
    
    #test for invalid session as well:
    u3_ch1 = {"token" : u3_session2_data['token'], "channel_id" : 1}
    u3_ch2 = {"token" : encode_jwt(3,3), "channel_id" : 2}
    u3_ch3 = {"token" : u3_session1_data['token'], "channel_id" : 3}
    u3_ch5 = {"token" : encode_jwt(3,0), "channel_id" : 5}
    u3_ch6 = {"token" : u3_session2_data['token'], "channel_id" : 6}


    ru3_ch1 = requests.post(f"{config.url}channel/join/v2", json=u3_ch1)
    assert ru3_ch1.status_code == 403
    ru3_ch2 = requests.post(f"{config.url}channel/join/v2", json=u3_ch2)
    assert ru3_ch2.status_code == 403
    ru3_ch3 = requests.post(f"{config.url}channel/join/v2", json=u3_ch3)
    assert ru3_ch3.status_code == 200
    ru3_ch5 = requests.post(f"{config.url}channel/join/v2", json=u3_ch5)
    assert ru3_ch5.status_code == 200
    ru3_ch6 = requests.post(f"{config.url}channel/join/v2", json=u3_ch6)
    assert ru3_ch6.status_code == 200
#############################################################
###########################CHANNEL_JOIN_TEST#############################
#########################################################################










#########################################################################
#########################CHANNEL_INVITE_TEST#############################
#########################################################################
"""
INERR:
channel_id does not refer to a valid channel
u_id does not refer to a valid user
u_id refers to a user who is already a member of the channel

ACER:
channel_id is valid and the authorised user is not a member of the channel
invalid token
"""
#u1 invites u3 to ch7
def test_invalid_channel_id(clear_and_register3_create6):
    #400
    u1_u3_ch7 = {"token" : encode_jwt(1,0), "channel_id" : 7, "u_id":3}
    ru1_u3_ch7 = requests.post(f"{config.url}channel/invite/v2", json=u1_u3_ch7)
    assert ru1_u3_ch7.status_code == 400

#invalid u_id
def test_u_id_invalid(clear_and_register3_create6):
    #400
    u1_u5_ch5 = {"token" : encode_jwt(1,0), "channel_id" : 5, "u_id":5}
    ru1_u5_ch5 = requests.post(f"{config.url}channel/invite/v2", json=u1_u5_ch5)
    assert ru1_u5_ch5.status_code == 400

#u_id is already a member

def test_u_id_already_member(clear_and_register3_create6):
    #400
    #make u_3 join ch5
    u1_u3_ch5 = {"token" : encode_jwt(1,0), "channel_id" : 5, "u_id":3}
    ru3_ch5 = requests.post(f"{config.url}channel/join/v2", json=u3_ch5)
    assert ru3_ch5.status_code == 200
    #let u_1 invite u_3 to ch_5
    ru1_u3_ch5 = requests.post(f"{config.url}channel/invite/v2", json=u1_u3_ch5)
    assert ru1_u3_ch5.status_code == 400

#valid ch_id, but auth_id is not a member of the channel

def test_valid_chid_authid_not_member(clear_and_register3_create6):
    #403
    #let u_id2 invite u_id3 to ch2
    u2_u3_ch2 = {"token" : encode_jwt(2,0), "channel_id" : 2, "u_id":3}
    ru2_u3_ch2 = requests.post(f"{config.url}channel/invite/v2", json=u2_u3_ch2)
    assert ru2_u3_ch2.status_code == 403

#invalid token: auth

def test_invalid_token_auth(clear_and_register3_create6):
    #403
    u4_u3_ch5 = {"token" : encode_jwt(4,0), "channel_id" : 5, "u_id":3}
    ru4_u3_ch5 = requests.post(f"{config.url}channel/invite/v2", json=u4_u3_ch5)
    assert ru4_u3_ch5.status_code == 403

#invalid token: session

def test_invalid_token_session(clear_and_register3_create6):
    #403
    u11_u3_ch5_invalid_sid = {"token" : encode_jwt(1,1), "channel_id" : 5, "u_id":3}
    ru11_u3_ch5_invalid_sid = requests.post(f"{config.url}channel/invite/v2", json=u11_u3_ch5_invalid_sid)
    assert ru11_u3_ch5_invalid_sid.status_code == 403

#u_id1 invites u_id2 to ch2 and u_id3 to ch5
#extra: login with u_1 to see if it works

def test_invite_simple(clear_and_register3_create6):
    u1_ch2_u2 = {"token" : encode_jwt(1,0), "channel_id" : 2, "u_id":2}
    #200
    #login first
    login1 = {"email": "osama2as820sadas02@gmail.com", "password": "dasdasdasdlakmLN"}
    rlogin1 = requests.post(f"{config.url}auth/login/v2", json=login1)
    rlogin1_data = rlogin1.json()
    assert rlogin1_data['auth_user_id'] == 1
    assert decode_jwt(rlogin1_data['token']) == {'u_id': 1, 'session_id': 1}
    u1_ch2_u3 = {"token" : rlogin1_data['token'], "channel_id" : 5, "u_id":3}
    
    #test
    ru1_ch2_u2 = requests.post(f"{config.url}channel/invite/v2", json=u1_ch2_u2)
    assert ru1_ch2_u2.status_code == 200

    ru1_ch2_u3 = requests.post(f"{config.url}channel/invite/v2", json=u1_ch2_u3)
    assert ru1_ch2_u3.status_code == 200


def test_invite_2_sessions_both(clear_and_register3_create6):
    #200
    #u_1 joins all channels
    ru1_ch4 = requests.post(f"{config.url}channel/join/v2", json=u1_ch4)
    assert ru1_ch4.status_code == 200
    ru1_ch6 = requests.post(f"{config.url}channel/join/v2", json=u1_ch6)
    assert ru1_ch6.status_code == 200

    #u_1 logs in to have another session
    login1 = {"email": "osama2as820sadas02@gmail.com", "password": "dasdasdasdlakmLN"}
    rlogin1 = requests.post(f"{config.url}auth/login/v2", json=login1)
    rlogin1_data = rlogin1.json()
    assert rlogin1_data['auth_user_id'] == 1
    assert decode_jwt(rlogin1_data['token']) == {'u_id': 1, 'session_id': 1}

    #we'll do a series of invites and alternate between sessions.
    token_u1_s0 = encode_jwt(1,0)
    token_u1_s1 = rlogin1_data['token']
    ch1 = {"token" : token_u1_s0, "channel_id" : 1, "u_id":3}
    ch2 = {"token" : token_u1_s1, "channel_id" : 2, "u_id":3}
    ch3 = {"token" : token_u1_s0, "channel_id" : 3, "u_id":3}
    ch4 = {"token" : token_u1_s1, "channel_id" : 4, "u_id":3}
    ch5 = {"token" : token_u1_s0, "channel_id" : 5, "u_id":3}
    ch6 = {"token" : token_u1_s1, "channel_id" : 6, "u_id":3}
    
    #test
    rch1 = requests.post(f"{config.url}channel/invite/v2", json=ch1)
    assert rch1.status_code == 200

    rch2 = requests.post(f"{config.url}channel/invite/v2", json=ch2)
    assert rch2.status_code == 200

    rch3 = requests.post(f"{config.url}channel/invite/v2", json=ch3)
    assert rch3.status_code == 200

    rch4 = requests.post(f"{config.url}channel/invite/v2", json=ch4)
    assert rch4.status_code == 200

    rch5 = requests.post(f"{config.url}channel/invite/v2", json=ch5)
    assert rch5.status_code == 200

    rch6 = requests.post(f"{config.url}channel/invite/v2", json=ch6)
    assert rch6.status_code == 200

    
    #all must return 200
#########################################################################
#########################CHANNEL_INVITE_TEST#############################
#########################################################################











#########################################################################
#########################CHANNEL_DETAILS_TEST############################
#########################################################################
"""
This is the only test left before doing the rest of the v1 functions assigned by me  
INER:
channel_id does not refer to a valid channel

ACER:
channel_id is valid and the authorised user is not a member of the channel
invalid token
"""

def test_channel_details_invalid_channel(clear_and_register3_create6):
    #400
    #channel details for channels 0 and 7:
    ch7_det = {"token" : encode_jwt(1,0), "channel_id" : 7}
    ch0_det = {"token" : encode_jwt(1,0), "channel_id" : 0}

    rch7_det = requests.get(f"{config.url}channel/details/v2", params=ch7_det)
    assert rch7_det.status_code == 400

    rch0_det = requests.get(f"{config.url}channel/details/v2", params=ch0_det)
    assert rch0_det.status_code == 400

def test_channel_detailsvalid_chid_user_not_member(clear_and_register3_create6):
    #403
    #user 3 asking for all channel details
    ch1_det = {"token" : encode_jwt(3,0), "channel_id" : 1}
    ch2_det = {"token" : encode_jwt(3,0), "channel_id" : 2}
    ch3_det = {"token" : encode_jwt(3,0), "channel_id" : 3}
    ch4_det = {"token" : encode_jwt(3,0), "channel_id" : 4}
    ch5_det = {"token" : encode_jwt(3,0), "channel_id" : 5}
    ch6_det = {"token" : encode_jwt(3,0), "channel_id" : 6}

    #make requests:
    rch1_det = requests.get(f"{config.url}channel/details/v2", params=ch1_det)
    assert rch1_det.status_code == 403
    rch2_det = requests.get(f"{config.url}channel/details/v2", params=ch2_det)
    rch3_det = requests.get(f"{config.url}channel/details/v2", params=ch3_det)
    rch4_det = requests.get(f"{config.url}channel/details/v2", params=ch4_det)
    rch5_det = requests.get(f"{config.url}channel/details/v2", params=ch5_det)
    rch6_det = requests.get(f"{config.url}channel/details/v2", params=ch6_det)



    
    #assert requests: have to be 403
    assert rch1_det.status_code == 403
    assert rch2_det.status_code == 403
    assert rch3_det.status_code == 403
    assert rch4_det.status_code == 403
    assert rch5_det.status_code == 403
    assert rch6_det.status_code == 403


def test_channel_details_invalid_token_auth_id(clear_and_register3_create6):
    #403
    #auth 4 asking for 2 channels
    ch6_det = {"token" : encode_jwt(4,0), "channel_id" : 4}
    ch4_det = {"token" : encode_jwt(4,0), "channel_id" : 6}

    #make requests
    rch6_det = requests.get(f"{config.url}channel/details/v2", params=ch6_det)
    rch4_det = requests.get(f"{config.url}channel/details/v2", params=ch4_det)

    #assert requests
    assert rch4_det.status_code == 403
    assert rch6_det.status_code == 403


def test_channel_details_invalid_token_session_id(clear_and_register3_create6):
    #403
    #u1 and 2 asking for their channels with inexisting session_ids:
    #u1 has 1, 2, 3, 5      u2 has 4, 6 : u1 will login 2 times and u2 will login once

    #logins:
    login1 = {"email": "osama2as820sadas02@gmail.com", "password": "dasdasdasdlakmLN"}
    login2 = {"email": "someemailadress@gmail.com", "password": "dasdasdasdlakmLN"}
    
    rlogin1 = requests.post(f"{config.url}auth/login/v2", json=login1)
    rlogin1_data = rlogin1.json()
    assert rlogin1_data['auth_user_id'] == 1
    assert decode_jwt(rlogin1_data['token']) == {'u_id': 1, 'session_id': 1}
    token1_s1 = rlogin1_data['token']

    rlogin12 = requests.post(f"{config.url}auth/login/v2", json=login1)
    rlogin12_data = rlogin12.json()
    assert rlogin12_data['auth_user_id'] == 1
    assert decode_jwt(rlogin12_data['token']) == {'u_id': 1, 'session_id': 2}
    token12_s1 = rlogin12_data['token']

    rlogin2 = requests.post(f"{config.url}auth/login/v2", json=login2)
    rlogin2_data = rlogin2.json()
    assert rlogin2_data['auth_user_id'] == 2
    assert decode_jwt(rlogin2_data['token']) == {'u_id': 2, 'session_id': 1}
    token2_s1 = rlogin2_data['token']
    #u1 and u2 will login as well to extend the range of tests.
    ch1_det = {"token" : encode_jwt(1,0), "channel_id" : 1} #200
    ch2_det = {"token" : token1_s1, "channel_id" : 2} #200
    ch3_det = {"token" : token12_s1, "channel_id" : 3} #200
    ch4_det = {"token" : encode_jwt(2,0), "channel_id" : 4} #200
    ch5_det = {"token" : encode_jwt(1,3), "channel_id" : 5} #403
    ch6_det = {"token" : token2_s1, "channel_id" : 6} #200
    ch6_det_invalid = {"token" : encode_jwt(2,2), "channel_id" : 6} #403


    #make a series of details
    rch1_det = requests.get(f"{config.url}channel/details/v2", params=ch1_det)
    assert rch1_det.status_code == 200

    rch2_det = requests.get(f"{config.url}channel/details/v2", params=ch2_det)
    assert rch2_det.status_code == 200

    rch3_det = requests.get(f"{config.url}channel/details/v2", params=ch3_det)
    assert rch3_det.status_code == 200

    rch4_det = requests.get(f"{config.url}channel/details/v2", params=ch4_det)
    assert rch4_det.status_code == 200

    rch5_det = requests.get(f"{config.url}channel/details/v2", params=ch5_det)
    assert rch5_det.status_code == 403

    rch6_det = requests.get(f"{config.url}channel/details/v2", params=ch6_det)
    assert rch6_det.status_code == 200

    rch6_det_invalid = requests.get(f"{config.url}channel/details/v2", params=ch6_det_invalid)
    assert rch6_det_invalid.status_code == 403

def test_channel_details_simple(clear_and_register3_create6):
    #test channels 1, 2, 4. No invites or join:
    ch1_det = {"token" : encode_jwt(1,0), "channel_id" : 1}
    ch2_det = {"token" : encode_jwt(1,0), "channel_id" : 2}
    ch4_det = {"token" : encode_jwt(2,0), "channel_id" : 4}

    #do the requests and fetch data:

    rch1_det = requests.get(f"{config.url}channel/details/v2", params=ch1_det)
    assert rch1_det.status_code == 200
    rch1_det_data = rch1_det.json()

    rch2_det = requests.get(f"{config.url}channel/details/v2", params=ch2_det)
    assert rch2_det.status_code == 200
    rch2_det_data = rch2_det.json()

    rch4_det = requests.get(f"{config.url}channel/details/v2", params=ch4_det)
    assert rch4_det.status_code == 200
    rch4_det_data = rch4_det.json()

    #now assert the data:
    #{ name, is_public, owner_members, all_members }
    #assert channel1 details
    assert rch1_det_data['name'] == "Channel1"
    assert rch1_det_data['is_public'] == False
    assert rch1_det_data['owner_members'] == [user_1_member]
    assert rch1_det_data['all_members'] == [user_1_member]

    #assert channel2 details
    assert rch2_det_data['name'] == "Channel2"
    assert rch2_det_data['is_public'] == True
    assert rch2_det_data['owner_members'] == [user_1_member]
    assert rch2_det_data['all_members'] == [user_1_member]

    #assert channel1 details
    assert rch4_det_data['name'] == "Channel4"
    assert rch4_det_data['is_public'] == False
    assert rch4_det_data['owner_members'] == [user_2_member]
    assert rch4_det_data['all_members'] == [user_2_member]

def test_channel_details_use_join_invite(clear_and_register3_create6):
    #user1 joins ch4, user 3 gets invited by user1 to join ch4, check details

    #user1 joins ch4:
    ru1_ch4 = requests.post(f"{config.url}channel/join/v2", json=u1_ch4)
    assert ru1_ch4.status_code == 200

    #user invites user3:
    u1_u3_ch4 = {"token" : encode_jwt(1,0), "channel_id" : 4, "u_id":3}
    ru1_u3_ch4 = requests.post(f"{config.url}channel/invite/v2", json=u1_u3_ch4)
    assert ru1_u3_ch4.status_code == 200

    #get channel details:
    ch4_det = {"token" : encode_jwt(3,0), "channel_id" : 4}
    rch4_det = requests.get(f"{config.url}channel/details/v2", params=ch4_det)
    assert rch4_det.status_code == 200
    rch4_det_data = rch4_det.json()
    assert rch4_det_data['name'] == "Channel4"
    assert rch4_det_data['is_public'] == False
    assert rch4_det_data['owner_members'] == [user_2_member]
    assert rch4_det_data['all_members'] == [user_1_member, user_2_member, user_3_member]


#########################################################################
#########################CHANNEL_DETAILS_TEST############################
#########################################################################

#########################################################################
#########################CHANNEL_MESSAGES_TEST###########################
#########################################################################
"""
This canot be tested until messages function is implemented successfully
INER:
-channel_id does not refer to a valid channel

(will try and do this)
-start is greater than the total number of messages in the channel

ACER:
-invalid token
-channel_id is valid and the authorised user is not a member of the channel
"""
def test_messages_invalid_channel_id(clear_and_register3_create6):
    """Ask for messages in channel, raise 400"""
    messages1 = {'token' : encode_jwt(1,0), 'channel_id' : 7, 'start' : 0}
    invalid_message = requests.get(f"{config.url}channel/messages/v2", params=messages1)
    assert invalid_message.status_code == 400

def test_messages_start_greaterthan_size(clear_and_register3_create6):
    """
    Plan:
    - make 10 messages
    - make start = 11
    - Expect a 400 to be raised
    """
    #make 10 messages:
    for i in range(0, 11):
        user1_message = {'token': encode_jwt(1,0), 'channel_id' : 3, 'message':"hey guys"}
        msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
        assert msg_request.status_code == 200
        msg_data = msg_request.json() #returns {msg:msgid}
        assert msg_data['message_id'] == i+1
    
    invalid_start = {'token' : encode_jwt(1,0), 'channel_id' : 1, 'start' : 11}

    invalid_session = requests.get(f"{config.url}channel/messages/v2", params=invalid_start)
    assert invalid_session.status_code == 400

def test_messages_invalid_token(clear_and_register3_create6):
    """Invalid tokens passed; must raise 403"""
    #from channel1:
    invalid_session = {'token' : encode_jwt(1,1), 'channel_id' : 1, 'start' : 0}
    invalid_id = {'token' : encode_jwt(4,0), 'channel_id' : 1, 'start' : 0}

    request_session = requests.get(f"{config.url}channel/messages/v2", params=invalid_session)
    assert request_session.status_code == 403

    request_id = requests.get(f"{config.url}channel/messages/v2", params=invalid_id)
    assert request_id.status_code == 403

def test_messages_not_member(clear_and_register3_create6):
    """User2 is not a member in channel1, must raise 403"""
    #ask user2 to fetch messages from ch1:
    invalid_input = {'token' : encode_jwt(2,0), 'channel_id' : 1, 'start' : 0}
    invalid_message = requests.get(f"{config.url}channel/messages/v2", params=invalid_input)
    assert invalid_message.status_code == 403

def test_messages_normal(clear_and_register3_create6):
    """Make 51 messages, start with 0, expect 50 to be end"""
    #user2 and user3 to join channel2:
    ru2_ch2 = requests.post(f"{config.url}channel/join/v2", json=u2_ch2)
    assert ru2_ch2.status_code == 200

    ru3_ch2 = requests.post(f"{config.url}channel/join/v2", json=u3_ch2)
    assert ru3_ch2.status_code == 200

    #Let user 1 do 25:
    for i in range(1, 26):
        user1_message = {'token': encode_jwt(1,0), 'channel_id' : 2, 'message':"hey guys"}
        msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
        assert msg_request.status_code == 200
        msg_data = msg_request.json() #returns {msg:msgid}
        assert msg_data['message_id'] == i
    
    #Let user2 make 15
    for i in range(26, 41):
        user1_message = {'token': encode_jwt(2,0), 'channel_id' : 2, 'message':"yooo"}
        msg2_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
        assert msg2_request.status_code == 200
        msg2_data = msg2_request.json() #returns {msg:msgid}
        assert msg2_data['message_id'] == i
    
    #Let user3 make 10
    for i in range(41, 52):
        user1_message = {'token': encode_jwt(3,0), 'channel_id' : 2, 'message':"suiiii"}
        msg2_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
        assert msg2_request.status_code == 200
        msg2_data = msg2_request.json() #returns {msg:msgid}
        assert msg2_data['message_id'] == i

    messages_request = {'token' : encode_jwt(1,0), 'channel_id' : 2, 'start' : 0}

    request_session = requests.get(f"{config.url}channel/messages/v2", params=messages_request)
    assert request_session.status_code == 200
    request_data = request_session.json()
    assert request_data['start'] == 0
    assert request_data['end'] == 50
    assert len(request_data['messages']) == 51
    assert request_data['messages'][0]['message_id'] == 51


def test_messages_less_than_50(clear_and_register3_create6):
    """Make 10 messages, ask start from 0 and 9, expect -1 in both"""
    for i in range(1, 11):
        user1_message = {'token': encode_jwt(1,0), 'channel_id' : 2, 'message':"hey guys"}
        msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
        assert msg_request.status_code == 200
        msg_data = msg_request.json() #returns {msg:msgid}
        assert msg_data['message_id'] == i
    
    start_zero = {'token' : encode_jwt(1,0), 'channel_id' : 2, 'start' : 0}
    start_nine = {'token' : encode_jwt(1,0), 'channel_id' : 2, 'start' : 9}


    request_session = requests.get(f"{config.url}channel/messages/v2", params=start_zero)
    assert request_session.status_code == 200
    request_data = request_session.json()
    assert request_data['start'] == 0
    assert request_data['end'] == -1
    assert len(request_data['messages']) == 10
    assert request_data['messages'][0]['message_id'] == 10

    request2 = requests.get(f"{config.url}channel/messages/v2", params=start_nine)
    assert request2.status_code == 200
    request2_data = request2.json()
    assert request2_data['start'] == 9
    assert request2_data['end'] == -1
    assert len(request2_data['messages']) == 1
    assert request2_data['messages'][0]['message_id'] == 1

def test_messages_between(clear_and_register3_create6):
    """make 100 messages, assert end = 75 since start is 25"""
    for i in range(1, 101):
        user1_message = {'token': encode_jwt(1,0), 'channel_id' : 2, 'message':"hey guys"}
        msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
        assert msg_request.status_code == 200
        msg_data = msg_request.json() #returns {msg:msgid}
        assert msg_data['message_id'] == i
    
    start_two_five = {'token' : encode_jwt(1,0), 'channel_id' : 2, 'start' : 25}
    

    request_session = requests.get(f"{config.url}channel/messages/v2", params=start_two_five)
    assert request_session.status_code == 200
    request_data = request_session.json()
    assert request_data['start'] == 25
    assert request_data['end'] == 75
    assert len(request_data['messages']) == 51
    assert request_data['messages'][0]['message_id'] == 75

def test_is_react_true(clear_and_register3_create6):
    """make 100 messages, assert end = 75 since start is 25"""
    for i in range(1, 101):
        user1_message = {'token': encode_jwt(1,0), 'channel_id' : 2, 'message':"hey guys"}
        msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
        assert msg_request.status_code == 200
        msg_data = msg_request.json() #returns {msg:msgid}
        assert msg_data['message_id'] == i
    
    start_two_five = {'token' : encode_jwt(1,0), 'channel_id' : 2, 'start' : 25}
    
    #user 1 reaction
    for i in range(1, 101):
        user1_react = {'token': encode_jwt(1,0), 'message_id': i,'react_id': 1}
        user1_reaction = requests.post(f"{config.url}message/react/v1", json=user1_react)
        assert user1_reaction.status_code == 200
        user1_data = user1_reaction.json()
        assert user1_data == {}

    request_session = requests.get(f"{config.url}channel/messages/v2", params=start_two_five)
    assert request_session.status_code == 200
    request_data = request_session.json()
    assert request_data['start'] == 25
    assert request_data['end'] == 75
    assert len(request_data['messages']) == 51
    assert request_data['messages'][0]['message_id'] == 75

def test_is_react_unreacting(clear_and_register3_create6):
    """make 100 messages, assert end = 75 since start is 25"""
    for i in range(1, 101):
        user1_message = {'token': encode_jwt(1,0), 'channel_id' : 2, 'message':"hey guys"}
        msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
        assert msg_request.status_code == 200
        msg_data = msg_request.json() #returns {msg:msgid}
        assert msg_data['message_id'] == i
    
    start_two_five = {'token' : encode_jwt(1,0), 'channel_id' : 2, 'start' : 25}
    
    #user 1 reaction
    for i in range(1, 101):
        user1_react = {'token': encode_jwt(1,0), 'message_id': i,'react_id': 1}
        user1_reaction = requests.post(f"{config.url}message/react/v1", json=user1_react)
        assert user1_reaction.status_code == 200
        user1_data = user1_reaction.json()
        assert user1_data == {}

    request_session = requests.get(f"{config.url}channel/messages/v2", params=start_two_five)
    assert request_session.status_code == 200
    request_data = request_session.json()
    assert request_data['start'] == 25
    assert request_data['end'] == 75
    assert len(request_data['messages']) == 51
    assert request_data['messages'][0]['message_id'] == 75

    #user 1 unreaction
    for i in range(1, 101):
        user1_react = {'token': encode_jwt(1,0), 'message_id': i,'react_id': 1}
        user1_reaction = requests.post(f"{config.url}message/unreact/v1", json=user1_react)
        assert user1_reaction.status_code == 200
        user1_data = user1_reaction.json()
        assert user1_data == {}
    
    request_session = requests.get(f"{config.url}channel/messages/v2", params=start_two_five)
    assert request_session.status_code == 200
    request_data = request_session.json()
    assert request_data['start'] == 25
    assert request_data['end'] == 75
    assert len(request_data['messages']) == 51
    assert request_data['messages'][0]['message_id'] == 75


#########################################################################
#########################CHANNEL_MESSAGES_TEST###########################
#########################################################################
