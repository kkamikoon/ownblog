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

    return render_template( f"/admin/{get_config('admin_theme')}/configs/configs.html",
                            configs=configs_data,
                            posts=posts )


@admin.route("/admin/configs/web", methods=['POST'])
@admin_only
def configs_web():
    title_tag    = request.form.get("title_tag")
    intro        = request.form.get("intro")

    # Theme
    admin_theme  = request.form.get("admin_theme")
    front_theme  = request.form.get("front_theme")

    set_config("admin_theme",  admin_theme)
    set_config("front_theme",  front_theme)

    recaptcha_site_key  = request.form.get("recaptcha_site_key")
    recaptcha_secret_key= request.form.get("recaptcha_secret_key")
    recaptcha_status    = request.form.get("recaptcha_status")

    # reCaptcha Settings
    if (    recaptcha_status     == 1   
        and recaptcha_site_key   != ""
        or  recaptcha_secret_key != "" ):
        flash(message=f"Please Setup Recaptcha correctly", category="error")
        db.session.rollback()
        return redirect(url_for("admin.configs"))

    set_config('recaptcha_site_key',    recaptcha_site_key)
    set_config('recaptcha_secret_key',  recaptcha_secret_key)
    set_config('recaptcha_status',      recaptcha_status)

    return redirect(url_for("admin.configs"))
    

@admin.route("/admin/configs/users", methods=['POST'])
@admin_only
def configs_users():
    user_default_verified   = request.form.get('user_default_verified')
    user_default_hidden     = request.form.get('user_default_hidden')
    user_default_banned     = request.form.get('user_default_banned')
    user_attach_type        = request.form.get('user_attach_type')
    user_description        = request.form.get('user_description')
    user_attach_hidden      = request.form.get('user_attach_hidden', type=int)

    set_config('user_default_verified', user_default_verified)
    set_config('user_default_hidden',   user_default_hidden)
    set_config('user_default_banned',   user_default_banned)

    user_attach             = Attach(type=user_attach_type,
                                    description=user_description,
                                    hidden=user_attach_hidden)
    
    # Commit users account
    try:
        db.session.add(user_attach)
    except Exception as e:
        flash(message=f"Attach(User) : {e._message}", category="error")
        db.session.rollback()
        return redirect(url_for("admin.configs"))
    else:
        db.session.commit()
    
    return redirect(url_for("admin.configs"))


@admin.route("/admin/configs/domain", methods=['POST'])
@admin_only
def configs_domain():    
    # User can only connect this domain if you `domain_check` set True
    domain      = request.form.get("domain")
    domain_check= request.form.get("domain_check")

    set_config('domain',        domain)
    set_config('domain_check',  domain_check)

    return redirect(url_for("admin.configs"))


@admin.route("/admin/configs/about", methods=['POST'])
@admin_only
def configs_about():
    # User can only connect this domain if you `domain_check` set True
    about_post_idx  = request.form.get("about_post_idx", type=int, default=None)

    set_config('about_post_idx',  about_post_idx)

    return redirect(url_for("admin.configs"))


