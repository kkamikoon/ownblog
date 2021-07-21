import datetime

from flask_sqlalchemy   import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__   = "users"
    __table_args__  = {'mysql_collate' : "utf8_general_ci"}

    # Core Attributes
    idx         = db.Column(db.Integer,     primary_key=True)
    uid         = db.Column(db.String(128), unique=True)
    name        = db.Column(db.String(128))
    password    = db.Column(db.String(256))
    email       = db.Column(db.String(128), unique=True)
    attach      = db.Column(db.Integer,     db.ForeignKey(  'users_attach.idx',
                                                            ondelete="SET NULL",
                                                            onupdate="CASCADE"))
    
    # Supplementary attributes
    hidden      = db.Column(db.Boolean,     default=False)
    banned      = db.Column(db.Boolean,     default=False)
    verified    = db.Column(db.Boolean,     default=False)
    admin       = db.Column(db.Boolean,     default=False)
    date        = db.Column(db.DateTime,    default=datetime.datetime.utcnow)

    # def __repr__(self):
    #     return  f"<Users {self.idx},{self.name},{self.password},{self.email},{self.type},{self.hidden},{self.banned},{self.verified},{self.admin}>"


class Attach(db.Model):
    __tablename__   = "users_attach"
    __table_args__  = {'mysql_collate' : "utf8_general_ci"}

    # Core Attributes
    idx         = db.Column(db.Integer,     primary_key=True)
    type        = db.Column(db.String(128))
    description = db.Column(db.String(2048))

    # Supplementary attributes
    hidden      = db.Column(db.Boolean,     default=False)


class Configs(db.Model):
    __tablename__   = "configs"
    __table_args__  = {'mysql_collate' : "utf8_general_ci"}

    # Core Attributes
    idx         = db.Column(db.Integer,     primary_key=True)
    key         = db.Column(db.String(128))
    value       = db.Column(db.String(256))

    # def __repr__(self):
    #     return f"<Configs {self.id},{self.key},{self.value}>"


class Categories(db.Model):
    __tablename__   = "categories"
    __table_args__  = {'mysql_collate' : "utf8_general_ci"}

    # Core Attributes
    idx         = db.Column(db.Integer,     primary_key=True)
    name        = db.Column(db.String(128), unique=True)

    # Supplementary attributes
    hidden      = db.Column(db.Boolean,     default=True)


class SubCategories(db.Model):
    __tablename__   = "sub_categories"
    __table_args__  = {'mysql_collate' : "utf8_general_ci"}

    # Core Attributes
    idx         = db.Column(db.Integer,     primary_key=True)
    category_idx= db.Column(db.Integer,     db.ForeignKey(  'categories.idx',
                                                            ondelete="SET NULL",
                                                            onupdate="CASCADE"))
    name        = db.Column(db.String(128), unique=True)

    # Supplementary attributes
    hidden      = db.Column(db.Boolean,     default=True)


class Posts(db.Model):
    __tablename__   = "posts"
    __table_args__  = {'mysql_collate' : "utf8_general_ci"}

    # Core Attributes
    idx             = db.Column(db.Integer,     primary_key=True)
    category_idx    = db.Column(db.Integer,     db.ForeignKey(  'categories.idx',
                                                                ondelete="SET NULL",
                                                                onupdate="CASCADE"))
    sub_category_idx= db.Column(db.Integer,     db.ForeignKey(  'sub_categories.idx',
                                                                ondelete="SET NULL",
                                                                onupdate="CASCADE"))
    title           = db.Column(db.String(256))
    abstract        = db.Column(db.String(512))
    filename        = db.Column(db.String(512), unique=True)
    fullpath        = db.Column(db.String(2048))
    hidden          = db.Column(db.Integer,     default=True)
    update          = db.Column(db.DateTime,    default=datetime.datetime.utcnow)
    date            = db.Column(db.DateTime,    default=datetime.datetime.utcnow)


class PostImages(db.Model):
    __tablename__   = "post_images"
    __table_args__  = {'mysql_collate' : "utf8_general_ci"}

    # Core Attributes
    idx         = db.Column(db.Integer,     primary_key=True)
    post_idx    = db.Column(db.Integer,     db.ForeignKey(  'posts.idx',
                                                            ondelete="SET NULL",
                                                            onupdate="CASCADE"))
    path        = db.Column(db.String(2048))
    date        = db.Column(db.DateTime,    default=datetime.datetime.utcnow)


class Tags(db.Model):
    __tablename__   = "tags"
    __table_args__  = {'mysql_collate' : "utf8_general_ci"}

    # Core Attributes
    idx         = db.Column(db.Integer,     primary_key=True)
    post_idx    = db.Column(db.Integer,     db.ForeignKey(  'posts.idx',
                                                            ondelete="SET NULL",
                                                            onupdate="CASCADE"))
    name        = db.Column(db.String(256))
    date        = db.Column(db.DateTime,    default=datetime.datetime.utcnow)


class TagList(db.Model):
    __tablename__   = "tag_list"
    __table_args__  = {'mysql_collate' : "utf8_general_ci"}

    # Core Attributes
    idx         = db.Column(db.Integer,     primary_key=True)
    tags_idx    = db.Column(db.Integer,     db.ForeignKey(  'tags.idx',
                                                            ondelete="SET NULL",
                                                            onupdate="CASCADE"))
    name        = db.Column(db.String(256), unique=True)
    date        = db.Column(db.DateTime,    default=datetime.datetime.utcnow)


class Themes(db.Model):    
    # To do...
    __tablename__   = "themes"
    __table_args__  = {'mysql_collate' : "utf8_general_ci"}

    # Core Attributes
    idx         = db.Column(db.Integer,     primary_key=True)
    name        = db.Column(db.String(128), unique=True)
    type        = db.Column(db.Boolean,     default=False)


class Logs(db.Model):
    __tablename__   = "logs"
    __table_args__  = {'mysql_collate' : "utf8_general_ci"}

    # Core Attributes
    idx         = db.Column(db.Integer,     primary_key=True)
    user_idx    = db.Column(db.Integer)
    name        = db.Column(db.String(128))
    host        = db.Column(db.String(128))
    ip          = db.Column(db.String(128))
    path        = db.Column(db.String(4096))
    cookie      = db.Column(db.String(1024))
    endpoint    = db.Column(db.String(256))
    date        = db.Column(db.DateTime,    default=datetime.datetime.utcnow)
