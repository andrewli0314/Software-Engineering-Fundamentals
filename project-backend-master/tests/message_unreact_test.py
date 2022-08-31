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


def test_invalid_messageID_error(clear__register3users_create4channels):
    #user 1 send a message
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

    #invalid message id given
    user1_react = {'token': encode_jwt(1,0), 'message_id': 4,'react_id': 1}
    user1_reaction = requests.post(f"{config.url}message/unreact/v1", json=user1_react)
    assert user1_reaction.status_code == 400

def test_invalid_reactID_given(clear__register3users_create4channels):
    #user 1 send a message
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

    #invlaid react id given
    user1_react = {'token': encode_jwt(1,0), 'message_id': 4,'react_id': 10}
    user1_reaction = requests.post(f"{config.url}message/unreact/v1", json=user1_react)
    assert user1_reaction.status_code == 400

def test_user_has_not_reacted_channel(clear__register3users_create4channels):
    #user 1 send a message
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

    #User1 unreacting to message not previously reacted to
    user1_react = {'token': encode_jwt(1,0), 'message_id': 1,'react_id': 1}
    user1_reaction = requests.post(f"{config.url}message/unreact/v1", json=user1_react)
    assert user1_reaction.status_code == 400

def test_user_has_not_reacted_dm(clear__register3users_create4channels):
     #creating dm between user1 and 2
    token1 = encode_jwt(1, 0)
    dm_1 = {"token": token1,"u_ids": [2]}
    create_dm_1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm_1.status_code == 200
    create_dm_1_result = create_dm_1.json()
    assert create_dm_1_result['dm_id'] == 1

    #user 1 sends dm to user 3
    dm_message1 = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': "Hey user 3"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json = dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 1

    #user 1 unreacts to own message
    user1_unreact = {'token': encode_jwt(1,0), 'message_id': 1,'react_id': 1}
    user1_unreaction = requests.post(f"{config.url}message/unreact/v1", json=user1_unreact)
    assert user1_unreaction.status_code == 400

def test_user_not_part_of_channel(clear__register3users_create4channels):
    #user 1 send a message to channel 2
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 2, 'message':"hey guys"}
    msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
    #assert msg_request.status_code == 200
    msg_data = msg_request.json() #returns {msg:msgid}
    assert msg_data['message_id'] == 1

    #invalid message id given
    user1_react = {'token': encode_jwt(2,0), 'message_id': 1,'react_id': 1}
    user1_reaction = requests.post(f"{config.url}message/unreact/v1", json=user1_react)
    assert user1_reaction.status_code == 400

def test_user_not_in_dm(clear__register3users_create4channels):
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

    #user 1 sends dm to user 3
    dm_message1 = {'token': encode_jwt(1,0), 'dm_id' : 2, 'message': "Hey user 3"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json = dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 1

    #user 2 reacts to message btwn user 1 and 3
    user2_react = {'token': encode_jwt(2,0), 'message_id': 1,'react_id': 1}
    user2_reaction = requests.post(f"{config.url}message/unreact/v1", json=user2_react)
    assert user2_reaction.status_code == 400

def test_react_channel(clear__register3users_create4channels):

    #user 1 send a message
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 3, 'message':"hey guys"}
    msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
    msg_data = msg_request.json() #returns {msg:msgid}
    assert msg_data['message_id'] == 1

    #user2 send a message to channel 1
    user2_msg = {'token': encode_jwt(2,0), 'channel_id' : 1, 'message':"hey guys"}
    msg_request2 = requests.post(f"{config.url}message/send/v1", json=user2_msg)
    msg2_data = msg_request2.json() #returns {msg:msgid}
    assert msg2_data['message_id'] == 2

    #user 1 reacts to own message
    user1_react = {'token': encode_jwt(1,0), 'message_id': 1,'react_id': 1}
    user1_reaction = requests.post(f"{config.url}message/react/v1", json=user1_react)
    assert user1_reaction.status_code == 200
    user1_data = user1_reaction.json()
    assert user1_data == {}

    #user 2 reacts to user 1 message
    user2_react = {'token': encode_jwt(2,0), 'message_id': 1,'react_id': 1}
    user2_reaction = requests.post(f"{config.url}message/react/v1", json=user2_react)
    assert user2_reaction.status_code == 200
    user2_data = user1_reaction.json()
    assert user2_data == {}

