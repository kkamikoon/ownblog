import os, datetime

from flask  import current_app as app
from flask  import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template,
    send_file,
    abort
)
from flask.helpers      import safe_join

from app.utils          import get_config
from app.utils          import user
from app.utils.markdown import get_markdown

from app.models         import db, Categories

from flask_misaka       import markdown

main = Blueprint("main", __name__)

from app.main   import sign
from app.main   import about
from app.main   import posts

@main.route("/", methods=['GET'])
def index():
    return render_template( f"/front/{get_config('front_theme')}/main/index.html" )


@main.route("/code", methods=['GET'])
def code():
    return render_template( f"/front/{get_config('front_theme')}/main/index.html",
                            md=get_markdown(theme="front",
                                            vendor=get_config("front_theme"),
                                            path="posts",
                                            filename="code.md"))



@main.route("/static/<theme>/<vendor>/<path:path>")
def themes(theme, vendor, path):
    filename = safe_join(app.root_path, "static", theme, "themes", vendor, path)

    if os.path.isfile(filename):
        return send_file(filename)
    else:
        abort(404)
    


@main.route("/static/<img>")
def image(img):
    filename = safe_join(app.root_path, "static", img)

    if os.path.isfile(filename):
        return send_file(filename)
    else:
        abort(404)
    





