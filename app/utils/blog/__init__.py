import os, shutil

from flask                  import current_app as app
from flask.helpers          import safe_join
from flask                  import session

from app.utils              import get_config
from app.models             import db, Categories


def get_categories():
    return db.session.query( Categories.name ).all()


def get_tmp_dir():
    tmp = safe_join(app.root_path, f"static", f"front", f"themes", get_config("front_theme"), f"tmp_{session.get('nonce')}")
    
    if not os.path.isdir(tmp):
        os.mkdir(tmp)
            
    return tmp


def clear_tmp_dir():
    tmp = get_tmp_dir()

    if os.path.isdir(tmp):
        shutil.rmtree(tmp)

    return True


def get_upload_dir():
    return get_config('upload_dir')
