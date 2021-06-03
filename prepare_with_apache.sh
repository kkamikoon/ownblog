# prepare to init
MAIN_WEB_DOMAIN="kkamikoon.com";
MAIN_WEB_DIR="/var/www/main";
MAIN_WEB_PW="main_web";
MAIN_WEB_ID="main_web";
APACHE_USER="www-data";
APACHE_GROUP="www-data"

# create user main_web
useradd -p $(openssl passwd -1 ${MAIN_WEB_PW}) ${MAIN_WEB_ID};

# move all data to defined dir
mkdir -p ${MAIN_WEB_DIR};
mv ./* ${MAIN_WEB_DIR};
chown -R ${APACHE_USER}:${APACHE_GROUP} ${MAIN_WEB_DIR};

# mkdir
mkdir -p ${MAIN_WEB_DIR}/ssl;
mkdir -p ${MAIN_WEB_DIR}/logs/http;
mkdir -p ${MAIN_WEB_DIR}/logs/https;

# apt setting
apt update -y;
apt install -y letsencrypt redis python3-pip mysql-server libapache2-mod-wsgi-py3 libapache2-mod-log-sql-mysql;

# python3 requirements install
pip3 install redis flask flask_migrate flask_sqlalchemy Flask-Mail flask_caching sqlalchemy sqlalchemy_utils;

# create mysql default user
sudo mysql -u root < mysql_default_user.sql;

# apache2 setting
cp ${MAIN_WEB_DIR}/main.conf /etc/apache2/sites-available/main.conf;

ENV="/etc/apache2/envvars";
COMP="Define main directory";

if [ -z "$(grep "${COMP}" ${ENV})" ];then
    sed -i'' -r -e "/export LANG C/a\\\n## ${COMP}\\nexport MAIN_WEB_DIR=\/var\/www\/main\/" ${ENV};
else
    echo "Already envvars setup";
fi

# enable apache2 rewrite module
sudo a2enmod rewrite;

# apache2 module setting
sudo a2enmod wsgi; #it's same with mod-wsgi & mod-wsgi-py3
sudo a2enmod ssl;
# sudo a2enmod unique_id; # for logging access log to mysql

# apache2 ensite
sudo a2ensite  main;
sudo a2dissite 000-default;

# change 'main_web' account shell status on /etc/passwd
sed -i "s/\/home\/main_web:\/bin\/sh/\/home\/main_web:\/sbin\/nologin/g" /etc/passwd;

# create letsencrypt ssl(this shell script starting apache2)

service apache2 stop;

# rm -rf ${MAIN_WEB_DIR}/ssl/${MAIN_WEB_DOMAIN};
# rm -rf /etc/letsencrypt/archive/${MAIN_WEB_DOMAIN};
# rm -rf /etc/letsencrypt/live/${MAIN_WEB_DOMAIN};
# rm -rf /etc/letsencrypt/renewal/${MAIN_WEB_DOMAIN};

# letsencrypt certonly --standalone -d ${MAIN_WEB_DOMAIN};

cp -r /etc/letsencrypt/archive/${MAIN_WEB_DOMAIN}/* ${MAIN_WEB_DIR}/ssl;

service apache2 start;
