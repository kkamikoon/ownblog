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
    
    # Commit users account
    try:
        db.session.commit()
    except Exception as e:
        flash(message=f"Failed to edit default user define : {e._message}", category="error")
        db.session.rollback()
        return redirect(url_for("admin.configs"))
    else:
        db.session.commit()
    
    return redirect(url_for("admin.configs"))


@admin.route("/admin/configs/users/<config>", methods=['GET'])
@admin_only
def configs_users_default(config):
    config_type={   "verified"  : get_config("user_default_verified"),
                    "hidden"    : get_config("user_default_hidden"),
                    "banned"    : get_config("user_default_banned")}.get(config, "attach")
    
    if config_type == "attach":
        user_attach = Attach.query.filter_by(idx=get_config("user_default_attach")).first()

        user_attach.hidden = not user_attach.hidden

        try:
            db.session.commit()
        except Exception as e:
            flash(message=f"Failed to set default user attachment hide status", category="error")
            db.session.rollback()
            return "No"

        return str(bool(user_attach.hidden))

    else: # verified, hidden, banned
        set_config(f"user_default_{config}", not config_type.get(config))

        return str(bool(config_type.get(config)))
    
    return "No"


@admin.route("/admin/configs/domain", methods=['POST'])
@admin_only
def configs_domain():    
    # User can only connect this domain if you `domain_check` set True
    domain      = request.form.get("domain")
    domain_check= request.form.get("domain_check")

    set_config('domain',        domain)
    set_config('domain_check',  domain_check)

    return redirect(url_for("admin.configs"))



@admin.route("/admin/configs/sns/<sns_type>", methods=['POST'])
@admin_only
def configs_sns(sns_type):


    twitter    = (request.form.get("twitter")   != None) # if not None == True
    instagram  = (request.form.get("instagram") != None) 
    github     = (request.form.get("github")    != None)
    facebook   = (request.form.get("facebook")  != None)
    youtube    = (request.form.get("youtube")   != None)

    set_config('twitter',   twitter)
    set_config('instagram', instagram)
    set_config('github',    github)
    set_config('facebook',  facebook)
    set_config('youtube',   youtube)

    return redirect(url_for("admin.configs"))

