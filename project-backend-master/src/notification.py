from src.data_store import data_store
from src.helpers import decode_jwt
def notifcation_get(token):
    '''
    Return the user's most recent 20 notifications, ordered from most recent to least recent.
    
    Input: token
    Returns: List of notifications (user's message was reacted to, or user was tagged, or added to dm/channel)
    '''
    token_dic = decode_jwt(token)
    auth_user_id = token_dic['u_id']
    store = data_store.get()
    user_store = store['users']
    #list to store the notifications
    notif_list = []
    for user in user_store:
        if user[0]['u_id'] == auth_user_id:
            #grabs notificaiton list in the user data
            notif_list = user[1]['notifications'][:20]
    return{
        'notifications': notif_list
    }
        