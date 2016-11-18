# from aol.relegence import Relegence
from flask_restful import Resource
from flask_restful import Api
from flask_restful import reqparse


from _clustering import *
from _story import *
from _taxonomy import *
from _article import *

# Make this a blueprint to avoid circular import

def init(app):
    api = Api(app)
    api.add_resource(StoryAPI, '/story/<string:story_id>')
    api.add_resource(StoryListAPI, '/story/')
    api.add_resource(StoryTrendingAPI, '/story/trending/<string:subject_id>')
    # api.add_resource(SubjectAPI, '/taxenomy/subjects/<string:subject_id>')
    api.add_resource(SubjectListAPI, '/taxonomy/subjects/')
    api.add_resource(StoryClusteringListAPI,'/clustering/story/<string:story_id>')
    api.add_resource(ArticleAPI,'/articles/<string:article_id>')

