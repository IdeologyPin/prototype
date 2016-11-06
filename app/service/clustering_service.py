from app.data import RelegenceService
from app.tasks.clustering import FV1ClusteringMethod
from app.tasks.clustering.clustering_method import StoryCollection
from app.api.dto import *
from app.model import Clustering
import app.jobQ as jq

import app.tasks.worker_env as wenv
wenv.init_spacy()

METHODS = {
    'DOC2VEC': None,
    'LDA': None,
    'FV1': FV1ClusteringMethod()
}

rs=RelegenceService()
rq=jq.get_RQ()


class ClusteringService():

    def cluster(self, story_id, method=None):
        '''
        Cluster the collection of documents for the story id.

        :param story_id:
        :param method:
        :return: the list of clusterings for this article collection
        '''
        story_id='773932258236952576'
        if method==None:
            method='FV1'

        collection = StoryCollection(story_id)

        clusterings = Clustering.by_collection_id(story_id)
        if clusterings==None or len(clusterings)==0:
            #run as async job
            # job = rq.enqueue(METHODS[method].run_clustering, collection)
            #run in same thread
            METHODS[method].run_clustering(collection)


        clusterings=Clustering.by_collection_id(story_id)
        dto=ClusteringListDto.from_mongo(clusterings)
        return dto
