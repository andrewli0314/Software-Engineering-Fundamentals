from logging import info
import sys
import signal
import json
from types import MethodDescriptorType
import flask
import requests
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src import config
from src.helpers import decode_jwt
from src.other import clear_v1
from src.error import InputError, AccessError
from src.data_store import data_store
from src.auth import auth_register_v1, auth_login_v1, auth_logout_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.channel import channel_details_v1, channel_invite_v1, channel_messages_v1, channel_join_v1
from src.channel import channel_leave_v1, channel_addowner_v1, channel_removeowner_v1
from src.message import message_unreact_v1, message_react_v1, message_send_v1, message_edit_v1, message_remove_v1, message_share_v1, message_unpin_v1, message_pin_v1, message_sendlater_v1
from src.admin import userpermission_change_v1, user_remove_v1, passwordreset_request_v1, passwordreset_reset_v1
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1, dm_details_v1, dm_leave_v1, dm_messages_v1, message_send_dm_v1, message_sendlaterdm_v1
from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1, users_all_v1, user_profile_uploadphoto_v1, user_stats_v1, users_stats_v1
from src.notification import notifcation_get
from src.search import search_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1

data = data_store.get()
with open("database.json", "r") as FILE:
	data = json.load(FILE)
	print(f"Loaded Data", data)

def getData():
	data = data_store.get()
	return data

def save():
	data = getData()
	users = data['users']
	channels = data['channels']
	dm = data['dm']
	save_data = {
		"users" : users, 
		"channels" : channels, 
		"dm:" : dm
	}
	with open('database.json', 'w') as FILE:
		json.dump(save_data, FILE)

def quit_gracefully(*args):
	'''For coverage'''
	exit(0)

def defaultHandler(err):
	response = err.get_response()
	print('response', err, err.get_response())
	response.data = dumps({
		"code": err.code,
		"name": "System Error",
		"message": err.get_description(),
	})
	response.content_type = 'application/json'
	return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

# Example
@APP.route("/echo", methods=['GET'])
def echo():
	data = request.args.get('data')
	if data == 'echo':
   		raise InputError(description='Cannot echo "echo"')
	return json.dumps({'data': data})

# Clear Header
@APP.route("/clear/v1", methods=['DELETE'])
def clear_data():
	"""clear function wrapper, returns {}"""
	clear_v1()
	return json.dumps({})

#############################################################################
###############################AUTH_HEADERS##################################
#############################################################################
# Auth Register Header
@APP.route("/auth/register/v2", methods=['POST'])
def auth_register_v2():
	"""auth_register function wrapper, returns {token, auth_user_id}"""
	info = request.get_json()
	reg_email = info['email']
	reg_password = info['password']
	reg_namef = info['name_first']
	reg_namel = info['name_last']
	json_ret = auth_register_v1(reg_email, reg_password, reg_namef, reg_namel)
	save()
	return json.dumps(json_ret)

# Auth Login Header
@APP.route("/auth/login/v2", methods=['POST'])
def auth_login_v2():
	"""auth_login function wrapper, returns {token, auth_user_id} and makes a new session_id"""
	info = request.get_json()
	reg_email = info['email']
	reg_password = info['password']
	# Check if it prints the right session id's
	# store = data_store.get()
	# susers = store['users'][0][1]['session_id']
	# print(susers)
	json_ret = auth_login_v1(reg_email, reg_password)
	save()
	return json.dumps(json_ret)

#Auth Logout Header
@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
	"""{token}"""
	info = request.get_json()
	token = info['token']
	json_ret = auth_logout_v1(token)
	save()
	return json.dumps(json_ret)

#   
#Auth passwordreset request Header
@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def admin_passwordreset_request():
	"""{ email }"""
	info = request.get_json()
	request_email = info
	json_ret = passwordreset_request_v1(request_email)
	save()
	return json.dumps(json_ret)

#Auth passwordreset reset Header
@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def admin_passwordreset_reset():
	"""{ reset_code, new_password }"""
	info = request.get_json()
	code = info['reset_code']
	password = info['new_password']
	json_ret = passwordreset_reset_v1(code, password)
	save()
	return json.dumps(json_ret)

