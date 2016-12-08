from app.data import RelegenceService
from app.model import Clustering, Article
from app.tasks.task import Task

import sys
from pygate import DataSource
from pygate.ext.spacy_io import SpacyDoc

class ClusteringMethod(Task):

    def run_clustering(self, article_collection):
        try:
            super(self.__class__, self).initialize()
            self._init_clustering(article_collection)
            self._cluster(article_collection)
            self._finish_clustering()
        except:
            e = sys.exc_info()[0]
            print e
            raise


    def _init_clustering(self, article_collection):
        '''
            Save a Clustering object to db. set status to running
            Have a ref to the model object in self.clustering
        '''
        self.clustering=None
        raise NotImplemented("override in child class")


    def _cluster(self, article_collection):
        '''
        run pipeline, convert the row results of the clustering to the db model and return.
        article_collection:
        Has an identifier for the article collection, story_id, subject_id etc.
        :return: a Clustering model object
        '''
        raise NotImplemented("override in child class")
        return Clustering()


    def _finish_clustering(self):
        self.clustering.status='finished'
        self.clustering.save()


class ArticleCollection(DataSource):

    def __init__(self, collection_id, query=[]):
        '''
        :param query: set of keyword args for querying the docs
        '''
        self.query=query

    def get_articles(self):
        raise NotImplemented()

    def iter_docs(self):
        raise NotImplemented()

class StoryCollection(ArticleCollection):

    def __init__(self, story_id):
        self.story_id=story_id
        self.collection_id=story_id

    def get_articles(self):
        rs=RelegenceService()
        return rs.get_articles_by_story(self.story_id)

    def process(self,doc):
        pass

    def iter_docs(self):
        articles=self.get_articles()
        for a in articles: #type: Article

            sdoc=SpacyDoc(a.text)
            sdoc['mongo']= a
            sdoc["id"] = a.article_id
            sdoc["title"] = a.title
            sdoc['url']=a.link
            sdoc['source_id']=a.source_id
            yield sdoc

