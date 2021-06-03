from flask  import current_app as app
from flask  import (
    request,
    redirect,
    url_for,
    render_template,
    flash,
)

from app.utils.security.auth import (
    signin_user,
    signout_user,
)

from app.utils.decorators   import ratelimit, whitelist_only

from app.utils.user import authed

from app.utils      import user, get_config

from app.models     import db, Users

from app.main       import main

import hashlib

@main.route("/sign", methods=['GET'])
# @whitelist_only
def sign():
    if authed():
        flash(message="You've been already signed in.", category="warning")
        return redirect(url_for(".index"))

    return render_template(f"/front/{get_config('front_theme')}/main/sign.html")


@main.route("/sign/in", methods=['POST'])
# @whitelist_only
# @ratelimit(method="POST", limit=5, interval=300)
def signin():
    username    = request.form.get("username", type=str)
    password    = hashlib.sha3_512(request.form.get("password", type=str).encode()).hexdigest()
    
    user_info   = db.session.query( Users.idx,
                                    Users.uid,
                                    Users.name,
                                    Users.email,
                                    Users.admin).filter(Users.uid       == username,
                                                        Users.password  == password).one_or_none()

    if user_info == None:
        flash(message="Failed to sign in.", category="error")
        return redirect(url_for(".sign"))
    else:
        signin_user(user_info)
        return redirect(url_for(".index"))
    

@main.route("/sign/out", methods=['GET'])
# @whitelist_only
def signout():
    # ------------------------------------------------------------
    if user.authed():
        # Delete from Redis
        sid = request.cookies.get(app.session_cookie_name)
        app.session_interface.store.delete(sid)
        
        # Delete from Client
        signout_user()
    
    return redirect(url_for(".index"))
    