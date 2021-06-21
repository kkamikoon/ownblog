from flask                  import current_app as app
from flask.helpers          import safe_join

from app.utils              import get_config

from app.models             import db, Tags, TagList


def get_tags():
    return TagList.query.all()


def remove_multiple_tags(tags):
    """
    :param  tags:       name of tag list (type is list)

    :comment:       remove multiple tags using tag name list

    :return:        True - successfully removed
                    False - failed to removed
    """
    try:
        db.session.query(Tags.idx).filter(Tags.name.in_(tags)).delete(synchronize_session=False)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False

    return True


def remove_specific_tag(tag, post_idx):
    """
    :param  tag:        tag name connected with post_idx
    :param  post_idx:   post idx on database

    :comment:       remove specific tag and update database

    :return:        True - successfully removed
                    False - failed to removed
    """
    try:
        # Tags.query.filter_by(   post_idx==post_idx,
        #                         name==tag).delete()
        db.session.query(Tags.name==tag, Tags.post_idx==post_idx).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False
    
    return True