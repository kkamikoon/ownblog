from flask  import current_app as app
from flask  import (
    render_template
)

from app.utils          import get_config
from app.utils.markdown import get_markdown
from app.models         import db, Posts

from app.main           import main

@main.route("/posts", methods=['GET'])
def posts():
    posts           = Posts.query.filter_by(hidden=False).limit(5).all()
    
    return render_template(f"/front/{get_config('front_theme')}/posts/index.html",
                            path='',
                            posts=posts)


@main.route("/posts/<post_idx>", methods=['GET'])
def post_detail(post_idx):
    post = Posts.query.filter_by(idx=post_idx).first()

    return render_template( f"/front/{get_config('front_theme')}/posts/detail.html",
                            post=get_markdown(post.fullpath),)
