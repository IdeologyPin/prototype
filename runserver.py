#!povmap/bin/python
from flask import Flask
from flask_cors import CORS, cross_origin

from app import env
env.init_mongo()

from app.api import rest_api
app = Flask(__name__)
rest_api.init(app)


CORS(app)

@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
  	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  	return response

app.run(debug=True, host='0.0.0.0')



