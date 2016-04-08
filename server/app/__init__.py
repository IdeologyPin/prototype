from flask import Flask
from flask_restful import Resource, Api
from lib.aol.relegence import Relegence

app = Flask(__name__)
api = Api(app)

# Needs to be moved to a separate file!
class showStories(Resource):
    def get(self):
        r = Relegence()
    	# 91485332
    	# 982618
    	# 4941761
        respJson = r.stories.by_subject(4941761)
        # return {'hello': 'world'}
        return respJson


class showTaxonomy(Resource):
    def get(self):
        r = Relegence()
        respJson=r.taxenomy.hierarchy.get_subjects()
        return respJson

api.add_resource(showStories, '/showStories')
api.add_resource(showTaxonomy, '/showTaxonomy')

from app import views
