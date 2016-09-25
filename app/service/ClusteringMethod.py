from app.model import Clustering

class ClusteringMethod(object):

    def cluster(self, articles):
        '''
        run pipeline, convert the row results of the clustering to the db model and return.
        :param articles:
        :return: a Clustering model object
        '''
        return Clustering()
