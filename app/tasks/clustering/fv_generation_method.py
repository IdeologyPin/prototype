from collections import Counter
from collections import defaultdict

import httplib2
import numpy as np
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from scipy.sparse import hstack
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import euclidean_distances


import textacy_keyterms as keyterms
from app.tasks.clustering.clustering_method import ClusteringMethod
from .. import worker_env as env


def run_fv_generation_method(articles, sentiment, debug=False):
    """
        runs all methods to return dictionary of clusters ids and sentence/dist
        and return list of sentence objects
        articles and story_id
    """
    articles = delete_repeating_titles(articles)
    articles = parse_articles(articles)
    if debug is True:
        print "parsed articles using spacy"
    sentence_objects = create_sentence_objects(articles)
    if debug is True:
        print "created sentence objects"
    sentence_objects = create_sentence_objects(articles)

    service=None
    if sentiment:
        service = get_google_service()
    if debug is True:
        if sentiment:
            print "got service"
    X = add_sentence_level_features(sentence_objects, articles, service, sentiment)
    if debug is True:
        print "clustering now"
    cluster_dict = cluster_sentence_vectors(sentence_objects,  X, reduce_dim=True, r=20)
    if debug is True:
        print "clustering done"
    return cluster_dict, sentence_objects


def delete_repeating_titles(articles):
    """
        delete articles that have the same title
        could we make this into an article feature?
    """
    non_repeating = []
    titles = set()
    for art in articles:
        title = art["title"]
        if title not in titles:
            non_repeating.append(art)
            titles.add(title)
    return non_repeating


def parse_articles(articles):
    """
        parse article content using spacy, add field in article dict called "parsed_content"
        articles: list of article jsons from aol api
        parser: spacy.load('en')
    """
    parser = env.PARSERS['spacy_parser']
    docs=[]
    for i, art in enumerate(articles):
        doc={}
        doc["parsed_content"] = parser(art.text)
        doc["id"]=art.article_id
        doc["title"]=art.title
        docs.append(doc)
    return docs


def create_sentence_objects(articles):
    """
        given articles, return list of sentence objects
    """
    sent_objects = []
    sent_count = 0
    for art in articles:
        beg_sent = sent_count
        art["beg_sent"] = beg_sent
        parsed_article = art['parsed_content']
        article_id = art["id"]
        for sent in parsed_article.sents:
            sent_obj = {}
            sent_obj["spacy_sent"] = sent
            sent_obj["sent_id"] = sent_count
            sent_obj["article_id"] = article_id
            sent_obj["feature_vector"] = None
            sent_obj["cluster_num"] = None
            sent_objects.append(sent_obj)
            sent_count += 1
        art["end_sent"] = sent_count - 1
    return sent_objects


def tokenize_sent(sentence, extra_stop):
    """
        tokenize spacy sent for bow features
    """
    cleaned_sent = []
    for tok in sentence["spacy_sent"]:
        if not tok.is_punct and not tok.is_stop and tok.orth_ not in extra_stop and\
           not tok.is_space:
            cleaned_sent.append(tok.lemma_)
    return cleaned_sent


def get_all_keywords(articles):
    """
        return a set of keywords in all articles
        -get keywords one articlea at a time-
    """
    keywords = set()
    for art in articles:
        keywords.update(get_article_keywords(art["parsed_content"]))
    return keywords


def get_article_keywords(article):
    """
        sgrank alg. to get keywords from article
    """
    ranked_results = keyterms.sgrank(article)
    return [tok[0].lower() for tok in ranked_results]


def make_keyword_dict(sent, keywords):
    """
        lemmatize the sentence so keywords that have changed tense can be found
        add keywords to sentence object
    """
    kwd_dict = {}
    sent["keywords"] = {}
    for kwd in keywords:
        if kwd in ' '.join([tok.lemma_ for tok in sent["spacy_sent"]]).lower():
            if kwd not in kwd_dict:
                kwd_dict[kwd] = 1
                sent["keywords"][kwd] = 1
            else:
                kwd_dict[kwd] += 1
                sent["keywords"][kwd] += 1
    return kwd_dict


def get_google_service():
    """
        to initialize googlecredentials
    """
    credentials = GoogleCredentials.get_application_default()
    scoped_credentials = credentials.create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    scoped_credentials.authorize(http)
    return discovery.build('language', 'v1beta1', http=http)


def get_sentiment(sent, service):
    """
        use google cloud nlp to get sentiment
    """

    body = {'document': {
                'type': 'PLAIN_TEXT',
                'content': sent.orth_
                }
            }
    request = service.documents().analyzeSentiment(body=body)
    response = request.execute()
    return [response["documentSentiment"]["magnitude"], response["documentSentiment"]["polarity"]]


