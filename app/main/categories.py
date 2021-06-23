from flask  import current_app as app
from flask  import (
    render_template
)

from app.utils          import get_config
from app.models         import db, Categories, SubCategories

from app.main           import main

@main.route("/categories", methods=['GET'])
def categories():
    categories      = Categories.query.filter_by(hidden=False).all()
    subcategories   = SubCategories.query.filter_by(hidden=False).all()

    all_categories  = []

    for category in categories:
        tmp = {}
        tmp['idx']    = category.idx
        tmp['name']   = category.name
        tmp['subs']   = [sub for sub in subcategories if sub.category_idx == category.idx ]

        all_categories.append(tmp)
    
    return render_template(f"/front/{get_config('front_theme')}/categories/index.html",
                            all_categories=all_categories)

