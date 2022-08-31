"""
This File contains channel_invite_v1, channel_details_v1, channel_messages_v1, and channel_join_v1
"""
from src.error import InputError, AccessError
from src.data_store import data_store
from src.channels import is_valid_token
from src.helpers import decode_jwt


#Function Helpers:
def is_valid(channel_id):
	"""
	Checks whether channel_id is valid or not, returns
		true if valid
	"""
	store = data_store.get()
	channel_list = store['channels']
	for channel in channel_list:
		if channel_id == channel['channel_id']:
			return True
	return False

def is_owner (auth_user_id, channel_id):
	"""
	Checks if auth_user_id is the owner of channel_id
	returns true if owner
	"""
	store = data_store.get()
	channel_list = store['channels']
	for channel in channel_list:
		if channel_id == channel['channel_id']:
			if  auth_user_id in channel['owner']:
				return True
	return False


def channel_index (channel_id):
	"""
	Function that takes in a channel id returns the index of a channel

	"""
	store = data_store.get()
	channel_list = store['channels']
	idx = 0
	for channel in channel_list:
		if channel_id == channel['channel_id']:
			break
		idx += 1
	return idx

def is_member (auth_user_id, channel_id):
	"""
	Checks if the user is already a member in the channel, takes in user id and channel id
	return true if user is already a member
	"""
	store = data_store.get()
	channel_list = store['channels']
	idx = channel_index(channel_id)
	#loop through the members list
	for member_id in channel_list[idx]['members']:
		if auth_user_id == member_id:
			return True
	return False

def is_private(channel_id):
	"""Checks if the channel is private or not by taking in channel id
		returns true if channel is private
	"""
	store = data_store.get()
	channel_list = store['channels']
	for channel in channel_list:
		if channel_id == channel['channel_id']:
			if channel['is_public']:
				return False
	return True

def is_global_owner(auth_user_id):
	"""
	Checks if the passed user id has permission id 1 
	returns true if valid
	"""
	store = data_store.get()
	user_list = store['users']
	for user in user_list:
		if user[0]['u_id'] == auth_user_id:
			if user[1]['is_global_member']:
				return True
	return False

def id_list_to_dic_list (u_id_list):
	"""
	Takes the passed list of u_id, returns a list of dictionaries
	with the corresponding details of the user
	"""
	store = data_store.get()
	user_list = store['users']
	return_list = []
	for user in user_list:
		for u_id in u_id_list:
			if user[0]['u_id'] == u_id:
				return_list.append(user[0])
	return return_list

def is_valid_user(u_id):
	"""
	Checks if the inputed user id is valid or not
	if it is, return true
	"""
	store = data_store.get()
	users_list = store['users']
	for user in users_list:
		if user[0]['u_id'] == u_id:
			return True
	return False

#Function implementation

def channel_invite_v1(token, channel_id, u_id):
    """
    takes in a token, channel id and user id. Function invites a authorised with u_id from
    the token to join a channel with channel_id. When invited, user joins channel immediately.
    In both public and private channels, all members are able to invite users.

    Input error if 
        channel_id, u_id is invalid or user is already in channel

    Access error if 
        channel id is valid but person sending invite is not member of channel
    """
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    # for generating a notification
    creator_handle_str = ' '
    notif = ' '
    invited_member_info = []
    # Raise errors first
    if not is_valid_token(auth_user_id, session_id):
        raise AccessError (description="Invalid Token")
    if not is_valid(channel_id):
        raise InputError (description="Channel_id does not refer to a valid channel")
    if not is_valid_user(u_id):
        raise InputError (description="u_id does not refer to a valid user")
    if is_member(u_id, channel_id):
        raise InputError (description="u_id refers to a user who is already a member of the channel")
    if is_valid(channel_id) and not is_member(auth_user_id, channel_id):
        raise AccessError(description="Authorised user is not a member of the channel")

    #All Precoditions sorted:
    store = data_store.get()
    channels_list = store['channels']
    user_list = store['users']
    channel_idx = channel_index (channel_id)
    channels_list[channel_idx]['members'].append(u_id)
    #Notifying users members that they have been added to channel
    for user in user_list:
        if user[0]['u_id'] == auth_user_id:
            creator_handle_str = user[0]['handle_str']
            notif = creator_handle_str + ' added you to ' + channels_list[channel_idx]['name']
        if user[0]['u_id'] == u_id:
            invited_member_info = user[1]
    invited_member_info['notifications'].insert(0, notif)        
    return {}

