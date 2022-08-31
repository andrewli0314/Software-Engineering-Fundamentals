"""This file has auth_register_v1 and auth_login_v1"""
import re
import jwt
from src.error import InputError, AccessError
from src.data_store import data_store
from src.helpers import hash, generate_jwt, decode_jwt
from src.channels import is_valid_token

REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check_dual_emails(email, email_list):
	"""Checks to see if the email has a duplicate
	# 1 for valid and 0 for not valid"""
	for mail in email_list:
		if email == mail:
			return 0
	return 1

def nextid(users_list):
	"""Returns the next ID for user"""
	last = 0
	for user in users_list:
		last = user
	last += 1
	return last

#Remove spaces in name_first and name_last
#maximum 20 characters
#if handle_str is found, add a 0.
#make sure all chars are alphanumeric
def name_to_handle_str (name_first, name_last):
	"""This Function makes sure that handle_string is properly handled"""
	handle_str = name_first.lower() + name_last.lower()
	handle_alphanumeric = ''.join(char for char in handle_str if char.isalnum())
	#cut down to 20 letters
	if len(handle_str) > 20:
		concatenated_str = ""
		for idx in range(0, 20):
			concatenated_str += handle_alphanumeric[idx]
		handle_alphanumeric = concatenated_str
	#check for any existing handle_str
	store = data_store.get()
	susers = store['users']
	#gives you a list of handle_str from users
	str_list = to_list(susers, 0, 'handle_str')
	#check if there are any similar handle_str to append a number with at the end:
	for h_str in str_list:
		if h_str == handle_alphanumeric:
			#We will append a number at the end; count how many repitions and append at the end
			i = -1
			for str_h in str_list:
				if handle_alphanumeric in str_h:
					i+=1
			handle_alphanumeric += str(i)

	return handle_alphanumeric

def to_list (users_list, idx, key):
	"""Converts a certain type data into a list"""
	return_list = []
	for user in users_list:
		return_list.append(user[idx][key])
	return return_list

def auth_login_v1(email, password):
    """
    auth_login_v1 takes an email and password as input and then checks if there is a
    dictionary in our users list that has the same email and password combination
    and generates an authentication token using their user ID

    Arguments:
        email (string) - entered by user email
        password (string) - entered by user password

    Exceptions:
        InputError  - Occurs when
            * email entered doesnt belong to a users
            * password doesn't match the users password 

    Return Value:
        Returns auth_user_id and token on condition that the correct email and password 
        combination has been entered
    """
    store = data_store.get()
    susers = store['users']
    email_list = to_list (susers, 0, 'email')
    password_list = to_list (susers, 1, 'password')
    user_id = to_list (susers, 0, 'u_id')
    score = 0
    idx = 0
    for registered_email in email_list:
        if email == registered_email:
            score = 1
            break
        idx += 1
    if score == 0:
        raise InputError (description="Email entered does not belong to a user")

    if password_list[idx] != hash(password):
        raise InputError (description="Password is not correct")
    return {
        'token' : generate_jwt(user_id[idx]),
        'auth_user_id' : user_id[idx]
    }


def auth_register_v1(email, password, name_first, name_last):
    """
    This function takes new users first name, last name, email and password and generates
    a new user dictionary with all the input data, handle which is a concatenation
    of the users first and last name and a user id and generates authentication 
    token for the users first session.

    Arguments:
        email (string) - email entered by new user
        password (string) - password entered by new user
        name_first (string) - first name entered by new user
        name_last (string) - last name entered by new user

    Exceptions:
        InputError - Occurs when:
            * email is not valid (syntax)
            * email address is being used by another user
            * password entered is less than 6 characters long
            * name_first not between 1-50 characters inclusive
            * name_last not between 1-50 characters inclusive

    Return Value:
        Returns auth_user_id and token
    """
    store = data_store.get()
    susers = store['users']
    semail = to_list(susers, 0, 'email')
    if not re.fullmatch(REGEX, email) or check_dual_emails(email,semail) != 1:
        raise InputError(description="Invalid email or email already in use")
    if len(password) < 6:
        raise InputError(description="Password must be greater than 6 characters")
    if  len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description="First name must be between 1 and 50 characters inclusive")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(description="Last name must be between 1 and 50 characters inclusive")

    nid = nextid(to_list (susers, 0, 'u_id'))

    #determines if the user is a global member based on the id:

    is_global = bool(nid == 1)

    #this will be appended in 'users'.
    #Index 0 is the details of the user, which will be used later on
    #Index 1 is the password, will only bu used in auth_login so it has no significance.
    user_dictionary = [
        {
                'u_id': nid,
                'email': email,
                'name_first': name_first,
                'name_last': name_last,
                'handle_str': name_to_handle_str(name_first, name_last)
        },
        {
            'password': hash(password),
            'is_global_member' : is_global,

            'session_id' :[0],
            'notifications':[]
        },
        {
            'reset_code': ''
        }
            ]
    susers.append(user_dictionary)
    return {
        'token' : jwt.encode({'u_id': nid, 'session_id': 0}, 'H11B_BEAGLE', algorithm='HS256'),
        'auth_user_id': nid
    }




def auth_logout_v1(token): 
	"""
	This function logs a user out of the server, given a valid token

	Arguments:
		token (str) - a string of the users hashed token

	Returns {}

	"""
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	#deal with errors first:
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError (description="Invalid Token")
	
	#Get the data from store:
	store = data_store.get()
	users_list = store['users']
	for user in users_list:
		if auth_user_id == user[0]['u_id']:
			user[1]['session_id'].remove(session_id)
	return {}
