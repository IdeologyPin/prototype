from flask import Flask
from flask_restful import Resource, Api
from lib.aol.relegence import Relegence
from app.povmap_api import showStories, showTaxonomy

app = Flask(__name__)
api = Api(app)

api.add_resource(showStories, '/showStories/<int:storyId>')
api.add_resource(showTaxonomy, '/showTaxonomy')


from app import views

