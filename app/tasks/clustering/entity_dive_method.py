from app.model import Clustering
from app.tasks.clustering.clustering_method import ClusteringMethod
from custom_pygate_prs import *
from scipy.sparse import hstack
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from collections import Counter

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

    pipe = Pipeline()
    pipe.setPRs(prs).setCorpus(articles_collection)

    result = pipe.process()
    ent_annots = ent_store.annots
    # kt_annots= kt_store.annots
    # unique_kt= set([kt.text for kt in kt_annots])
    unique_ent_dict= defaultdict(lambda :[])
    unique_ents=[]
    for ent in ent_annots:
        unique_ent_dict[ent['wikidata']].append(ent.text)
    for key, ent_texts in unique_ent_dict:
        ename=sorted(ent_texts, key=len)[-1]
        unique_ents.append(ename)

    for ent in unique_ents:
        fe = CustomEntityFeatureExtractor()
        fann_store=AnnotationStore('Sentence', filterby_attrib_exist='FSentence')
        Pipeline.setPRs([fe, fann_store]).process()
        fsents=fann_store.annots
        X = get_sentiment(fsents)
        clust_dict = cluster_by_sentiment(fsents, X, N_CLUSTERS=2)


    # X = extract_feature_vector(sentences, **params)
    print 'feature extraction completed!'
    # clust_dict = cluster_sentence_vectors(sentences, X, N_CLUSTERS=2)
    # return clust_dict

def get_sentiment(sentences):

    sentiment_list = []
    for sent in sentences:
        sentiment_list.append([sent.get_feature('gs_score')])
    X = sentiment_list
    return X


def cluster_by_sentiment(sentences, X, N_CLUSTERS=5):
    """
        given vector results and number of clusters return cluster objects
    """
    # kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=45)
    # cluster_assignments = kmeans.fit_predict(X)
    # centroids = kmeans.cluster_centers_

    NEG_THRESHOLD = -0.75
    POS_THRESHOLD = .25

    cluster_dict = {
        1:{'vector':[1], "sentences":[]},
        0:{'vector':[0], "sentences":[]},
        -1:{'vector':[-1], "sentences":[]}
        }


    for score, sentence in zip(X, sentences):
        if score >= POS_THRESHOLD:
            cluster_dict[1]['sentences'].append(sentence)
        elif score <= NEG_THRESHOLD:
            cluster_dict[-1]['sentences'].append(sentence)
        else:
            cluster_dict[0]['sentences'].append(sentence)

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