import base64
import codecs

from app.utils import string_types

def hexencode(s):
    if isinstance(s, string_types):
        s = s.encode("utf-8")
    encoded = codecs.encode(s, "hex")
    try:
        encoded = encoded.decode("utf-8")
    except UnicodeDecodeError:
        pass
    return encoded