import jwt
from src.config import photo_path, photo_storage_path
from src.error import InputError, AccessError
from src.data_store import data_store
from src.helpers import decode_jwt
from src.channels import is_valid_token
from src.channel import is_valid_user, id_list_to_dic_list
from src.channel import is_valid_user, is_global_owner, is_member, is_owner
from src.dm import is_dm_member
from src.auth import to_list, check_dual_emails
import re
from PIL import Image
import sys 
import urllib.request
import imgspy
import requests
import os
import time
import datetime
from datetime import datetime
from datetime import timezone

REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

#helper function

def update_profile_img_url(u_id: int, url: str) -> None:
    """Update the user's img_url (the photo displayed)
    
    Arguments:
        u_id (int) - The user's id
        url (str) - url being used for accessing the photo
    Return Value:
        Returns None if updated user's url successfully
    """
    store = data_store.get()
    users_list = store['users']

    store['users'][users_list]['profile_img_url'] = url

def user_profile_v1(token, u_id):
	""" For a valid user, returns information about their user_id, email, first name, last name, and handle

	Args:
		token ([string]): an authorisation hash that the person who claims they are that user, is actually that user
		u_id: a int stats unique id of a valid user
	
	Returns:
		Dictionary { user } = {'u_id', 'email', 'name_first', 'name_last', 'handle_str'}
	"""
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	#deal with errors first:
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")
	if not is_valid_user(u_id):
		raise InputError(description="u_id is not valid")
	

	store = data_store.get()
	users_list = store['users']

	for user in users_list:
		if user[0]['u_id'] == u_id:
			return_dic = user[0]
			break
	
	return {'user' : return_dic}

def user_profile_setname_v1(token, name_first, name_last):
	""" For a valid user, can change and set the new first and last name

	Args:
		token ([string]): an authorisation hash that the person who claims they are that user, is actually that user
		name_first: a string of  1 and 50 characters inclusive for set first name
		name_last: a string of  1 and 50 characters inclusive for set last name
	
	Returns:
		update the user profile, return empty string
	"""
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	#deal with errors first:
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")
	
	if len(name_first) < 1 or len(name_first) > 50:
		raise InputError(f'name_first {name_first} is not between 1 and 50 characters inclusively in length')

	if len(name_last) < 1 or len(name_last) > 50:
		raise InputError(f'name_last {name_last} is not between 1 and 50 characters inclusively in length')

	store = data_store.get()
	users_list = store['users']
	for user in users_list:
		if user[0]['u_id'] == auth_user_id:
			user[0]['name_first'] = name_first
			user[0]['name_last'] = name_last
	return {}

def user_profile_setemail_v1(token, email):
	""" For a valid user, can change and set the new first and last name

	Args:
		token ([string]): an authorisation hash that the person who claims they are that user, is actually that user
		emial: a string with correct email format
	
	Returns:
		update the user profile, return empty string
	"""
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	#deal with errors first:
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")

	store = data_store.get()
	susers = store['users']
	semail = to_list(susers, 0, 'email')
	if not re.fullmatch(REGEX, email) or check_dual_emails(email,semail) != 1:
		raise InputError(description="Invalid email or email already in use")

	for user in susers:
		if user[0]['u_id'] == auth_user_id:
			user[0]['email'] = email

	return {}

def user_profile_sethandle_v1(token, handle_str):
	""" Updated the handle with given handle string

	Args:
		token ([string]): an authorisation hash that the person who claims they are that user, is actually that user
		handle_str ([string]): a string need to be updated
	Returns:
		no need to return any value, already updated
	"""
	
	# decode the token
	token_dic = decode_jwt(token)
	target_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	
	if not is_valid_token(target_user_id, session_id):
		raise AccessError(description = "Invalid Token")
	if len(handle_str) < 3 or len(handle_str) > 20:
		raise InputError(description = "Length of handle must be between 3 and 20 characters inclusive.")
	if handle_str.isalnum() == False:
		raise InputError(description = "Handlestr contains characters that are not alphanumeric.")
		
	store = data_store.get()
	store_users = store['users']
	target_user = 0

	# find target user and check if the handle is used by other user
	for i, user in enumerate(store_users):
		if user[0]['u_id'] == target_user_id:
			target_user = i
		if user[0]['handle_str'] == handle_str and user[0]['u_id'] != token_dic['u_id']:
			raise InputError(description = "The handle is already used by another user.")
	
	# if handle string is alphanumeric, update the handle_str
	store_users[target_user][0]['handle_str'] = handle_str    
	
	return {}

