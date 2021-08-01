CREATE USER 'blog'@'localhost' IDENTIFIED BY 'blog';
GRANT ALL PRIVILEGES ON blog_test.* TO 'blog'@'localhost';
FLUSH PRIVILEGES;
