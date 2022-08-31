"""Has channels_create_v1, channels_list_v1, channels_listall_v1"""
from src.error import InputError, AccessError
from src.data_store import data_store
from src.helpers import decode_jwt


def is_valid_token(auth_user_id, session_id):
	"""Checks if the passed token is valid or not
		takes in a user id and session id, 
		if invalid returns false
	"""
	store = data_store.get()
	users_list = store['users']
	for user in users_list:
		if user[0]['u_id'] == auth_user_id:
			if session_id in user[1]['session_id']:
				return True
	return False

def channels_list_v1(token):
	"""Provide a list of all channels that the authorised user is part of.
		takes in a token and returns a list of all channels that the user is a 
		part of.
		if token is invalid it raises a access error
	"""
	#decodes the token to get user id and session
	token_dic = decode_jwt(token) 
	auth_user_id = token_dic['u_id'] #user id
	session_id = token_dic['session_id'] #session id
	#deal with errors first:
	#checking for invalid user
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token") 
	#Then run the function implementation
	store = data_store.get()
	channels_list = store['channels']
	#channels is a list of dictionaries: {channel_id, name, owner, members, is_public}
	#fetch channel_id and name only
	rchannels_list = []
	for channel in channels_list:
		if auth_user_id in channel['members']:
			dictionary = {"channel_id" : channel['channel_id'], "name" : channel['name'] }
			rchannels_list.append(dictionary)
	return {
		"channels": rchannels_list
	}

def channels_listall_v1(token):
	"""Provide a list of all channels, including private channels and the details
		takes in a token and returns a list of all channels
		if an invalid token is given, it raises an access error
	"""
	#decodes the token to get user id and session
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']#user id
	session_id = token_dic['session_id']#session id
	#deal with errors first:
	#checking for invalid user
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")

	store = data_store.get()
	# getting an instance of the data store
	channels_list = store['channels'] #getting a section of data store

	# Channel dictionary
	rchannels_list = []

	# Adds all channels into the channel dic
	for channel in channels_list:
		dictionary = {'channel_id' : channel['channel_id'], 'name' : channel['name'] }
		rchannels_list.append(dictionary) #adds each channel to current list of channels

	return {
		'channels':
			rchannels_list
	}

def channels_create_v1(token, name, is_public):
	"""creates a new chennel that is either public or private, creator joins automatically
		Takes in a token, a channel name and an boolean value for whether the channel will
		be public or private.
		if invalid token is provided an access error will be raised
		if the name is too long (> 20 char) or too short (< 0 char), input error will
		be raised
		Function appends the channel to data store and returns its channel id
	"""

	#decode the token to get user id and session
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id'] # user id
	session_id = token_dic['session_id'] # session id
	#checking for invalid user
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError(description="Invalid Token")
	#checks for invalid input
	if len(name) <1 or len(name) > 20:
		raise InputError(description="Length of channel name must be more at least 1 and at most 20 characters")
	# gets instance of data store
	store = data_store.get()
	# getting specific list in the data store
	store_channels = store['channels']
	#assigneing a new channel id
	length = len(store_channels)
	if length == 0:
		last_cid = 0
	else:
		last_cid = store_channels[length-1]['channel_id']
	next_cid = last_cid + 1 #new channel id generated
	details = {
		'channel_id':next_cid,
		'name':name,
		'owner': [],
		'members': [],
		'messages':[],
		'is_public' : is_public,
		'standup':[]
	}
	details['owner'].append (auth_user_id)
	details['members'].append (auth_user_id)
	store_channels.append(details) #adding the new channel to data store
	return {
		'channel_id': next_cid,
	}