def users_all_v1(token):
    token_dic = decode_jwt(token)
    target_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    
    if not is_valid_token(target_user_id, session_id):
        raise AccessError(description = "Invalid Token")
    
    store = data_store.get()
    users_list = store['users']

    id_list = []
    for user in users_list:
        if user[0]['email'] != "N/A":
            id_list.append(user[0]['u_id'])
    
    users_list = id_list_to_dic_list(id_list)
    return {
        'users' : users_list
    }

def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):

    """
    Given a valid token, Fetches the required statistics about this user

    Arguments:
        token <string>   - the user's hashed auth_user_id
        url_path <string>- the url path of the flask server 
        img_url <string> - the url of the image the user wishes to upload
        x_start <int>    - the starting x coordinate of the cropped image
        y_start <int>    - the starting y coordinate of the cropped image
        x_end <int>      - the ending x coordinate of the cropped image
        y_end <int>      - the ending y coordinate of the cropped image

    Exceptions:
        AccessError      - Occurs when the token given isn't valid
        InputError       - img_url returns an HTTP status other than 200.
        InputError       - any of x_start, y_start, x_end, y_end are not 
                           within the dimensions of the image at the URL.
        InputError       - Image uploaded is not a JPG

    Return Value:
        Returns {}
    """

    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    #deal with errors first:
    if not is_valid_token(auth_user_id, session_id):
        raise AccessError (description="Invalid Token")

    response = requests.get(img_url)
    if response.status_code != 200:
        raise InputError("img_url returns an HTTP status other than 200.")

    img_info = imgspy.info(img_url)
    if img_info.get('type') != 'jpg':
        raise InputError("Image uploaded is not a JPG.")

    img_width = img_info.get('width')
    img_height = img_info.get('height')

    wrong_dimension = False

    if x_start < 0 or x_start > x_end or x_end > img_width:
        wrong_dimension = True
    if y_start < 0 or y_start > y_end or y_end > img_height:
        wrong_dimension = True

    if wrong_dimension:
        raise InputError("any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URLs.")

    user_photo_path = photo_storage_path + '.jpg'

    urllib.request.urlretrieve(img_url, user_photo_path)

    photo = Image.open(user_photo_path)
    cropped_photo = photo.crop((x_start, y_start, x_end, y_end))
    cropped_photo.save(user_photo_path)

    url = photo_path + '.jpg'

    update_profile_img_url(auth_user_id, url)
    
    return {}
 
