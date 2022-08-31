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
            "name_first": "Andres",
            "name_last": "Iniesta"
            }

user_3 =  {
            "email": "someemailadressss@gmail.com",
            "password": "dasdasdasdlakmLN",
            "name_first": "suii",
            "name_last": "suii"
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

def test_channelleave_invalid_token(clear__register3users_create4channels):
    #testing for invalid session
    """User1 will leave channel1, must return 403"""
    ch1_leave = {'token': encode_jwt(1,1), 'channel_id' : 1, 'message':"hello"}
    request = requests.post(f"{config.url}message/send/v1", json=ch1_leave)
    assert request.status_code == 403
    #testing for invalid id
    ch1_leave2 = {'token': encode_jwt(4,0), 'channel_id' : 1, 'message':"bye"}
    request2 = requests.post(f"{config.url}message/send/v1", json=ch1_leave2)
    assert request2.status_code == 403

def test_channelleave_invalid_channel(clear__register3users_create4channels):
   #test invalid channel
    """Leave channel_is 5, must raise 400"""
    ch5_leave = {'token': encode_jwt(1,0), 'channel_id' : 5, 'message':"comp1531"}
    request = requests.post(f"{config.url}message/send/v1", json=ch5_leave)
    assert request.status_code == 400

def test_send_message_not_member(clear__register3users_create4channels):
    #invalid memeber
    "let user3 send msg to channel 3"
    user3_message = {'token': encode_jwt(3,0), 'channel_id' : 3, 'message':"hey guys"}
    invalid_request = requests.post(f"{config.url}message/send/v1", json=user3_message)
    assert invalid_request.status_code == 403

def test_send_message_long_message(clear__register3users_create4channels):
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
    
    invalid_dic = {'token': encode_jwt(1,0), 'channel_id' : 1, 'message':invalid_message}
    valid_dic = {'token': encode_jwt(1,0), 'channel_id' : 1, 'message':valid_message}

    invalid_request = requests.post(f"{config.url}message/send/v1", json=invalid_dic)
    assert invalid_request.status_code == 400

    valid_request = requests.post(f"{config.url}message/send/v1", json=valid_dic)
    assert valid_request.status_code == 200

def test_send_message(clear__register3users_create4channels):
    #testing sending message user 1 send a message
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 3, 'message':"hey guys"}
    msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
    assert msg_request.status_code == 200
    msg_data = msg_request.json() #returns {msg:msgid}
    assert msg_data['message_id'] == 1

    #user2 send a message to channel 1
    user2_msg = {'token': encode_jwt(2,0), 'channel_id' : 1, 'message':"hey guys"}
    msg_request2 = requests.post(f"{config.url}message/send/v1", json=user2_msg)
    assert msg_request2.status_code == 200
    msg2_data = msg_request2.json() #returns {msg:msgid}
    assert msg2_data['message_id'] == 2

def test_send_message_tag_non_alnum(clear__register3users_create4channels):
    #testing sending message user 1 send a message
    user1_message = {'token': encode_jwt(1,0), 'channel_id' : 3, 'message':"@osamaalalmabrouk0 hello there"}
    msg_request = requests.post(f"{config.url}message/send/v1", json=user1_message)
    assert msg_request.status_code == 200
    msg_data = msg_request.json() #returns {msg:msgid}
    assert msg_data['message_id'] == 1