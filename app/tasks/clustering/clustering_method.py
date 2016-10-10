from app.model import Clustering
from app.data import RelegenceService
class ClusteringMethod(object):

    def cluster(self, article_collection):
        '''
        run pipeline, convert the row results of the clustering to the db model and return.
        article_collection:
        Has an identifier for the article collection, story_id, subject_id etc.
        :return: a Clustering model object
        '''
        return Clustering()



class ArticleCollection(object):

    def __init__(self, collection_id, query=[]):
        '''
        :param query: set of keyword args for querying the docs
        '''
        self.query=query

    def get_articles(self):
        pass

class StoryCollection(ArticleCollection):

    def __init__(self, story_id):
        self.story_id=story_id
        self.collection_id=story_id

    def get_articles(self):
        rs=RelegenceService()
        return rs.get_articles_by_story(self.story_id)