def user_stats_v1(token):
    '''
    Fetches the required statistics about this user's use of UNSW Streams.
    
    Argument: 
    token <string>   - the user's hashed auth_user_id
    
    Exceptions:
    if the given token belongs to a valid user1
    
    Return Value: { 
    'channels_joined': [{num_channels_joined, time_stamp}],
    'dms_joined': [{num_dms_joined, time_stamp}], 
    'messages_sent': [{num_messages_sent, time_stamp}], 
    'involvement_rate':  integer between 0 to 1 }
    '''
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    if not is_valid_token(auth_user_id, session_id):
        raise AccessError (description="Invalid Token")
    
    store = data_store.get()
    channels_list = store['channels']
    dm_list = store['dm']
    threads = store['threads']
    messages_sent = 0
    channels_joined = 0
    dms_joined = 0
    message_num = 0
    channel_time = int(datetime.now(timezone.utc).timestamp())
    dm_time = int(datetime.now(timezone.utc).timestamp())
    message_time = int(datetime.now(timezone.utc).timestamp())
    for channel in channels_list:
        message_num += len(channel['messages'])
        if is_member(auth_user_id, channel['channel_id']):
            channels_joined += 1
            channel_time = int(datetime.now(timezone.utc).timestamp())
            for ch_message in channel['messages']:
                if ch_message['u_id'] == auth_user_id:
                    messages_sent += 1
                    message_time = int(datetime.now(timezone.utc).timestamp())
    for dm in dm_list:
        message_num += len(dm['messages'])
        if is_dm_member(auth_user_id, dm['dm_id']):
            dms_joined += 1
            dm_time = int(datetime.now(timezone.utc).timestamp())
            for dm_message in dm['messages']:
                if dm_message['u_id'] == auth_user_id:
                    messages_sent += 1
                    message_time = int(datetime.now(timezone.utc).timestamp())

    message_num+=len(threads)
    joined = channels_joined + dms_joined + messages_sent
    total = len(channels_list) + len(dm_list) + message_num
    involv_rate = 0
    if total == 0:
        involv_rate = 0
    elif joined >= total:
        involv_rate = 1
    else:
        involv_rate = joined / total
    
    user_channel = {'num_channels_joined': channels_joined, 'Time_stamp': channel_time}
    user_dm = {'num_dms_joined': dms_joined, 'Time stamp': dm_time}
    user_message = {'num_messages_sent': messages_sent, 'TIme stamp': message_time}
    
    stat = {
        'channels_joined': [user_channel],
        'dms_joined': [user_dm], 
        'messages_sent': [user_message], 
        'involvement_rate':  involv_rate
        }

    return {
        'user_stats': stat
    }
        
   
def users_stats_v1(token):
    '''
    Fetches the required statistics about this user's use of UNSW Streams.
    
    Argument: 
    token <string>   - the user's hashed auth_user_id
    
    Exceptions:
    if the given token belongs to a valid user1
    
    Return Value: { 
    channels_exist: [{num_channels_exist, time_stamp}], 
    dms_exist: [{num_dms_exist, time_stamp}], 
    messages_exist: [{num_messages_exist, time_stamp}], 
    utilization_ratechannels_exist    
    }
    '''
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    if not is_valid_token(auth_user_id, session_id):
        raise AccessError (description="Invalid Token")
    
    store = data_store.get()
    users_list = store['users']
    channels_list = store['channels']
    dm_list = store['dm']
    threads = store['threads']
    
    message_num = 0
    for channel in channels_list:
        message_num += len(channel['messages'])
        
    for dm in dm_list:
        message_num += len(dm['messages'])
        
    
    message_num+=len(threads)
    
    joined_at_least_one = 0
    found_in_dm = 0
    for user in users_list:
        user_id = user[0]['u_id']
        for dm in dm_list:
            if is_dm_member(user_id, dm['dm_id']):
                joined_at_least_one += 1
                found_in_dm = 1
                break
        if found_in_dm != 1:
            for channel in channels_list:
                if is_member(user_id, channel['channel_id']):
                    joined_at_least_one += 1
                    break
        found_in_dm =  0               
    exist_channel = len(channels_list)
    exist_dm = len(dm_list) 
    exist_msg = message_num
    exist_users = len(users_list)
    utilization_rate  = joined_at_least_one/exist_users

    current_time = int(datetime.now(timezone.utc).timestamp())
    
    channel_stat = {'num_channels_exist': exist_channel, 'time_stamp': current_time}
    dm_stat = {'num_dms_exist': exist_dm, 'Time stamp': current_time}
    message_stat = {'num_messages_exist': exist_msg, 'TIme stamp': current_time}
    
    stats = {
        'channels_exist': [channel_stat],
        'dms_exist': [dm_stat], 
        'messages_sent': [message_stat], 
        'utilization_ratechannels_exist': utilization_rate
        }
    #print(stats)
    return {
        'workspace_stats': stats
    } 

