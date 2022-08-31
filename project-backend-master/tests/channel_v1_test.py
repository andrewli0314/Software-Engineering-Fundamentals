from os import remove
import re
from typing_extensions import IntVar
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
def clear__register3users_create4channels():
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

    #Create 4 channels:
    create_ch1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_ch1.status_code == 200
    create_ch2 = requests.post(f"{config.url}channels/create/v2", json=channel_2)
    assert create_ch2.status_code == 200
    create_ch3 = requests.post(f"{config.url}channels/create/v2", json=channel_3)
    assert create_ch3.status_code == 200
    create_ch4 = requests.post(f"{config.url}channels/create/v2", json=channel_4)
    assert create_ch4.status_code == 200

    """
    u1 = [1,2,3,4] /-/-
    u2 = [1,3,4] /-/-
    u3 = [1, 2] /-/-
    """
    
    #invite user1 to ch4
    u2_ch4_u1 = {"token" : token2, "channel_id" : 4, "u_id":1}
    ru2_ch4_u1 = requests.post(f"{config.url}channel/invite/v2", json=u2_ch4_u1)
    assert ru2_ch4_u1.status_code == 200

    #invite user3 to ch1
    u1_ch1_u3 = {"token" : token1, "channel_id" : 1, "u_id":3}
    ru1_ch1_u3 = requests.post(f"{config.url}channel/invite/v2", json=u1_ch1_u3)
    assert ru1_ch1_u3.status_code == 200

    #invite user2 to ch1:
    u1_ch1_u2 = {"token" : token1, "channel_id" : 1, "u_id":2}
    ru1_ch1_u2 = requests.post(f"{config.url}channel/invite/v2", json=u1_ch1_u2)
    assert ru1_ch1_u2.status_code == 200

    #user2 joins ch3:
    u2_ch3 = {"token" : token2 , "channel_id" : 3}
    ru2_ch3 = requests.post(f"{config.url}channel/join/v2", json=u2_ch3)
    assert ru2_ch3.status_code == 200

    #user3 joins ch2:
    u3_ch2 = {"token" : encode_jwt(3,0) , "channel_id" : 2}
    ru3_ch2 = requests.post(f"{config.url}channel/join/v2", json=u3_ch2)
    assert ru3_ch2.status_code == 200

#########################################################################
#######################CHANNEL_LEAVE_TESTS###############################
#########################################################################
def test_channelleave_invalid_token(clear__register3users_create4channels):
    """User1 will leave channel1, must return 403"""
    ch1_leave = {'token': encode_jwt(1,1), 'channel_id' : 1}
    request = requests.post(f"{config.url}channel/leave/v1", json=ch1_leave)
    assert request.status_code == 403

    ch1_leave2 = {'token': encode_jwt(4,0), 'channel_id' : 1}
    request2 = requests.post(f"{config.url}channel/leave/v1", json=ch1_leave2)
    assert request2.status_code == 403

def test_channelleave_invalid_channel(clear__register3users_create4channels):
    """Leave channel_is 5, must raise 400"""
    ch5_leave = {'token': encode_jwt(1,0), 'channel_id' : 5}
    request = requests.post(f"{config.url}channel/leave/v1", json=ch5_leave)
    assert request.status_code == 400

def test_channelleave_not_member(clear__register3users_create4channels):
    "let user3 leave channels 1 and 2, first arg is 200, last must raise 400"
    ch1_leave = {'token': encode_jwt(3,0), 'channel_id' : 1}
    ch3_leave = {'token': encode_jwt(3,0), 'channel_id' : 3}

    leave_ch1 = requests.post(f"{config.url}channel/leave/v1", json=ch1_leave)
    assert leave_ch1.status_code == 200

    leave_ch3 = requests.post(f"{config.url}channel/leave/v1", json=ch3_leave)
    assert leave_ch3.status_code == 403

