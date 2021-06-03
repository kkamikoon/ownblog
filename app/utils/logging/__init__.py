from flask  import current_app as app
from flask  import (
    request,
    session,
)
from app.models     import Logs, db
from app.utils      import user as current_user


def error_logging():
    pass

def access_logging():
    log = Logs( user_idx=session.get("idx"),
                name=session.get("name"),
                host=request.host,
                ip=current_user.get_ip(),
                path=request.path,
                cookie=request.cookies.get(app.session_cookie_name),
                endpoint=request.endpoint)
    try:
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    else:
        db.session.commit()