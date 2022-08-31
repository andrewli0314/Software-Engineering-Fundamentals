from os import remove
import re
from typing_extensions import IntVar
import pytest
import requests
import json
import time
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


def test_notification_channel(clear__register3users_create4channels):
    #User1 send msg in channel
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 1, 'message':"Hey guys"}  
    msg1 = requests.post(f"{config.url}message/send/v1", json=user1_message)
    #assert msg1.status_code == 200
    msg1_data = msg1.json() #returns {msg:msgid}
    assert msg1_data['message_id'] == 1

    #user 1 reacts to own channel message
    user1_react = {'token': encode_jwt(1,0), 'message_id': 1,'react_id': 1}
    user1_reaction = requests.post(f"{config.url}message/react/v1", json=user1_react)
    assert user1_reaction.status_code == 200
    user1_data = user1_reaction.json()
    assert user1_data == {}

    #User2 tags user 1 in channel
    user1_message = {'token': encode_jwt(2,0), 'channel_id' : 1, 'message':"Hey @osamaalmabrouk"}  
    msg1 = requests.post(f"{config.url}message/send/v1", json=user1_message)
    #assert msg1.status_code == 200
    msg1_data = msg1.json() #returns {msg:msgid}
    assert msg1_data['message_id'] == 2

    #user 2 reacts to user 1 channel message
    user2_react = {'token': encode_jwt(2,0), 'message_id': 1,'react_id': 1}
    user2_reaction = requests.post(f"{config.url}message/react/v1", json=user2_react)
    assert user2_reaction.status_code == 200
    user2_data = user2_reaction.json()
    assert user2_data == {}

    #getting user 1's notifications
    notif1 = {"token":encode_jwt(1, 0)}
    get_notif = requests.get(f"{config.url}notifications/get/v1", params=notif1)
    assert get_notif.status_code == 200

