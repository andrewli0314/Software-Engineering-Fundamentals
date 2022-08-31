from src.error import InputError, AccessError
from src.data_store import data_store
from src.channels import is_valid_token
from src.channel import is_owner, is_valid, is_member, channel_index, is_global_owner
from src.helpers import decode_jwt
from src.dm import is_dm_member, is_valid_dm, message_send_dm_v1, is_dm_creator
import time
import threading

#Message send helper funciton:
def send_message_later(message_dic, sleep_time, channel_id, auth_user_id):
    store = data_store.get()
    time.sleep(sleep_time)
    channel_list = store['channels']
    idx = channel_index(channel_id)
    channel_list[idx]['messages'].insert(0, message_dic)
    channel_name = channel_list[idx]['name']

    #shoot a message if a tag is there:
    message = message_dic['message']
    message_pre = ""
    if len(message) < 20:
        for i in range(len(message)):
            message_pre += message[i]
    else:
        for i in range(0, 20):
            message_pre += message[i]

    mentioned_handles = []
    mentioned_name = ""
    for i in range (len(message)):
        if message[i] == "@":
            i += 1
            mentioned_name = ""
            while message[i].isalnum() and i != len(message)-1:
                mentioned_name += message[i]
                i += 1
            if message[i].isalnum():
                mentioned_name += message[i]
            mentioned_handles.append(mentioned_name)
    
    

    auth_handle = ""
    #get auth_handle:
    for user in store['users']:
        if user[0]['u_id'] == auth_user_id:
            auth_handle = user[0]['handle_str']

    for handle in mentioned_handles:
        if get_u_id(handle) != -1 and is_member(get_u_id(handle), channel_id):
            notification = f"{auth_handle} tagged you in {channel_name}: {message_pre}"
            for user in store['users']:
                if user[0]['handle_str'] == handle:
                    user[1]['notifications'].insert(0,notification)
    
    #print(f"Inserted {message_dic} in channel_id : {channel_id}\n")

#gets the u_id by having the handle_str only:
def get_u_id(handle_str):
    store = data_store.get()
    users_list = store['users']

    for user in users_list:
        if user[0]['handle_str'] == handle_str:
            return user[0]['u_id']
    
    return -1

def message_send_v1(token, channel_id, message):

    """Send a message from authorised_user to the channel specified by channel_id.
    Note: Each message should have it's own unique ID. I.E. No messages should share
    an ID with another message, even if that other message is in a different channel.

    Arguments:
        token (int) - string
        channel_id (int) - The id of the channel the message was sent in
        message (str) - The message contents

    Exceptions:
        InputError - Channel id does not have a reference to a valid channel
        InputError - Message is more than 1000 characters
        AccessError - Valid channel id and authorised user is not a member in the channel

    Return Value:
        Returns message_id on successfully sending a message
    """

    #Error checks
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    if not is_valid_token(auth_user_id, session_id):
        raise AccessError (description="Invalid Token")
    if not is_valid(channel_id):
        raise InputError(description="Channel_id does not refer to a valid channel")
    if len(message) < 1 or len(message) > 1000:
        raise InputError(description="Invalid length of message")
    if is_valid(channel_id) and not is_member(auth_user_id, channel_id):
        raise AccessError (description="Authorised user is not a member of the channel")
    # adding message to channel and assigning channel ID
    store = data_store.get()
    store_channel_list = store['channels']
    dm_list = store['dm']
    threads = store['threads']
    message_id = 0
    for channel in store_channel_list:
        message_id += len(channel['messages'])
    for dm in dm_list:
        message_id += len(dm['messages'])
    message_id+=len(threads)
    message_id += 1
    react_dict_1 = {'react_id':1, 'u_id':[], 'is_this_user_reacted':False}
    idx = channel_index(channel_id)
    time_created = int(time.time())
    channel_name = store_channel_list[idx]['name']

    #Before sending anything, shoot some notifications if a user handle is mentioned:
    message_pre = ""
    if len(message) < 20:
        for i in range(len(message)):
            message_pre += message[i]
    else:
        for i in range(0, 20):
            message_pre += message[i]
    mentioned_handles = []
    mentioned_name = ""
    for i in range (len(message)):
        if message[i] == "@":
            i += 1
            mentioned_name = ""
            while message[i].isalnum() and i != len(message)-1:
                mentioned_name += message[i]
                i += 1
            if message[i].isalnum():
                mentioned_name += message[i]
            mentioned_handles.append(mentioned_name)
    auth_handle = ""
    #get auth_handle:
    for user in store['users']:
        if user[0]['u_id'] == auth_user_id:
            auth_handle = user[0]['handle_str']

    for handle in mentioned_handles:
        if get_u_id(handle) != -1 and is_member(get_u_id(handle), channel_id):
            notification = f"{auth_handle} tagged you in {channel_name}: {message_pre}"
            for user in store['users']:
                if user[0]['handle_str'] == handle:
                    user[1]['notifications'].insert(0,notification)

    message_dic = {'message_id' : message_id, 'u_id' : auth_user_id, 'message' : message, 'time_created' : time_created,  'reacts':[react_dict_1], 'is_pinned' : False}
    store_channel_list[idx]['messages'].insert(0, message_dic)
    return {'message_id' : message_id}

