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

from app.utils              import get_config
from app.utils.user         import is_admin, get_current_user
from app.utils.decorators   import admin_only
from app.utils.blog         import get_tmp_dir

admin = Blueprint("admin", __name__)

from app.admin              import users
from app.admin              import setup
from app.admin              import configs
from app.admin              import logs
from app.admin              import posts
from app.admin              import categories
from app.admin              import test

@admin.route("/admin", methods=['GET'])
@admin_only
def index():
    return redirect(url_for(".dashboard"))


@admin.route("/admin/dashboard", methods=['GET', 'POST'])
@admin_only
def dashboard():
    if is_admin():
        user = get_current_user()
        return render_template( f"/admin/{get_config('admin_theme')}/main/dashboard.html", user=user)
    else:
        return redirect(url_for("main.sign"))


@admin.route("/admin/image/uploads", methods=['POST'])
@admin_only
def image_uploads():
    files       = request.files
    tmp_dir     = get_tmp_dir()
    dirs        = []
    
    # path on html : /static/<theme>/<vendor>/<path:path>
    for fkey, fvalue in files.items():
        path    =  tmp_dir.replace(app.root_path, "").replace("/themes", "")
        name    = ( hashlib.sha3_256(os.urandom(64)).hexdigest() +
                    "."                                          +
                    fvalue.filename.split(".")[1] ) # file extension
        
        dirs.append(path + "/" + name)

        # save file
        files[fkey].save(os.path.join(tmp_dir, name))

    return "".join(f"![{d}](http://{request.host}{d})\n" for d in dirs)