def test_channel_leave1(clear__register3users_create4channels):
    """
    Reminders:
    - User1 is admin in 1,2,3 and a member in 4
    - User2 is admin in 4 and member in 1 and 3
    - User3 is member in 1 and 2.
    """
    #Plan:
        #- users 2 and 3 leave ch1, assert
        # user1 leaves ch4 assert
    
    #after: 1[1,2,3] - 2[3,4] - 3[2]

    #leaving channel1:
    u2_leave_ch1 = {'token' : encode_jwt(2,0), 'channel_id' : 1}
    u3_leave_ch1 = {'token' : encode_jwt(3,0), 'channel_id' : 1}
    u1_leave_ch4 = {'token': encode_jwt(1,0), 'channel_id' : 4}

    u2_leave = requests.post(f"{config.url}channel/leave/v1", json=u2_leave_ch1)
    assert u2_leave.status_code == 200

    u3_leave = requests.post(f"{config.url}channel/leave/v1", json=u3_leave_ch1)
    assert u3_leave.status_code == 200

    u1_leave = requests.post(f"{config.url}channel/leave/v1", json=u1_leave_ch4)
    assert u1_leave.status_code == 200

    #fetch channel details to check:

    ch1_det = {"token" : encode_jwt(1,0), "channel_id" : 1}
    ch4_det = {"token" : encode_jwt(2,0), "channel_id" : 4}

    #do the requests and fetch data:

    rch1_det = requests.get(f"{config.url}channel/details/v2", params=ch1_det)
    assert rch1_det.status_code == 200
    rch1_det_data = rch1_det.json()

    rch4_det = requests.get(f"{config.url}channel/details/v2", params=ch4_det)
    assert rch4_det.status_code == 200
    rch4_det_data = rch4_det.json()

    #assert channel1 details
    assert rch1_det_data['name'] == "Channel1"
    assert rch1_det_data['is_public'] == False
    assert len(rch1_det_data['owner_members']) == 1
    assert len(rch1_det_data['all_members']) == 1

    #assert channel4 details
    assert rch4_det_data['name'] == "Channel4"
    assert rch4_det_data['is_public'] == False
    assert len(rch4_det_data['owner_members']) == 1
    assert len(rch4_det_data['all_members']) == 1

    #try getting ch1 and ch4 data from users who left, must return 403
    ch1_det_invalid = {"token" : encode_jwt(3,0), "channel_id" : 1}
    ch4_det_invalid = {"token" : encode_jwt(1,0), "channel_id" : 4}
    rch1_det = requests.get(f"{config.url}channel/details/v2", params=ch1_det_invalid)
    assert rch1_det.status_code == 403

    rch4_det = requests.get(f"{config.url}channel/details/v2", params=ch4_det_invalid)
    assert rch4_det.status_code == 403

def test_channel_leave_one_admin(clear__register3users_create4channels):
    """Plan: user1 leaves ch1 and user2 leave ch4, channels must continue without admins"""
    u1_leave_ch1 = {'token' : encode_jwt(1,0), 'channel_id' : 1}
    u2_leave_ch4 = {'token': encode_jwt(2,0), 'channel_id' : 4}

    u1_leave = requests.post(f"{config.url}channel/leave/v1", json=u1_leave_ch1)
    assert u1_leave.status_code == 200

    u2_leave = requests.post(f"{config.url}channel/leave/v1", json=u2_leave_ch4)
    assert u2_leave.status_code == 200


    #fetch channel details to check:

    ch1_det = {"token" : encode_jwt(3,0), "channel_id" : 1}
    ch4_det = {"token" : encode_jwt(1,0), "channel_id" : 4}

    #do the requests and fetch data:

    rch1_det = requests.get(f"{config.url}channel/details/v2", params=ch1_det)
    assert rch1_det.status_code == 200
    rch1_det_data = rch1_det.json()

    rch4_det = requests.get(f"{config.url}channel/details/v2", params=ch4_det)
    assert rch4_det.status_code == 200
    rch4_det_data = rch4_det.json()

    #assert channel1 details
    assert rch1_det_data['name'] == "Channel1"
    assert rch1_det_data['is_public'] == False
    assert len(rch1_det_data['owner_members']) == 0
    assert len(rch1_det_data['all_members']) == 2

    #assert channel4 details
    assert rch4_det_data['name'] == "Channel4"
    assert rch4_det_data['is_public'] == False
    assert len(rch4_det_data['owner_members']) == 0
    assert len(rch4_det_data['all_members']) == 1

    #try getting ch1 and ch4 data from users who left, must return 403
    ch1_det_invalid = {"token" : encode_jwt(1,0), "channel_id" : 1}
    ch4_det_invalid = {"token" : encode_jwt(2,0), "channel_id" : 4}
    rch1_det = requests.get(f"{config.url}channel/details/v2", params=ch1_det_invalid)
    assert rch1_det.status_code == 403

    rch4_det = requests.get(f"{config.url}channel/details/v2", params=ch4_det_invalid)
    assert rch4_det.status_code == 403

