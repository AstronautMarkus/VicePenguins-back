from flask import Flask

from .main import main as main_blueprint
from .mods import mods as mods_blueprint

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_blueprint)    
    app.register_blueprint(mods_blueprint, url_prefix='/mods')

    return app
