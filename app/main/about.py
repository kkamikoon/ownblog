from flask  import current_app as app
from flask  import (
    render_template
)

from app.utils          import user, get_config
from app.utils.markdown import get_markdown

from app.main           import main

@main.route("/about", methods=['GET'])
def about():
    return render_template(f"/front/{get_config('front_theme')}/main/about.html",
                            md=get_markdown(theme="front",
                                            vendor=get_config("front_theme"),
                                            path="posts",
                                            filename="about.md"))
