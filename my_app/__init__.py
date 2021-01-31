from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_gravatar import Gravatar

# set instance_relative_config=True
# app.config.from_pyfile() will load the specified file from the instance/ directory.
from my_app.tools.add_base import make_superadmin

app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.ProductionConfig')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py', silent=True)


# Initialize Gravatar
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

ckeditor = CKEditor(app)

# initialize Bootstrap
Bootstrap(app)

import my_app.models
import my_app.views

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

make_superadmin("admin@email.com")
make_superadmin("test-admin@email.com")
