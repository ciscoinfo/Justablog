# set instance_relative_config=True
# app.config.from_pyfile() will load the specified file from the instance/ directory.
app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')
# Variables defined in the instance/config.py file override the value in config.py

# λ heroku apps
#  »   Warning: heroku update available from 7.42.13 to 7.47.11.
# === cisco.ad@gmail.com Apps
# cisco-blog
# pizzacisco
#
# CiscoPC@DESKTOP-MURIUU3 /f/309. Python/UDEMY - Python Bootcamp 2021/Day 69 - Blog part4/blog-with-users-start (master)
# λ heroku git:remote -a cisco-blog
#  »   Warning: heroku update available from 7.42.13 to 7.47.11.
# set git remote heroku to https://git.heroku.com/cisco-blog.git
# CiscoPC@DESKTOP-MURIUU3 /f/309. Python/UDEMY - Python Bootcamp 2021/Day 69 - Blog part4/blog-with-users-start (master)
# λ heroku config
#  »   Warning: heroku update available from 7.42.13 to 7.47.11.
# === cisco-blog Config Vars
# SENDER_MAIL: "zarkinpython12@gmail.com"
# SENDER_PASS: "o3X+8P4D`^?&Ssy"
# TO_MAIL:     "zarkingo@yahoo.fr"