# 1. Requirements

## Ubuntu 18.04 ~

- 만약 ubuntu 18.04 혹은 그 이상의 버전을 사용하신다면 아래의 방법으로 라이브러리를 설치할 수 있습니다.

    ```bash
    apt update -y
    apt install -y apache2 letsencrypt redis python3-pip mysql-server libapache2-mod-wsgi-py3 libapache2-mod-log-sql-mysql
    ```

## Python3 requirements install

- Python3 모듈 설치(option 1)

    ```bash
    python3 -m pip install --upgrade
    pip3 install redis flask flask_migrate flask_sqlalchemy Flask-Mail flask_caching flask_socketio flask-recaptcha sqlalchemy sqlalchemy_utils pymysql flask_misaka
    ```

- Python3 모듈 설치(option 2)

    ```bash
    python3 -m pip install --upgrade
    pip3 install -r requirements.txt
    ```

## Create mysql default user

- MySQL 계정 생성

    ```bash
    $ sudo mysql -u root < user.sql
    ```

    웹 설정을 위해 blog MySQL 계정을 추가해야 합니다. 하지만 보안을 위해서 기본으로 제공된 계정 정보를 변경하여 구동하는 것을 추천드립니다. 계정 정보는 `app/config.py`와 `user.sql` 파일의 내용을 수정하시면 됩니다.

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

- Flask를 구동하기 위해서는 Reverse Proxy를 설정하시는 것을 추천드립니다. 만약 여러분께서 `Apache2`나 `Nginx` 등의 웹 서버를 통해 Reverse Proxy를 설정하고자 한다면 `WSGI(혹은 uWSGI)` 혹은 `Gunicorn`과 같은 모듈이 필요합니다.

    ```python
    # wsgi.py (for apache2 mod_wsgi)
    import sys
    sys.path.insert(0, '/your/directory/of/blog')
    from app import create_app

    application = create_app()
    ```

- 하지만 `일단 구동`을 원하신다면 아래와 같은 명령어를 통해 구동이 가능합니다.

    ```bash
    $ python3 run.py
    ```

    포트번호는 아래의 파일에서 변경할 수 있습니다.

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

- 설정 파일 `blog.conf` 작성된 BLOG_DIR의 환경값을 설정하도록 합니다. 이 값은 `/etc/apache2/envvar` 파일에 한 줄 삽입하면 됩니다.

    ```
    ...
    export BLOG_DIR=/your/directory/of/blog/
    ...
    ```

## Add apache2 module

- Apache2 서비스를 온전히 실행시키기 위해서는 위의 세 가지 모듈을 enable 상태로 만들어야 합니다.

    ```
    sudo a2enmod rewrite
    sudo a2enmod wsgi
    sudo a2enmod ssl
    ```

- rewrite : Apache2 모듈 중 하나로, 들어온 요청(Request)을 다른 URL 혹은 파일로 포워딩합니다.

    - RewriteEngine
    - RewriteCond
    - RewriteRule
    - etc

- WSGI : Apache2 모듈 중 하나로, WSGI 설정을 사용할 수 있도록 합니다. 이 모듈은 apt 명령어로 설치가 가능하며, 라이브러리 이름은 다음과 같습니다.

    Library name : `libapache2-mod-wsgi-py3`

    - WSGIScriptAlias
    - WSGIDaemonProcess
    - WSGIApplicationGroup
    - etc.

- ssl : Apache2 모듈 중 하나로 conf 파일 내에 SSL 설정이 가능하도록 합니다.

    - SSLCertificateFile
    - SSLCertificateKeyFile
    - SSLCertificateChainFile
    - etc.

## Add apache2 conf

- 주어진 설정 파일(blog.conf)를 반드실 enable 상태로 변경해야 합니다. 또한 기본으로 실행되어 있는 설정파일(000-default.conf)를 disable 시켜야 합니다.

    ```
    sudo a2ensite blog
    sudo a2dissite 000-default
    ```

# 3. Licenses

- GNU General Public License v3.0

# 4. Links

- Example : [https://kkamikoon.com](https://kkamikoon.com)
- Template : [https://adminlte.io](https://adminlte.io) (MIT)