#########################################################################
#######################CHANNEL_LEAVE_TESTS###############################
#########################################################################



#########################################################################
#######################CHANNEL_ADDOWNER_TESTS############################
#########################################################################
def test_addowner_invalid_channel(clear__register3users_create4channels):
    """user1 will add user2 as an admin in channel5, must raise 400"""
    u1addu2_ch5 = {'token':encode_jwt(1,0), 'channel_id' : 5, 'u_id' : 2}
    invalid_request = requests.post(f"{config.url}/channel/addowner/v1", json=u1addu2_ch5)
    assert invalid_request.status_code == 400  

def test_addowner_invalid_uid(clear__register3users_create4channels):
    """u1 will add u4 to ch1 as an admin, must raise 400"""
    u1addu4_ch1 = {'token':encode_jwt(1,0), 'channel_id' : 1, 'u_id' : 4}
    invalid_request = requests.post(f"{config.url}/channel/addowner/v1", json=u1addu4_ch1)
    assert invalid_request.status_code == 400

def test_addowner_uid_not_member(clear__register3users_create4channels):
    """u2 will add u3 to be an owner of ch4, u3 is not a member; must raise 400"""
    u2addu3_ch4 = {'token':encode_jwt(2,0), 'channel_id' : 4, 'u_id' : 3}
    invalid_request = requests.post(f"{config.url}/channel/addowner/v1", json=u2addu3_ch4)
    assert invalid_request.status_code == 400

def test_addowner_uidalready_an_owner(clear__register3users_create4channels):
    """
    u1 will add u2 to be an owner, returns 200
    u1 will do it again, must raise 400
    """
    add_owner = {'token' : encode_jwt(1,0), 'channel_id' : 1, 'u_id' : 2}
    valid_request = requests.post(f"{config.url}channel/addowner/v1", json=add_owner)
    assert valid_request.status_code == 200

    invalid_request = requests.post(f"{config.url}channel/addowner/v1", json=add_owner)
    assert invalid_request.status_code == 400

def test_addowner_invalid_token(clear__register3users_create4channels):
    """Tests for invalid token, must raise 403"""
    u1addu2_ch1 = {'token':encode_jwt(1,1), 'channel_id':1, 'u_id' : 2}
    invalid_request = requests.post(f"{config.url}/channel/addowner/v1", json=u1addu2_ch1)
    assert invalid_request.status_code == 403

    u4addu2_ch1 = {'token':encode_jwt(4,0), 'channel_id':1, 'u_id' : 2}
    invalid_request2 = requests.post(f"{config.url}/channel/addowner/v1", json=u4addu2_ch1)
    assert invalid_request2.status_code == 403

def test_addowner_authid_not_owner(clear__register3users_create4channels):
    """u3 will add u2 to be an owner in u1, must raise 403"""
    u3addu2_ch1 = {'token':encode_jwt(3,0), 'channel_id':1, 'u_id' : 2}
    invalid_request = requests.post(f"{config.url}/channel/addowner/v1", json=u3addu2_ch1)
    assert invalid_request.status_code == 403

