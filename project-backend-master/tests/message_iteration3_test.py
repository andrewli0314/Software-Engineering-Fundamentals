import time
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
            "name_first": "Martin",
            "name_last": "Hernandez"
            }

user_2 =  {
            "email": "someemailadress@gmail.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "J",
            "name_last": "Cole"
            }

user_3 =  {
            "email": "someemailadressss@gmail.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "Osama",
            "name_last": "Almabrouk"
            }

user_4 =  {
            "email": "somsaeemailadressss@gmail.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "suii",
            "name_last": "suii"
            }


@pytest.fixture
def clear__register3users_createdmschannels_send8messages():
    """
    This will create 3 users, create 2 channels, 2 dms, and send 8 messages:
    """
    response_del = requests.delete(f"{config.url}clear/v1")
    assert response_del.status_code == 200
    register1 = requests.post(f"{config.url}auth/register/v2", json=user_1)
    register2 = requests.post(f"{config.url}auth/register/v2", json=user_2)
    register3 = requests.post(f"{config.url}auth/register/v2", json=user_3)
    register4 = requests.post(f"{config.url}auth/register/v2", json=user_4)
    r1_data = register1.json()
    r2_data = register2.json()
    r3_data = register3.json()
    token1 = r1_data['token']
    token2 = r2_data['token']
    token3 = r3_data['token']
    assert register1.status_code == 200
    assert register2.status_code == 200
    assert register3.status_code == 200
    assert register4.status_code == 200
    #list of channels:
    channel_1 = {"token": token1,"name": "Channel1","is_public": False}
    channel_2 = {"token": token1,"name": "Channel2","is_public": True}

    #Create 4 channels:
    create_ch1 = requests.post(f"{config.url}channels/create/v2", json=channel_1)
    assert create_ch1.status_code == 200
    create_ch2 = requests.post(f"{config.url}channels/create/v2", json=channel_2)
    assert create_ch2.status_code == 200

    """
    u1 = [owner of 1,2] /-/-
    u2 = [member in 1] /-/-
    u3 = [member of 1 and 2] /-/-
    """
    
    #invite user3 to ch1
    u1_ch1_u3 = {"token" : token1, "channel_id" : 1, "u_id":3}
    ru1_ch1_u3 = requests.post(f"{config.url}channel/invite/v2", json=u1_ch1_u3)
    assert ru1_ch1_u3.status_code == 200

    #invite user2 to ch1:
    u1_ch1_u2 = {"token" : token1, "channel_id" : 1, "u_id":2}
    ru1_ch1_u2 = requests.post(f"{config.url}channel/invite/v2", json=u1_ch1_u2)
    assert ru1_ch1_u2.status_code == 200

    #user3 joins ch2:
    u3_ch2 = {"token" : encode_jwt(3,0) , "channel_id" : 2}
    ru3_ch2 = requests.post(f"{config.url}channel/join/v2", json=u3_ch2)
    assert ru3_ch2.status_code == 200

    #list of users
    users_1 = [1, 3]
    users_2 = [4]
    

    """
    u1 = [member in 1] /-/-
    u2 = [creator of 1 and member in 2] /-/-
    u3 = [creator of 2 and member in 1] /-/-
    u4 = [member in 2]
    """

    #list of dms:
    dm_1 = {"token": token2,"u_ids": users_1}
    dm_2 = {"token": token3,"u_ids": users_2}

    #Create 2 dms:
    create_dm1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm1.status_code == 200
    create_dm2 = requests.post(f"{config.url}dm/create/v1", json = dm_2)
    assert create_dm2.status_code == 200

    #Send messages:
    #Send 8 messages: 2 to each:.

    #u1 sends 2 messages to ch1:
    for i in range(1, 3):
        ch1_msg1 = {'token': encode_jwt(1,0), 'channel_id' : 1, 'message':f"hey guys{i}"}
        msg_request = requests.post(f"{config.url}message/send/v1", json=ch1_msg1)
        assert msg_request.status_code == 200
        msg1_data = msg_request.json() #returns {msg:msgid}
        assert msg1_data['message_id'] == i

    #u2 sends 3 messages to ch1:
    for i in range(3,6):
        dm1_msg2 = {'token': encode_jwt(2,0), 'dm_id' : 1, 'message': f"Hola {i}"}
        dm_msg_request = requests.post(f"{config.url}message/senddm/v1", json = dm1_msg2)
        assert dm_msg_request.status_code == 200
        msg1_data = dm_msg_request.json() #returns {msg:msgid}
        assert msg1_data['message_id'] == i
    
    #u3 sends 2 messages to dm2:
    for i in range(6, 8):
        dm2_msg = {'token': encode_jwt(3,0), 'dm_id' : 2, 'message': f"Hola {i}"}
        dm2_msg_request = requests.post(f"{config.url}message/senddm/v1", json = dm2_msg)
        assert dm2_msg_request.status_code == 200
        msg1_data = dm2_msg_request.json() #returns {msg:msgid}
        assert msg1_data['message_id'] == i

    