def channel_details_v1(token, channel_id):
	"""
	takes in a token and channel id.
	if user with the token is a member of the channel, return the details about 
	the channel (name, public or private,  owners, all members)

	Input error when 
		channel_id is not a valid channel

	Access error if 
		channel id is valid but person requesting the details is not
		a member of the channel
	"""
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")
	if not is_valid(channel_id):
		raise InputError(description="Channel_id does not refer to a valid channel")
	if is_valid(channel_id) and not is_member(auth_user_id, channel_id):
		raise AccessError (description="Authorised user is not a member of the channel")
	#Preconditions done
	store = data_store.get()
	channels_list = store['channels']
	channel_idx = channel_index (channel_id)
	channel_name = channels_list[channel_idx]['name']
	channel_is_public = channels_list[channel_idx]['is_public']
	owner_id_list = channels_list[channel_idx]['owner']
	member_id_list = channels_list[channel_idx]['members']
	members_dic_list = id_list_to_dic_list(member_id_list)
	owners_dic_list = id_list_to_dic_list(owner_id_list)
	return {
		'name': channel_name,
		'is_public' : channel_is_public,
		'owner_members': owners_dic_list,
		'all_members': members_dic_list,
	}


def channel_messages_v1(token, channel_id, start):
	"""
	takes in a token, channel id and the start index of messages.
	
	In a channel with the id channel_id, if the authorised that the token refers to is a member,
	return up to 50 messages between start index and start + 50.

	function returns a new index "end" which is the value of "start + 50", or,
	if this function has returned the least recent messages in the channel, 
	returns -1 in "end" to indicate there are no more messages to load after this return.

	Input Error if
		channel_id does not correspond to a channel or if start index is more than 
		the total number of messages in the channel

	Access error if 
		channel id is valid but person requesting the details is not
		a member of the channel
	"""
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	#deal with errors
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")
	if not is_valid (channel_id):
		raise InputError(description="Channel_id does not refer to a valid channel")
	if is_valid (channel_id) and not is_member(auth_user_id, channel_id):
		raise AccessError (description="Authorised user is not a member of the channel")

	store = data_store.get()
	channels_list = store['channels']
	channel_messages_list = channels_list[channel_index(channel_id)]['messages']

	message_list = []

	if start > len(channel_messages_list):
		raise InputError ("Start is greater than the total number of messages in the channel")

	#if startIndex + the 50 message > length, this means we wont be able to print the whole list,
	#so we return -1:

	if start + 50 > len(channel_messages_list):
		end = -1
		end_index = len(channel_messages_list) - 1
	else:
		end_index = start + 50
		end = end_index

	for i in range (start, end_index + 1):
		message_list.append(channel_messages_list[i])
	for message in message_list:
		for x in range(len(message['reacts'])):
			if auth_user_id not in message['reacts'][x-1]['u_id']:
				message['reacts'][x-1]['is_this_user_reacted'] = False
				#print(message['reacts'][0])
			else:
				message['reacts'][x-1]['is_this_user_reacted'] = True
				#print(message['reacts'][0])
	return {
		'messages': message_list,
		'start' : start,
		'end' : end,
	}

#done
def channel_join_v1(token, channel_id):
	"""
	Takes in a token and channel id. 
	Given a channel_id of a channel that the authorised user can join, adds them to that channel.

	Input error if 
		channel_id, u_id is invalid or user is already in channel

	Access error if 
		channel id is valid but person sending invite is not member of channel
	"""
	token_dic = decode_jwt(token)#obtaining the user id and session id from the jwt
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	# Raise errors first
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")
	if not is_valid(channel_id):
		raise InputError(description="Channel_id does not refer to a valid channel")
	if is_member (auth_user_id, channel_id):
		raise InputError(description="The authorised user is already a member of the channel")
	if is_private(channel_id):
		if not is_member(auth_user_id, channel_id) and not is_global_owner(auth_user_id):
			raise AccessError (description='Channel is private and user is neither a member nor a global owner')
	#if passed all above, we gucci
	store = data_store.get()
	channels_list = store['channels']
	channel_idx = channel_index (channel_id)
	channels_list[channel_idx]['members'].append(auth_user_id)
	return {
	}