def test_unreact_channel(clear__register3users_create4channels):
    #user 1 send a message
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 3, 'message':"hey guys"}
    msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
    msg_data = msg_request.json() #returns {msg:msgid}
    assert msg_data['message_id'] == 1

    #user2 send a message to channel 1
    user2_msg = {'token': encode_jwt(2,0), 'channel_id' : 1, 'message':"hey guys"}
    msg_request2 = requests.post(f"{config.url}message/send/v1", json=user2_msg)
    msg2_data = msg_request2.json() #returns {msg:msgid}
    assert msg2_data['message_id'] == 2

    #user 1 reacts to own message
    user1_react = {'token': encode_jwt(1,0), 'message_id': 1,'react_id': 1}
    user1_reaction = requests.post(f"{config.url}message/react/v1", json=user1_react)
    assert user1_reaction.status_code == 200
    user1_data = user1_reaction.json()
    assert user1_data == {}

    #user 1 unreacts to own message
    user1_react = {'token': encode_jwt(1,0), 'message_id': 1,'react_id': 1}
    user1_reaction = requests.post(f"{config.url}message/unreact/v1", json=user1_react)
    assert user1_reaction.status_code == 200
    user1_data = user1_reaction.json()
    assert user1_data == {}

def test_unreact_dm(clear__register3users_create4channels):
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

    #user 1 sends dm to user 3
    dm_message1 = {'token': encode_jwt(1,0), 'dm_id' : 2, 'message': "Hey user 3"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json = dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 1

    #user 1 reacts to own message
    user1_react = {'token': encode_jwt(1,0), 'message_id': 1,'react_id': 1}
    user1_reaction = requests.post(f"{config.url}message/react/v1", json=user1_react)
    assert user1_reaction.status_code == 200
    user1_data = user1_reaction.json()
    assert user1_data == {}

    #user 3 reacts to user 1 message
    user3_react = {'token': encode_jwt(3,0), 'message_id': 1,'react_id': 1}
    user3_reaction = requests.post(f"{config.url}message/react/v1", json=user3_react)
    assert user3_reaction.status_code == 200
    user3_data = user3_reaction.json()
    assert user3_data == {}

    #user 1 unreacts to own message
    user1_unreact = {'token': encode_jwt(1,0), 'message_id': 1,'react_id': 1}
    user1_unreaction = requests.post(f"{config.url}message/unreact/v1", json=user1_unreact)
    assert user1_unreaction.status_code == 200
    user1_data = user1_unreaction.json()
    assert user1_data == {}

def test_unreact_mix_channel_dm(clear__register3users_create4channels):
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

    #user 3 unreacts to user 1 dm message
    user3_unreact = {'token': encode_jwt(3,0), 'message_id': 3,'react_id': 1}
    user3_unreaction = requests.post(f"{config.url}message/unreact/v1", json=user3_unreact)
    assert user3_unreaction.status_code == 200
    user3_data = user3_unreaction.json()
    assert user3_data == {}

    #user 1 unreacts to own dm message wiht user 3
    user1_unreact = {'token': encode_jwt(1,0), 'message_id': 3,'react_id': 1}
    user1_unreaction = requests.post(f"{config.url}message/unreact/v1", json=user1_unreact)
    assert user1_unreaction.status_code == 200
    user1_data = user1_unreaction.json()
    assert user1_data == {}

    #user 1 unreacts to own channel message
    user1_unreact = {'token': encode_jwt(1,0), 'message_id': 1,'react_id': 1}
    user1_unreaction = requests.post(f"{config.url}message/unreact/v1", json=user1_unreact)
    assert user1_unreaction.status_code == 200
    user1_data = user1_unreaction.json()
    assert user1_data == {}

    #user 2 unreacts to user 1 channel message
    user2_react = {'token': encode_jwt(2,0), 'message_id': 1,'react_id': 1}
    user2_reaction = requests.post(f"{config.url}message/unreact/v1", json=user2_react)
    assert user2_reaction.status_code == 200
    user2_data = user1_reaction.json()
    assert user2_data == {}

