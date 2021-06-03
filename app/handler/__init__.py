from flask import current_app as app
from flask import render_template

from app.utils import get_config

# 403
def forbidden(error):
    return render_template(f"/front/{get_config('front_theme')}/handler/403.html", error=error.description), 403

# 404
def page_not_found(error):
    return render_template(f"/front/{get_config('front_theme')}/handler/404.html", error=error.description), 404

# 429
def too_many_requests(error):
    return render_template(f"/front/{get_config('front_theme')}/handler/429.html", error=error.description), 429

# 500
def general_error(error):
    return render_template(f"/front/{get_config('front_theme')}/handler/500.html"), 500

# 502
def gateway_error(error):
    return render_template(f"/front/{get_config('front_theme')}/handler/502.html", error=error.description), 502
