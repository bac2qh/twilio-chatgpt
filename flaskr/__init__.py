"""
A Flask application is an instance of the Flask class. 
Everything about the application, such as configuration and URLs, 
will be registered with this class.

this file serves as: 
1. The application factory for the flask instance 
2. Tells Python that flaskr directory should be treated as a package 
"""

import os
from flask import Flask
from flaskr.config import Config

sms = []


def create_app(config_class=Config, test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
    )
    # if not test_config:
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config
    #     app.config.from_mapping(test_config)

    # make sure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')

    from . import api
    app.register_blueprint(api.bp)

    from . import project
    app.register_blueprint(project.bp)

    return app
