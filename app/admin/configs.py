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

    # About Post
    # User can only connect this domain if you `domain_check` set True
    about_post_idx  = request.form.get("about_post_idx", type=int, default=None)
    set_config('about_post_idx',  about_post_idx)

    # Post page size
    post_page_size  = request.form.get("post_page_size", type=int, default=None)
    set_config('post_page_size',  post_page_size)

    return redirect(url_for("admin.configs"))



@admin.route("/admin/configs/google", methods=['POST'])
@admin_only
def configs_google():
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

    # Google Analytics 
    analytics_id        = request.form.get("analytics_id")

    set_config('analytics_id',          analytics_id)
    
    return redirect(url_for("admin.configs"))


@admin.route("/admin/configs/users", methods=['POST'])
@admin_only
def configs_users():
    user_attach_idx = request.form.get("user_attach_idx")
    user_attach     = Attach.query.filter_by(idx=user_attach_idx).first()
    
    if user_attach == None:
        flash(message=f"Failed to set default user attachment", category="error")
        return redirect(url_for("admin.configs"))

    set_config("user_attach_idx", user_attach_idx)
    
    return redirect(url_for("admin.configs"))



@admin.route("/admin/configs/users/<config_type>", methods=['GET'])
@admin_only
def configs_users_default(config_type):
    if config_type == "attach":
        user_attach = Attach.query.filter_by(idx=get_config("user_attach_idx")).first()

        if user_attach == None:
            # flash(message=f"No matched user attachment", category="error")
            return "No"

        user_attach.hidden = not user_attach.hidden

        try:
            db.session.commit()
        except Exception as e:
            # flash(message=f"Failed to set default hide status of user attachment", category="error")
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
    facebook   = request.form.get("facebook")
    twitter    = request.form.get("twitter")
    instagram  = request.form.get("instagram") 
    youtube    = request.form.get("youtube")
    github     = request.form.get("github")
    
    set_config('facebook',  facebook)
    set_config('twitter',   twitter)
    set_config('instagram', instagram)    
    set_config('youtube',   youtube)
    set_config('github',    github)

    return redirect(url_for("admin.configs"))



@admin.route("/admin/configs/google/<service_type>", methods=['GET'])
@admin_only
def configs_google_status(service_type):
    status = get_config(f"set_google_{service_type}")

    if status == None:
        set_config(f"set_google_{service_type}", True)
        return str(True)
    
    set_config(f"set_google_{service_type}", not status)

    return str(not bool(status))



@admin.route("/admin/configs/sns/<sns_type>", methods=['GET'])
@admin_only
def configs_sns_status(sns_type):
    status = get_config(f"{sns_type}_open")

    if status == None:
        set_config(f"{sns_type}_open", True)
        return str(True)
    
    set_config(f"{sns_type}_open", not status)

    return str(not bool(status))




