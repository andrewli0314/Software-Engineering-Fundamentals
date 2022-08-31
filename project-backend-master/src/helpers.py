from src.data_store import data_store
import hashlib
import jwt
import re
import json
import math
import time
from src.error import InputError, AccessError
from src.data_store import data_store

SECRET = 'H11B_BEAGLE'

def generate_new_session_id(auth_user_id):
	"""Generates a new sequential session ID

	Returns:
		number: The next session ID
	"""
	store = data_store.get()
	susers = store['users']
	for user in susers:
		if user[0]['u_id'] == auth_user_id:
			session_list = user[1]['session_id']
			if user[1]['session_id'] == []:
				return_session_id = 0
				session_list.append(return_session_id)
			else:
				return_session_id = session_list[-1] + 1
				session_list.append(return_session_id)
	return return_session_id


def hash(input_string):
	"""Hashes the input string with sha256

	Args:
		input_string ([string]): The input string to hash

	Returns:
		string: The hexidigest of the encoded string
	"""
	return hashlib.sha256(input_string.encode()).hexdigest()


def generate_jwt(auth_user_id):
	"""Generates a JWT using the global SECRET

	Args:
		username ([string]): The username
		session_id ([string], optional): The session id, if none is provided will
										 generate a new one. Defaults to None.

	Returns:
		string: A JWT encoded string
	"""
	session_id = generate_new_session_id(auth_user_id)
	return jwt.encode({'u_id': auth_user_id, 'session_id': session_id}, SECRET, algorithm='HS256')

def encode_jwt(auth_user_id, session_id):
	"""Generates a JWT using the global SECRET

	Args:
		username ([string]): The username
		session_id ([string], optional): The session id, if none is provided will
										 generate a new one. Defaults to None.

	Returns:
		string: A JWT encoded string
	"""
	return jwt.encode({'u_id': auth_user_id, 'session_id': session_id}, SECRET, algorithm='HS256')

def decode_jwt(encoded_jwt):
	"""Decodes a JWT string into an object of the data

	Args:
		encoded_jwt ([string]): The encoded JWT as a string

	Returns:
		Object: An object storing the body of the JWT encoded string
	"""
	return jwt.decode(encoded_jwt, SECRET, algorithms=['HS256'])
