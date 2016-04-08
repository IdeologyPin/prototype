from lib.aol.relegence import Relegence
from flask_restful import Resource


class showStories(Resource):
    def get(self, storyId):
        r = Relegence()
    	# 91485332
    	# 982618
    	# 4941761
        respJson = r.stories.by_subject(storyId)
        return respJson


class showTaxonomy(Resource):
    def get(self):
        r = Relegence()
        respJson = r.taxonomy.hierarchy.get_subjects()
        return respJson