def message_edit_v1(token,message_id, message):

    """Given a message, update its text with new text. If the new message is an empty string, the message is deleted.

    Arguments:
        token (string) - string
        message_id (int) - The user's message id
        message (str) - The message contents

    Exceptions:
        InputError - Length of message is over 1000 characters
        InputError - message_id does not refer to a valid message within a channel
        AccessError when none of the following are true:
            - Message with message_id was sent by the authorised user making this request
            - The authorised user has owner access in the channel 
            - The authorised user has owner access in the channel 
            - The authorised user has owner access in the channel 

    Return Value:
       {}
    """

    #Getting user details
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    #getting datastore
    store = data_store.get()
    store_channel_message = store['channels']
    if not is_valid_token(auth_user_id, session_id):
        raise AccessError (description="Invalid Token")
    # if not is_valid(channel_id):
    #     raise InputError(description="Channel_id does not refer to a valid channel")
            #error checks
    
    if len(message) < 1 or len(message) > 1000:
        raise InputError(description="Invalid length of message")
    channel_id = 0
    for channel in store_channel_message:
        for x in range(len(channel['messages'])):
            if channel['messages'][x]['message_id'] == message_id:
                channel_id = channel['channel_id']
                if not is_member(auth_user_id, channel_id):
                    raise InputError(description="auth_user is not a member in this channel.")
                if (channel['messages'][x]['u_id'] != auth_user_id):
                    if (not is_owner(auth_user_id, channel_id)):
                        raise AccessError(description="Either message was not sent by this user or User is not channel owner")
    for channel in store_channel_message:
        for x in range(len(channel['messages'])):
            if channel['messages'][x]['message_id']== message_id:
                channel['messages'][x]['message'] = message
                channel['messages'][x]['time_created']=int(time.time())
    return {}

def message_remove_v1(token, message_id):

    """Given a message_id for a message, this message is removed from the channel/DM

    Arguments:
        token (string) - String
        message_id (int) - The user's message id

    Exceptions:
        InputError - Message (based on ID) no longer exists
        AccessError when none of the following are true:
            - Message with message_id was sent by the authorised user making this request
            - The authorised user has owner access in the channel

    Return Value:
       {}
    """

    #Getting user details
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    #getting datastore
    store = data_store.get()
    store_channel_message = store['channels']
    if not is_valid_token(auth_user_id, session_id):
        raise AccessError (description="Invalid Token")
    # if not is_valid(channel_id):
    #     raise InputError(description="Channel_id does not refer to a valid channel")
            #error checks
    channel_id = 0
    for channel in store_channel_message:
        for x in range(len(channel['messages'])):
            if channel['messages'][x]['message_id'] == message_id:
                channel_id = channel['channel_id']
                if not is_member(auth_user_id, channel_id):
                    raise InputError(description="auth_user is not a member in this channel.")
                if (channel['messages'][x]['u_id'] != auth_user_id):
                    if (not is_owner(auth_user_id, channel_id)):
                        raise AccessError(description="Either message was not sent by this user or User is not channel owner")
    for channel in store_channel_message:
        for x in range(len(channel['messages'])):
            if channel['messages'][x]['message_id']== message_id:
                del channel['messages'][x]
                break
            break
    return {}

