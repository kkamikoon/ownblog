import shutil

from flask  import current_app as app
from flask  import (
    Blueprint,
    request,
    redirect,
    flash,
    url_for,
    render_template
)

from app.utils              import get_config
from app.utils.decorators   import admin_only
from app.models             import db, Posts, Categories
from app.utils.blog         import get_upload_dir, clear_tmp_dir

admin = Blueprint("admin", __name__)

from app.admin              import admin

@admin.route("/admin/posts", methods=['GET'])
@admin_only
def posts():
    posts   = db.session.query( Posts.idx,
                                Posts.category_idx,
                                Posts.title,
                                Posts.filename ).all()

    return render_template( f"/admin/{get_config('admin_theme')}/contents/posts.html",
                            posts=posts)

@admin.route("/admin/posts/add", methods=['GET', 'POST'])
@admin_only
def posts_add():
    if clear_tmp_dir():
        pass
    else:
        flash(message="Occuring error on clearing tmp directory.", category="error")
        redirect(url_for("admin.posts"))
    
    if request.method == "POST":
        title           = request.form.get("title")
        category_idx    = request.form.get("category_idx")
        hidden          = request.form.get("hidden")
        body            = request.form.get("body")

        # print(f"[=] title        : {title}")
        # print(f"[=] category_idx : {category_idx}")
        # print(f"[=] hidden       : {hidden}")
        # print(f"[=] body         : {body}")

        if category_idx == "":
            flash(message="Be calm... Your post is just saved in temp. Set your categories first.", category="warning")
            return redirect(url_for("admin.categories"))

        return redirect(url_for("admin.posts"))
    
    return render_template( f"/admin/{get_config('admin_theme')}/contents/write.html")
