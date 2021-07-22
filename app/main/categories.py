from flask  import current_app as app
from flask  import (
    render_template,
    request
)

from app.utils          import get_config
from app.models         import db, Categories, SubCategories, Posts

from app.main           import main

@main.route("/categories", methods=['GET'])
def categories():
    categories      = Categories.query.filter_by(hidden=False).all()
    subcategories   = SubCategories.query.filter_by(hidden=False).all()

    all_categories  = []

    for category in categories:
        tmp         = {}
        tmp['idx']  = category.idx
        tmp['name'] = category.name
        tmp['subs'] = [ sub for sub in subcategories if sub.category_idx == category.idx ]

        all_categories.append(tmp)
    
    return render_template( f"/front/{get_config('front_theme')}/categories/index.html",
                            all_categories=all_categories )


@main.route("/categories/<int:category_idx>", methods=['GET'])
def category_select(category_idx):
    page    = request.args.get("page",  default=1,  type=int)

    category= Categories.query.filter_by(   idx=category_idx,
                                            hidden=False ).first()

    if category == None:
        flash(message="No matched category.", category="error")
        return redirect(url_for(".categories"))

    # Case of post pages 
    posts   = Posts.query.filter_by(category_idx=category.idx,
                                    hidden=False ).order_by(Posts.idx.desc())\
                                                  .offset((page-1) * get_config("post_page_size"))\
                                                  .limit(get_config("post_page_size"))\
                                                  .all()
                            
    # Page count
    counts  = int(Posts.query.filter_by(category_idx=category.idx,
                                        hidden=False).count() / get_config("post_page_size"))
    
    return render_template( f"/front/{get_config('front_theme')}/categories/select.html",
                            name=category.name,
                            posts=posts,
                            counts=counts,
                            page=page )


@main.route("/categories/sub/<int:sub_category_idx>", methods=['GET'])
def sub_category_select(sub_category_idx):
    page        = request.args.get("page", default=1, type=int)

    sub_category= SubCategories.query.filter_by(idx=sub_category_idx,
                                                hidden=False ).first()

    if sub_category == None:
        flash(message="No matched sub category.", category="error")
        return redirect(url_for(".categories"))

    # Case of post pages 
    posts   = Posts.query.filter_by(sub_category_idx=sub_category.idx,
                                    hidden=False ).order_by(Posts.idx.desc())\
                                                  .offset((page-1) * get_config("post_page_size"))\
                                                  .limit(get_config("post_page_size"))\
                                                  .all()
    
    # Page count
    counts  = int(Posts.query.filter_by(sub_category_idx=sub_category.idx,
                                        hidden=False).count() / get_config("post_page_size"))
    
    return render_template( f"/front/{get_config('front_theme')}/categories/select.html",
                            name=sub_category.name,
                            posts=posts,
                            counts=counts,
                            page=page )

