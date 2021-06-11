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

from flask.helpers          import safe_join

from app.utils              import get_config
from app.utils.decorators   import admin_only
from app.models             import (
    db,
    Posts,
    PostImages,
    Categories
)

from app.utils.blog         import (
    get_img_upload_path,
    get_post_upload_path,
    get_images_path,
    get_ext,
    get_filename,
    get_tmp_dir,
    clear_tmp_dir,
    get_post_body,
    to_route_path
)

from app.utils.blog.posts   import (
    remove_post,
    remove_specific_post_image
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
    # Request method check
    if request.method == "POST":
        title           = request.form.get("title")
        category_idx    = request.form.get("category_idx")
        body            = request.form.get("body")
        abstract        = request.form.get("abstract")

        if category_idx == "":
            flash(message="Be calm... Your post is just saved in temp. Set your categories first.", category="warning")
            return redirect(url_for("admin.categories"))
        
        # Temp image upload to upload path. And replace temp path to upload path
        img_pathes      = get_images_path(body)
        upload_pathes   = []

        for path in img_pathes:
            # temp pathes to upload path
            upload_path = get_img_upload_path(title=title,
                                              ext=get_ext(path=path))
            
            # replace img path on body
            body        = body.replace( path,
                                        to_route_path(upload_path))

            # copy temp to upload path
            shutil.copyfile(safe_join(  get_tmp_dir(),
                                        get_filename(path=path)),   # temp path
                            upload_path)                            # copy to this path

            # temporary saving upload pathes for update database(PostImages)
            upload_pathes.append(upload_path)

                
        
        # markdown file saving
        file_for_upload = get_post_upload_path(title=title)

        with open(file_for_upload, "w") as upload_file_w:
            upload_file_w.write(body)

        post    = Posts(title=title,
                        category_idx=category_idx,
                        abstract=abstract,
                        filename=file_for_upload.split("/")[-1],
                        fullpath=file_for_upload)

        try:
            db.session.add(post)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        except Exception as e:
            db.session.rollback()
            flash(message="Unknown error occured", category="error")
            return redirect(url_for("admin.posts"))


        # Image update to database
        post    = Posts.query.filter_by(idx=post.idx).first()

        if post == None:
            flash(message="Failed to update images of this post.", category="error")
            return redirect(url_for("admin.posts"))

        for path in upload_pathes:
            img = PostImages(post_idx=post.idx,
                             path=path)
            try:
                db.session.add(img)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
            except Exception as e:
                db.session.rollback()
                flash(message="Unknown error occured", category="error")
                return redirect(url_for("admin.posts"))

        
        # clear temp dir
        clear_tmp_dir()

        # Finish
        flash(message="Post upload successfully.", category="success")
        return redirect(url_for("admin.posts"))

    # clear temp directory.
    if clear_tmp_dir():
        pass
    else:
        flash(message="Occuring error on clearing tmp directory.", category="error")
        return redirect(url_for("admin.posts"))

    return render_template( f"/admin/{get_config('admin_theme')}/contents/write.html")



@admin.route("/admin/posts/<post_idx>", methods=['GET', 'POST'])
@admin_only
def posts_detail(post_idx):
    post = Posts.query.filter_by(idx=post_idx).first()

    if post == None:
        flash(message=f"No matched post.", category="error")
        return redirect(url_for("admin.posts"))

    imgs = PostImages.query.filter_by(post_idx=post.idx).all()

    # Edit function
    if request.method == "POST":
        title               = request.form.get("title")
        category_idx        = request.form.get("category_idx")
        body                = request.form.get("body")
        abstract            = request.form.get("abstract")

        # markdown file full path modifying
        file_for_upload = get_post_upload_path(title=title)
        shutil.move(post.fullpath, file_for_upload)

        # update database(Posts)
        post.title          = title
        post.category_idx   = category_idx
        post.abstract       = abstract
        post.filename       = file_for_upload.split("/")[-1]
        post.fullpath       = file_for_upload

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(message=f"Unknown error occured", category="error")
            return redirect(url_for("admin.posts"))

        # update images on body
        img_pathes          = get_images_path(body)     # route pathes
        existing_pathes     = []                        
        upload_pathes       = []

        # Filtering existing pathes
        for img in imgs:
            try:
                img_pathes.remove(to_route_path(img.path)) # full path
            except ValueError:
                existing_pathes.append(img.path)
                

        # New images upload process - temp files
        for path in img_pathes:
            # temp pathes to upload path
            upload_path = get_img_upload_path(title=title,
                                              ext=get_ext(path=path))

            # replace img path on body
            body        = body.replace( path,
                                        to_route_path(upload_path))

            # copy temp to upload path
            shutil.copyfile(safe_join(  get_tmp_dir(),
                                        get_filename(path=path)),   # temp path
                            upload_path)                            # copy to this path

            # temporary saving upload pathes for update database(PostImages)
            upload_pathes.append(upload_path)

        # saving markdown file
        with open(post.fullpath, "w", encoding="utf-8") as edit_file_w:
            edit_file_w.write(body)


        # update new images to database
        for path in upload_pathes:
            img = PostImages(post_idx=post.idx,
                             path=path)
            try:
                db.session.add(img)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
            except Exception as e:
                db.session.rollback()
                flash(message=f"Unknown error occured", category="error")
                return redirect(url_for("admin.posts"))
        

        # remove not used existing post
        for path in existing_pathes:
            if not remove_specific_post_image(path):
                flash(message=f"Failed to remove img : {path}", category="error")
                        

        flash(message=f"Edit post successfully", category="success")
        return redirect(url_for("admin.posts"))

        
    # GET Method
    body = open(post.fullpath, "r", encoding="utf-8").read()

    return render_template( f"/admin/{get_config('admin_theme')}/contents/posts_detail.html",
                            post=post,
                            body=body)



@admin.route("/admin/posts/del/<post_idx>", methods=['GET', 'POST'])
@admin_only
def posts_del(post_idx):
    title   = request.form.get("title",     type=str)
    post    = Posts.query.filter_by(idx=post_idx).first()

    # No matched post selected
    if post == None:
        flash(message="No matched posts", category="error")
        return redirect(url_for("admin.posts_detail", post_idx=post_idx))
    
    # No matched title
    if post.title != title:
        flash(message="Title is not matched", category="error")
        return redirect(url_for("admin.posts_detail", post_idx=post_idx))

    if not remove_post(post):
        flash(message="Failed to delete post", category="error")
        return redirect(url_for("admin.posts_detail", post_idx=post_idx))
    

    flash(message="Post removed successfully.", category="success")
    return redirect(url_for("admin.posts"))
    

    
