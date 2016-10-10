#!povmap/bin/python
from flask import Flask
from flask_cors import CORS, cross_origin

from app import env
env.init_mongo()

from app.api import rest_api
app = Flask(__name__)
rest_api.init(app)


CORS(app)

app.run(debug=True)



