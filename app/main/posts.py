from flask  import current_app as app
from flask  import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.utils          import get_config
from app.utils.markdown import get_markdown
from app.models         import db, Posts

from app.main           import main

@main.route("/posts", methods=['GET'])
def posts():
    page   = request.args.get("page", default=1, type=int)

    if page <= 0:
        flash(message="None valid page.", category="warning")
        return redirect(url_for(".posts"))

    # Case of post pages    
    posts  = Posts.query.filter_by(hidden=False).order_by(Posts.idx.desc())\
                                                .offset((page-1) * get_config("post_page_size"))\
                                                .limit(get_config("post_page_size"))\
                                                .all()
    
    counts = int(Posts.query.filter_by(hidden=False).count() / get_config("post_page_size"))

    return render_template( f"/front/{get_config('front_theme')}/posts/index.html",
                            path='',
                            posts=posts,
                            counts=counts,
                            page=page )


@main.route("/posts/<post_idx>", methods=['GET'])
def post_detail(post_idx):
    post    = Posts.query.filter_by(idx=post_idx,
                                    hidden=False).first()

    if post == None:
        flash(message="None valid post selected.", category="error")
        return redirect(url_for(".posts"))
    
    return render_template( f"/front/{get_config('front_theme')}/posts/detail.html",
                            post=get_markdown(post.fullpath),
                            title=post.title,
                            abstract=post.abstract )

