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

def test_not_member_channel(clear__register3users_create4channels):
    
    #User1 send msg in channel 2
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 2, 'message':"Comp1531 Team Hello"} 
    msg1 = requests.post(f"{config.url}message/send/v1", json=user1_message)
    assert msg1.status_code == 200

    #User2 tries to  search for that message in channel 2
    search1 = {'token':encode_jwt(2, 0), 'query_str':"Comp"}
    search_result =  requests.get(f"{config.url}search/v1", params= search1)
    assert search_result.status_code == 200

def test_not_member_dm(clear__register3users_create4channels):
    #creating dm between user1 and 3
    token1 = encode_jwt(1, 0)
    dm_1 = {"token": token1,"u_ids": [3]}
    create_dm_1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm_1.status_code == 200
    create_dm_1_result = create_dm_1.json()
    assert create_dm_1_result['dm_id'] == 1

    #user 1 sends dm to user 3
    dm_message1 = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': "Hey user 3, hows your assignment?"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json = dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 1

    #user2 searches for message in user 1 and user 3's dm
    search1 = {'token':encode_jwt(2, 0), 'query_str':"user 3"}
    search_result =  requests.get(f"{config.url}search/v1", params= search1)
    assert search_result.status_code == 200

def test_search_error_more_than_1000_char(clear__register3users_create4channels):
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
    
    #User2 send msg in channel
    user1_message = {'token': encode_jwt(2,0), 'channel_id' : 3, 'message':"Hey guys"} 
    msg1 = requests.post(f"{config.url}message/send/v1", json=user1_message)
    assert msg1.status_code == 200

    #User 2 search with invalid length
    search1 = {'token':encode_jwt(2, 0), 'query_str':invalid_message}
    search_result =  requests.get(f"{config.url}search/v1", params= search1)
    assert search_result.status_code == 400

def test_search_error_less_than_1(clear__register3users_create4channels):
    #User1 send msg in channel
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 1, 'message':"Hey guys"}  
    msg1 = requests.post(f"{config.url}message/send/v1", json=user1_message)
    assert msg1.status_code == 200

    search1 = {'token':encode_jwt(1, 0), 'query_str':""}
    search_result =  requests.get(f"{config.url}search/v1", params= search1)
    assert search_result.status_code == 400

def test_search_channel(clear__register3users_create4channels):
    #User1 send msg in channel
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 1, 'message':"Hey guys"}  
    msg1 = requests.post(f"{config.url}message/send/v1", json=user1_message)
    assert msg1.status_code == 200

    #User2 send message in channel
    user2_message = {'token': encode_jwt(2,0), 'channel_id' : 1, 'message':"hello everybody"}  
    msg2 = requests.post(f"{config.url}message/send/v1", json=user2_message)
    assert msg2.status_code == 200

    #user3 send message in channel
    user3_message = {'token': encode_jwt(2,0), 'channel_id' : 1, 'message':"I'm in the kitchen right now"}  
    msg3 = requests.post(f"{config.url}message/send/v1", json=user3_message)
    assert msg3.status_code == 200

    #user 1 sends message again
    user1_message2 = {'token': encode_jwt(1,0), 'channel_id' : 1, 'message':"okay, see ya later"}  
    msg1_2 = requests.post(f"{config.url}message/send/v1", json=user1_message2)
    assert msg1_2.status_code == 200
   
    search1 = {'token':encode_jwt(1, 0), 'query_str':"He"}
    search_result =  requests.get(f"{config.url}search/v1", params= search1)
    assert search_result.status_code == 200

def test_search_dms(clear__register3users_create4channels):
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

    #user 3 replys to user 1
    dm_message2 = {'token': encode_jwt(3,0), 'dm_id' : 2, 'message': "Hello! How are you doing?"}
    dm_sent2 = requests.post(f"{config.url}message/senddm/v1", json = dm_message2)
    assert dm_sent2.status_code == 200
    dm_sent2_result = dm_sent2.json()
    assert dm_sent2_result['message_id'] == 2
    
    #User2 sends dm to user 1
    dm_message3 = {'token': encode_jwt(2,0), 'dm_id' : 1, 'message': "Hi User 1, There has been a change in schedule"}
    dm_sent3 = requests.post(f"{config.url}message/senddm/v1", json = dm_message3)
    assert dm_sent3.status_code == 200
    dm_sent3_result = dm_sent3.json()
    assert dm_sent3_result['message_id'] == 3

    #User 1 replys to user 2
    dm_message4 = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': "Understood, Thanks for the heads up!!!!"}
    dm_sent4 = requests.post(f"{config.url}message/senddm/v1", json = dm_message4)
    assert dm_sent4.status_code == 200
    dm_sent4_result = dm_sent4.json()
    assert dm_sent4_result['message_id'] == 4

    #search for user 1's dms with "He"
    search1 = {'token':encode_jwt(1, 0), 'query_str':"He"}
    search_result =  requests.get(f"{config.url}search/v1", params= search1)
    assert search_result.status_code == 200

