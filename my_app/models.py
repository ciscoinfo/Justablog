# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from my_app import db
from my_app import fn_tools


##CONFIGURE TABLES


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)

    # ------------ Parent relationship ------------ #

    # The "author" refers to the author property in the BlogPost class.
    posts = relationship("BlogPost", back_populates="blogpost_author")

    # "comment_author" refers to the comment_author property in the Comment class.
    comments = relationship("Comment", back_populates="comment_author")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    # author = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # ------------ Parent relationship ------------ #
    comments = relationship("Comment", back_populates="comment_post")

    # ------------ Child relationship ------------ #

    # ------------ Child of : User
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Create reference to the User object, the "posts" refers to the posts property in the User class.
    blogpost_author = relationship("User", back_populates="posts")


    # New instance instantiation procedure
    def __init__(self, author, title, subtitle, body, img_url):
        self.author = author
        self.title = title
        self.subtitle = subtitle
        self.body = body
        self.img_url = img_url
        self.date = fn_tools.get_date()

    # def __repr__(self):
    #     return '<BlogPost %r>' % self.id


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    # ------------ Child relationship ------------ #

    # ------------ Child of : User
    # "users.id" The users refers to the tablename of the Users class.
    # "comments" refers to the comments property in the User class.
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Create reference to the User object, the "posts" refers to the posts property in the User class.
    comment_author = relationship("User", back_populates="comments")

    # ------------ Child of : BlogPost
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    comment_post = relationship("BlogPost", back_populates="comments")

    def __init__(self, text, author_id, post_id):
        self.text = text
        self.author_id = author_id
        self.post_id = post_id

# User.__table__.drop(engine)
# Line below only required once, when creating DB.
# db.create_all()