def add_sentence_level_features(sentence_objects, articles, service, sentiment=True):
    """
        add feature vector to sentence object. features:
        - bow
        - keywords
    """
    extra_stop = ["n't", "'s", "'m"]
    vect_bow = DictVectorizer()
    #BOW features
    X_bow = vect_bow.fit_transform(Counter(tokenize_sent(sent, extra_stop)) for sent in sentence_objects)
    #keyword features
    vect_keywords = DictVectorizer()
    keywords = get_all_keywords(articles)
    X_keyword = vect_keywords.fit_transform(make_keyword_dict(sent, keywords) for sent in sentence_objects)
    print "sentiment analysis"
    #sentiment features:
    if sentiment:
        X_sentiment = [get_sentiment(sent["spacy_sent"], service) for sent in sentence_objects]

    #concatenate
    if sentiment:
        vects = hstack([X_bow, X_keyword, X_sentiment])
    else:
        vects = hstack([X_bow, X_keyword])

    #add vector to sentence_object
    num = 0
    for vect in vects.toarray():
        sentence_objects[num]["feature_vector"] = vect
        num += 1
    return vects


def dimensionality_reduction(X, r):
    """
        reduce dimensions using SVD
    """
    U, s, V = np.linalg.svd(X.toarray())
    return rank_r_approx(U, s, r)


def rank_r_approx(U, s, r):
    """
        return dimensionally reduced X, with rank r
    """
    sigma = np.zeros((r, r), float)
    np.fill_diagonal(sigma, s[:r])
    return np.dot(U[:, :r], sigma)


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


def  cluster_sentence_vectors(sentence_objects, X, r=100, reduce_dim=True, N_CLUSTERS=5):
    """
        given vector results and number of clusters return cluster objects
        reduce_dim is True on default
    """
    kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=0)

    if reduce_dim:
        X_reduced = dimensionality_reduction(X, r)
        cluster_assignments = kmeans.fit_predict(X_reduced)
        centroids = kmeans.cluster_centers_
        cluster_dict = {x: {"vector": centroids[x], "sentences": [], "reduced": True}
                        for x in xrange(len(centroids))}
    else:
        cluster_assignments = kmeans.fit_predict(X)
        centroids = kmeans.cluster_centers_
        cluster_dict = {x: {"vector": centroids[x], "sentences": [], "reduced": False}
                        for x in xrange(len(centroids))}

    temp_cluster_keywords = {x: {} for x in xrange(len(centroids))}
    count = 0
    for sent in sentence_objects:
        cluster_num = cluster_assignments[count]
        sent["cluster_num"] = cluster_num
        if reduce_dim:
            reduced_vect = X_reduced[count]
            sent["reduced_feature_vector"] = reduced_vect
            dist_to_centroid = euclidean_distances(centroids[cluster_num], sent["reduced_feature_vector"])[0][0]
        else:
            dist_to_centroid = euclidean_distances(centroids[cluster_num], sent["feature_vector"])[0][0]

        sent["dist_to_centroid"] = dist_to_centroid
        #add to cluster object
        cluster_dict[cluster_num]["sentences"].append((sent["sent_id"], dist_to_centroid))
        # merge keyword dictionaries together
        temp_cluster_keywords[cluster_num] = merge_kwd_counts([temp_cluster_keywords[cluster_num], sent["keywords"]])
        count += 1

    NUM_KEYWORDS = 10
    for cluster_num in temp_cluster_keywords:
        clustered = sorted(temp_cluster_keywords[cluster_num].items(), key=lambda x: x[1])[0:NUM_KEYWORDS]
        cluster_dict[cluster_num]["keywords"] = [x[0] for x in clustered]

    return cluster_dict


from app.model import *

class FV1ClusteringMethod(ClusteringMethod):

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


        articles=article_collection.get_articles()
        cluster_dict, sentence_objects=run_fv_generation_method(articles, False, debug=True)
        art_dict={}
        for a in articles:
            art_dict[a.id]=a

        centroids=[]
        nodes=defaultdict(lambda :None)
        for key, cluster in cluster_dict.iteritems():
            key=str(key)
            centroids.append(Centroid(id=str(key), name=cluster['keywords'][0], tags=cluster['keywords']))
            for sent in cluster['sentences']:
                id=sent[0]
                score=sent[1]
                sent=sentence_objects[id]
                doc=nodes[sent['article_id']]
                if doc==None:
                    article=art_dict[sent['article_id']]
                    n=Node(article=sent['article_id'], span_type='Document', scores={}, label=article.title+" "+article.source, link=article.link)
                    nodes[sent['article_id']]=n
                    for clust_key in cluster_dict.keys():
                        n.scores[str(clust_key)] = [0]
                    n.scores[key] = [score]
                else:
                    doc.scores[key].append(score)

        for node in nodes.values():
            for c_id, sent_scores in node.scores.iteritems():
                 node.scores[c_id]=sum(sent_scores)/len(sent_scores)

        clustering=self.clustering
        clustering.clusters=centroids
        clustering.nodes=nodes.values()
        clustering.save()


