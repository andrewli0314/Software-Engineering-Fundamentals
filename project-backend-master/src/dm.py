from src.data_store import data_store
from src.error import InputError, AccessError
from src.helpers import decode_jwt
from src.channels import is_valid_token
from src.channel import is_valid_user, id_list_to_dic_list
import time
import threading

#Helper functions:
#Message send helper funciton:
def send_message_later(message_dic, sleep_time, dm_id, auth_user_id):
	store = data_store.get()
	time.sleep(sleep_time)
	dm_list = store['dm']
	message = message_dic['message']
	idx = 0
	for dm in dm_list:
		if dm['dm_id'] == dm_id:
			#Before sending anything, shoot some notifications if a user handle is mentioned:
			dm_name = ""
			auth_handle = ""
			for dm in dm_list:
				if dm['dm_id'] == dm_id:
					dm_name = dm['name']

			for user in store['users']:
				if user[0]['u_id'] == auth_user_id:
					auth_handle = user[0]['handle_str']

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
			#print(mentioned_handles)
			
			for handle in mentioned_handles:
				if get_u_id(handle) != -1 and is_dm_member(get_u_id(handle), dm_id):
					notification = f"{auth_handle} tagged you in {dm_name}: {message_pre}"
					for user in store['users']:
						if user[0]['handle_str'] == handle:
							user[1]['notifications'].append(notification)
							#print(user[1]['notifications'])
			
			store['dm'][idx]['messages'].insert(0, message_dic)
			#print(store['dm'][idx]['dm_id'])
			#print(f"Inserted {message_dic} at dm_d {dm_id}")
			#break
		idx += 1

def is_valid_dm(dm_id):
	store = data_store.get()
	dm_list = store['dm']
	for dm in dm_list:
		if dm['dm_id'] == dm_id:
			return True
	return False

def is_dm_creator(auth_user_id, dm_id):
	store = data_store.get()
	dm_list = store['dm']
	for dm in dm_list:
		if dm['dm_id'] == dm_id:
			if auth_user_id in dm['creator_id']:
				return True
	return False

def is_dm_member(auth_user_id, dm_id):
	store = data_store.get()
	dm_list = store['dm']
	members_list = []
	creators_list = []
	for dm in dm_list:
		if dm['dm_id'] == dm_id:
			members_list = dm['members']
			creators_list = dm['creator_id']
	
	if auth_user_id in members_list:
		return True
	if auth_user_id in creators_list:
		return True
	return False

#gets the u_id by having the handle_str only:
def get_u_id(handle_str):
	store = data_store.get()
	users_list = store['users']

	for user in users_list:
		if user[0]['handle_str'] == handle_str:
			return user[0]['u_id']
	
	return -1


def dm_create_v1(token, u_ids):
    """
    This function creates a dm channel for the user. 
    On success, add new dm channel to the data structure.

    Arguments:
        token (string) - Input token which signify that an authorised and
                          valid user is requesting for this information
        u_ids (list) - List of IDs of the user allow in the dm channel

    Exceptions:
        InputError - Occurs when u_id is invalid.
        AccessError - Occurs when authorised user (token) is invalid.
    Return Value:
        Returns a dictionary containing dm_id and dm_name. Then dm_name is made up
        of handles.
        dm_id (int)
        dm_name (string)
    """
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    #deal with errors first:
    if not is_valid_token(auth_user_id, session_id):
        raise AccessError (description="Invalid Token")

    for u_id in u_ids:
        if not is_valid_user(u_id):
            raise InputError(description="u_id in u_ids does not refer to a valid user")
    store = data_store.get()
    dm_list = store['dm']
    dm_id = len(dm_list) + 1
    user_list = store['users']
    #for notification function
    creator_handle_str = ' '
    notifs = ' '
    #get a list of handles and sort alphabetically
    handle_list = []
    for user in user_list:
        if user[0]['u_id'] == auth_user_id:
            handle_list.append(user[0]['handle_str'])
            creator_handle_str = user[0]['handle_str']
    for user in user_list:
        for u_id in u_ids:
            if u_id == user[0]['u_id']:
                handle_list.append(user[0]['handle_str'])
    sorted_handle = sorted(handle_list)

    dm_name = ", ".join(handle for handle in sorted_handle)
    dm_dic = {
        'dm_id': dm_id,
        'name' : dm_name,
        'creator_id' : [auth_user_id],
        'members' : u_ids,
        'messages':[],
    }
    dm_list.append(dm_dic)
    #generating notification for added user
    for user in user_list:
        for u_id in u_ids:
            if u_id == user[0]['u_id']:
                notifs = creator_handle_str + " has added you to " + dm_name
                user[1]['notifications'].insert(0,notifs)
    return {"dm_id": dm_id}

