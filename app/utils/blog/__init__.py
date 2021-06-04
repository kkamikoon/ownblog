import os, re, shutil

from flask                  import current_app as app
from flask.helpers          import safe_join
from flask                  import session

from app.utils              import get_config
from app.models             import db, Categories

from uuid                   import uuid4

def get_categories():
    return Categories.query.all()


def get_category(idx):
    return Categories.query.filter_by(idx=idx).first()


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


def get_post_upload_path(title):
    """
    :param  title:  title of post

    :return:        safe joined root path of post directory
    """
    return get_config("upload_dir") + "/posts/" + title.replace(" ", "_") + ".md"


def get_img_upload_path():
    """
    :return:        safe joined root path of image directory
    """
    return get_config('upload_dir') + "/images/"


def get_images_path(body):
    """
    :param  body:   markdown text data
    
    :return:        path of images - list type (filtered duplicates)
    """
    img_regex = re.compile(r"/static/front/[a-zA-Z0-9]*/tmp_[a-z0-9]*/[a-z0-9]*[\.a-z0-9]{1,10}")
    return list(set(body.findall(img_regex)))