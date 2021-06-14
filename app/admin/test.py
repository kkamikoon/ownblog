import os, hashlib

from flask  import current_app as app
from flask  import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template,
    session
)

from flask.helpers          import safe_join

from app.admin              import admin

from app.utils              import get_config
from app.utils.user         import is_admin, get_current_user
from app.utils.decorators   import admin_only

@admin.route("/admin/test", methods=['GET'])
@admin_only
def test():
    return render_template( f"/admin/{get_config('admin_theme')}/main/test.html" )