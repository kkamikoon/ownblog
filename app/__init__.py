import os

# Cache
from app.cache import cache

# Utilities
from app.utils import (
    set_config,
    get_config
)

from app.utils.initialization   import (
    init_template_globals,
    init_request_processors
)

# Flask ReCaptcha
from flask_recaptcha            import  ReCaptcha

# Markdown(Flask Misaka)
from flask_misaka       import Misaka

# SQLAlchemy && Migrations
from sqlalchemy                 import create_engine 
from app.utils.migrations       import migrations, create_database

# Models
from app.models import (
    db,
    Users,
    Configs
)

# Flask
from jinja2 import FileSystemLoader
from flask  import (
    Flask,
    request,
    session,
    g,
    redirect,
    url_for,
    abort,
    render_template,
    flash
)

# Redis
from app.utils.security import redis

from app.utils.config   import is_setup, set_email, get_email

# Global Variables
recaptcha   = ReCaptcha()
md          = Misaka(fenced_code=True)


def create_app(config="app.config.Config"):
    app = Flask(__name__, template_folder="templates")

    # Set Config
    app.config.from_object(config)

    with app.app_context():
        # Create Database(if it doesn't created)
        url = create_database()

        # Set MySQL's charset to utf8mb4 forcely
        app.config["SQLALCHEMY_DATABASE_URI"] = str(url)

        # Set Redis Session 
        app.session_interface = redis.RedisSessionInterface()
        
        # Register Database
        db.init_app(app)

        # Initialization
        init_template_globals(app)
        init_request_processors(app)

        # Create DB Session & Engine (if db is not defined, create db too.)
        db.create_all()

        # Cache Initialization
        cache.init_app(app)
        app.cache = cache

        # Set ReCaptcha
        if is_setup():
            app.config["RECAPTCHA_SITE_KEY"]   = get_config("recaptcha_site_key")
            app.config["RECAPTCHA_SECRET_KEY"] = get_config("recaptcha_secret_key")

        recaptcha.init_app(app)

        # Markdown(Misaka) Initialization
        md.init_app(app)

        if is_setup():
            get_email()
        else:
            # default theme
            set_config("admin_theme", "adminlte3")
            set_config("front_theme", "kkami")
            
            # email configuration
            set_email()

        from app.main       import main
        from app.admin      import admin
        from app.handler    import page_not_found, forbidden, general_error, gateway_error, too_many_requests
        
        app.register_blueprint(main)
        app.register_blueprint(admin)

        # Error Handler
        app.register_error_handler(403, forbidden)
        app.register_error_handler(404, page_not_found)
        app.register_error_handler(429, too_many_requests)
        app.register_error_handler(500, general_error)
        app.register_error_handler(502, gateway_error)

        return app
