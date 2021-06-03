from flask  import current_app as app
from flask  import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template
)

from app.utils              import get_config
from app.utils.decorators   import admin_only

admin = Blueprint("admin", __name__)

from app.admin              import admin

@admin.route("/admin/test", methods=['GET'])
@admin_only
def test():
    return render_template( f"/admin/{get_config('admin_theme')}/main/test.html" )
