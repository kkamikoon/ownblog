import os
from app.utils.encoding import hexencode

def generate_nonce():
    return hexencode(os.urandom(32))