"""{ token, channel_id, u_id }"""
def test_addowner1(clear__register3users_create4channels):
    """
    add u2 to be an admin in ch1
    add u3 to be an admin in ch1

    add u1 to be an admin in ch4

    assert via details
    """

    u2_admin_ch1 = {'token' : encode_jwt(1,0), 'channel_id' : 1, 'u_id' : 2}
    u3_admin_ch1 = {'token' : encode_jwt(2,0), 'channel_id' : 1, 'u_id' : 3}
    u1_admin_ch4 = {'token' : encode_jwt(2,0), 'channel_id' : 4, 'u_id' : 1}


    request_u2 = requests.post(f"{config.url}channel/addowner/v1", json=u2_admin_ch1)
    assert request_u2.status_code == 200

    request_u3 = requests.post(f"{config.url}channel/addowner/v1", json=u3_admin_ch1)
    assert request_u3.status_code == 200

    request_u1 = requests.post(f"{config.url}channel/addowner/v1", json=u1_admin_ch4)
    assert request_u1.status_code == 200

    #fetch channel details
    ch1_det = {"token" : encode_jwt(3,0), "channel_id" : 1}
    ch4_det = {"token" : encode_jwt(1,0), "channel_id" : 4}

    #do the requests and fetch data:

    rch1_det = requests.get(f"{config.url}channel/details/v2", params=ch1_det)
    assert rch1_det.status_code == 200
    rch1_det_data = rch1_det.json()

    rch4_det = requests.get(f"{config.url}channel/details/v2", params=ch4_det)
    assert rch4_det.status_code == 200
    rch4_det_data = rch4_det.json()

    #assert channel1 details
    assert rch1_det_data['name'] == "Channel1"
    assert rch1_det_data['is_public'] == False
    assert len(rch1_det_data['owner_members']) == 3
    assert len(rch1_det_data['all_members']) == 3

    #assert channel4 details
    assert rch4_det_data['name'] == "Channel4"
    assert rch4_det_data['is_public'] == False
    assert len(rch4_det_data['owner_members']) == 2
    assert len(rch4_det_data['all_members']) == 2

#########################################################################
#######################CHANNEL_ADDOWNER_TESTS############################
#########################################################################




#########################################################################
######################CHANNEL_REMOVEOWNER_TESTS##########################
#########################################################################

def test_remowner_invalid_channel(clear__register3users_create4channels):
    """user1 will remove user2 as an admin in channel5, must raise 400"""
    u1remu2_ch5 = {'token':encode_jwt(1,0), 'channel_id' : 5, 'u_id' : 2}
    invalid_request = requests.post(f"{config.url}/channel/removeowner/v1", json=u1remu2_ch5)
    assert invalid_request.status_code == 400  

def test_remowner_invalid_uid(clear__register3users_create4channels):
    """user1 will remove user4 as an admin in channel1, must raise 400"""
    u1remu4_ch1 = {'token':encode_jwt(1,0), 'channel_id' : 1, 'u_id' : 4}
    invalid_request = requests.post(f"{config.url}/channel/removeowner/v1", json=u1remu4_ch1)
    assert invalid_request.status_code == 400  

def test_remowner_uid_not_owner(clear__register3users_create4channels):
    """user2 will remove user1 as an admin in channel4, must raise 400"""
    u1remu2_ch4 = {'token':encode_jwt(2,0), 'channel_id' : 4, 'u_id' : 1}
    invalid_request = requests.post(f"{config.url}/channel/removeowner/v1", json=u1remu2_ch4)
    assert invalid_request.status_code == 400  

def test_remowner_only_owner(clear__register3users_create4channels):
    """Only Admin removes himself as an admin, must raise 400"""
    u1remu1_ch1 = {'token':encode_jwt(1,0), 'channel_id' : 1, 'u_id' : 1}
    invalid_request = requests.post(f"{config.url}/channel/removeowner/v1", json=u1remu1_ch1)
    assert invalid_request.status_code == 400 

def test_remowner_invalid_token(clear__register3users_create4channels):
    """Invalid tokens inserted, must raise 403"""
    #add owner and assert 200:
    #user1 adds user2 to channel1:
    u1addu2_ch1 = {'token':encode_jwt(1,0), 'channel_id' : 1, 'u_id' : 2}
    valid_add = requests.post(f"{config.url}/channel/addowner/v1", json=u1addu2_ch1)
    assert valid_add.status_code == 200

    u1remu2_ch1 = {'token':encode_jwt(1,1), 'channel_id' : 1, 'u_id' : 2}
    invalid_rem = requests.post(f"{config.url}/channel/removeowner/v1", json=u1remu2_ch1)
    assert invalid_rem.status_code == 403

    u4remu2_ch1 = {'token':encode_jwt(4,0), 'channel_id' : 1, 'u_id' : 2}
    invalid_rem2 = requests.post(f"{config.url}/channel/removeowner/v1", json=u4remu2_ch1)
    assert invalid_rem2.status_code == 403

