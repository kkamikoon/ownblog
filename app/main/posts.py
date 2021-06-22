from flask  import current_app as app
from flask  import (
    render_template
)

from app.utils          import get_config
from app.utils.markdown import get_markdown
from app.models         import db, Posts, Categories, SubCategories

from app.main           import main

@main.route("/posts", methods=['GET'])
def posts():
    posts           = Posts.query.limit(5).all()

    categories      = Categories.query.filter_by(hidden=False).all()
    subcategories   = SubCategories.query.filter_by(hidden=False).all()

    all_categories  = []

    for category in categories:
        tmp = {}
        tmp['idx']    = category.idx
        tmp['name']   = category.name
        tmp['subs']   = [sub for sub in subcategories if sub.category_idx == category.idx ]

        all_categories.append(tmp)
    
    return render_template(f"/front/{get_config('front_theme')}/posts/index.html",
                            posts=posts,
                            all_categories=all_categories)


@main.route("/posts/<post_idx>", methods=['GET'])
def post_detail(post_idx):
    post = Posts.query.filter_by(idx=post_idx).first()

    return render_template( f"/front/{get_config('front_theme')}/posts/detail.html",
                            post=get_markdown(post.fullpath),)
