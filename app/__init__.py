from flask import Flask
from flask_cors import CORS

from .routes.main import main as main_blueprint
from .routes.mods import mods as mods_blueprint
from .routes.users import users as users_blueprint
from .routes.stats import stats as stats_blueprint
from .routes.skins import skins as skins_blueprint

def create_app():
    
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(main_blueprint)    
    app.register_blueprint(mods_blueprint, url_prefix='/mods')
    app.register_blueprint(users_blueprint, url_prefix='/users')
    app.register_blueprint(stats_blueprint, url_prefix='/stats')
    app.register_blueprint(skins_blueprint, url_prefix='/skins')

    return app
