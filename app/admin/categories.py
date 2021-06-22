from flask  import current_app as app
from flask  import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template,
    flash
)

from app.utils              import get_config
from app.utils.decorators   import admin_only
from app.models             import db, Categories, SubCategories

admin = Blueprint("admin", __name__)

from app.admin              import admin

@admin.route("/admin/categories", methods=['GET'])
@admin_only
def categories():
    categories      = Categories.query.all()
    subcategories   = SubCategories.query.all()

    return render_template( f"/admin/{get_config('admin_theme')}/contents/categories.html",
                            categories=categories,
                            subcategories=subcategories)


@admin.route("/admin/categories/add", methods=['POST'])
@admin_only
def categories_add():
    # request.form.get("admin") == None => unchecked
    # Core attributes
    name        = request.form.get("name",          type=str)
    category_idx= request.form.get("category_idx",  type=int)

    # Supplementary attributes
    hidden      = (request.form.get("hidden")   != None) # if not None == True

    # Set user object
    if category_idx != None: # if category idx is set
        category=SubCategories( name=name,
                                category_idx=category_idx,
                                hidden=hidden)
    else:
        category=Categories(name=name,
                            hidden=hidden)

    try:
        db.session.add(category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # msg = e.orig.args[1] # Error Message
        flash(message=e.orig.args[1], category="error")
        return redirect(url_for(".categories"))
    else:
        db.session.commit()
        
    return redirect(url_for(".categories"))


@admin.route("/admin/categories/del/<int:category_idx>", methods=['POST'])
@admin_only
def categories_del(category_idx):
    # request.form.get("admin") == None => unchecked
    # Core attributes
    uid         = request.form.get("uid")   

    # Get user object
    user = Users.query.filter_by(idx=user_idx, name=uid).first_or_404()

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(message=e.orig.args[1], category="error")
        return redirect(url_for(".categories"))
    else:
        db.session.commit()
        
    return redirect(url_for(".categories"))