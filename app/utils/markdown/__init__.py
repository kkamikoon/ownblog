from flask         import current_app as app
from flask.helpers import safe_join

def get_markdown(path):
    return open(path, "r", encoding='utf-8').read()