from flask  import current_app as app
from flask  import (
    flash,
    request,
    redirect,
    url_for,
    render_template,
    jsonify
)

from app.utils      import user, get_config, set_config

from app.models     import db, Logs

from app.utils.decorators import admin_only

# Get Blueprint
from app.admin import admin

@admin.route("/admin/logs", methods=['GET'])
@admin_only
def logs():
    logs_data   = db.session.query( Logs.idx,
                                    Logs.host,
                                    Logs.ip,
                                    Logs.path,
                                    Logs.endpoint,
                                    Logs.time).all()
    return render_template( f"/admin/{get_config('admin_theme')}/logs/index.html",
                            logs_data=logs_data)


@admin.route("/admin/logs/<int:log_idx>", methods=['GET'])
@admin_only
def log_detail(log_idx):
    log   = Logs.query.filter_by(idx=log_idx).first_or_404()
    
    return jsonify({"host"     : log.host,
                    "user"     : log.name,
                    "ip"       : log.ip,
                    "path"     : log.path,
                    "endpoint" : log.endpoint,
                    "time"     : log.time,
                    "cookie"   : log.cookie})
    