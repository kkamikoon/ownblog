import hashlib, re

from flask  import current_app as app
from flask  import (
    flash,
    request,
    redirect,
    url_for,
    render_template
)

from app.utils      import user, get_config

from app.models     import db, Users, Attach

from app.utils.decorators import admin_only

# Get Blueprint
from app.admin import admin

@admin.route("/admin/users", methods=['GET'])
@admin_only
def users():
    attaches    = Attach.query.all()
    users       = db.session.query( Users.idx,
                                    Users.uid,
                                    Users.name,
                                    Users.attach,
                                    Users.verified,
                                    Users.email,
                                    Users.admin ).all()

    return render_template(f"/admin/{get_config('admin_theme')}/users/index.html",
                            users=users,
                            attaches=attaches)


@admin.route("/admin/users/<int:user_idx>", methods=['GET'])
@admin_only
def users_detail(user_idx):
    # Get user object
    user = Users.query.filter_by(idx=user_idx).first_or_404()
    
    return render_template(f"/admin/{get_config('admin_theme')}/users/detail.html",
                            user=user)


@admin.route("/admin/users/add", methods=['POST'])
@admin_only
def users_add():
    # request.form.get("admin") == None => unchecked
    # Core attributes
    uid         = request.form.get("uid")
    name        = request.form.get("name")
    email       = request.form.get("email")
    attach      = request.form.get("attach", type=int)
    password    = request.form.get("password")

    # Supplementary attributes
    hidden      = (request.form.get("hidden")   != None) # if not None == True
    banned      = (request.form.get("banned")   != None)
    verified    = (request.form.get("verified") != None)
    admin       = (request.form.get("admin")    != None)

    # Set user object
    user = Users(uid=uid,
                 name=name,
                 email=email,
                 attach=attach,
                 password=password,
                 hidden=hidden,
                 banned=banned,
                 verified=verified,
                 admin=admin)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # msg = e.orig.args[1] # Error Message
        flash(message=e.orig.args[1], category="error")
        return redirect(url_for(".users"))
    else:
        db.session.commit()
        
    return redirect(url_for(".users"))


@admin.route("/admin/users/edit/<int:user_idx>", methods=['POST'])
@admin_only
def users_edit(user_idx):
    # request.form.get("admin") == None => unchecked
    # Core attributes
    uid         = request.form.get("uid")
    name        = request.form.get("name")
    email       = request.form.get("email")
    password    = request.form.get("password")

    # Supplementary attributes
    hidden      = (request.form.get("hidden")   != None) # if not None == True
    banned      = (request.form.get("banned")   != None)
    verified    = (request.form.get("verified") != None)
    admin       = (request.form.get("admin")    != None)

    # Get user object
    user = Users.query.filter_by(idx=user_idx).first_or_404()
    
    # Set user object
    if password != None:
        user.password = hashlib.sha3_512(password.encode()).hexdigest()

    user.uid        = uid
    user.name       = name
    user.email      = email
    user.hidden     = hidden
    user.banned     = banned
    user.verified   = verified
    user.admin      = admin

    # Commit into database
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(message=e.orig.args[1], category="error")
        return redirect(url_for(".users_detail", user_idx=user_idx))
    else:
        db.session.commit()
    
    return redirect(url_for(".users_detail", user_idx=user.idx))


@admin.route("/admin/users/del/<int:user_idx>", methods=['POST'])
@admin_only
def users_del(user_idx):
    # request.form.get("admin") == None => unchecked
    # Core attributes
    uid         = request.form.get("uid")   

    # Get user object
    user = Users.query.filter_by(idx=user_idx, name=uid).first_or_404()

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(message=e.orig.args[1], category="error")
        return redirect(url_for(".users", user_idx=user_idx))
    else:
        db.session.commit()
        
    return redirect(url_for(".users"))