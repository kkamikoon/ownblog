MAIN_WEB_DOMAIN="kkamikoon.com" 
MAIN_WEB_DIR="/var/www/main_web";

service apache2 stop

rm -rf ${MAIN_WEB_DIR}/ssl/${MAIN_WEB_DOMAIN}
rm -rf /etc/letsencrypt/archive/${MAIN_WEB_DOMAIN}
rm -rf /etc/letsencrypt/live/${MAIN_WEB_DOMAIN}
rm -rf /etc/letsencrypt/renewal/${MAIN_WEB_DOMAIN}

letsencrypt certonly --standalone -d ${MAIN_WEB_DOMAIN}

cp -r /etc/letsencrypt/archive/${MAIN_WEB_DOMAIN}/* ${MAIN_WEB_DIR}/ssl/

service apache2 start