#########################################################################
############################MESSAGES_PIN#################################
#########################################################################
"""
channel:
    u1 = [owner of 1,2] /-/-
    u2 = [member in 1] /-/-
    u3 = [member of 1] /-/-
"""

"""
dm:
    u1 = [member in 1] /-/-
    u2 = [creator of 1] /-/-
    u3 = [creator of 2 and member in 1] /-/-
    u4 = [member in 2]
"""

"""
Messages:
    2 in ch1 (by u1)
    3 in dm1 (by u2)
    2 in dm2 (by u3)
"""

def test_pin_invalid_token(clear__register3users_createdmschannels_send8messages):
    #try pinning message id 2 with an invalid token:
    invalid_token = {'token' : encode_jwt(1,1), 'message_id' : 1}
    invalid_request = requests.post(f"{config.url}message/pin/v1", json=invalid_token)
    assert invalid_request.status_code == 403

def test_invalid_messageid(clear__register3users_createdmschannels_send8messages):
    invalid_msgid = {'token' : encode_jwt(1,0), 'message_id' : 8}
    invalid_msgidreq = requests.post(f"{config.url}message/pin/v1", json=invalid_msgid)
    assert invalid_msgidreq.status_code == 400

    user_notmember = invalid_msgid = {'token' : encode_jwt(2,0), 'message_id' : 7}
    notmember_req = requests.post(f"{config.url}message/pin/v1", json=user_notmember)
    assert notmember_req.status_code == 400

def test_chmsg_already_pinned(clear__register3users_createdmschannels_send8messages):
    for i in range(2):
        code = 200
        if i == 1:
            code = 400
        valid_req = {'token' : encode_jwt(1,0), 'message_id' : 1}
        valid_req1 = requests.post(f"{config.url}message/pin/v1", json=valid_req)
        assert valid_req1.status_code == code

def test_user_not_chowner(clear__register3users_createdmschannels_send8messages):
    #ask user2 to pin when he's not an owner:
    invalid_msgid = {'token' : encode_jwt(2,0), 'message_id' : 2}
    invalid_msgidreq = requests.post(f"{config.url}message/pin/v1", json=invalid_msgid)
    assert invalid_msgidreq.status_code == 403

def test_user_not_dmcreator_but_global_owner(clear__register3users_createdmschannels_send8messages):
    invalid_msgid = {'token' : encode_jwt(1,0), 'message_id' : 4}
    invalid_msgidreq = requests.post(f"{config.url}message/pin/v1", json=invalid_msgid)
    assert invalid_msgidreq.status_code == 200

def test_dm_not_member(clear__register3users_createdmschannels_send8messages):
    invalid_msgid = {'token' : encode_jwt(2,0), 'message_id' : 7}
    invalid_msgidreq = requests.post(f"{config.url}message/pin/v1", json=invalid_msgid)
    assert invalid_msgidreq.status_code == 400

def test_dm_not_creator(clear__register3users_createdmschannels_send8messages):
    invalid_msgid = {'token' : encode_jwt(4,0), 'message_id' : 7}
    invalid_msgidreq = requests.post(f"{config.url}message/pin/v1", json=invalid_msgid)
    assert invalid_msgidreq.status_code == 403

