# set instance_relative_config=True
# app.config.from_pyfile() will load the specified file from the instance/ directory.
app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')
# Variables defined in the instance/config.py file override the value in config.py