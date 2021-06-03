import functools

from flask  import current_app as app
from flask  import (
    request,
    redirect,
    url_for,
    abort,
    jsonify,
)
from app.cache      import cache
from app.utils      import user as current_user
from app.utils.user import (
    is_admin,
    authed,
    get_current_user,
)
from app.utils.security.auth import (
    in_whitelist
)


def authed_only(f):
    @functools.wraps(f)
    def authed_only_wrapper(*args, **kwargs):
        if authed():
            return f(*args, **kwargs)
        else:
            return redirect(url_for("main.sign"))

    return authed_only_wrapper


def admin_only(f):
    @functools.wraps(f)
    def admin_only_wrapper(*args, **kwargs):
        if is_admin():
            return f(*args, **kwargs)
        else:
            return redirect(url_for("main.sign"))

    return admin_only_wrapper


def whitelist_only(f):
    @functools.wraps(f)
    def whitelist_only_wrapper(*args, **kwargs):
        if in_whitelist():
            return f(*args, **kwargs)
        else:
            abort(404)
    
    return whitelist_only_wrapper


def ratelimit(method="POST", limit=50, interval=300, key_prefix="rl"):
    def ratelimit_decorator(f):
        @functools.wraps(f)
        def ratelimit_wrapper(*args, **kwargs):
            ip_address  = current_user.get_ip()
            key         = f"{key_prefix}:{ip_address}:{request.endpoint}"
            current     = cache.get(key)

            if request.method == method:
                if ( current and int(current) > limit - 1 ):
                    return abort(429)
                else:
                    if current is None:
                        cache.set(key, 1, timeout=interval)
                    else:
                        cache.set(key, int(current) + 1, timeout=interval)

            return f(*args, **kwargs)

        return ratelimit_wrapper

    return ratelimit_decorator
