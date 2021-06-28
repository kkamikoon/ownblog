from os             import path, listdir

from flask          import current_app as app
from flask.helpers  import safe_join

# from app.utils      import set_config, get_config

def get_themes(category=None):
    if category == "front" or category == None:
        path = safe_join(app.root_path, "static", "front", "themes")
    else:
        path = safe_join(app.root_path, "static", category, "themes")

    return listdir(path)
    
