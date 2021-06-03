import os, hashlib

from flask      import session
from flask      import current_app as app

from app.utils  import user as current_user
from app.utils.security.csrf import generate_nonce
# from CTFd.exceptions import UserNotFoundException, UserTokenExpiredException

def signin_user(user):
    # check repulication
    app.session_interface.repulication(user)

    session["idx"]      = user.idx
    session["name"]     = user.name
    session["email"]    = user.email
    session["admin"]    = user.admin
    session["nonce"]    = generate_nonce()

def signout_user():
    # Delete from client
    session.clear()

def in_whitelist():
    #req_ip  = current_user.get_ip()
    req_ip = current_user.get_ip_x_forwarded_for()
    
    ip_whitelist = []
    net_whitelist= ['0.0.0.0/0']

    # Specified IP
    if req_ip in ip_whitelist:
        return True

    # Specified Network
    for net in net_whitelist:
        if ip_address(req_ip) in ip_network(net):
            return True
        
    return False
