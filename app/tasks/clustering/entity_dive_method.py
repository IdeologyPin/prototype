from app.model import Clustering
from app.tasks.clustering.clustering_method import ClusteringMethod
from custom_pygate_prs import *
from scipy.sparse import hstack
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from collections import Counter

def run_entity_dive_method(articles_collection):
    ent_store = AnnotationStore('Entity', filterby_attrib_exist='FSentence')
    kt_store = AnnotationStore('KeyTerm', filterby_attrib_exist='FSentence')

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
    entities = ent_store.annots
    kt_terms= kt_store.annots



    # X = extract_feature_vector(sentences, **params)
    print 'feature extraction completed!'
    # clust_dict = cluster_sentence_vectors(sentences, X, N_CLUSTERS=2)
    # return clust_dict

def get_sentiment(sentences, kt, ent, all_sent):

    vect_kt = DictVectorizer()
    if kt is not True:
        vect_ent_bow = DictVectorizer()
        entity_bow_list = []
    else:
        vect_ent = DictVectorizer()
        entity_list = []
    kt_list = []
    sentiment_list = []

    for sent in sentences:
        if kt is not True:
            entity_list.append([e['wikidata'] for e in sent.get_relation('entity')])
        else:
            entity_bow_list.append([])
        key_terms = [kt.text for kt in sent.get_relation('key_term')]
        kt_list.append(key_terms)
        sent['key_terms'] = dict((kt, 1) for kt in key_terms)
        sentiment_list.append([sent.get_feature('gs_magnitude'), sent.get_feature('gs_score')])
    if kt is not True:
        X_ent = vect_ent_bow.fit_transform(Counter(ent) for ent in entity_bow_list)
    else:
        X_ent = vect_ent.fit_transform(Counter(ent) for ent in entity_list)
    X_kt = vect_kt.fit_transform(Counter(kt) for kt in kt_list)
    X = hstack([X_ent, X_kt, sentiment_list])
    return X