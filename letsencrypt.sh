BLOG_DOMAIN="example.com" 
BLOG_DIR="/your/directory/of/blog";

service apache2 stop

rm -rf ${BLOG_DIR}/ssl/${BLOG_DOMAIN}
rm -rf /etc/letsencrypt/archive/${BLOG_DOMAIN}
rm -rf /etc/letsencrypt/live/${BLOG_DOMAIN}
rm -rf /etc/letsencrypt/renewal/${BLOG_DOMAIN}

letsencrypt certonly --standalone -d ${BLOG_DOMAIN}

cp -r /etc/letsencrypt/archive/${BLOG_DOMAIN}/* ${BLOG_DIR}/ssl/

service apache2 start
