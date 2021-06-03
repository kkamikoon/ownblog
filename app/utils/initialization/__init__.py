from flask import (
    abort,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from app.utils.user import (
    authed,
    is_admin,
    get_current_user,
    get_attach
)

from app.utils.security.auth import (
    in_whitelist
)

from app.utils.url     import (
    current_url,
    current_endpoint
)

from app.utils.blog    import (
    get_categories,
    get_category
)
from app.utils.config  import is_setup
from app.utils         import get_config
from app.utils.logging import access_logging

from app.models        import db

def init_template_globals(app):
    # Init utils
    app.jinja_env.globals.update(get_config=get_config)

    # Config utils
    app.jinja_env.globals.update(is_setup=is_setup)

    # User utils
    app.jinja_env.globals.update(get_attach=get_attach)
    app.jinja_env.globals.update(authed=authed)
    app.jinja_env.globals.update(is_admin=is_admin)
    app.jinja_env.globals.update(get_current_user=get_current_user)

    # Security utils
    app.jinja_env.globals.update(in_whitelist=in_whitelist)

    # Blog utils
    app.jinja_env.globals.update(get_categories=get_categories)
    app.jinja_env.globals.update(get_category=get_category)

    # URL utils
    app.jinja_env.globals.update(current_url=current_url)
    app.jinja_env.globals.update(current_endpoint=current_endpoint)

    @app.template_filter("endpoint_for_header")
    def endpoint_for_header(endpoint):
        '''
        :param endpoint:  string value of endpoint like 'admin.dashboard'
        '''
        return endpoint.split('.')[-1].capitalize()

    @app.template_filter("captialize")
    def captialize(string):
        '''
        :param endpoint:  Anything string value
        '''
        return string.capitalize()


def init_request_processors(app):
    @app.before_request
    def needs_setup():
        if is_setup() is False:
            if request.endpoint in (
                "admin.setup",
                "main.themes",
                "main.image"
            ):
                return
            else:
                return redirect(url_for("admin.setup"))

    @app.before_request
    def tracker():
        # Logging
        if request.endpoint in (
            "admin.setup",
            "main.themes",
            "main.image",
            "admin.logs",
            "admin.log_detail"
        ):
            pass
        else:
            access_logging()

        if authed():
            user = get_current_user()
            
            if user and user.banned:
                return render_template(f"/front/{get_config('front_theme')}/handler/banned.html")

            db.session.close()
