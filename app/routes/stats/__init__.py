from flask import Blueprint
from flask_cors import CORS

stats = Blueprint('stats', __name__)

CORS(stats, supports_credentials=True)

from . import ModStat, GetStats