#############################################################################
#############################CHANNELS_HEADERS################################
#############################################################################
# Channels Create Header:
@APP.route("/channels/create/v2", methods=['POST'])
def channels_create_v2():
	"""Channels_create wrapper, returns {channel_id}"""
	#an AccessError is thrown when the token passed in is invalid.
	info = request.get_json()
	token = info['token']
	ch_name = info['name']
	ch_is_public = info['is_public']
	json_ret = channels_create_v1(token, ch_name,ch_is_public)
	save()
	return json.dumps(json_ret)

#Channels list header:
@APP.route("/channels/list/v2", methods=['GET'])
def channels_list_v2():
	"""
	Wrapper of channels_list_v1 function
	Returns {"channels" : [list of channel dictionaries in the form {channel_id, name}]}
	"""
	token = flask.request.args.get('token')
	# info = requests.args.get()
	# token = info['token']
	# print(f"token = {token}")
	json_ret = channels_list_v1(token)
	save()
	return json.dumps(json_ret)

#Channels listall header:
@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall_v2():
	"""Wrapper of channels listall v1"""
	token = flask.request.args.get('token')
	# info = request.get_json()
	# token = info['token']
	json_ret = channels_listall_v1(token)
	save()
	return json.dumps(json_ret)

#############################################################################
#############################CHANNEL_HEADERS#################################
#############################################################################
#Channel Details Header:
@APP.route("/channel/details/v2", methods=['GET'])
def channel_details_v2():
	"""{ token, channel_id }"""
	token = flask.request.args.get('token')
	channel_id = int(flask.request.args.get('channel_id'))
	json_ret = channel_details_v1(token, channel_id)
	save()
	return json.dumps(json_ret)

#Channel Join Header:
@APP.route("/channel/join/v2", methods=['POST'])
def channel_join_v2():
	info = request.get_json()
	token = info['token']
	channel_id = info['channel_id']
	json_ret = channel_join_v1(token, channel_id)
	save()
	return json.dumps(json_ret)

#Channel Invite Header:
@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite_v2():
	"""{ token, channel_id, u_id }"""
	info = request.get_json()
	token = info['token']
	channel_id = info['channel_id']
	u_id = info['u_id']
	json_ret = channel_invite_v1(token, channel_id, u_id)
	save()
	return json.dumps(json_ret)

#Channel Messages Header:
@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages_v2():
	"""{ token, channel_id, start }"""  
	token = flask.request.args.get('token')
	channel_id = int(flask.request.args.get('channel_id'))
	start = int(flask.request.args.get('start'))
	json_ret = channel_messages_v1(token, channel_id, start)
	save()
	return json.dumps(json_ret)

#Channel Leave Header:
@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
	"""{ token, channel_id }"""
	info = request.get_json()
	token = info['token']
	channel_id = info['channel_id']
	json_ret = channel_leave_v1(token, channel_id)
	save()
	return json.dumps(json_ret)

#Channel Addowner Header:
@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
	"""{ token, channel_id, u_id }"""
	info = request.get_json()
	token = info['token']
	channel_id = info['channel_id']
	u_id = info['u_id']
	json_ret = channel_addowner_v1(token, channel_id, u_id)
	save()
	return json.dumps(json_ret)

#Channel Removeowner Header:
@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner():    
	"""{ token, channel_id, u_id }"""
	info = request.get_json()
	token = info['token']
	channel_id = info['channel_id']
	u_id = info['u_id']
	json_ret = channel_removeowner_v1(token, channel_id, u_id)
	save()
	return json.dumps(json_ret)
#############################################################################
##############################MESSAGE_HEADERS################################
############################################################################# 
#Message Send Header:
@APP.route("/message/send/v1", methods=['POST'])
def message_send():
	info = request.get_json()
	token = info['token']
	channel_id = info['channel_id']
	message = info['message']
	json_ret = message_send_v1(token, channel_id, message)
	save()
	return json.dumps(json_ret)

#Message Edit Header
@APP.route("/message/edit/v1", methods=['PUT'])
def message_edit():
	info = request.get_json()
	token = info['token']
	message_id = info['message_id']
	message = info['message']
	json_ret = message_edit_v1(token, message_id, message)
	save()
	return json.dumps(json_ret)

