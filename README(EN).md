# 1. Requirements

## Ubuntu 18.04 ~

- if you use ubuntu 18.04 or higher version of Ubuntu, you can install those library.

    ```bash
    apt update -y
    apt install -y apache2 letsencrypt redis python3-pip mysql-server libapache2-mod-wsgi-py3 libapache2-mod-log-sql-mysql certbot python3-certbot-apache2
    ```

## Python3 requirements install

- Python3 modules install(option 1)

    ```bash
    python3 -m pip install --upgrade
    pip3 install redis flask flask_migrate flask_sqlalchemy Flask-Mail flask_caching flask_socketio flask-recaptcha sqlalchemy sqlalchemy_utils pymysql flask_misaka
    ```

- Python3 modules install(option 2)

    ```bash
    python3 -m pip install --upgrade
    pip3 install -r requirements.txt
    ```

## Create mysql default user

- Insert your MySQL account.

    ```bash
    $ sudo mysql -u root < user.sql
    ```

    You should add your MySQL account for your blog. But i recommand you to modify default account information for your security. You can edit your MySQL account information on `app/config.py` and `user.sql`.

- app/config.py

    ```python
    import os

    class Config(object):
        """
        Configuration of Python Flask
        """
        # Session(Redis) Settings
        SESSION_COOKIE_NAME = "KID-SES"
        SESSION_TYPE        = "redis"

        # Cache Type
        CACHE_TYPE          = "filesystem"
        CACHE_DIR           = os.path.join(
            os.path.dirname(__file__), os.pardir, ".cache", "filesystem_cache"
        )
        CACHE_THRESHOLD = (
            0
        )

        # SQLAlchemy Settings
        db_info         = {
            "user"      : "blog",
            "password"  : "blog",
            "host"      : "localhost",
            "port"      : 3306,
            "database"  : "blog"
        }
        
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_info['user']}:{db_info['password']}@{db_info['host']}:{db_info['port']}/{db_info['database']}?charset=utf8"
        SQLALCHEMY_TRACK_MODIFICATIONS = False

        # ....
    ```

- user.sql

    ```sql
    CREATE USER 'blog'@'localhost' IDENTIFIED BY 'blog';
    GRANT ALL PRIVILEGES ON blog.* TO 'blog'@'localhost';
    FLUSH PRIVILEGES;
    ```

## Initiate Flask

- I recommand the reverse proxy setting. If you want to set-up reverse proxy with `Apache2` or `Nginx`, you need to use `WSGI(or uWSGI)` or `Gunicorn` or something.

    ```python
    # wsgi.py (for apache2 mod_wsgi)
    import sys
    sys.path.insert(0, '/your/directory/of/blog')
    from app import create_app

    application = create_app()
    ```

- But you can `Quick Start` with this command.

    ```bash
    $ python3 run.py
    ```

    You can change your port number.
    ```python
    # run.py (for `quick stark` or debugging)
    from app import create_app

    app     = create_app()

    if __name__ == "__main__":
        app.run(debug=True,
                threaded=True,
                host="0.0.0.0",
                port=80)
    ```

# 2. Web Server setting(Apache2)

## Add apache2 envvar value

- This is apache2 environment value that it helps you to configure your config file(like wol.conf). This value can be written on `/etc/apache2/envvar`.

    ```
    ...
    export BLOG_DIR=[/your/directory/of/blog/]
    ...
    ```

## Add apache2 module

- You should enable these modules, if you want to init apache2 service.

    ```
    sudo a2enmod rewrite
    sudo a2enmod wsgi
    sudo a2enmod ssl
    ```

- rewrite : One of apache2 module what makes your request forward to other URL or File.
    - RewriteEngine
    - RewriteCond
    - RewriteRule
    - etc
- WSGI : One of apache2 module that it makes you can use 'kind of WSGI configuration' on your apache2 config files. This module can install using apt-get(or apt) command.

    Library name : `libapache2-mod-wsgi-py3`

    - WSGIScriptAlias
    - WSGIDaemonProcess
    - WSGIApplicationGroup
    - etc.

- ssl : One of apache2 module that it makes you can use SSL configuration in your apache2 config files.
    - SSLCertificateFile
    - SSLCertificateKeyFile
    - SSLCertificateChainFile
    - etc.

## Add apache2 conf

- Your configuration file(blog.conf) should be ensited, and should dissite default config file(000-default.conf)

    ```
    sudo a2ensite blog
    sudo a2dissite 000-default
    ```

# 3. Licenses

- GNU General Public License v3.0

# 4. Links

- Example : [https://kkamikoon.com](https://kkamikoon.com)
- Template : [https://adminlte.io](https://adminlte.io) (MIT)