def test_channels_dm_mix(clear__register3users_create4channels):
    #creating dm between user1 and 2
    token1 = encode_jwt(1, 0)
    dm_1 = {"token": token1,"u_ids": [2]}
    create_dm_1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm_1.status_code == 200
    create_dm_1_result = create_dm_1.json()
    assert create_dm_1_result['dm_id'] == 1

    #creat dm between user2 and 3
    dm_2 = {"token": encode_jwt(2, 0), "u_ids":[3]}
    create_dm_2 = requests.post(f"{config.url}dm/create/v1", json = dm_2)
    assert create_dm_1.status_code == 200
    create_dm_2_result = create_dm_2.json()
    assert create_dm_2_result['dm_id'] == 2

    #User 1 sends dm to  user 2
    dm_message1 = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': "Hi User 2, wanna go to the beach around 1pm? Maybe with user 3 as well?"}
    dm_sent1 = requests.post(f"{config.url}message/senddm/v1", json = dm_message1)
    assert dm_sent1.status_code == 200
    dm_sent1_result = dm_sent1.json()
    assert dm_sent1_result['message_id'] == 1

    #User2 replys with dm to user 1
    dm_message2 = {'token': encode_jwt(2,0), 'dm_id' : 1, 'message': "sure, why not. Lets see if user 3 wants to come"}
    dm_sent2 = requests.post(f"{config.url}message/senddm/v1", json = dm_message2)
    assert dm_sent2.status_code == 200
    dm_sent2_result = dm_sent2.json()
    assert dm_sent2_result['message_id'] == 2

    #User 1 replys in dm with user 2
    dm_message3 = {'token': encode_jwt(1,0), 'dm_id' : 1, 'message': "yeah, ill chuck a message on the channel"}
    dm_sent3 = requests.post(f"{config.url}message/senddm/v1", json = dm_message3)
    assert dm_sent3.status_code == 200
    dm_sent3_result = dm_sent3.json()
    assert dm_sent3_result['message_id'] == 3

    #User 1 sends message in channel
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 1, 'message':"Hey User 3, U keen to join me and user 2 at the beach probs around 1pm?"}  
    msg1 = requests.post(f"{config.url}message/send/v1", json=user1_message)
    msg_data1 = msg1.json()
    assert msg_data1['message_id'] == 4

    #User 3 replys
    user3_message = {'token': encode_jwt(3,0), 'channel_id' : 1, 'message':"Sure, I'll see you and user 2 there at 1pm"}  
    msg2 = requests.post(f"{config.url}message/send/v1", json=user3_message)
    msg_data2 = msg2.json()
    assert msg_data2['message_id'] == 5

    #User 3 Dm's User 2
    dm_message4 = {'token': encode_jwt(3,0), 'dm_id' : 2, 'message': "Can you bring the surfboard? I'll bring some drinks"}
    dm_sent4 = requests.post(f"{config.url}message/senddm/v1", json = dm_message4)
    assert dm_sent4.status_code == 200
    dm_sent4_result = dm_sent4.json()
    assert dm_sent4_result['message_id'] == 6

    #User 2 replys to User 3
    dm_message5 = {'token': encode_jwt(2,0), 'dm_id' : 2, 'message': "sure, no problemo see you then!"}
    dm_sent5 = requests.post(f"{config.url}message/senddm/v1", json = dm_message5)
    assert dm_sent5.status_code == 200
    dm_sent5_result = dm_sent5.json()
    assert dm_sent5_result['message_id'] == 7

    #User 2 search for message with 're' in it
    search1 = {'token':encode_jwt(2, 0), 'query_str':"Re"}
    search_result =  requests.get(f"{config.url}search/v1", params= search1)
    assert search_result.status_code == 200

    #User 2 search for message with 'er' in it
    search2 = {'token':encode_jwt(2, 0), 'query_str':"eR"}
    search_result_2 =  requests.get(f"{config.url}search/v1", params= search2)
    assert search_result_2.status_code == 200

    #user 2 search for all messages with letter 'e'
    search3 = {'token':encode_jwt(2, 0), 'query_str':"E"}
    search_result_3 =  requests.get(f"{config.url}search/v1", params= search3)
    assert search_result_3.status_code == 200

