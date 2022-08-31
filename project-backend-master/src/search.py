from src.channel import is_member
from src.dm import is_dm_member
from src.data_store import data_store
from src.helpers import decode_jwt
from src.error import InputError
def search_v1(token, query_str):
    '''
    Given a query string, return a collection of messages in all of the channels/DMs 
    that the user has joined that contain the query.

    Inputs: token, query_str
    Returns: List of all messages containing the query string in all dms and channels that the user is a member of

    Input error:
        -If length of query_str is < 1 or > 1000 characters
    '''
    #Error checking
    if len(query_str) < 1 or len(query_str) > 1000:
        raise InputError(description="Length of query is too short or too long")
    msg_list=[]
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    store = data_store.get()
    dm_list = store['dm'] 
    channel_list = store['channels']
    dm_id = 0
    #Search through dms for messages containing query string
    for dm in dm_list:
        for dm_message in dm['messages']:
            dm_id = dm['dm_id']
            if is_dm_member(auth_user_id, dm_id):
                if query_str.lower() in dm_message['message'].lower():
                    msg_list.append(dm_message)
    #Search through channels for messages containing query string
    channel_id = 0
    for channel in channel_list:
        for x in range(len(channel['messages'])):
            if query_str.lower() in channel['messages'][x]['message'].lower():
                channel_id = channel['channel_id']
                if is_member(auth_user_id, channel_id):
                    msg_list.append(channel['messages'][x])
    msg_list = sorted(msg_list, key=lambda x: x['time_created'], reverse=True)
    for message in msg_list:
        for x in range(len(message['reacts'])):
            if auth_user_id not in message['reacts'][x-1]['u_id']:
                message['reacts'][x-1]['is_this_user_reacted'] = False
                #print(message['reacts'][0])
            else:
                message['reacts'][x-1]['is_this_user_reacted'] = True
                #print(message['reacts'][0])
    return {'messages': msg_list}

