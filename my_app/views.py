from my_app import app

# Import flask dependencies
from flask import request, render_template, flash, redirect, url_for, abort
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from datetime import date

# import forms
import my_app.forms as forms

# Import password / encryption helper tools
from werkzeug.security import generate_password_hash, check_password_hash

# Import the database object from the main app module
from my_app import db

# Import module models (i.e. User)
from my_app.models import BlogPost
from my_app.models import User
from my_app.models import Comment

from functools import wraps

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin:
            return f(*args, **kwargs)
        return abort(403)

    return decorated_function


def get_hash_password(password):
    hash_and_salted_password = generate_password_hash(
        password=password,
        method='pbkdf2:sha256',
        salt_length=8
    )
    return hash_and_salted_password


# ------------------ MENU

@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts, current_user=current_user)

@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", current_user=current_user)

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = forms.CommentForm()
    requested_post = BlogPost.query.get(post_id)

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            # normally can't happen since the form doesn't appear
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=form.body.data,
            author_id=current_user.id,
            post_id=post_id
        )
        db.session.add(new_comment)
        db.session.commit()
    form.body.data = ""
    return render_template("post.html", post=requested_post, form=form, current_user=current_user)


# ------------------ LOGIN

@app.route('/register', methods=["GET", "POST"])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        name = form.name.data
        # print(f"{email}\t{passw}\t{name}")

        # check if email exists in database
        user = User.query.filter_by(email=email).first()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        # else
        # create password
        hash_and_salted_password = get_hash_password(password)
        # new user
        new_user = User(
            email=email,
            name=name,
            password=hash_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()
        # Log in and authenticate user after adding details to database.
        login_user(new_user)
        return redirect(url_for("get_all_posts"))

    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # search by email
        user = User.query.filter_by(email=email).first()

        if user:
            # Check stored password hash against entered password hashed.
            if check_password_hash(user.password, password):
                login_user(user)
                # flash('Logged in successfully')
                return redirect(url_for('get_all_posts'))
            # Password incorrect
            flash('Password incorrect, please try again.')
        else:
            # Email doesn't exist
            flash('That email does not exist, please try again.')
        return redirect(url_for('login'))

    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))

# ------------------ POSTS


@app.route("/new-post")
@admin_only
def add_new_post():
    form = forms.CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)



@app.route("/edit-post/<int:post_id>")
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = forms.CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, current_user=current_user)



@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))