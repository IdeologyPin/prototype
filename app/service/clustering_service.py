from redis import Redis
from rq import Queue

from app.data import RelegenceService
from app.tasks.clustering import FV1ClusteringMethod
from app.tasks.clustering.clustering_method import StoryCollection
from app.api.dto import *
METHODS = {
    'DOC2VEC': None,
    'LDA': None,
    'FV1': FV1ClusteringMethod()
}

rs=RelegenceService()

redis_conn = Redis()
q = Queue(connection=redis_conn)

class ClusteringService():

    def cluster(self, story_id, method=None):
        '''
        :param story_id:
        :param method:
        :return:
        '''
        if method==None:
            method='FV1'

        collection = StoryCollection(story_id)
        job = q.enqueue(METHODS[method].cluster, collection)
        return BaseDto()
