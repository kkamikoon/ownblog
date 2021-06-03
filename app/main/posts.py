from flask  import current_app as app
from flask  import (
    render_template
)

from app.utils          import get_config

from app.models         import db, Posts

from app.main           import main

@main.route("/posts", methods=['GET'])
def posts():
    posts = Posts.query.limit(5).all()

    return render_template(f"/front/{get_config('front_theme')}/main/posts.html",
                            posts=posts)


@main.route("/posts/<post_idx>", methods=['GET'])
def post_detail(post_idx):
    pass