def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    '''
    og_message_id is the ID of the original message.
    Channel_id is the channel that the message is being shared to, and is -1 if 
    it is being sent to a DM. dm_id is the DM that the message is being shared to,
    and is -1 if it is being sent to a channel. message is the optional message in
    addition to the shared message, and will be an empty string '' 
    if no message is given.

    Param: token, og_message_id, channel_id, dm_id
    Returns: shared_message_id

    Input Error if:
        -channel id and dm id are both invalid
        -neither channel_id nor dm_id are -1 
        -og_message_id does not refer to a valid message within a channel/DM that the authorised user has joined
        -length of message is more than 1000 characters
    Access Error if:
        -User is not part of dm or channel that they are trying to share a message to
    '''

    #getting the user id 
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    #error checks for message length, channel id and dm id as well as membership
    if channel_id != -1 and dm_id != -1:
        raise InputError
    if is_valid(channel_id):
        if not is_member(auth_user_id, channel_id):
            raise AccessError(description="user not part of channel")
    if is_valid_dm(dm_id):
        if not is_dm_member(auth_user_id, dm_id):
            raise AccessError(description="user not part of dm")
    #if no message is given, message is an empty string
    if len(message) == 0:
        message = ''
    elif len(message) > 1000:
        raise InputError(description="Invalid length of message")
    message_found = False
    #To store the shared message id and shared message
    shared_message_id = 0
    shared_msg = ''
    #obtainign datastore for channel and dms
    store = data_store.get()
    store_channel_message = store['channels']
    dm_list = store['dm']
    #Looping through channels and to find the message that needs to be shared
    for channel in store_channel_message:
        for x in range(len(channel['messages'])):
            if channel['messages'][x]['message_id'] == og_message_id:
                og_channel_id = channel['channel_id']
                if is_member(auth_user_id, og_channel_id):
                    message_found = True
                    shared_msg = message + ' ' + channel['messages'][x]['message']
                    break
    for dm in dm_list:
        for dm_message in dm['messages']:
            if dm_message['message_id']==og_message_id:
                og_dm_id = dm['dm_id']
                if is_dm_member(auth_user_id, og_dm_id):
                    message_found = True
                    shared_msg = message + ' ' + dm_message['message']
                    break
    #checking if message does exist
    if message_found == False:
        raise InputError(description="message does not exist in dm or channel that user is in")
    #share the message to channel as another message
    if channel_id != -1:
        sent_message = message_send_v1(token, channel_id, shared_msg)
    #share the message to dm as another message
    if dm_id != -1:
        sent_message = message_send_dm_v1(token, dm_id, shared_msg)
    shared_message_id = sent_message['message_id']
    return {'shared_message_id':shared_message_id}

