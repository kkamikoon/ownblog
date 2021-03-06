import os, re, shutil

from flask                  import current_app as app
from flask.helpers          import safe_join
from flask                  import session

from app.utils              import get_config
from app.models             import db, Categories, SubCategories

from uuid                   import uuid4

def get_categories():
    return Categories.query.all()


def get_category(idx):
    return Categories.query.filter_by(idx=idx).first()


def get_subcategories():
    return SubCategories.query.all()


def get_subcategories_of_category(category_idx):
    return SubCategories.query.filter_by(category_idx=category_idx).all()


def get_all_categories():
    categories      = Categories.query.all()
    all_categories  = []

    for category in categories:
        # Categories
        all_categories.append({ "name"              : category.name,
                                "hidden"            : category.hidden,
                                "category_idx"      : category.idx,
                                "sub_category_idx"  : None,})
        # Sub categories
        for sub in SubCategories.query.filter_by(category_idx=category.idx):
            all_categories.append({ "name"              : sub.name,
                                    "hidden"            : sub.hidden,
                                    "category_idx"      : sub.category_idx,
                                    "sub_category_idx"  : sub.idx,})

    return all_categories

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
    return get_config("upload_dir") + f"/posts/{filename_filtering(title)}_{str(uuid4()).replace('-', '_')}.md" 


def get_img_upload_path(title, ext):
    """
    :param  title:  title of post
    
    :return:        safe joined root path of image directory
    """
    return get_config('upload_dir') + f"/images/{filename_filtering(title)}_{str(uuid4()).replace('-', '_')}{ext}"


def get_images_path(body):
    """
    :param  body:   markdown text data
    
    :return:        path of images - list type (filtered duplicates)
    """
    #img_regex = re.compile(r"/static/front/[a-zA-Z0-9]*/tmp_[a-z0-9]*/[a-z0-9]*[\.a-z0-9]{1,10}")
    img_regex = re.compile(r"/static/front/[a-zA-Z0-9_/]*/[a-z0-9_]*[\.a-z0-9]{1,10}")

    return list(set(img_regex.findall(body)))


def get_ext(path):
    """
    :param  path:       file path for filter ext

    :return:            ext (.gif, .png, etc)
    """

    _, ext = os.path.splitext(path)

    return ext


def get_filename(path):
    """
    :param  path:       file path for get some file name

    :return:            filename
    """

    return os.path.split(path)[-1]


def get_post_body(path):
    """
    :param  path:       full path of post markdown file.

    :return:            string data of markdown that read
    """
    with open(path, "r", encoding="utf-8") as file_r:
        return file_r.read()


def to_route_path(path):
    """
    :param  path:       path for switch to route path(root_path -> route path)

    :return:            route path (/static/<theme>/<vendor>/<path:path>)
    """

    return path.replace(app.root_path, "").replace("/themes", "")


def filename_filtering(filename):
    filter_list = ["/", '(', ")"]
    
    for f in filter_list:
        filename = filename.replace(f, "_")
    
    return filename
