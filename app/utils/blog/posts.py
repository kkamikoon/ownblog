import os, re, shutil

from flask                  import current_app as app
from flask.helpers          import safe_join

from app.utils              import get_config

from app.models             import db, PostImages


def remove_post(post):
    """
    :param  post:   Posts model class data

    :comment:       Must do this function first before delete post.

    :return:        True - successfully removed
                    False - failed to removed
    """
    if post == None:
        return False

    if not remove_post_images(post):
        return False
    
    os.remove(post.fullpath)

    try:
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False

    return True


def remove_post_images(post):
    """
    :param  post:   Posts model class data

    :comment:       Must do this function first before delete post.

    :return:        True - successfully removed
                    False - failed to removed
    """
    if post == None:
        return False
    
    post_images = PostImages.query.filter_by(post_idx=post.idx).all()

    for image in post_images:
        os.remove(image.path)

    try:
        db.session.query(PostImages.post_idx==post.idx).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False

    return True


def remove_specific_post_image(path):
    """
    :param  path:   path of post image (using matching post)

    :comment:       remove specific image and update database

    :return:        True - successfully removed
                    False - failed to removed
    """
    try:
        db.session.query(PostImages.path==path).delete()
        os.remove(path)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False
    
    return True