def test_dmmsg_already_pinned(clear__register3users_createdmschannels_send8messages):
    for i in range(2):
        code = 200
        if i == 1:
            code = 400
        valid_req = {'token' : encode_jwt(3,0), 'message_id' : 6}
        valid_req1 = requests.post(f"{config.url}message/pin/v1", json=valid_req)
        assert valid_req1.status_code == code

def test_pin_chmsg_not_member(clear__register3users_createdmschannels_send8messages):
    invalid_msgid = {'token' : encode_jwt(4,0), 'message_id' : 2}
    invalid_msgidreq = requests.post(f"{config.url}message/pin/v1", json=invalid_msgid)
    assert invalid_msgidreq.status_code == 400


#########################################################################
##########################MESSAGES_UNPIN#################################
#########################################################################

"""
channel:
    u1 = [owner of 1,2] /-/-
    u2 = [member in 1] /-/-
    u3 = [member of 1] /-/-
"""

"""
dm:
    u1 = [member in 1] /-/-
    u2 = [creator of 1] /-/-
    u3 = [creator of 2 and member in 1] /-/-
    u4 = [member in 2]
"""

"""
Messages:
    2 in ch1 (by u1)
    3 in dm1 (by u2)
    2 in dm2 (by u3)
"""

def test_unpin_invalid_token(clear__register3users_createdmschannels_send8messages):
    #try pinning message id 2 with an invalid token:
    invalid_token = {'token' : encode_jwt(1,1), 'message_id' : 1}
    invalid_request = requests.post(f"{config.url}message/unpin/v1", json=invalid_token)
    assert invalid_request.status_code == 403

def test_unpin_invalid_messageid(clear__register3users_createdmschannels_send8messages):
    invalid_msgid = {'token' : encode_jwt(1,0), 'message_id' : 8}
    invalid_msgidreq = requests.post(f"{config.url}message/unpin/v1", json=invalid_msgid)
    assert invalid_msgidreq.status_code == 400

    user_notmember = invalid_msgid = {'token' : encode_jwt(2,0), 'message_id' : 7}
    notmember_req = requests.post(f"{config.url}message/unpin/v1", json=user_notmember)
    assert notmember_req.status_code == 400

def test_unpin_chmsg_already_pinned(clear__register3users_createdmschannels_send8messages):
    pin_msg = valid_req = {'token' : encode_jwt(1,0), 'message_id' : 1}
    pin_req = requests.post(f"{config.url}message/pin/v1", json=pin_msg)
    assert pin_req.status_code == 200

    for i in range(2):
        code = 200
        if i == 1:
            code = 400
        valid_req = {'token' : encode_jwt(1,0), 'message_id' : 1}
        valid_req1 = requests.post(f"{config.url}message/unpin/v1", json=valid_req)
        assert valid_req1.status_code == code

def test_unpin_user_not_chowner(clear__register3users_createdmschannels_send8messages):
    #ask user2 to pin when he's not an owner:
    invalid_msgid = {'token' : encode_jwt(2,0), 'message_id' : 2}
    invalid_msgidreq = requests.post(f"{config.url}message/unpin/v1", json=invalid_msgid)
    assert invalid_msgidreq.status_code == 403

def test_unpin_user_not_dmcreator_but_global_owner(clear__register3users_createdmschannels_send8messages):
    #pin by user2:
    pin_dm_req = {'token' : encode_jwt(2,0), 'message_id' : 4}
    pin_dm_reqreq = requests.post(f"{config.url}message/pin/v1", json=pin_dm_req)
    assert pin_dm_reqreq.status_code == 200

    invalid_msgid = {'token' : encode_jwt(1,0), 'message_id' : 4}
    invalid_msgidreq = requests.post(f"{config.url}message/unpin/v1", json=invalid_msgid)
    assert invalid_msgidreq.status_code == 200

def test_unpin_dm_not_member(clear__register3users_createdmschannels_send8messages):
    invalid_msgid = {'token' : encode_jwt(2,0), 'message_id' : 7}
    invalid_msgidreq = requests.post(f"{config.url}message/unpin/v1", json=invalid_msgid)
    assert invalid_msgidreq.status_code == 400

