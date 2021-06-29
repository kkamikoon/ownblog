from datetime import datetime

from flask  import current_app as app
from flask  import (
    flash,
    request,
    redirect,
    url_for,
    render_template
)

from app.utils      import user, get_config, set_config

from app.models     import db, Configs, Attach, Posts

from app.utils.decorators import admin_only

# Get Blueprint
from app.admin import admin


@admin.route("/admin/configs", methods=['GET'])
@admin_only
def configs():    
    configs_data= db.session.query( Configs.key, Configs.value ).all()
    posts       = Posts.query.all()
    attaches    = Attach.query.filter(Attach.idx != 1).all() # Except admin type

    return render_template( f"/admin/{get_config('admin_theme')}/configs/configs.html",
                            configs=configs_data,
                            posts=posts,
                            attaches=attaches )


@admin.route("/admin/configs/web", methods=['POST'])
@admin_only
def configs_web():
    # Web Titles
    title_tag    = request.form.get("title_tag")
    intro        = request.form.get("intro")

    # Theme
    admin_theme  = request.form.get("admin_theme")
    front_theme  = request.form.get("front_theme")

    set_config("admin_theme",  admin_theme)
    set_config("front_theme",  front_theme)

    # Recaptcha (Key & Status)
    recaptcha_site_key  = request.form.get("recaptcha_site_key")
    recaptcha_secret_key= request.form.get("recaptcha_secret_key")
    recaptcha_status    = request.form.get("recaptcha_status")

    if (    recaptcha_status     == 1   
        and recaptcha_site_key   != ""
        or  recaptcha_secret_key != "" ):
        flash(message=f"Please Setup Recaptcha correctly", category="error")
        db.session.rollback()
        return redirect(url_for("admin.configs"))

    set_config('recaptcha_site_key',    recaptcha_site_key)
    set_config('recaptcha_secret_key',  recaptcha_secret_key)
    set_config('recaptcha_status',      recaptcha_status)

    # About Post
    # User can only connect this domain if you `domain_check` set True
    about_post_idx  = request.form.get("about_post_idx", type=int, default=None)

    set_config('about_post_idx',  about_post_idx)

    return redirect(url_for("admin.configs"))
    

@admin.route("/admin/configs/users", methods=['POST'])
@admin_only
def configs_users():
    user_default_attach     = request.form.get("user_default_attach")
    user_attach             = Attach.query.filter_by(idx=get_config("user_default_attach")).first()
    
    if user_attach == None:
        flash(message=f"Failed to set default user attachment", category="error")
        return redirect(url_for("admin.configs"))

    set_config("user_default_attach", user_default_attach)
    
    return redirect(url_for("admin.configs"))


@admin.route("/admin/configs/users/<config_type>", methods=['GET'])
@admin_only
def configs_users_default(config_type):
    if config_type == "attach":
        user_attach = Attach.query.filter_by(idx=get_config("user_default_attach")).first()

        user_attach.hidden = not user_attach.hidden

        try:
            db.session.commit()
        except Exception as e:
            flash(message=f"Failed to set default hide status of user attachment", category="error")
            db.session.rollback()
            return "No"

        return str(bool(user_attach.hidden))

    else: # verified, hidden, banned
        set_config(f"user_default_{config_type}", not get_config(f"user_default_{config_type}"))

        return str(bool(get_config(f"user_default_{config_type}")))
    
    return "No"


@admin.route("/admin/configs/domain", methods=['POST'])
@admin_only
def configs_domain():    
    # User can only connect this domain if you `domain_check` set True
    domain      = request.form.get("domain")

    set_config('domain',        domain)

    return redirect(url_for("admin.configs"))

    

@admin.route("/admin/configs/sns", methods=['POST'])
@admin_only
def configs_sns():
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

    return redirect(url_for("admin.configs"))

