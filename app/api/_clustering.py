from flask_restful import Resource
from flask_restful import reqparse
from app.service import ClusteringService
#clustering/story/<int:story_id>/<int:clustering_id>
class StoryClusteringAPI(Resource):
    pass

#clustering/story/<int:story_id>
class StoryClusteringListAPI(Resource):

    def __init__(self):
        parser = self.parser = reqparse.RequestParser()
        # regex to match subject name. default is .*
        parser.add_argument('method', required=False)
        self.cs=ClusteringService()

    def get(self, story_id):
        args = self.parser.parse_args()
        method=args['method']
        clustering=self.cs.cluster(story_id, method)
        return clustering.to_json()

    #update multiple articles in the story clusters. moving docs between cluster ids are implemented here.
    def put(self):
        pass

    #update whole cluster -> re run pipeline
    def post(self):
        pass

    #delete all clusterings for this story
    def delete(self):
        pass



#clustering/subject/<int:subject_id>
class TopicClusteringAPI(Resource):
    pass


