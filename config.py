import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# default config
class BaseConfig(object):

    # Statement for enabling the development environment
    DEBUG = False

    # CONNECT TO DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'local_db', 'new_blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_CONNECT_OPTIONS = {}

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', -1)
    CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY', -1)
    # Secret key for signing cookies
    SECRET_KEY = os.environ.get('SECRET_KEY', -1)
