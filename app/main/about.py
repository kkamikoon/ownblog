from flask  import current_app as app
from flask  import (
    render_template
)

from app.utils          import user, get_config
from flask.helpers      import safe_join
from app.utils.markdown import get_markdown

from app.models         import db, Posts

from app.main           import main

@main.route("/about", methods=['GET'])
def about():
    about = Posts.query.filter_by(idx=get_config("about_post")).first()

    if about == None:
        path = safe_join(app.root_path, "static", "front", "posts", "about.md")

        return render_template( f"/front/{get_config('front_theme')}/main/about.html",
                                about=open(path, "r", encoding="utf-8").read())

    return render_template(f"/front/{get_config('front_theme')}/main/about.html",
                            about=get_markdown(about.fullpath))