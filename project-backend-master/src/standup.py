import time
import threading
from src.error import InputError, AccessError
from src.data_store import data_store
from src.channels import is_valid_token
from src.channel import is_owner, is_valid, is_member, channel_index, is_global_owner
from src.helpers import decode_jwt
from src.message import message_send_v1
import datetime
from datetime import datetime
from datetime import timezone

def standup_msg(token, channel_id, auth_user_id, channel):
    store = data_store.get()
    channel_list = store['channels']
    dm_list = store['dm']
    message_id = 0
    for ch in channel_list:
        message_id += len(ch['messages'])
    for dm in dm_list:
        message_id += len(dm['messages'])
    message_id+=1
    time_created = int(time.time())
    if channel['standup'][0]['message'] != '':
        stored_message = channel['standup'][0]['message']
        message_dic = {
            'message_id' : message_id, 
            'u_id' : auth_user_id, 
            'message' : stored_message, 
            'time_created' : time_created
        }
        channel['messages'].insert(0, message_dic)
    channel['standup'].remove(channel['standup'][0])

def standup_start_v1(token, channel_id, length):
    """
    A user in a channel start standup in X length seconds
    
    Arguments:
        token ([string]): an authorisation hash that belongs to a global user
        channel_id: the id number of the channel
        length: an integer, 'X' seconds which  standup will last

    Exceptions:
        invalid token
        invali channel_id
        length is negative
        an active standup is currently running in the channel
        channel_is is valid but auth user is not the member of the channel

    Return Value:
        finished time
    """
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    
    if not is_valid_token(auth_user_id, session_id):
        raise AccessError(description = "Invalid Token")
    if not is_valid(channel_id):
        raise InputError(description="Invalid channel_id")
    if length < 0:
        raise InputError(description="Invalid length of second(s).")
    if not is_member(auth_user_id, channel_id):
        raise AccessError(description="Auth user is not a member of given channel.")
    active = standup_active_v1(token, channel_id)
    if active['is_active'] == True:
        raise InputError(description="An active standup is currently running in the channel.")
    
    time_create = int(datetime.now(timezone.utc).timestamp())
    time_finish = time_create + length
    
    store = data_store.get()
    store_channel_list = store['channels']
    idx = channel_index(channel_id)

    standup_dic = {'active' : True, 'u_id' : auth_user_id, 'message' : '', 'ending_time':time_finish}
    store_channel_list[idx]['standup'].insert(0, standup_dic)

    add_msg = threading.Timer(length, standup_msg, [token, channel_id, auth_user_id, store_channel_list[idx]])
    add_msg.start()
      
    return {'time_finish': time_finish} 
    
def standup_active_v1(token, channel_id):
    """
    to check the given channel has standup actived or not
    
    Arguments:
        token ([string]): an authorisation belongs to a user who start the stand up
        channel_id: the id number of the channel

    Exceptions:
        invalid token
        invali channel_id
        channel_is is valid but auth user is not the member of the channel

    Return Value:
        finished time as timestamp
    """
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    if not is_valid_token(auth_user_id, session_id):
        raise AccessError(description = "Invalid Token")
    if not is_valid(channel_id):
        raise InputError(description="Invalid channel_id")
    if not is_member(auth_user_id, channel_id):
        raise AccessError(description="Auth user is not a member of given channel.")
    
    active = False
    finishtime = None
    store = data_store.get()
    store_channel_list = store['channels']
    idx = channel_index(channel_id)
    standups = store_channel_list[idx]['standup']
    
    if standups == []:
        active = False
        finishtime = None
    else:
        active = True
        finishtime = standups[0]['ending_time']
        
    return {
        'is_active': active,
        'time_finish': finishtime
    }

def standup_send_v1(token, channel_id, message):
    """
    A user in a channel send message in standup mode in X length seconds
    
    Arguments:
        token ([string]): an authorisation of a user belongs to the channel want to send message
        channel_id: the id number of the channel
        message: an string, message send under standup which will be buffered

    Exceptions:
        invalid token
        invali channel_id
        message length is over 1000 characters
        no active standup is currently running in the channel
        channel_is is valid but auth user is not the member of the channel

    Return Value:
        no need return any
    """
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    
    if not is_valid_token(auth_user_id, session_id):
        raise AccessError(description = "Invalid Token")
    if not is_valid(channel_id):
        raise InputError(description="Invalid channel_id")
    if len(message) > 1000:
        raise InputError(description="Invalid length of message")
    if not is_member(auth_user_id, channel_id):
        raise AccessError(description="Auth user is not a member of given channel.")
    active = standup_active_v1(token, channel_id)
    if active['is_active'] != True:
        raise InputError(description="No active standup is currently running in the channel.")
    
    msg_list = ''
    user_handle = ''   
    store = data_store.get()
    user_list = store['users']
    store_channel_list = store['channels']
    idx = channel_index(channel_id)
    for user in user_list:
        if user[0]['u_id'] == auth_user_id:
            user_handle = user[0]['handle_str']   
    if store_channel_list[idx]['standup'][0]['message'] == '':
        msg_list = user_handle + ': ' + message
    else:
        msg_list = '\n' + user_handle + ': ' + message
    
    store_channel_list[idx]['standup'][0]['message'] += msg_list
    
    return {}