#Message Remove Header
@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
	info = request.get_json()
	token = info['token']
	message_id = info['message_id']
	json_ret = message_remove_v1(token, message_id)
	save()
	return json.dumps(json_ret)

@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
	info = request.get_json()
	token = info['token']
	dm_id = info['dm_id']
	message = info['message']
	json_ret = message_send_dm_v1(token, dm_id, message)
	save()
	return json.dumps(json_ret)
#Message share header
@APP.route("/message/share/v1", methods=['POST'])
def message_share():
	info = request.get_json()
	token = info['token']
	og_message_id = info['og_message_id']
	message = info['message']
	channel_id = info['channel_id']
	dm_id = info['dm_id']
	json_ret = message_share_v1(token, og_message_id, message, channel_id, dm_id)
	save()
	return json.dumps(json_ret)
#Message react header
@APP.route("/message/react/v1", methods=['POST'])
def message_react():
	info = request.get_json()
	token = info['token']
	message_id = info['message_id']
	react_id = info['react_id']
	json_ret = message_react_v1(token, message_id, react_id)
	save()
	return json.dumps(json_ret)

@APP.route("/message/pin/v1", methods=['POST'])
def message_pin():
	info = request.get_json()
	token = info['token']
	message_id = info['message_id']
	json_ret = message_pin_v1(token, message_id)
	save()
	return json.dumps(json_ret)

@APP.route("/message/unpin/v1", methods=['POST'])
def message_unpin():
	info = request.get_json()
	token = info['token']
	message_id = info['message_id']
	json_ret = message_unpin_v1(token, message_id)
	save()
	return json.dumps(json_ret)


@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater():
	info = request.get_json()
	token = info['token']
	channel_id = info['channel_id']
	message = info['message']
	time_sent = info['time_sent']
	return json.dumps(message_sendlater_v1(token, channel_id, message, time_sent))

@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlaterdm():
	info = request.get_json()
	token = info['token']
	dm_id = info['dm_id']
	message = info['message']
	time_sent = info['time_sent']
	return json.dumps(message_sendlaterdm_v1(token, dm_id, message, time_sent))

#Message unreact header
@APP.route("/message/unreact/v1", methods=['POST'])
def message_unreact():
	info = request.get_json()
	token = info['token']
	message_id = info['message_id']
	react_id = info['react_id']
	json_ret = message_unreact_v1(token, message_id, react_id)
	save()
	return json.dumps(json_ret)

#############################################################################
###############################DM_HEADERS####################################
#############################################################################
@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
	"""{ token, u_ids }"""
	info = request.get_json()
	token = info['token']
	u_ids = info['u_ids']
	json_ret = dm_create_v1(token,u_ids)
	save()
	return json.dumps(json_ret)

@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
	"""{token}"""
	token = flask.request.args.get('token')
	json_ret = dm_list_v1(token)
	save()
	return json.dumps(json_ret)

@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
	"""{ token, u_ids }"""
	info = request.get_json()
	token = info['token']
	dm_id = info['dm_id']
	json_ret = dm_remove_v1(token, dm_id)
	save()
	return json.dumps(json_ret)

@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
	token = flask.request.args.get('token')
	dm_id = int(flask.request.args.get('dm_id'))
	json_ret = dm_details_v1(token, dm_id)
	save()
	return json.dumps(json_ret)

@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():
	info = request.get_json()
	token = info['token']
	dm_id = info['dm_id']
	json_ret = dm_leave_v1(token, dm_id)
	save()
	return json.dumps(json_ret)

@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
	token = flask.request.args.get('token')
	dm_id = int(flask.request.args.get('dm_id'))
	start = int(flask.request.args.get('start'))
	json_ret = dm_messages_v1(token, dm_id, start)
	save()
	return json.dumps(json_ret)


#############################################################################
##############################USERS_HEADERS##################################
#############################################################################
@APP.route("/users/all/v1", methods=['GET'])
def users_all():
	token = flask.request.args.get('token')
	json_ret = users_all_v1(token)
	save()
	return json.dumps(json_ret)


#############################################################################
##############################USER_HEADERS###################################
#############################################################################
@APP.route("/user/profile/v1", methods=['GET'])
def user_profile():
	token = flask.request.args.get('token')
	u_id = int(flask.request.args.get('u_id'))
	json_ret = user_profile_v1(token, u_id)
	save()
	return json.dumps(json_ret)

