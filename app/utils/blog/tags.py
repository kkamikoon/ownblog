from flask                  import current_app as app
from flask.helpers          import safe_join

from app.utils              import get_config

from app.models             import db, TagList

def get_tags():
    return TagList.query.all()