def dm_list_v1(token):
	"""
	This function list all the dm channels the user has access to.

	Arguments:
		token (string) - Input token which signify that an authorised and
						  valid user is requesting for this information
	Exceptions:
		AccessError - Occurs when authorised user (token) is invalid.
	Return Value:
		Returns a list of dictionary containing DMs made from {dm_id, name}. 
	"""
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	#deal with errors first:
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")
	
	store = data_store.get()
	dm_list = store['dm']
	return_list = []
	for dm in dm_list:
		if auth_user_id in dm['members'] or auth_user_id in dm['creator_id']:
			dm_dic = {'dm_id' : dm['dm_id'], 'name': dm['name']}
			return_list.append(dm_dic)
	#List of dictionaries, where each dictionary contains types { dm_id, name }
	return {"dms": return_list}


def dm_remove_v1(token, dm_id):
	"""
	This function remove the DM from existence
	"""
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	#deal with errors first:
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")
	if not is_valid_dm(dm_id):
		raise InputError(description="Invalid dm_id")
	if is_valid_dm(dm_id) and not is_dm_creator(auth_user_id, dm_id):
		raise AccessError(description="Authorised user is not the original dm creator")
	
	#here, we can continue:
	store = data_store.get()
	dm_list = store['dm']
	for dm in dm_list:
		if dm['dm_id'] == dm_id:
			dm_list.remove(dm)
			break
	return{}
	

def dm_details_v1(token, dm_id):
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	#deal with errors first:
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")
	if not is_valid_dm(dm_id):
		raise InputError(description="Invalid dm_id")
	if not is_dm_member(auth_user_id, dm_id):
		raise AccessError(description="Not a member of the dm.")
	
	store = data_store.get()
	dm_list = store['dm']
	id_list = []

	for dm in dm_list:
		if dm['dm_id'] == dm_id:
			dm_name = dm['name']
			for creator in dm['creator_id']:
				id_list.append(creator)
			for member in dm['members']:
				id_list.append(member)
	
	members_data = id_list_to_dic_list(id_list)
	return {"name": dm_name, "members": members_data}


	
def dm_leave_v1(token, dm_id):
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	#deal with errors first:
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")
	if not is_valid_dm(dm_id):
		raise InputError(description="Invalid dm_id")
	if is_valid_dm(dm_id) and not is_dm_member(auth_user_id, dm_id):
		raise AccessError(description="Auth user is not a member to be removed.")
	
	store = data_store.get()
	dm_list = store['dm']
	for dm in dm_list:
		if dm['dm_id'] == dm_id:
			if auth_user_id in dm['members']:
				dm['members'].remove(auth_user_id)
			elif auth_user_id in dm['creator_id']:
				dm['creator_id'].remove(auth_user_id)
			break
	
	return{}


