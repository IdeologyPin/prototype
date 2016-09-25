# from aol.relegence import Relegence
from flask_restful import Resource
from flask_restful import Api
from flask_restful import reqparse

from app import app

# Make this a blueprint to avoid circular import
api = Api(app)



# stories/<story_id> -> details about story
class StoriesAPI(Resource):

    '''
    get story details + doc urls for the story.
    '''
    def get(self, storyId):
        # r = Relegence()
        # # 91485332
        # # 982618
        # # 4941761
        # respJson = r.stories.by_subject(storyId)
        # return respJson
        return "not built"

# /stories
class StoriesListAPI(Resource):

    def __init__(self):
        parser = self.parser = reqparse.RequestParser()
        # regex to match subject name. default is .*
        parser.add_argument('match')

    '''
    get list of stories
    '''
    def get(self):
        args = self.parser.parse_args()



class Taxonomy_SubjectsAPI(Resource):
    def get(self):
        # r = Relegence()
        # respJson = r.taxonomy.hierarchy.get_subjects()
        # return respJson
        return "not built"

class Taxonomy_EntityAPI(Resource):
    def get(self):
        pass

#articles/<int:article_id>
class ArticleAPI(Resource):
    pass

#clustering/story/<int:story_id>
class StoryClusteringListAPI(Resource):

    def __init__(self):
        parser = self.parser = reqparse.RequestParser()
        # regex to match subject name. default is .*
        parser.add_argument('method')

    def get(self, story_id):
        pass

    #update multiple articles in the story clusters. moving docs between cluster ids are implemented here.
    def put(self):
        pass

    #update whole cluster -> re run pipeline
    def post(self):
        pass

    #delete all clusterings for this story
    def delete(self):
        pass

#clustering/story/<int:story_id>/<int:clustering_id>
class StoryClusteringAPI(Resource):
    pass

#clusters/subject/<int:subject_id>
class TopicClustersAPI(Resource):
    pass


api.add_resource(StoriesAPI, '/stories/<int:story_id>')
api.add_resource(Taxonomy_SubjectsAPI, '/taxenomy/subjects/<int:subject_id>')

api.add_resource(StoryClustersAPI,'clusters/story/<int:story_id>', endpoint='cluster_story')