
from app.model import Clustering
from app.tasks.clustering.clustering_method import ClusteringMethod
from custom_pygate_prs import *
from scipy.sparse import hstack
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from collections import Counter


def run_fv_generation_method(articles_collection):
    ann_store = AnnotationStore('Sentence', filterby_attrib_exist='FSentence')
    doc_store = DocumentStore('~')

    prs = [
        DuplicateClearingPR(),
        #         SentimentAnalyserPR('Sentence'),
        #         SentimentHighlighter(),
        KeyTermAnnotatorPR(),
        RelEntityTagger(),
        CustomFeatureExtractor(kt=True, ent=True, all_sent=False),
        BratEmbeddingToMongoPR(['KeyTerm', 'PosSentiment', 'NegSentiment', 'Entity']),
        ann_store, doc_store]

    pipe = Pipeline()
    pipe.setPRs(prs).setCorpus(articles_collection)

    result = pipe.process()

    sentences = ann_store.annots
    X = extract_feature_vector(sentences)
    print 'feature extraction completed!'
    clust_dict = cluster_sentence_vectors(sentences, X, N_CLUSTERS=2)
    return clust_dict


def extract_feature_vector(sentences):
    vect_ent = DictVectorizer()
    vect_kt = DictVectorizer()
    entity_list = []
    kt_list = []

    for sent in sentences:
        entity_list.append([e['wikidata'] for e in sent.get_relation('entity')])
        key_terms = [kt.text for kt in sent.get_relation('key_term')]
        kt_list.append(key_terms)
        sent['key_terms'] = dict((kt, 1) for kt in key_terms)

    X_ent = vect_ent.fit_transform(Counter(ent) for ent in entity_list)
    X_kt = vect_kt.fit_transform(Counter(kt) for kt in kt_list)
    X_sentiment = None
    X = hstack([X_ent, X_kt])
    return X


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


def cluster_sentence_vectors(sentences, X, N_CLUSTERS=5):
    """
        given vector results and number of clusters return cluster objects
    """
    kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=45)
    cluster_assignments = kmeans.fit_predict(X)
    centroids = kmeans.cluster_centers_

    cluster_dict = {
        x: {"vector": centroids[x], "sentences": [], "reduced": False}
        for x in xrange(len(centroids))}

    temp_cluster_keywords = {x: {} for x in xrange(len(centroids))}

    for i, sent in enumerate(sentences):
        sent['feature_vector'] = X.toarray()[i]
        cluster_num = cluster_assignments[i]
        sent["cluster_num"] = cluster_num
        dist_to_centroid = euclidean_distances(centroids[cluster_num], sent["feature_vector"])[0][0]
        sent["dist_to_centroid"] = dist_to_centroid
        # add to cluster object
        cluster_dict[cluster_num]["sentences"].append(sent)
        # merge keyword dictionaries together
        temp_cluster_keywords[cluster_num] = merge_kwd_counts([temp_cluster_keywords[cluster_num], sent["key_terms"]])

    NUM_KEYWORDS = 10
    for cluster_num in temp_cluster_keywords:
        clustered = sorted(temp_cluster_keywords[cluster_num].items(), key=lambda x: x[1])[0:NUM_KEYWORDS]
        cluster_dict[cluster_num]["keywords"] = [x[0] for x in clustered]

    return cluster_dict




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