def test_authid_not_owner(clear__register3users_create4channels):
    """Ask u2 to remove u1 as an owner from channel1 when u2 itself is not an owner"""
    u2remu1_ch1 = {'token':encode_jwt(2,0), 'channel_id' : 1, 'u_id' : 1}
    invalid_request = requests.post(f"{config.url}/channel/removeowner/v1", json=u2remu1_ch1)
    assert invalid_request.status_code == 403

"""{ token, channel_id, u_id }"""
def test_remowner1(clear__register3users_create4channels):
    """
    user2 will be added to ch1, user1 will be added to ch4, then they remove the original owners.
    Assert details; make sure they're removed from ownership but remain members.
    """
    #Add u2 to be an admin in ch1 and u1 to be an admin in ch4
    u2_admin_ch1 = {'token' : encode_jwt(1,0), 'channel_id' : 1, 'u_id' : 2}
    u1_admin_ch4 = {'token' : encode_jwt(2,0), 'channel_id' : 4, 'u_id' : 1}

    request_u1 = requests.post(f"{config.url}channel/addowner/v1", json=u1_admin_ch4)
    assert request_u1.status_code == 200

    request_u2 = requests.post(f"{config.url}channel/addowner/v1", json=u2_admin_ch1)
    assert request_u2.status_code == 200

    remove_u1_admin = {'token' : encode_jwt(2,0), 'channel_id' : 1, 'u_id' : 1}
    remove_u4_admin = {'token' : encode_jwt(1,0), 'channel_id' : 4, 'u_id' : 2}

    remove_u1 = requests.post(f"{config.url}channel/removeowner/v1", json=remove_u1_admin)
    assert remove_u1.status_code == 200

    remove_u4 = requests.post(f"{config.url}channel/removeowner/v1", json=remove_u4_admin)
    assert remove_u4.status_code == 200



    #fetch channel details
    ch1_det = {"token" : encode_jwt(3,0), "channel_id" : 1}
    ch4_det = {"token" : encode_jwt(1,0), "channel_id" : 4}

    #do the requests and fetch data:

    rch1_det = requests.get(f"{config.url}channel/details/v2", params=ch1_det)
    assert rch1_det.status_code == 200
    rch1_det_data = rch1_det.json()

    rch4_det = requests.get(f"{config.url}channel/details/v2", params=ch4_det)
    assert rch4_det.status_code == 200
    rch4_det_data = rch4_det.json()

    #assert channel1 details
    u1_det = {
    "u_id" : 1,
    "email" : "osama2as820sadas02@gmail.com", 
    "name_first": "Osama",
    "name_last": "Almabrouk",
    "handle_str" : "osamaalmabrouk"
    }
    
    u2_det = {
    "u_id" : 2,
    "email" : "someemailadress@gmail.com", 
    "name_first": "Osama",
    "name_last": "Almabrouk",
    "handle_str" : "osamaalmabrouk0"
    }

    assert rch1_det_data['name'] == "Channel1"
    assert rch1_det_data['is_public'] == False
    assert rch1_det_data['owner_members'] == [u2_det]
    assert len(rch1_det_data['owner_members']) == 1
    assert len(rch1_det_data['all_members']) == 3

    #assert channel4 details
    assert rch4_det_data['name'] == "Channel4"
    assert rch4_det_data['is_public'] == False
    assert rch4_det_data['owner_members'] == [u1_det]
    assert len(rch4_det_data['owner_members']) == 1
    assert len(rch4_det_data['all_members']) == 2



#########################################################################
######################CHANNEL_REMOVEOWNER_TESTS##########################
#########################################################################
