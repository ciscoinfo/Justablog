from typing import Callable
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


from flask_gravatar import Gravatar

app = Flask(__name__)


# Configurations
app.config.from_object('config')

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

import my_app.models

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

ckeditor = CKEditor(app)

# initialize Bootstrap
Bootstrap(app)

import my_app.views


# if __name__ == "__main__":
#     app.run(debug=True)