###########################################################################################
#############################   MORE IMPLEMENTATIONS ######################################
###########################################################################################

def channel_leave_v1(token, channel_id):
	"""
	Takes in a token and channel id.

	If the authorised user (referred to by token) is a member of the channel with channel_id,
	remove them as a member, messages should remain. If the only channel owner leaves, 
	channel will remain

	Input error if
		channel_id does not refer to a valid channel

	Access error if 
		channel id is valid but person requesting the details is not
		a member of the channel
	"""
	#break down the token first:
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	# Raise errors first
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token") #not authorised user
	if not is_valid(channel_id):
		raise InputError(description="Channel not Valid") #invalid channel id
	if is_valid(channel_id) and not is_member(auth_user_id, channel_id):
		raise AccessError(description="Authorised user is not a member of the channel")
	
	#Get data:
	store = data_store.get()
	channels_list = store['channels']
	channel_idx = channel_index (channel_id)
	#"If the only channel owner leaves, the channel will remain."
	#if the user is an owner, remove it from the owner list:
	if is_owner(auth_user_id, channel_id):
		channels_list[channel_idx]['owner'].remove(auth_user_id)
	#"remove them as a member of the channel"
	channels_list[channel_idx]['members'].remove(auth_user_id)
	return {}


def channel_addowner_v1(token, channel_id, u_id):
	"""
	Takes in a token, channel_id and user id (u_id)
	Make user with user id u_id an owner of the channel.

	Input error:
		channel_id does not refer to a valid channel /-/-
		u_id does not refer to a valid user /-/-
		u_id refers to a user who is not a member of the channel /-/-
		u_id refers to a user who is already an owner of the channel /-/-

	Access Error
		channel id is valid but authorised user is not an owner
	"""
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	#raise errors:
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")
	if not is_valid(channel_id):
		raise InputError(description="Invalid channel_id")
	if not is_valid_user(u_id):
		raise InputError(description="Invalid u_id")
	if not is_member(u_id, channel_id):
		raise InputError(description="u_id is not a member of the channel")
	if is_owner(u_id, channel_id):
		raise InputError(description="u_id is already an owner in this channel")
	if is_valid(channel_id) and not is_owner(auth_user_id, channel_id):
		raise AccessError(description="Authorised user does not have owner permissions in the channel")
	
	#since we passed all of the errors, we're set:
	store = data_store.get()
	channels_list = store['channels']
	idx = channel_index(channel_id)
	channels_list[idx]['owner'].append(u_id)
	return {}

def channel_removeowner_v1(token, channel_id, u_id):
	"""
	Takes in a token, channel_id and user id (u_id)

	Remove user with user id u_id as an owner of the channel.

	Input Error if:
		channel_id does not refer to a valid channel 
		u_id does not refer to a valid user 
		u_id refers to a user who is not an owner of the channel 
		u_id refers to a user who is currently the only owner of the channel

	Access Error if:
		channel_id is valid and the authorised user does not have owner permissions in the channel
	"""
	token_dic = decode_jwt(token) # to obtain u_id and session_id from jwt
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	#raise errors:
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")
	if not is_valid(channel_id):
		raise InputError(description="Invalid channel_id")
	if not is_valid_user(u_id):
		raise InputError(description="Invalid u_id")
	if not is_owner(u_id, channel_id):
		raise InputError(description="u_id is not an owner to be removed")
	if is_valid(channel_id) and not is_owner(auth_user_id, channel_id):
		raise AccessError(description="Authorised user is not an owner in this channel")
	#getting data form the data store
	store = data_store.get() 
	channels_list = store['channels']
	idx = channel_index(channel_id)
	#iterate to see if user is the only owner in channel
	if is_owner(u_id, channel_id) and len(channels_list[idx]['owner']) == 1:
		raise InputError(description="u_id is the only owner of this channel")
	channels_list[idx]['owner'].remove(u_id)
	return {}

