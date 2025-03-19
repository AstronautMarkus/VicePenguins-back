from flask import Flask

from .routes.main import main as main_blueprint
from .routes.mods import mods as mods_blueprint
from .routes.users import users as users_blueprint

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_blueprint)    
    app.register_blueprint(mods_blueprint, url_prefix='/mods')
    app.register_blueprint(users_blueprint, url_prefix='/users')

    return app
