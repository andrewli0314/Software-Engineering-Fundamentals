import jwt
from src.error import InputError, AccessError
from src.data_store import data_store
from src.helpers import hash, generate_jwt, decode_jwt
from src.channels import is_valid_token
from src.channel import is_valid_user, is_global_owner, is_member, is_owner
from src.dm import is_dm_member, is_dm_creator
from src.auth import auth_logout_v1
# below for passwordreset
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from random import randint
import re

REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# help function
def random_with_six_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# change user's permission by global users
def userpermission_change_v1(token, u_id, permission_id):
	""" change the user's permission by global user
	Args:
		token ([string]): an authorisation hash that belongs to a global user
		user_id: id of the user who's permission need to be changed
		permission_id: either 1 or 2, 1 for global user and 2 for other members
	Returns:
		no need to return any value, already updated
	"""   
	# decode the token
	token_dic = decode_jwt(token)
	auth_user_id = token_dic['u_id']
	session_id = token_dic['session_id']
	
	if not is_valid_token(auth_user_id, session_id):
		raise AccessError(description = "Invalid Token")
	if not is_valid_user(u_id):
		raise InputError(description="Invalid u_id")
	if permission_id != 1 and permission_id != 2:
		raise InputError(description="Invalid permission_id")
	if not is_global_owner(auth_user_id):
		raise AccessError(description="Auth user is not a global member")
	
	# check if it's valid user and permission id
	# check if it's valid global user and how many of global user
	store = data_store.get()
	users_list = store['users']
	count_global_user = 0
	for user in users_list:
		if user[1]['is_global_member']:
			count_global_user += 1
	
	if count_global_user == 1 and is_global_owner(u_id):
		raise InputError(description="u_id is the only global owner")
	
	for user in users_list:
		if user[0]['u_id'] == u_id:
			if permission_id == 1:
				user[1]['is_global_member'] = True
			if permission_id == 2:
				user[1]['is_global_member'] = False
   
	return {}    
	
# to remove the user from stream, can be found by user id but will not in user list
def user_remove_v1(token, u_id):
    """ change the user's permission by global user
    Args:
        admin_token ([string]): an authorisation hash that belongs to a global user
        user_id: id of the user who need to be removed
        
        no need to return any value, already updated
    """   
    # decode the token
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    session_id = token_dic['session_id']
    if not is_valid_token(auth_user_id, session_id):
        raise AccessError(description = "Invalid Token")
    if not is_valid_user(u_id):
        raise InputError(description="u_id is not a valid user")
    if not is_global_owner(auth_user_id):
        raise AccessError(description="auth user is not a global owner")
    
    store = data_store.get()
    users_list = store['users']
    channels_list = store['channels']
    dm_list = store['dm']
    

    count_global_user = 0
    for user in users_list:
        if user[1]['is_global_member']:
            count_global_user += 1
        
    
    if count_global_user == 1 and is_global_owner(u_id):
        raise InputError(description="u_id is the only global owner")
    

    ##Go ahead and do ur own implementation:
    ##Removed from all channels and dms:
    for channel in channels_list:
        if is_member(u_id, channel['channel_id']):
            for message in channel['messages']:
                if message['u_id'] == u_id:
                    message['message'] = "Removed user"
            channel['members'].remove(u_id)
        if is_owner(u_id, channel['channel_id']):
            channel['owner'].remove(u_id)
        
    
    for dm in dm_list:
        if is_dm_member(u_id, dm['dm_id']):
            #remove message content:
            for message in dm['messages']:
                if message['u_id'] == u_id:
                    message['message'] = "Removed user"
            if u_id in dm['members']:
                dm['members'].remove(u_id)
            if u_id in dm['creator_id']:
                dm['creator_id'].remove(u_id)
            
        
    for user in users_list:
        if user[0]['u_id'] == u_id:
            user[0]['email'] = "N/A"
            user[0]['handle_str'] = "N/A"
            user[0]['name_first'] = "Removed"
            user[0]['name_last'] = "user"
            user[1]['session_id'] = [-1]
    
    return {}
    
def passwordreset_request_v1(email):
    """
    Passwordset_request takes request from user to change the password.
    A random six digits will be send as reset code to verify
    
    Arguments:
        email (string) - entered by user email

    Exceptions:
        No error will be raised if user entered invalid email addresses for a security/privacy concern

    Return Value:
        No return value request here
    """
    request_email = email['email']
    #print(email)
    if not re.fullmatch(REGEX, request_email):
        raise InputError(description="Invalid email format entered.")
    
    # When a user requests a password reset, they should be logged out of all current sessions
    store = data_store.get()
    susers = store['users']
    registered_user = 0
    user_data = {}
    for user in susers:
        if user[0]['email'] == request_email:
            user_data = user
            registered_user = 1
            sessions = user[1]['session_id']
            session_size = len(sessions)
            i = 0
            while i < session_size:
                token = jwt.encode({'u_id': user[0]['u_id'], 'session_id': sessions[0]}, 'H11B_BEAGLE', algorithm='HS256')
                auth_logout_v1(token)
                i += 1
    # if given email does not belongs to any registered user, end process, do nothing
    if registered_user == 0:
        return {}
    
    resetcode = str(random_with_six_digits(6))
    mail_content = str(resetcode) + ' is your code to reset your password.'
    user_data[2]['reset_code'] = resetcode
    
    #The mail addresses and password
    sender_address = 'dc.cocopala@gmail.com'
    sender_pass = '*~=X@c~A>cK$m@{0:l'
    receiver_address = request_email
    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = Header('COMP1531Project', 'utf-8')
    message['To'] = Header(user_data[0]['handle_str'], 'utf-8')
    message['Subject'] = 'Reset code from COMP1531 project.'   #The subject line
    
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    
    #Create SMTP session for sending the mail
    smtp_session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    smtp_session.starttls() #enable security
    smtp_session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    smtp_session.sendmail(sender_address, receiver_address, text)
    smtp_session.quit()
    
    return {}
    
  
def passwordreset_reset_v1(reset_code, new_password):
    """
    A randomsix digits will be entered to verify auth user
    Then new password will be reset
    
    Arguments:
        reset_code - code send to user's email for resetting password
        new_password - password user want to replace the old onw

    Exceptions:
        invalid resetcode been entered
        password length is less than 6
        password same as current password

    Return Value:
        No return value request here
    """    
    if len(new_password) < 6:
        raise InputError(description="Password must be greater than 6 characters.") 
    
    store = data_store.get()
    susers = store['users']
    found_code = 0
    
    for user in susers:
        if user[2]['reset_code'] == str(reset_code):
            found_code = 1
            if user[1]['password'] == hash(new_password):
                raise InputError(description="Cannot use previous password as new password.") 
            else:
                user[1]['password'] = hash(new_password)
            user[2]['reset_code'] = ''
            
        
    if found_code == 0:
        raise InputError(description="Invalid reset code entered.") 
    
    return {}

    
