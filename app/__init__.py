from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)

from . import env
from . import data
from . import env
from . import model
from . import api

env.init_mongo()

CORS(app)