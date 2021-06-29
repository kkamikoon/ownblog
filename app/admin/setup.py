import hashlib, re, os, datetime

from flask  import current_app as app
from flask  import (
    flash,
    request,
    redirect,
    url_for,
    render_template,
    send_file,
    abort
)

from flask.helpers  import safe_join

from app.utils      import get_config, set_config
from app.utils      import user as current_user

from app.models     import db, Users, Categories, Attach
from sqlalchemy.orm import load_only

from app.utils.decorators    import admin_only
from app.utils.user          import authed, get_current_user, is_admin
from app.utils.config        import is_setup
from app.utils.security.auth import signin_user

# Get Blueprint
from app.admin import admin

@admin.route("/admin/setup", methods=['GET', 'POST'])
def setup():
    if not is_setup():
        if request.method == "POST":
            # WEB ------------------------------------------------
            # Title 
            title_tag    = request.form.get("title_tag")
            intro        = request.form.get("intro")

            set_config("title_tag", title_tag)
            set_config("intro",     intro)

            # Theme
            admin_theme  = request.form.get("admin_theme")
            front_theme  = request.form.get("front_theme")

            set_config("admin_theme",  admin_theme)
            set_config("front_theme",  front_theme)

            # reCaptcha Settings
            recaptcha_site_key  = request.form.get("recaptcha_site_key")
            recaptcha_secret_key= request.form.get("recaptcha_secret_key")
            recaptcha_status    = request.form.get("recaptcha_status")

            if (    recaptcha_status     == 1   
                and recaptcha_site_key   != ""
                or  recaptcha_secret_key != "" ):
                flash(message=f"Please Setup Recaptcha correctly", category="error")
                db.session.rollback()
                return redirect(url_for("admin.setup"))

            set_config('recaptcha_site_key',    recaptcha_site_key)
            set_config('recaptcha_secret_key',  recaptcha_secret_key)
            set_config('recaptcha_status',      recaptcha_status)
            

            # Admin ----------------------------------------------
            # Admin Attachment Settings
            admin_attach_type       = request.form.get('admin_attach_type')
            admin_attach_description= request.form.get('admin_attach_description')
            admin_attach_hidden     = request.form.get('admin_attach_hidden', type=int)

            admin_attach            = Attach(type=admin_attach_type,
                                             description=admin_attach_description,
                                             hidden=admin_attach_hidden)

            try:
                db.session.add(admin_attach)
            except Exception as e:
                flash(message=f"Attach(Admin) : {e._message}", category="error")
                db.session.rollback()
                return redirect(url_for("admin.setup"))
            else:
                db.session.commit()

            # Admin Account
            uid         = request.form.get("uid")
            email       = request.form.get("email")
            password    = request.form.get("password")
            name        = request.form.get("name")
            attach      = request.form.get("admin_attachment",   type=int)

            account     = Users(uid=uid,
                                name=name,
                                email=email,
                                password=hashlib.sha3_512(password.encode()).hexdigest(),
                                attach=attach,
                                verified=True,
                                hidden=False,
                                admin=True)

            # Commit admin account
            try:
                db.session.add(account)
            except Exception as e:
                flash(message=f"Admin  : {e._message}", category="error")
                db.session.rollback()
                return redirect(url_for("admin.setup"))
            
            # Users ----------------------------------------------
            user_default_verified   = request.form.get('user_default_verified')
            user_default_hidden     = request.form.get('user_default_hidden')
            user_default_banned     = request.form.get('user_default_banned')
            user_attach_type        = request.form.get('user_attach_type')
            user_attach_description = request.form.get('user_attach_description')
            user_default_attach     = request.form.get('user_default_attach', type=int)

            set_config('user_default_verified', user_default_verified)
            set_config('user_default_hidden',   user_default_hidden)
            set_config('user_default_banned',   user_default_banned)

            user_attach             = Attach(type=user_attach_type,
                                             description=user_attach_description,
                                             hidden=user_default_attach)
            
            # Commit users account
            try:
                db.session.add(user_attach)
            except Exception as e:
                flash(message=f"Attach(User) : {e._message}", category="error")
                db.session.rollback()
                return redirect(url_for("admin.setup"))
            else:
                db.session.commit()

            set_config("user_attach_idx",   user_attach.idx)

            # Domain ----------------------------------------------
            # Domain Checking
            domain      = request.form.get("domain")
            domain_check= request.form.get("domain_check")

            set_config('domain',        domain)
            set_config('domain_check',  domain_check)

            # SNS -------------------------------------------------
            twitter    = request.form.get("twitter")
            instagram  = request.form.get("instagram") 
            github     = request.form.get("github")
            facebook   = request.form.get("facebook")
            youtube    = request.form.get("youtube")

            set_config('twitter',   twitter)
            set_config('instagram', instagram)
            set_config('github',    github)
            set_config('facebook',  facebook)
            set_config('youtube',   youtube)

            # Image Upload Directory ------------------------------
            upload_dir  = safe_join(app.root_path, 'static', 'front')
            set_config('upload_dir',    upload_dir)
            
            # image directory setup
            if not os.path.isdir(upload_dir + "/images"):
                os.mkdir(upload_dir + "/images")

            # post directory setup
            if not os.path.isdir(upload_dir + "/posts"):
                os.mkdir(upload_dir + "/posts")
                
            # Setup completed
            set_config("setup", True)

            return redirect(url_for("admin.index"))
        
        # if setup is note completed
        return render_template( f"/admin/{get_config('admin_theme')}/configs/setup.html" )

    else:
        flash(message="Your Web had been set already.", category="info")
        return redirect(url_for("admin.index"))
        