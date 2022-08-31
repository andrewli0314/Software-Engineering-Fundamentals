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
    u1 = [1,2,3, member of 4] /-/-
    u2 = [member in 1 and 3, owner 4] /-/-
    u3 = [member of 1 and 2] /-/-
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

    #encode_jwt(1,0) #to test for invalid tokens and to get valid token
def test_non_dm_member_share(clear__register3users_create4channels):
    #creating dm between user1 and 2
    token1 = encode_jwt(1, 0)
    dm_1 = {"token": token1,"u_ids": [2]}
    create_dm_1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm_1.status_code == 200
    create_dm_1_result = create_dm_1.json()
    assert create_dm_1_result['dm_id'] == 1

    #creat dm between user1 and 3
    dm_2 = {"token":token1, "u_ids":[3]}
    create_dm_2 = requests.post(f"{config.url}dm/create/v1", json = dm_2)
    assert create_dm_1.status_code == 200
    create_dm_2_result = create_dm_2.json()
    assert create_dm_2_result['dm_id'] == 2

    #user 1 sends dm to user 2
    dm_message1 = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': "Hello there"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json = dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 1

    #User 3 tries to share to dm between user 1 and 2 
    u3_share_dm = {'token': encode_jwt(3,0), 'og_message_id': 1, 'message': 'I said this to user 2', 'channel_id':-1, 'dm_id': 2}
    dm_shared3 = requests.post(f"{config.url}message/share/v1", json = u3_share_dm)
    assert dm_shared3.status_code == 400

def test_share_to_nonmember_dm(clear__register3users_create4channels):
    #creating dm between user1 and 2
    token1 = encode_jwt(1, 0)
    dm_1 = {"token": token1,"u_ids": [2]}
    create_dm_1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm_1.status_code == 200
    create_dm_1_result = create_dm_1.json()
    assert create_dm_1_result['dm_id'] == 1

    #creat dm between user1 and 3
    dm_2 = {"token":token1, "u_ids":[3]}
    create_dm_2 = requests.post(f"{config.url}dm/create/v1", json = dm_2)
    assert create_dm_1.status_code == 200
    create_dm_2_result = create_dm_2.json()
    assert create_dm_2_result['dm_id'] == 2

    #user 1 sends dm to user 2
    dm_message1 = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': "Hello there"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json = dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 1

    #User 2 tries to share message to dm between user 1 and 3
    u2_share_dm = {'token': encode_jwt(2,0), 'og_message_id': 1, 'message': 'user 1 said this to me', 'channel_id':-1, 'dm_id': 2}
    dm_shared2 = requests.post(f"{config.url}message/share/v1", json = u2_share_dm)
    assert dm_shared2.status_code == 403

def test_non_channel_member_share(clear__register3users_create4channels):
     #testing sending message user 1 send a message
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 3, 'message':"hey guys"}
    msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
    # assert msg_request.status_code == 200
    msg_data = msg_request.json() #returns {msg:msgid}
    assert msg_data['message_id'] == 1

    #user 3 shares user 1's message to channel 3
    u3_share = {'token': encode_jwt(3,0), 'og_message_id': 1, 'message': 'look at this', 'channel_id':1, 'dm_id':-1}
    share_request = requests.post(f"{config.url}message/share/v1", json=u3_share)
    assert share_request.status_code == 400

def test_invalid_og_msg_id_dm(clear__register3users_create4channels):
    #creating dm between user1 and 2
    token1 = encode_jwt(1, 0)
    dm_1 = {"token": token1,"u_ids": [2]}
    create_dm_1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm_1.status_code == 200
    create_dm_1_result = create_dm_1.json()
    assert create_dm_1_result['dm_id'] == 1

    #user 1 sends dm to user 2
    dm_message1 = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': "Hey user 2"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json = dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 1

    #user 1 shares message with user 2
    u1_share_dm = {'token': encode_jwt(1,0), 'og_message_id': 10, 'message': 'I said this to user 2', 'channel_id':-1, 'dm_id': 1}
    dm_shared1 = requests.post(f"{config.url}message/share/v1", json = u1_share_dm)
    assert dm_shared1.status_code == 400

def test_invalid_og_msg_id_channel(clear__register3users_create4channels):
    #testing sending message user 1 send a message
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 3, 'message':"hey guys"}
    msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
   # assert msg_request.status_code == 200
    msg_data = msg_request.json() #returns {msg:msgid}
    assert msg_data['message_id'] == 1

    #user2 send a message to channel 1
    user2_msg = {'token': encode_jwt(2,0), 'channel_id' : 1, 'message':"hey guys"}
    msg_request2 = requests.post(f"{config.url}message/send/v1", json=user2_msg)
    msg2_data = msg_request2.json() #returns {msg:msgid}
    assert msg2_data['message_id'] == 2

    #user 2 shares their message to channel 3
    user2_share_to_channel2 ={'token': encode_jwt(2,0), 'og_message_id': 2, 'message': 'look at this', 'channel_id':4, 'dm_id':-1}
    share_request = requests.post(f"{config.url}message/share/v1", json=user2_share_to_channel2)
    assert msg_request.status_code == 200
    msg_share_request_data = share_request.json()
    assert msg_share_request_data['shared_message_id'] == 3