def dm_messages_v1(token, dm_id, start):
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	#deal with errors first:
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")
	if not is_valid_dm(dm_id):
		raise InputError(description="Invalid dm_id")
	if not is_dm_member(auth_user_id, dm_id):
		raise AccessError(description="Authorised user is not a member in this DM")
	
	store = data_store.get()
	dm_list = store['dm']
	dm_dic = {}
	for dm in dm_list:
		if dm['dm_id'] == dm_id:
			dm_dic = dm
			break
	
	if start > len(dm_dic['messages']):
		raise InputError(description="start is greater than number of messages in this DM")
	
	message_list = []
	
	if start + 50 > len(dm_dic['messages']):
		end = -1
		end_index = len(dm_dic['messages']) - 1
	else:
		end_index = start + 50
		end = end_index

	for i in range (start, end_index + 1):
		message_list.append(dm_dic['messages'][i])
	
	for message in message_list:
		for x in range(len(message['reacts'])):
			if auth_user_id not in message['reacts'][x-1]['u_id']:
				message['reacts'][x-1]['is_this_user_reacted'] = False
				#print(message['reacts'][0])
			else:
				message['reacts'][x-1]['is_this_user_reacted'] = True
				#print(message['reacts'][0])
		return{
		'messages': message_list,
		'start': start,
		'end': end,
	}

def message_send_dm_v1(token, dm_id, message):
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	#deal with errors first:
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")
	if not is_valid_dm(dm_id):
		raise InputError(description="Invalid dm_id")
	if len(message) < 1 or len(message) > 1000:
		raise InputError(description="Message too long/short")
	if is_valid_dm(dm_id) and not is_dm_member(auth_user_id, dm_id):
		raise AccessError(description="Authorised user is not a member in this dm")
	
	store = data_store.get()
	channels_list = store['channels']
	dm_list = store['dm']
	threads = store['threads']
	message_id = 0
	for channel in channels_list:
		message_id += len(channel['messages'])
	for dm in dm_list:
		message_id += len(dm['messages'])
	message_id+=len(threads)
	message_id += 1

	react_dict_1 = {'react_id':1, 'u_id':[], 'is_this_user_reacted':False}

	#Before sending anything, shoot some notifications if a user handle is mentioned:
	dm_name = ""
	auth_handle = ""
	for dm in dm_list:
		if dm['dm_id'] == dm_id:
			dm_name = dm['name']

	for user in store['users']:
		if user[0]['u_id'] == auth_user_id:
			auth_handle = user[0]['handle_str']

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
	
	for handle in mentioned_handles:
		if get_u_id(handle) != -1 and is_dm_member(get_u_id(handle), dm_id):
			notification = f"{auth_handle} tagged you in {dm_name}: {message_pre}"
			for user in store['users']:
				if user[0]['handle_str'] == handle:
					user[1]['notifications'].insert(0,notification)


	message_info = {
		'message_id' : message_id, 
		'u_id': auth_user_id,
		'message' : message,
		'time_created' : int(time.time()),
		'reacts' : [react_dict_1], 
		'is_pinned': False
	}
	for dm in dm_list:
		if dm['dm_id'] == dm_id:
			dm['messages'].insert(0, message_info)
	return {'message_id' : message_id}


def message_sendlaterdm_v1(token, dm_id, message, time_sent):
	"""
	Send a message from the authorised user to the DM specified by dm_id automatically at a 
	specified time in the future.
	

	Arguments:
		token (str) - dictionary contains auth_user_id and session_id
		dm_id (int) - The id of the channel the message was sent in
		message (str) - The message contents
		time_sent (int) - time the message will be sent

	Exceptions:
		InputError - dm_id does not refer to a valid DM
		InputError - Message is more than 1000 characters
		InputError - Time sent is time in the past
		AccessError - Valid dm id and authorised user is not a member in the channel

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
	if not is_valid_dm(dm_id):
		raise InputError(description="dm_id does not refer to a valid channel")
	if len(message) < 1 or len(message) > 1000:
		raise InputError(description="Invalid length of message")
	if time_diff < 0:
		raise InputError(description="Time_sent is a time in the past")
	if is_valid_dm(dm_id) and not is_dm_member(auth_user_id, dm_id):
		raise AccessError (description="Authorised user is not a member of the dm")



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
	x = threading.Thread(target=send_message_later, args=(message_dic, time_diff, dm_id, auth_user_id))
	threads.append(x)
	x.start()
	return {'message_id' : message_id}