def test_notificationI_dms(clear__register3users_create4channels):
    #Creating dm between user 1 and user 2
    token1 = encode_jwt(1, 0)
    dm_1 = {"token": token1,"u_ids": [2]}
    create_dm_1 = requests.post(f"{config.url}dm/create/v1", json=dm_1)
    assert create_dm_1.status_code == 200

    #User 1 sends dm message to user 2
    dm_message1 = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': "Hey user 2"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json=dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 1

    #user 1 reacts to own dm message
    user1_react = {'token': encode_jwt(1,0), 'message_id': 1,'react_id': 1}
    user1_reaction = requests.post(f"{config.url}message/react/v1", json=user1_react)
    assert user1_reaction.status_code == 200
    user1_data = user1_reaction.json()
    assert user1_data == {}

    #user 2 reacts to user 1 channel message
    user2_react = {'token': encode_jwt(2,0), 'message_id': 1,'react_id': 1}
    user2_reaction = requests.post(f"{config.url}message/react/v1", json=user2_react)
    assert user2_reaction.status_code == 200
    user2_data = user2_reaction.json()
    assert user2_data == {}

    #user 2 tags user 1 in dm
    dm_message1 = {'token': encode_jwt(2,0), 'dm_id' : 1, 'message': "hi @osamaalmabrouk"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json=dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 2

    #getting user 1's notifications
    notif1 = {"token":encode_jwt(1, 0)}
    get_notif = requests.get(f"{config.url}notifications/get/v1", params=notif1)
    assert get_notif.status_code == 200

def test_notification_mix_channel_dm(clear__register3users_create4channels):
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

    #creat dm between user2 and 3
    dm_3 = {"token":encode_jwt(2,0), "u_ids":[3]}
    create_dm_3 = requests.post(f"{config.url}dm/create/v1", json = dm_3)
    assert create_dm_3.status_code == 200
    create_dm_3_result = create_dm_3.json()
    assert create_dm_3_result['dm_id'] == 3

    #user 1 send a message to channel
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 3, 'message':"hey guys"}
    msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
    msg_data = msg_request.json() #returns {msg:msgid}
    assert msg_data['message_id'] == 1

    #user2 send a message to channel 1
    user2_msg = {'token': encode_jwt(2,0), 'channel_id' : 1, 'message':"hey guys"}
    msg_request2 = requests.post(f"{config.url}message/send/v1", json=user2_msg)
    msg2_data = msg_request2.json() #returns {msg:msgid}
    assert msg2_data['message_id'] == 2

    #user 1 sends dm to user 3
    dm_message1 = {'token': encode_jwt(1,0), 'dm_id' : 2, 'message': "Hey user 3"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json = dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 3

    #user 1 sends dm to user 2
    dm_message1 = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': "Hey user 2"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json = dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 4
    
    #user 2 sends dm to user 3
    dm_message2 = {'token': encode_jwt(2,0), 'dm_id' : 3, 'message': "Hey Osama"}
    dm_sent2 = requests.post(f"{config.url}message/senddm/v1", json = dm_message2)
    assert dm_sent2.status_code == 200
    dm_sent2_result = dm_sent2.json()
    assert dm_sent2_result['message_id'] == 5

    #user 1 reacts to own message
    user1_react = {'token': encode_jwt(1,0), 'message_id': 3,'react_id': 1}
    user1_reaction = requests.post(f"{config.url}message/react/v1", json=user1_react)
    assert user1_reaction.status_code == 200
    user1_data = user1_reaction.json()
    assert user1_data == {}


    #user 3 reacts to user 1 dm message
    user3_react = {'token': encode_jwt(3,0), 'message_id': 3,'react_id': 1}
    user3_reaction = requests.post(f"{config.url}message/react/v1", json=user3_react)
    assert user3_reaction.status_code == 200
    user3_data = user3_reaction.json()
    assert user3_data == {}

    #user 2 reacts to user 1 dm message
    user2_react = {'token': encode_jwt(2,0), 'message_id': 4,'react_id': 1}
    user2_reaction = requests.post(f"{config.url}message/react/v1", json=user2_react)
    assert user2_reaction.status_code == 200
    user2_data = user2_reaction.json()
    assert user2_data == {}

    #user 1 reacts to own channel message
    user1_react = {'token': encode_jwt(1,0), 'message_id': 1,'react_id': 1}
    user1_reaction = requests.post(f"{config.url}message/react/v1", json=user1_react)
    assert user1_reaction.status_code == 200
    user1_data = user1_reaction.json()
    assert user1_data == {}

    #user 2 reacts to user 1 channel message
    user2_react = {'token': encode_jwt(2,0), 'message_id': 1,'react_id': 1}
    user2_reaction = requests.post(f"{config.url}message/react/v1", json=user2_react)
    assert user2_reaction.status_code == 200
    user2_data = user1_reaction.json()
    assert user2_data == {}

    #user 3 reacts to user 2 dm
    user3_react = {'token': encode_jwt(3,0), 'message_id': 5,'react_id': 1}
    user3_reaction = requests.post(f"{config.url}message/react/v1", json=user3_react)
    assert user3_reaction.status_code == 200
    user3_data = user3_reaction.json()
    assert user3_data == {}


    #user 3 tags user 2 in dm
    dm_message2 = {'token': encode_jwt(3,0), 'dm_id' : 3, 'message': "Hey @osamaalmabrouk0"}
    dm_sent2 = requests.post(f"{config.url}message/senddm/v1", json = dm_message2)
    assert dm_sent2.status_code == 200
    dm_sent2_result = dm_sent2.json()
    assert dm_sent2_result['message_id'] == 6


    #getting user 1's notifications
    notif1 = {"token":encode_jwt(1, 0)}
    get_notif = requests.get(f"{config.url}notifications/get/v1", params=notif1)
    assert get_notif.status_code == 200

    #getting user 2's notifications
    notif2 = {"token":encode_jwt(2, 0)}
    get_notif2 = requests.get(f"{config.url}notifications/get/v1", params=notif2)
    assert get_notif2.status_code == 200

def test_send_message_later_tag_alnum_true(clear__register3users_create4channels):
    #tagging user 2
    save_time = int(time.time())
    valid_token = {'token' : encode_jwt(2, 0), 'channel_id' : 1, 'message' : "@osamaalmabrouk0", 'time_sent' : save_time}
    valid_reqq = requests.post(f"{config.url}message/sendlater/v1", json=valid_token)
    assert valid_reqq.status_code == 200
    msg_data = valid_reqq.json()
    assert msg_data['message_id'] == 1
    time.sleep(2)
    #getting user 2's notifications
    notif2 = {"token":encode_jwt(2, 0)}
    get_notif2 = requests.get(f"{config.url}notifications/get/v1", params=notif2)
    assert get_notif2.status_code == 200

def test_notification_tagging_non_member(clear__register3users_create4channels):
    #creating dm between user1 and 2
    token1 = encode_jwt(1, 0)
    dm_1 = {"token": token1,"u_ids": [2]}
    create_dm_1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm_1.status_code == 200
    create_dm_1_result = create_dm_1.json()
    assert create_dm_1_result['dm_id'] == 1

    #tagging user 3
    dm_message1 = {'token': encode_jwt(2,0), 'dm_id' : 1, 'message': "hi @osamaalmabrouk1"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json=dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 1


def test_send_messagedm_later_tagging(clear__register3users_create4channels):

    #creating dm between user1 and 2
    token1 = encode_jwt(1, 0)
    dm_1 = {"token": token1,"u_ids": [2]}
    create_dm_1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm_1.status_code == 200
    create_dm_1_result = create_dm_1.json()
    assert create_dm_1_result['dm_id'] == 1

    #tag with send later in dms
    save_time = int(time.time() + 1)
    valid_token = {'token' : encode_jwt(2, 0), 'dm_id' : 1, 'message' : "Wassup @osamaalmabrouk", 'time_sent' : save_time}
    valid_reqq = requests.post(f"{config.url}message/sendlaterdm/v1", json=valid_token)
    assert valid_reqq.status_code == 200
    msg_data = valid_reqq.json()
    assert msg_data['message_id'] == 1

    #non alphanumeric after handle
    save_time = int(time.time() + 1)
    valid_token = {'token' : encode_jwt(2, 0), 'dm_id' : 1, 'message' : "@osamaalmabrouk Wassup", 'time_sent' : save_time}
    valid_reqq = requests.post(f"{config.url}message/sendlaterdm/v1", json=valid_token)
    assert valid_reqq.status_code == 200
    msg_data = valid_reqq.json()
    assert msg_data['message_id'] == 2

    #invalid handle
    save_time = int(time.time() + 1)
    valid_token = {'token' : encode_jwt(2, 0), 'dm_id' : 1, 'message' : "@osamaalmabrouk2 Wassup", 'time_sent' : save_time}
    valid_reqq = requests.post(f"{config.url}message/sendlaterdm/v1", json=valid_token)
    assert valid_reqq.status_code == 200
    msg_data = valid_reqq.json()
    assert msg_data['message_id'] == 3

    time.sleep(2)


    #getting user 2's notifications
    notif2 = {"token":encode_jwt(1, 0)}
    get_notif2 = requests.get(f"{config.url}notifications/get/v1", params=notif2)
    assert get_notif2.status_code == 200