def test_unpin_dm_not_creator(clear__register3users_createdmschannels_send8messages):

    invalid_msgid = {'token' : encode_jwt(4,0), 'message_id' : 7}
    invalid_msgidreq = requests.post(f"{config.url}message/unpin/v1", json=invalid_msgid)
    assert invalid_msgidreq.status_code == 403

def test_unpin_dmmsg_already_pinned(clear__register3users_createdmschannels_send8messages):
    pin_req = {'token' : encode_jwt(3,0), 'message_id' : 6}
    pin_reqreq = requests.post(f"{config.url}message/pin/v1", json=pin_req)
    assert pin_reqreq.status_code == 200
    for i in range(2):
        code = 200
        if i == 1:
            code = 400
        valid_req = {'token' : encode_jwt(3,0), 'message_id' : 6}
        valid_req1 = requests.post(f"{config.url}message/unpin/v1", json=valid_req)
        assert valid_req1.status_code == code

def test_unpin_pin_chmsg_not_member(clear__register3users_createdmschannels_send8messages):
    invalid_msgid = {'token' : encode_jwt(4,0), 'message_id' : 2}
    invalid_msgidreq = requests.post(f"{config.url}message/unpin/v1", json=invalid_msgid)
    assert invalid_msgidreq.status_code == 400


#########################################################################
######################MESSAGES_SENDLATER#################################
#########################################################################
"""
channel:
    u1 = [owner of 1,2] /-/-
    u2 = [member in 1] /-/-
    u3 = [member of 1] /-/-
"""

"""
dm:
    u1 = [member in 1] /-/-
    u2 = [creator of 1] /-/-
    u3 = [creator of 2 and member in 1] /-/-
    u4 = [member in 2]
"""

"""
Messages:
    2 in ch1 (by u1)
    3 in dm1 (by u2)
    2 in dm2 (by u3)
"""

def test_messages_sendlater_invalid_token(clear__register3users_createdmschannels_send8messages):
    invalid_token = {'token' : encode_jwt(1,1), 'channel_id' : 1, 'message' : "Wassup dawg", 'time_sent' : int(time.time() + 2)}
    invalid_request = requests.post(f"{config.url}message/sendlater/v1", json=invalid_token)
    assert invalid_request.status_code == 403

def test_messages_sendlater_invalid_chid(clear__register3users_createdmschannels_send8messages):
    invalid_chid = {'token' : encode_jwt(1,0), 'channel_id' : 1, 'message' : "Wassup dawg", 'time_sent' : int(time.time() - 2)}
    invalid_request = requests.post(f"{config.url}message/sendlater/v1", json=invalid_chid)
    assert invalid_request.status_code == 400

def test_messages_sendlater_long_msg(clear__register3users_createdmschannels_send8messages):
    "Send a long message, should raise 400. "
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
    invalid_input = {'token' : encode_jwt(1,0), 'channel_id' : 1, 'message' : invalid_message, 'time_sent' : (int(time.time()) + 2)}


    #has 1000 chars
    valid_message = "vSO1Xx3sVDvSanODuMrDsnHqML9mur5GVGHMQbwENoQKVn7L75uiaqyc6G"\
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
    valid_input = {'token' : encode_jwt(1,0), 'channel_id' : 2, 'message' : valid_message, 'time_sent' : (int(time.time()) + 2)}

    #Do dem requests:
    invalid_request = requests.post(f"{config.url}message/sendlater/v1", json=invalid_input)
    assert invalid_request.status_code == 400

    valid_request = requests.post(f"{config.url}message/sendlater/v1", json=valid_input)
    assert valid_request.status_code == 200

def test_messages_sendlater_sent_in_past(clear__register3users_createdmschannels_send8messages):
    time_in_past = {'token' : encode_jwt(1,0), 'channel_id' : 3, 'message' : "Wassup dawg", 'time_sent' : (int(time.time())-2)}
    invalid_request = requests.post(f"{config.url}message/sendlater/v1", json=time_in_past)
    assert invalid_request.status_code == 400

