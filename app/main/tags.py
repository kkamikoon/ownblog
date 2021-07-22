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

            p_idxs  = [ tag.post_idx for tag in tags if tag.post_idx != None ]

            # Do not change the order of tag list
            ordered_tags = []

            for v in tag_list:
                if v not in ordered_tags:
                    ordered_tags.append(v)

        except Exception as e:
            flash(message="You've been wrong action for selecting tags", category="warning")
            return redirect(url_for(".tags"))

        try:
            # if the tuple(or list) is None or empty, in_ function occurring error.
            # https://stackoverflow.com/questions/35375179/sql-alchemy-tuple-func-in-queries-and-none-values
            # So... i choose the list value about p_idxs to [0] if it is `None` value.
            posts   = db.session.query( Posts.idx,
                                        Posts.title,
                                        Posts.date).filter( Tags.post_idx.in_([0] if p_idxs == [] else p_idxs),
                                                            Posts.idx==Tags.post_idx,
                                                            Posts.hidden==False).group_by(Tags.post_idx).all()
        except Exception as e:
            flash(message="Unknown error on searching posts.", category="error")
            return redirect(url_for(".tags"))


        return render_template( f"/front/{get_config('front_theme')}/tags/index.html",
                                posts=posts,
                                selected_tags=" ".join(ordered_tags))
    
    return render_template( f"/front/{get_config('front_theme')}/tags/index.html" )

