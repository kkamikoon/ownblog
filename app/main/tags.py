from flask  import current_app as app
from flask  import (
    request,
    render_template,
    redirect,
    url_for,
    flash
)

from app.utils          import user, get_config
from flask.helpers      import safe_join
from app.utils.markdown import get_markdown

from app.models         import db, Tags, Posts

from app.main           import main

@main.route("/tags", methods=['GET', 'POST'])
def tags():
    if request.method == "POST":
        selected_tags   = request.form.get("selected_tags",  type=str,   default=None)
        
        try:
            tag_list= selected_tags.split(" ")
            tags    = db.session.query( Tags.name,
                                        Tags.post_idx).filter(  Tags.name.in_(tag_list)).all()
        except Exception as e:
            flash(message="You've been wrong action for selecting tags", category="warning")
            return redirect(url_for(".tags"))

        posts   = db.session.query( Posts.idx,
                                    Posts.title,
                                    Posts.date).filter( Tags.post_idx.in_([ tag.post_idx for tag in tags ]),
                                                        Posts.idx==Tags.post_idx,
                                                        Posts.hidden==False).group_by(Tags.post_idx).all()

        # Do not change the order
        ordered_tags = []

        for v in tag_list:
            if v not in ordered_tags:
                ordered_tags.append(v)

        return render_template( f"/front/{get_config('front_theme')}/tags/index.html",
                                posts=posts,
                                selected_tags=" ".join(ordered_tags))
    
    return render_template( f"/front/{get_config('front_theme')}/tags/index.html" )