def test_messages_sendlater_not_channel_member(clear__register3users_createdmschannels_send8messages):
    #test that for user 4 in channel1:
    user_not_member = {'token' : encode_jwt(4,0), 'channel_id' : 2, 'message' : "Wassup dawg", 'time_sent' : (int(time.time())+2)}
    invalid_request = requests.post(f"{config.url}message/sendlater/v1", json=user_not_member)
    assert invalid_request.status_code == 403

def test_send_message_later(clear__register3users_createdmschannels_send8messages):
    save_time = int(time.time() + 10)
    valid_token = {'token' : encode_jwt(2, 0), 'channel_id' : 1, 'message' : "Wassup dawg", 'time_sent' : save_time}
    valid_reqq = requests.post(f"{config.url}message/sendlater/v1", json=valid_token)
    assert valid_reqq.status_code == 200
    msg_data = valid_reqq.json()
    assert msg_data['message_id'] == 8

    send_5atafi = {'token': encode_jwt(1,0), 'channel_id' : 1, 'message':"hey guys"}
    msg_request = requests.post(f"{config.url}message/send/v1", json=send_5atafi)
    assert msg_request.status_code == 200
    data_5a6afi = msg_request.json() #returns {msg:msgid}
    assert data_5a6afi['message_id'] == 9

    #get messages from channel1:
    get_messages = {'token' : encode_jwt(1,0), 'channel_id' : 1, 'start' : 0}
    get_messages_req = requests.get(f"{config.url}channel/messages/v2", params=get_messages)
    assert get_messages_req.status_code == 200
    full_data = get_messages_req.json()
    assert full_data['messages'][0]['message_id'] == 9

    time.sleep(11)
    get_messages = {'token' : encode_jwt(1,0), 'channel_id' : 1, 'start' : 0}
    get_messages_req = requests.get(f"{config.url}channel/messages/v2", params=get_messages)
    assert get_messages_req.status_code == 200
    full_data = get_messages_req.json()
    assert full_data['messages'][0]['message_id'] == 8

def test_send_message_later_tag_alnum_false(clear__register3users_createdmschannels_send8messages):
    save_time = int(time.time() + 10)
    valid_token = {'token' : encode_jwt(2, 0), 'channel_id' : 1, 'message' : "@martinhernandez hello there", 'time_sent' : save_time}
    valid_reqq = requests.post(f"{config.url}message/sendlater/v1", json=valid_token)
    assert valid_reqq.status_code == 200
    msg_data = valid_reqq.json()
    assert msg_data['message_id'] == 8

def test_send_message_later_tag_alnum_true(clear__register3users_createdmschannels_send8messages):
    save_time = int(time.time() + 10)
    valid_token = {'token' : encode_jwt(2, 0), 'channel_id' : 1, 'message' : "@martinhernandez", 'time_sent' : save_time}
    valid_reqq = requests.post(f"{config.url}message/sendlater/v1", json=valid_token)
    assert valid_reqq.status_code == 200
    msg_data = valid_reqq.json()
    assert msg_data['message_id'] == 8

def test_send_message_later_tag_invalid_user(clear__register3users_createdmschannels_send8messages):
    save_time = int(time.time() + 10)
    valid_token = {'token' : encode_jwt(2, 0), 'channel_id' : 1, 'message' : "@martinhernandez0", 'time_sent' : save_time}
    valid_reqq = requests.post(f"{config.url}message/sendlater/v1", json=valid_token)
    assert valid_reqq.status_code == 200
    msg_data = valid_reqq.json()
    assert msg_data['message_id'] == 8
#########################################################################
######################MESSAGES_SENDLATERDM###############################
#########################################################################

"""
channel:
    u1 = [owner of 1,2] /-/-
    u2 = [member in 1] /-/-
    u3 = [member of 1] /-/-
"""

"""
dm:
    u1 = [member in 1] /-/-
    u2 = [creator of 1] /-/-
    u3 = [creator of 2 and member in 1] /-/-
    u4 = [member in 2]
"""

"""
Messages:
    2 in ch1 (by u1)
    3 in dm1 (by u2)
    2 in dm2 (by u3)
"""