def message_react_v1(token, message_id, react_id): 
    '''
    Given a message in a channel or dm that a user is a member of, adds react to message

    Params: Token, message id and react id

    returns nothing

    Inputerror if:
        message id is invalid
        react id is invalid
        User has already reacted before
    '''
    #to obtain the user id
    token_dic = decode_jwt(token) 
    auth_user_id = token_dic['u_id']
    #variables to store value of channel or dm_id
    channel_id = 0
    dm_id = 0
    #bools for if the message is found and where (dm or channel)
    message_found = False
    found_in_channel = False
    found_in_dm = False
    #List to store who has reacted to message in channel or dm
    channel_react = []
    dm_react = []
    #datastore
    store = data_store.get()
    store_channel_message = store['channels']
    dm_list = store['dm']
    user_info = store['users']
    #for functionality with notifiactions
    sender_id = 0
    sender_info = []
    reactor_handle_str =' '
    dm_name = ' '
    channel_name = ' '
    #error check for invalid react id
    if react_id != 1:
        raise InputError(description="Invalid React_id")
    #looping through channel to find the message with id message_id
    for channel in store_channel_message:
        for x in range(len(channel['messages'])):
            if channel['messages'][x]['message_id'] == message_id:
                channel_id = channel['channel_id']
                if is_member(auth_user_id, channel_id):
                    found_in_channel = True
                    channel_react = channel['messages'][x]['reacts']
                    sender_id = channel['messages'][x]['u_id']
                    channel_name = channel['name']
                    break
    #looping through dm to find the message with id message_id
    for dm in dm_list:
        for dm_message in dm['messages']:
            if dm_message['message_id'] == message_id:
                dm_id = dm['dm_id']
                if is_dm_member(auth_user_id, dm_id):
                    found_in_dm = True
                    dm_react = dm_message['reacts']
                    sender_id = dm_message['u_id']
                    dm_name = dm['name']
                    break
    #finding handle_str of original sender and person who reacted
    for user in user_info:
        if user[0]['u_id'] == sender_id:
            sender_info = user[1]
        if user[0]['u_id'] == auth_user_id:
            reactor_handle_str = user[0]['handle_str']

    #determines if a message was found in either a channel or dm
    message_found = found_in_channel ^ found_in_dm
    #error checking if message_id is invalid and if user is part of dm or channel
    if message_found == False:
        raise InputError (description="Message_id does not refer to a valid message")
    if found_in_channel == True:
        if auth_user_id not in channel_react[react_id-1]['u_id']:
            channel_react[react_id-1]['u_id'].append(auth_user_id)
            notif = reactor_handle_str + " reacted to your message in " + channel_name
            # idx = channel_index(channel_id)
            # print(store_channel_message[idx]['messages'])
        else:
            raise InputError(description="User has already reacted to this message")
    if found_in_dm == True:
        if auth_user_id not in dm_react[react_id-1]['u_id']:
            dm_react[react_id-1]['u_id'].append(auth_user_id)
            #print(dm_list)
            notif = reactor_handle_str + " reacted to your message in " + dm_name
        else:
            raise InputError(description="User has already reacted to this message")
    sender_info['notifications'].insert(0,notif)
    return{}
    
def message_unreact_v1(token, message_id, react_id):
    '''
    Given a message in a channel or dm that a user is a member of, unreacts to message

    Params: Token, message id and react id

    returns nothing

    Inputerror if:
        message id is invalid
        react id is invalid
        User has not reacted yet
    '''
    #to obtain the user id
    token_dic = decode_jwt(token) 
    auth_user_id = token_dic['u_id']
    #variables to store value of channel or dm_id
    channel_id = 0
    dm_id = 0
    #bools for if the message is found and where (dm or channel)
    message_found = False
    found_in_channel = False
    found_in_dm = False
    #List to store who has reacted to message in channel or dm
    channel_react = []
    dm_react = []
    #datastore
    store = data_store.get()
    store_channel_message = store['channels']
    dm_list = store['dm']
    #error check for invalid react id
    if react_id != 1:
        raise InputError(description="Invalid React_id")
    #looping through channel to find the message with id message_id
    for channel in store_channel_message:
        for x in range(len(channel['messages'])):
            if channel['messages'][x]['message_id'] == message_id:
                channel_id = channel['channel_id']
                if is_member(auth_user_id, channel_id):
                    found_in_channel = True
                    channel_react = channel['messages'][x]['reacts']
                    break
    #looping through dm to find the message with id message_id
    for dm in dm_list:
        for dm_message in dm['messages']:
            if dm_message['message_id'] == message_id:
                dm_id = dm['dm_id']
                if is_dm_member(auth_user_id, dm_id):
                    found_in_dm = True
                    dm_react = dm_message['reacts']
                    break
    #determines if a message was found in either a channel or dm
    message_found = found_in_channel ^ found_in_dm
    #error checking if message_id is invalid and if user is part of dm or channel
    if message_found == False:
        raise InputError (description="Message_id does not refer to a valid message")
    #removing user's id from list of people who have reacted
    if found_in_channel == True:
        if auth_user_id not in channel_react[0]['u_id']:
            raise InputError(description="User has not reacted to this message yet")
        else:
            channel_react[react_id-1]['u_id'].remove(auth_user_id)
            #idx = channel_index(channel_id)
            #print(store_channel_message[idx]['messages'])
    if found_in_dm == True:
        if auth_user_id not in dm_react[0]['u_id']:
            raise InputError(description="User has not reacted to this message yet")
        else:
            dm_react[react_id-1]['u_id'].remove(auth_user_id)
            #print(dm_list)
    return{}

