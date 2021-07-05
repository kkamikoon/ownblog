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
    Categories,
    Tags
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
    remove_multiple_post_images
)

from app.utils.blog.tags    import (
    remove_multiple_tags
)

admin = Blueprint("admin", __name__)

from app.admin              import admin

@admin.route("/admin/posts", methods=['GET'])
@admin_only
def posts():
    posts   = db.session.query( Posts.idx,
                                Posts.category_idx,
                                Posts.title,
                                Posts.filename,
                                Posts.hidden ).all()

    return render_template( f"/admin/{get_config('admin_theme')}/contents/posts.html",
                            posts=posts)


@admin.route("/admin/posts/add", methods=['GET', 'POST'])
@admin_only
def posts_add():
    # Request method check
    if request.method == "POST":
        title           = request.form.get("title",         type=str, default="Empty Title")
        category_idxs   = request.form.get("category_idxs", type=str, default=None)
        body            = request.form.get("body",          type=str, default="Empty Body")
        abstract        = request.form.get("abstract",      type=str, default="No abstract")
        tags            = request.form.get("tags").split(" ")

        if category_idxs == None:
            # flash(message="Be calm... Your post is just saved in temp. Set your categories first.", category="warning")
            flash(message="Set your categories first.", category="warning")
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

        with open(file_for_upload, "w", encoding="utf-8") as upload_file_w:
            upload_file_w.write(body)

        # Split category idx
        cate_subcate    = category_idxs.split(":")
        c_idx           = cate_subcate[0]

        if cate_subcate[1] == "":
            sc_idx = None
        else:
            sc_idx = cate_subcate[1]

        post    = Posts(title=title,
                        category_idx=c_idx,
                        sub_category_idx=sc_idx,
                        abstract=abstract,
                        filename=file_for_upload.split("/")[-1],
                        fullpath=file_for_upload)
                        
        print(f"[=] post : {post}")

        try:
            db.session.add(post)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        except Exception as e:
            db.session.rollback()
            flash(message="Unknown error occured on posts", category="error")
            return redirect(url_for("admin.posts"))

        # Image update to database
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
                flash(message="Unknown error occured on images", category="error")
                return redirect(url_for("admin.posts"))

        # Tags update to database
        for tag in tags:
            t   = Tags( post_idx=post.idx,
                        name=tag.lower())
            try:
                db.session.add(t)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
            except Exception as e:
                db.session.rollback()
                flash(message="Unknown error occured on tags", category="error")
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

    return render_template( f"/admin/{get_config('admin_theme')}/contents/write.html" )



@admin.route("/admin/posts/<post_idx>", methods=['GET', 'POST'])
@admin_only
def posts_detail(post_idx):
    post = Posts.query.filter_by(idx=post_idx).first()

    if post == None:
        flash(message=f"No matched post.", category="error")
        return redirect(url_for("admin.posts"))

    imgs = PostImages.query.filter_by(post_idx=post.idx).all()
    tags = Tags.query.filter_by(post_idx=post.idx).all()

    # Edit function
    if request.method == "POST":
        title               = request.form.get("title")
        category_idxs       = request.form.get("category_idxs") # Category : Sub Category
        body                = request.form.get("body")
        abstract            = request.form.get("abstract")
        new_tags            = request.form.get("tags").split(" ")

        # markdown file full path modifying
        file_for_upload = get_post_upload_path(title=title)
        shutil.move(post.fullpath, file_for_upload)

        # Split category idx
        cate_subcate    = category_idxs.split(":")
        c_idx           = cate_subcate[0]

        if cate_subcate[1] == "":
            sc_idx = None
        else:
            sc_idx = cate_subcate[1]

        # update database(Posts)
        post.title              = title
        post.category_idx       = c_idx
        post.sub_category_idx   = sc_idx
        post.abstract           = abstract
        post.filename           = file_for_upload.split("/")[-1]
        post.fullpath           = file_for_upload

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
        existing_tags       = []

        # Filtering existing pathes
        for img in imgs:
            try:
                img_pathes.remove(to_route_path(img.path)) # full path
            except ValueError:
                existing_pathes.append(img.path)
        
        # Filtering existing tags
        for tag in tags:
            try:
                new_tags.remove(tag.name)
            except ValueError:
                existing_tags.append(tag.name)

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
                flash(message=f"Unknown error occured on update new images", category="error")
                return redirect(url_for("admin.posts"))
        
        # remove not used existing images
        if not remove_multiple_post_images(existing_pathes):
            flash(message=f"Failed to delete multiple post images", category="error")
            return redirect(url_for("admin.posts"))

        # update new tags to database
        for tag in new_tags:
            t   = Tags( post_idx=post.idx,
                        name=tag)
            try:
                db.session.add(t)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
            except Exception as e:
                db.session.rollback()
                flash(message=f"Unknown error occured on update new tags", category="error")
                return redirect(url_for("admin.posts"))

        # # remove not used existing tags
        if not remove_multiple_tags(tags=existing_tags):
            flash(message=f"Failed to delete multiple tags", category="error")
            return redirect(url_for("admin.posts"))


        flash(message=f"Edit post successfully", category="success")
        return redirect(url_for("admin.posts"))

        
    # GET Method
    body = open(post.fullpath, "r", encoding="utf-8").read()

    print(post.category_idx)
    print(post.sub_category_idx)

    return render_template( f"/admin/{get_config('admin_theme')}/contents/posts_detail.html",
                            post=post,
                            tags=" ".join([tag.name for tag in tags]),
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
    

    
@admin.route("/admin/posts/hidden/<post_idx>", methods=['GET'])
@admin_only
def posts_hidden(post_idx):
    post    = Posts.query.filter_by(idx=post_idx).first()

    # No matched post selected
    if post == None:
        flash(message="No matched posts", category="error")
        return "No"
    
    post.hidden = not post.hidden

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(message=f"Failed to edit post hidden value [idx:{post.idx}]", category="error")
        return "No"

    return str(bool(post.hidden))

    