@APP.route("/user/profile/setname/v1", methods=['PUT'])
def user_setname():
	info = request.get_json()
	token = info['token']
	name_first = info['name_first']
	name_last = info['name_last']
	json_ret = user_profile_setname_v1(token, name_first, name_last)
	save()
	return json.dumps(json_ret)


@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def user_setemail():
	info = request.get_json()
	token = info['token']
	email = info['email']
	json_ret = user_profile_setemail_v1(token, email)
	save()
	return json.dumps(json_ret)

#User Profile Sethandle Header:
@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_profile_sethandle():
	"""{ token, handle_str }"""
	info = request.get_json()
	user_token = info['token']
	new_handle = info['handle_str']
	json_ret = user_profile_sethandle_v1(user_token, new_handle)
	save()
	return json.dumps(json_ret)

#User Profile uploadphoto Header:
@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])
def user_profile_uploadphoto():
	"""{ token, img_url, x_start, y_start, x_end, y_end }"""
	info = request.get_json()
	user_token = info['token']
	url = info['img_url']
	start_x = info['x_start']
	start_y = info['y_start']
	end_x = info['x_end']
	end_y = info['y_end']
	json_ret = user_profile_uploadphoto_v1(user_token, url, start_x, start_y, end_x, end_y)
	save()
	return json.dumps(json_ret)
	
@APP.route("/user/stats/v1", methods=['GET'])
def user_stats():
	token = flask.request.args.get('token')
	json_ret = user_stats_v1(token)
	save()
	return json.dumps(json_ret)

@APP.route("/users/stats/v1", methods=['GET'])
def users_stats():
	token = flask.request.args.get('token')
	json_ret = users_stats_v1(token)
	save()
	return json.dumps(json_ret)

#############################################################################
###############################ADMIN_HEADERS#################################
#############################################################################
#Admin User Remove Header
@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove():
	"""{ token, u_id }"""
	info = request.get_json()
	admin_token = info['token']
	user_id = info['u_id']
	json_ret = user_remove_v1(admin_token, user_id)
	save()
	return json.dumps(json_ret)
	
#Admin UserPermission Change Header
@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change():
	"""{ token, u_id, permission_id }"""
	info = request.get_json()
	admin_token = info['token']
	user_id = info['u_id']
	permission_id = info['permission_id']
	json_ret = userpermission_change_v1(admin_token, user_id, permission_id)
	save()
	return json.dumps(json_ret)
	
#Search Header
@APP.route("/search/v1", methods=['GET'])
def search():
	token = flask.request.args.get('token')
	query_str = flask.request.args.get('query_str')
	json_ret = search_v1(token, query_str)
	save()
	return json.dumps(json_ret)
	
#notification header
@APP.route("/notifications/get/v1", methods=['GET'])
def notification():
	token = flask.request.args.get('token')
	json_ret = notifcation_get(token)
	save()
	return json.dumps(json_ret)
	

#############################################################################
###############################STANDUP_HEADERS###############################
#############################################################################

# standup start Header
@APP.route("/standup/start/v1", methods=['POST'])
def standup_start():
	"""{ token, channel_id, length }"""
	info = request.get_json()
	token = info['token']
	channel_id = info['channel_id']
	length = info['length']
	json_ret = standup_start_v1(token, channel_id, length)
	save()
	return json.dumps(json_ret)

# standup active Header
@APP.route("/standup/active/v1", methods=['GET'])
def standup_active():
	token = flask.request.args.get('token')
	channel_id = int(flask.request.args.get('channel_id'))
	json_ret = standup_active_v1(token, channel_id)
	save()
	return json.dumps(json_ret)

# Standup Send Header:
@APP.route("/standup/send/v1", methods=['POST'])
def standup_send():
	info = request.get_json()
	token = info['token']
	channel_id = info['channel_id']
	message = info['message']
	json_ret = standup_send_v1(token, channel_id, message)
	save()
	return json.dumps(json_ret)

#### NO NEED TO MODIFY BELOW THIS POINT
if __name__ == "__main__":
	signal.signal(signal.SIGINT, quit_gracefully) # For coverage
	#To run coverage, remove debug=True from the parameter set below
	APP.run(port=config.port) # Do not edit this port