def message_pin_v1(token, message_id):
    """
    Given a message, pin it if its not pinned
        Arguments:
        token (string) - string
        message_id (int) - The user's message id

        Exceptions:
        InputError - Message is already pinned
        InputError - Message_id does not refer to a valid message within a channel/dm the authorised user has joined
        AccessError - When message_id is valid but authorised user does not have owner permissions in the channel/dm


        Note: global owners have owner permissions in every channel they have joined. 
        Return Value:
        {}
    """

    #Getting user details
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    #getting datastore
    store = data_store.get()
    channels_list = store['channels']
    dm_list = store['dm']

    if not is_valid_token(auth_user_id, session_id):
        raise AccessError (description="Invalid Token")
    
    #check if message_id is a valid message:
    channel_id = -1
    dm_id = -1

    #check through channels:
    for channel in channels_list:
        for x in range(len(channel['messages'])):
            if channel['messages'][x]['message_id'] == message_id:
                channel_id = channel['channel_id']
                if not is_member(auth_user_id, channel_id):
                    raise InputError(description="auth_user is not a member in this channel/invalid message.")
                if (not is_owner(auth_user_id, channel_id) and not is_global_owner(auth_user_id)):
                    raise AccessError(description="Valid message but authorised user has not owner permissions in this channel")
                else:
                    if channel['messages'][x]['is_pinned']:
                        raise InputError(description="Message already pinned")
                    else:
                        channel['messages'][x]['is_pinned'] = True
    
    #check through dms:
    for dm in dm_list:
        for x in range(len(dm['messages'])):
            if dm['messages'][x]['message_id'] == message_id:
                dm_id = dm['dm_id']
                if not is_dm_member(auth_user_id, dm_id):
                    raise InputError(description="auth_user is not a member in this dm/invalid message.")
                if (not is_dm_creator(auth_user_id, dm_id) and not is_global_owner(auth_user_id)):
                    raise AccessError(description="Valid message but authorised user has not owner permissions in this channel")
                else:
                    if dm['messages'][x]['is_pinned']:
                        raise InputError(description="Message already pinned")
                    else:
                        dm['messages'][x]['is_pinned'] = True
    
    if channel_id == -1 and dm_id == -1:
        raise InputError(description="Message Does not exist")
    
    return {}