def test_blank_message_given(clear__register3users_create4channels):
    #creating dm between user1 and 2
    token1 = encode_jwt(1, 0)
    dm_1 = {"token": token1,"u_ids": [2]}
    create_dm_1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm_1.status_code == 200
    create_dm_1_result = create_dm_1.json()
    assert create_dm_1_result['dm_id'] == 1

    #creat dm between user1 and 3
    dm_2 = {"token":token1, "u_ids":[3]}
    create_dm_2 = requests.post(f"{config.url}dm/create/v1", json = dm_2)
    assert create_dm_1.status_code == 200
    create_dm_2_result = create_dm_2.json()
    assert create_dm_2_result['dm_id'] == 2

    #user 1 sends dm to user 2
    dm_message1 = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': "Hello there"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json = dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 1

    #User 1 share to dm 2
    u3_share_dm = {'token': encode_jwt(1,0), 'og_message_id': 1, 'message': '', 'channel_id':-1, 'dm_id': 2}
    dm_shared3 = requests.post(f"{config.url}message/share/v1", json = u3_share_dm)
    assert dm_shared3.status_code == 200

def test_share_channel(clear__register3users_create4channels):
    #has 1001 chars.
    invalid_message = "vSO1Xx3sVDvSanODuMrDsnHqML9mur5GVGHMQbwENoQKVn7L75uiaqyc6G"\
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

    #testing sending message user 1 send a message
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 3, 'message':"hey guys"}
    msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
   # assert msg_request.status_code == 200
    msg_data = msg_request.json() #returns {msg:msgid}
    assert msg_data['message_id'] == 1

    #user2 send a message to channel 1
    user2_msg = {'token': encode_jwt(2,0), 'channel_id' : 1, 'message':"hey guys"}
    msg_request2 = requests.post(f"{config.url}message/send/v1", json=user2_msg)
    msg2_data = msg_request2.json() #returns {msg:msgid}
    assert msg2_data['message_id'] == 2

    #user 2 shares their message to channel 3
    user2_share_to_channel2 ={'token': encode_jwt(2,0), 'og_message_id': 2, 'message': 'look at this', 'channel_id':3, 'dm_id':-1}
    share_request = requests.post(f"{config.url}message/share/v1", json=user2_share_to_channel2)
    assert msg_request.status_code == 200
    msg_share_request_data = share_request.json()
    assert msg_share_request_data['shared_message_id'] == 3

    #user 1 shares user 2's message to channel 3
    u1_share = {'token': encode_jwt(1,0), 'og_message_id': 2, 'message': 'look at this', 'channel_id':3, 'dm_id':-1}
    share_request = requests.post(f"{config.url}message/share/v1", json=u1_share)
    assert msg_request.status_code == 200
    msg_share_request_data = share_request.json()
    assert msg_share_request_data ['shared_message_id'] == 4

    #test invalid channel, user 2 shares to channel 2
    invalid_u2 = {'token': encode_jwt(2,0), 'og_message_id': 2, 'message': 'look at this', 'channel_id':2, 'dm_id':-1}
    invalid_request= requests.post(f"{config.url}message/share/v1", json=invalid_u2)
    assert invalid_request.status_code == 403

    #test cid and dm_id both not -1
    invalid_u2 = {'token': encode_jwt(2,0), 'og_message_id': 2, 'message': 'look at this', 'channel_id':3, 'dm_id':3}
    invalid_request= requests.post(f"{config.url}message/share/v1", json=invalid_u2)
    assert invalid_request.status_code == 400

    #test og_message id invlaid
    invalid_u2 = {'token': encode_jwt(2,0), 'og_message_id': 0, 'message': 'look at this', 'channel_id':3, 'dm_id':-1}
    invalid_request= requests.post(f"{config.url}message/share/v1", json=invalid_u2)
    assert invalid_request.status_code == 400

    #test message too long
    invalid_u2 = {'token': encode_jwt(2,0), 'og_message_id': 2, 'message': invalid_message, 'channel_id':3, 'dm_id':-1}
    invalid_request= requests.post(f"{config.url}message/share/v1", json=invalid_u2)
    assert invalid_request.status_code == 400

def test_share_dm(clear__register3users_create4channels):
    #creating dm between user1 and 2
    token1 = encode_jwt(1, 0)
    dm_1 = {"token": token1,"u_ids": [2]}
    create_dm_1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm_1.status_code == 200
    create_dm_1_result = create_dm_1.json()
    assert create_dm_1_result['dm_id'] == 1

    #creat dm between user1 and 3
    dm_2 = {"token":token1, "u_ids":[3]}
    create_dm_2 = requests.post(f"{config.url}dm/create/v1", json = dm_2)
    assert create_dm_1.status_code == 200
    create_dm_2_result = create_dm_2.json()
    assert create_dm_2_result['dm_id'] == 2

    #user 1 sends dm to user 2
    dm_message1 = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': "Hey user 2"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json = dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 1

    #user 1 shares message with user 2
    u1_share_dm = {'token': encode_jwt(1,0), 'og_message_id': 1, 'message': 'I said this to user 2', 'channel_id':-1, 'dm_id': 2}
    dm_shared1 = requests.post(f"{config.url}message/share/v1", json = u1_share_dm)
    #assert dm_shared1.status_code == 200
    dm_shared1_result = dm_shared1.json()
    assert dm_shared1_result['shared_message_id'] == 2