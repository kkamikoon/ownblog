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

from sqlalchemy.exc         import IntegrityError

from app.utils              import get_config
from app.utils.decorators   import admin_only
from app.models             import db, Posts, Categories
from app.utils.blog         import (
    get_img_upload_dir,
    get_post_upload_dir,
    clear_tmp_dir
    get_images_path
)

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
        body            = request.form.get("body")
        abstract        = request.form.get("abstract")

        if category_idx == "":
            flash(message="Be calm... Your post is just saved in temp. Set your categories first.", category="warning")
            return redirect(url_for("admin.categories"))
        
        # markdown file saving        
        file_for_upload = get_upload_dir(title)

        with open(file_for_upload, "w") as upload_file_w:
            upload_file_w.write(body)

        post    = Posts(title=title,
                        category_idx=category_idx,
                        abstract=abstract,
                        filename=file_for_upload.split("/")[-1],
                        filedir=file_for_upload)

        try:
            db.session.add(post)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        except Exception as e:
            db.session.rollback()
            flash(message="Unknown error occured", category="error")
            return redirect(url_for("admin.posts"))

        
        flash(message="Post upload successfully.", category="success")
        return redirect(url_for("admin.posts"))
    
    return render_template( f"/admin/{get_config('admin_theme')}/contents/write.html")
