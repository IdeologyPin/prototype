from pygate import *
from pygate.ext.google_nlp import SentimentAnalyserPR
from pygate.ext.spacy_io import SpacyDoc
from pygate.ext.textacy import KeyTermAnnotatorPR
from pygate.prs import SPMRulePR

from app.model import Clustering
from app.tasks.clustering.clustering_method import ClusteringMethod


class DuplicateClearingPR(PR):
    def __init__(self):
        self.examined_titles = set()

    def process(self, doc):
        '''
        :type SpacyDoc
        :param doc:
        :return:
        '''
        title = doc["title"]
        doc.sents
        if title in self.examined_titles:
            raise ValueError("Duplicate Article: title"+title)
        self.examined_titles.add(title)



class CustomFeatureExtractor(PR):

    def process(self,doc):
        '''
        :type doc SpacyDoc
        :param doc:
        :return:
        '''
        for kt in doc['KeyTerm']:
            sents=doc.query_overlappedby_y(kt, 'Sentence')
            list(sents)[0][2].add_relation('key_term', kt)

class SentimentHighlighter(PR):

    def process(self,doc):
        pass


class BratEmbeddingToMongoPR(PR):

    def __init__(self, anno_types):
        self.anno_types=anno_types

    def process(self,doc):
        art=doc['mongo']
        id=0
        art.entities=[]
        for anno_type in self.anno_types:
            if anno_type in doc:
                annots=doc[anno_type]
                for a in annots:
                    id+=1
                    art.entities.append(['T'+str(id), anno_type, [[a.cStart, a.cEnd]]])
        art.save()

def run_fv_generation_method(articles_collection):
    ann_store = AnnotationStore('Sentence')
    doc_store = DocumentStore('~')

    prs = [
        DuplicateClearingPR(),
        SentimentAnalyserPR('Sentence'),
        SPMRulePR('@Sentence.gs_score > 0.6 -->  @PosSentiment'),
        SPMRulePR('@Sentence.gs_score < -0.6 -->  @NegSentiment'),
        KeyTermAnnotatorPR(),
        CustomFeatureExtractor(),
        BratEmbeddingToMongoPR(['KeyTerm', 'PosSentiment', 'NegSentiment']),
        ann_store, doc_store]
    pipe = Pipeline()
    pipe.setPRs(prs).setCorpus(articles_collection)
    result=pipe.process(5)


    for a in ann_store:
        pass




class FV1ClusteringMethod2(ClusteringMethod):

    def _init_clustering(self, article_collection):
        clustering = Clustering(
            name="Feature Vector Custom 1 for articles in story:" + article_collection.collection_id, method="FV1",
            collection_id=article_collection.collection_id, status='running')
        clustering.save()
        self.clustering=clustering

    def _cluster(self, article_collection):
        '''
        :param article_collection: Object that can query mongodb for articles.
         has a collection_id: identifier for the article collection story_id or subject_id
         type app.service.clustering_method.ArticleCollection
        :return:
        '''

        clusters= run_fv_generation_method(article_collection)


        # art_dict={}
        # for a in articles:
        #     art_dict[a.id]=a
        #
        # centroids=[]
        # nodes=defaultdict(lambda :None)
        # for key, cluster in cluster_dict.iteritems():
        #     key=str(key)
        #     centroids.append(Centroid(id=str(key), name=cluster['keywords'][0], tags=cluster['keywords']))
        #     for sent in cluster['sentences']:
        #         id=sent[0]
        #         score=sent[1]
        #         sent=sentence_objects[id]
        #         doc=nodes[sent['article_id']]
        #         if doc==None:
        #             article=art_dict[sent['article_id']]
        #             n=Node(article=sent['article_id'], span_type='Document', scores={}, label=article.title+" "+article.source, link=article.link)
        #             nodes[sent['article_id']]=n
        #             for clust_key in cluster_dict.keys():
        #                 n.scores[str(clust_key)] = [0]
        #             n.scores[key] = [score]
        #         else:
        #             doc.scores[key].append(score)
        #
        # for node in nodes.values():
        #     for c_id, sent_scores in node.scores.iteritems():
        #          node.scores[c_id]=sum(sent_scores)/len(sent_scores)
        #
        # clustering=self.clustering
        # clustering.clusters=centroids
        # clustering.nodes=nodes.values()
        # clustering.save()