def test_messages_sendlaterdm_invalid_token(clear__register3users_createdmschannels_send8messages):
    invalid_token = {'token' : encode_jwt(1,1), 'dm_id' : 1, 'message' : "Wassup dawg", 'time_sent' : int(time.time() + 2)}
    invalid_request = requests.post(f"{config.url}message/sendlaterdm/v1", json=invalid_token)
    assert invalid_request.status_code == 403

def test_messages_sendlaterdm_invalid_dmid(clear__register3users_createdmschannels_send8messages):
    invalid_chid = {'token' : encode_jwt(1,0), 'dm_id' : 3, 'message' : "Wassup dawg", 'time_sent' : int(time.time())}
    invalid_request = requests.post(f"{config.url}message/sendlaterdm/v1", json=invalid_chid)
    assert invalid_request.status_code == 400

def test_messages_sendlaterdm_long_msg(clear__register3users_createdmschannels_send8messages):
    "Send a long message, should raise 400. "
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
    invalid_input = {'token' : encode_jwt(1,0), 'dm_id' : 1, 'message' : invalid_message, 'time_sent' : (int(time.time()) + 2)}


    #has 1000 chars
    valid_message = "vSO1Xx3sVDvSanODuMrDsnHqML9mur5GVGHMQbwENoQKVn7L75uiaqyc6G"\
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
    valid_input = {'token' : encode_jwt(1,0), 'dm_id' : 1, 'message' : valid_message, 'time_sent' : (int(time.time()) + 2)}

    #Do dem requests:
    invalid_request = requests.post(f"{config.url}message/sendlaterdm/v1", json=invalid_input)
    assert invalid_request.status_code == 400

    valid_request = requests.post(f"{config.url}message/sendlaterdm/v1", json=valid_input)
    assert valid_request.status_code == 200

def test_messages_sendlaterdm_sent_in_past(clear__register3users_createdmschannels_send8messages):
    time_in_past = {'token' : encode_jwt(1,0), 'dm_id' : 1, 'message' : "Wassup dawg", 'time_sent' : (int(time.time())-2)}
    invalid_request = requests.post(f"{config.url}message/sendlaterdm/v1", json=time_in_past)
    assert invalid_request.status_code == 400

def test_messages_sendlaterdm_not_channel_member(clear__register3users_createdmschannels_send8messages):
    #test that for user 4 in channel1:
    user_not_member = {'token' : encode_jwt(1,0), 'dm_id' : 2, 'message' : "Wassup dawg", 'time_sent' : (int(time.time())+2)}
    invalid_request = requests.post(f"{config.url}message/sendlaterdm/v1", json=user_not_member)
    assert invalid_request.status_code == 403

def test_send_messagedm_later(clear__register3users_createdmschannels_send8messages):
    save_time = int(time.time() + 10)
    valid_token = {'token' : encode_jwt(2, 0), 'dm_id' : 1, 'message' : "Wassup dawg", 'time_sent' : save_time}
    valid_reqq = requests.post(f"{config.url}message/sendlaterdm/v1", json=valid_token)
    assert valid_reqq.status_code == 200
    msg_data = valid_reqq.json()
    assert msg_data['message_id'] == 8

    send_5atafi = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message':"hey guys"}
    msg_request = requests.post(f"{config.url}message/senddm/v1", json=send_5atafi)
    assert msg_request.status_code == 200
    data_5a6afi = msg_request.json() #returns {msg:msgid}
    assert data_5a6afi['message_id'] == 9

    #get messages from channel1:
    get_messages = {'token' : encode_jwt(1,0), 'dm_id' : 1, 'start' : 0}
    get_messages_req = requests.get(f"{config.url}dm/messages/v1", params=get_messages)
    assert get_messages_req.status_code == 200
    full_data = get_messages_req.json()
    assert full_data['messages'][0]['message_id'] == 9

    time.sleep(11)
    get_messages = {'token' : encode_jwt(1,0), 'dm_id' : 1, 'start' : 0}
    get_messages_req = requests.get(f"{config.url}dm/messages/v1", params=get_messages)
    assert get_messages_req.status_code == 200
    full_data = get_messages_req.json()
    print(full_data)
    assert full_data['messages'][0]['message_id'] == 8

