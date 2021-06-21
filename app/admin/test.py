import os, hashlib
import inspect 

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

from app.admin              import admin

from app.utils              import get_config
from app.utils.user         import is_admin, get_current_user
from app.utils.decorators   import admin_only

from app.models             import (
    db,
    Posts,
    PostImages,
    Categories,
    Tags
)

@admin.route("/admin/test", methods=['GET'])
@admin_only
def test():

    # print(inspect.getargspec(db.session.delete))
    # print(dir(db.session.delete))
    o_tags = Tags.query.all()
    print(f"[=] origin tags : {o_tags}")

    selected = [ tag.name for tag in o_tags ][:2]

    print(f"[=] selected    : {selected}")

    n_tags = db.session.query(Tags.name).filter(Tags.name.in_(selected)).all()
    print(f"[=] new tags    : {n_tags}")

    n_tags = Tags.query.filter(Tags.name.in_(selected)).all()
    print(f"[=] new tags    : {n_tags}")

    # Failed
    # n_tags = Tags.query.filter_by(name = in_(selected)).all()
    # print(f"[=] new tags    : {n_tags}")

    # Failed
    # n_tags = Tags.query.all().where(Tags.name.in_(selected))
    # print(f"[=] new tags    : {n_tags}")

    
    print(f"[=] new tags    : {n_tags}")

    print(f"[=] in          : {Tags.name.in_(selected)}")

    try:
        # Tags.query.filter(Tags.name.in_(selected)).delete()
        db.session.query(Tags.name).filter(Tags.name.in_(selected)).delete(synchronize_session=False)
        db.session.commit()
    except Exception as e:
        print(f"[-] Error : {e}")
        db.session.rollback()
    
   
    return render_template( f"/admin/{get_config('admin_theme')}/main/test.html" )