def test_is_user_reacted_channel(clear__register3users_create4channels):
    """make 10 messages, assert end = 75 since start is 25"""
    for i in range(1, 101):
        user1_message = {'token': encode_jwt(1,0), 'channel_id' : 2, 'message':"hey guys"}
        msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
        assert msg_request.status_code == 200
        msg_data = msg_request.json() #returns {msg:msgid}
        assert msg_data['message_id'] == i
       
    #user 1 reaction
    for i in range(1, 101):
        user1_react = {'token': encode_jwt(1,0), 'message_id': i,'react_id': 1}
        user1_reaction = requests.post(f"{config.url}message/react/v1", json=user1_react)
        assert user1_reaction.status_code == 200
        user1_data = user1_reaction.json()
        assert user1_data == {}

    #search for user 1's dms with "He"
    search1 = {'token':encode_jwt(1, 0), 'query_str':"He"}
    search_result =  requests.get(f"{config.url}search/v1", params= search1)
    assert search_result.status_code == 200

def test_is_user_unreacted_channel(clear__register3users_create4channels):
    """make 10 messages, assert end = 75 since start is 25"""
    for i in range(1, 101):
        user1_message = {'token': encode_jwt(1,0), 'channel_id' : 2, 'message':"hey guys"}
        msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
        assert msg_request.status_code == 200
        msg_data = msg_request.json() #returns {msg:msgid}
        assert msg_data['message_id'] == i
        
    #user 1 reaction
    for i in range(1, 101):
        user1_react = {'token': encode_jwt(1,0), 'message_id': i,'react_id': 1}
        user1_reaction = requests.post(f"{config.url}message/react/v1", json=user1_react)
        assert user1_reaction.status_code == 200
        user1_data = user1_reaction.json()
        assert user1_data == {}

    #search for user 1's msg with "He"
    search1 = {'token':encode_jwt(1, 0), 'query_str':"He"}
    search_result =  requests.get(f"{config.url}search/v1", params= search1)
    assert search_result.status_code == 200

    #user 1 unreaction
    for i in range(1, 101):
        user1_react = {'token': encode_jwt(1,0), 'message_id': i,'react_id': 1}
        user1_reaction = requests.post(f"{config.url}message/unreact/v1", json=user1_react)
        assert user1_reaction.status_code == 200
        user1_data = user1_reaction.json()
        assert user1_data == {}

    #search for user 1's msg with "He"
    search1 = {'token':encode_jwt(1, 0), 'query_str':"He"}
    search_result =  requests.get(f"{config.url}search/v1", params= search1)
    assert search_result.status_code == 200

def test_is_user_reacted_dm(clear__register3users_create4channels):
    #creating dm between user1 and 2
    token1 = encode_jwt(1, 0)
    dm_1 = {"token": token1,"u_ids": [2]}
    create_dm_1 = requests.post(f"{config.url}dm/create/v1", json = dm_1)
    assert create_dm_1.status_code == 200
    create_dm_1_result = create_dm_1.json()
    assert create_dm_1_result['dm_id'] == 1
    
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

    #search for user 1's dms with "He"
    search1 = {'token':encode_jwt(1, 0), 'query_str':"He"}
    search_result =  requests.get(f"{config.url}search/v1", params= search1)
    assert search_result.status_code == 200

    #user 1 unreacts
    for i in range(1, 52):
        user1_react = {'token': encode_jwt(1,0), 'message_id': i,'react_id': 1}
        user1_reaction = requests.post(f"{config.url}message/unreact/v1", json=user1_react)
        assert user1_reaction.status_code == 200
        user1_data = user1_reaction.json()
        assert user1_data == {}
    
    #search for user 1's dms with "He"
    search1 = {'token':encode_jwt(1, 0), 'query_str':"He"}
    search_result =  requests.get(f"{config.url}search/v1", params= search1)
    assert search_result.status_code == 200