def message_unpin_v1(token, message_id):
    """Given a message, unpins it if its pinned
    Arguments:
        token (string) - string
        message_id (int) - The user's message id

    Exceptions:
        InputError - Message is unpinned
        InputError - Message_id does not refer to a valid message within a channel/dm the authorised user has joined
        AccessError - When message_id is valid but authorised user does not have owner permissions in the channel/dm


    Note: global owners have owner permissions in every channel they have joined. 
    Return Value:
       {}
    """
    #Getting user details
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    #getting datastore
    store = data_store.get()
    channels_list = store['channels']
    dm_list = store['dm']

    if not is_valid_token(auth_user_id, session_id):
        raise AccessError (description="Invalid Token")
    
    #check if message_id is a valid message:
    channel_id = -1
    dm_id = -1

    #check through channels:
    for channel in channels_list:
        for x in range(len(channel['messages'])):
            if channel['messages'][x]['message_id'] == message_id:
                channel_id = channel['channel_id']
                if not is_member(auth_user_id, channel_id):
                    raise InputError(description="auth_user is not a member in this channel/invalid message.")
                if (not is_owner(auth_user_id, channel_id) and not is_global_owner(auth_user_id)):
                    raise AccessError(description="Valid message but authorised user has not owner permissions in this channel")
                else:
                    if not channel['messages'][x]['is_pinned']:
                        raise InputError(description="Message already unpinned")
                    else:
                        channel['messages'][x]['is_pinned'] = False
    
    #check through dms:
    for dm in dm_list:
        for x in range(len(dm['messages'])):
            if dm['messages'][x]['message_id'] == message_id:
                dm_id = dm['dm_id']
                if not is_dm_member(auth_user_id, dm_id):
                    raise InputError(description="auth_user is not a member in this dm/invalid message.")
                if (not is_dm_creator(auth_user_id, dm_id) and not is_global_owner(auth_user_id)):
                    raise AccessError(description="Valid message but authorised user has not owner permissions in this channel")
                else:
                    if not dm['messages'][x]['is_pinned']:
                        raise InputError(description="Message already unpinned")
                    else:
                        dm['messages'][x]['is_pinned'] = False
    
    if channel_id == -1 and dm_id == -1:
        raise InputError(description="Message Does not exist")
    
    return {}

def message_sendlater_v1(token, channel_id, message, time_sent):
    """
    Send a message from the authorised user to the channel specified by channel_id automatically at a 
    specified time in the future.
    
    Arguments:
        token (str) - dictionary contains auth_user_id and session_id
        channel_id (int) - The id of the channel the message was sent in
        message (str) - The message contents
        time_sent (int) - time the message will be sent

    Exceptions:
        InputError - Channel id does not have a reference to a valid channel
        InputError - Message is more than 1000 characters
        InputError - Time sent is time in the past
        AccessError - Valid channel id and authorised user is not a member in the channel

    Return Value:
        Returns message_id on successfully sending a message
    """
    #make this instantly to check the timestamp difference and raise an error if its int he past:
    instant_time = int(time.time()) 
    time_diff = time_sent - instant_time

    #Error checks
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    if not is_valid_token(auth_user_id, session_id):
        raise AccessError (description="Invalid Token")
    if not is_valid(channel_id):
        raise InputError(description="Channel_id does not refer to a valid channel")
    if len(message) < 1 or len(message) > 1000:
        raise InputError(description="Invalid length of message")
    if time_diff < 0:
        raise InputError(description="Time_sent is a time in the past")
    if is_valid(channel_id) and not is_member(auth_user_id, channel_id):
        raise AccessError (description="Authorised user is not a member of the channel")



    # adding message to channel and assigning channel ID
    store = data_store.get()
    store_channel_list = store['channels']
    dm_list = store['dm']
    threads = store['threads']
    message_id = 0
    for channel in store_channel_list:
        message_id += len(channel['messages'])
    for dm in dm_list:
        message_id += len(dm['messages'])
    message_id+=len(threads)
    message_id+=1

    #function requires threading; will return bunch of stuff here
    message_dic = {'message_id' : message_id, 'u_id' : auth_user_id, 'message' : message, 'time_created' : time_sent,  'reacts' : [], 'is_pinned': False}
    x = threading.Thread(target=send_message_later, args=(message_dic, time_diff, channel_id, auth_user_id))
    threads.append(x)
    x.start()
    return {'message_id' : message_id}
