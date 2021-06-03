CREATE USER 'blog'@'localhost' IDENTIFIED BY 'blog';
GRANT ALL PRIVILEGES ON blog.* TO 'blog'@'localhost';
FLUSH PRIVILEGES;