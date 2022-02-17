import os
from flask import Flask
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'dev'
    if test_config is None:
        # load the instance config if exists
        app.config['ENV'] = 'development'
        app.config['DEBUG'] = True
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if exists
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import sqlexcute
    sqlexcute.init_app(app)

    from . import login
    app.register_blueprint(login.bp)

    from . import blog
    app.register_blueprint(blog.bp)

    from . import passage
    app.register_blueprint(passage.bp)

    return app
