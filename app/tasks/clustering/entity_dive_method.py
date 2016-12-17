from app.model import Clustering, Centroid, Node, ClusteringList, Story, ClusteringEmbedded
from app.tasks.clustering.clustering_method import ClusteringMethod
from custom_pygate_prs import *
from scipy.sparse import hstack
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from collections import Counter

NEG_THRESHOLD = -0.75
POS_THRESHOLD = .25

def run_entity_dive_method(articles_collection):
    ent_store = AnnotationStore('Entity')
    kt_store = AnnotationStore('KeyTerm')

    doc_store = DocumentStore('~')

    prs = [
        DuplicateClearingPR(),
        SentimentAnalyserPR('Sentence'),
        SentimentHighlighter(),
        KeyTermAnnotatorPR(),
        RelEntityTagger(),
        BratEmbeddingToMongoPR(['KeyTerm', 'PosSentiment', 'NegSentiment', 'Entity']),
        ent_store, kt_store, doc_store]

    pipe = Pipeline(articles_collection)
    pipe.setPRs(prs).setCorpus(articles_collection)

    result = pipe.process(3)
    ent_annots = ent_store.annots
    # kt_annots= kt_store.annots
    # unique_kt= set([kt.text for kt in kt_annots])
    unique_ent_dict= defaultdict(lambda :[])

    for ent in ent_annots:
        unique_ent_dict[ent['wikidata']].append(ent.text)
    for key, ent_texts in unique_ent_dict.iteritems():
        ename=sorted(ent_texts, key=len)[-1]
        unique_ent_dict[key]=ename

    clust_dicts={}
    for ent_id, ename in unique_ent_dict.iteritems():
        fe = CustomEntityFeatureExtractor(ent_id)
        fann_store=AnnotationStore('Sentence', filterby_attrib_exist='FSentence')
        Pipeline(result).setPRs([fe, fann_store]).process()
        fsents=fann_store.annots
        X = get_sentiment(fsents)
        clust_dict = cluster_by_sentiment(fsents, X)
        clust_dicts[ename]=clust_dict

    clutering_list_model = make_clustering_list_model(clust_dicts)
    clutering_list_model.collection_id=articles_collection.story_id
    clutering_list_model.name= Story.find_by_id(articles_collection.story_id).title
    return clutering_list_model


def make_clustering_list_model(clust_dicts):
    clusterings=[]
    nodes = defaultdict(lambda: None)

    for ename, cluster_set in clust_dicts.iteritems():

        centroids = {} # are the clusters in that clustering
        for key, cluster in cluster_set.iteritems():
            ename_key = ename + '_' + key
            centroids[key]=(Centroid(id=ename_key, name=key, tags=cluster['keywords'], node_ids=[]))
            for sent in cluster['sentences']:
                score = sent['score']
                node = nodes[sent.doc['id']]
                if node == None:
                    article = sent.doc['mongo']
                    node = Node(article=sent.doc['id'], span_type='Document', scores={},
                                label=article.title + " " + article.source, link=article.link)
                    nodes[sent.doc['id']] = node
                    for clust_key in cluster_set.keys(): #keys are pos, neu, neg
                        node.scores[ename+'-'+clust_key] = [0]
                    node.scores[ename_key] = [score]
                    node.scores[ename+'_avg']=[score]
                else:
                    node.scores[ename_key].append(score)
                    node.scores[ename + '_avg'].append(score)

        for node in nodes.itervalues():
            senti_scores=node.scores.get(ename + '_avg')
            if senti_scores:
                avg_sentiment=sum(senti_scores)/len(senti_scores)
                node.scores[ename + '_avg']= avg_sentiment
                if avg_sentiment>= POS_THRESHOLD:
                    key='pos'
                elif avg_sentiment <= NEG_THRESHOLD:
                    key='neg'
                else:
                    key='neu'
                centroids[key].node_ids.append(str(node.article))
        clustering = ClusteringEmbedded(name=ename + ' -' + 'sentiment based clustering', clusters=centroids.values())
        clusterings.append(clustering)

    return ClusteringList(clusterings=clusterings, nodes=nodes, method='ENTDD')

def get_sentiment(sentences):

    sentiment_list = []
    for sent in sentences:
        sentiment_list.append([sent.get_feature('gs_score')])
    X = sentiment_list
    return X


def cluster_by_sentiment(sentences, X):
    """
        given vector results and number of clusters return cluster objects
    """
    # kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=45)
    # cluster_assignments = kmeans.fit_predict(X)
    # centroids = kmeans.cluster_centers_



    cluster_dict = {
        'pos':{'vector':[1], "sentences":[], 'keywords':[]},
        'neu':{'vector':[0], "sentences":[], 'keywords':[]},
        'neg':{'vector':[-1], "sentences":[], 'keywords':[]}
        }


    for scores, sentence in zip(X, sentences):
        senti_score=scores[0]
        sentence['score']=senti_score
        if senti_score >= POS_THRESHOLD:
            cluster_dict['pos']['sentences'].append(sentence)
        elif senti_score <= NEG_THRESHOLD:
            cluster_dict['neg']['sentences'].append(sentence)
        else:
            cluster_dict['neu']['sentences'].append(sentence)

    # temp_cluster_keywords[cluster_num] = merge_kwd_counts([temp_cluster_keywords[cluster_num], sent["key_terms"]])
    return cluster_dict


def merge_kwd_counts(keywords):
    """
        given list of dicts with keywords, merges them into one dict
    """
    kwds_aggregation = defaultdict(list)
    for d in keywords:
        for key, value in d.iteritems():
            if key in kwds_aggregation:
                kwds_aggregation[key] += value
            else:
                kwds_aggregation[key] = value
    return kwds_aggregation


class ENTDDClusteringMethod(ClusteringMethod):
    def _init_clustering(self, article_collection):
        clustering = Clustering(
            name="Entity Deep Drive: " + article_collection.collection_id, method="ENTDD",
            collection_id=article_collection.collection_id, status='running')
        clustering.save()
        self.clustering = clustering

    def _cluster(self, article_collection):
        '''
        :param article_collection: Object that can query mongodb for articles.
         has a collection_id: identifier for the article collection story_id or subject_id
         type app.service.clustering_method.ArticleCollection
        :return:
        '''

        clutering_list_model = run_entity_dive_method(article_collection)
        clutering_list_model.save()

