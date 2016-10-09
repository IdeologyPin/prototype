from app.data import souce_relegence
from app.model import Story, Article
from fv_generation_method import run_feature_generation_method

METHODS = {
    'DOC2VEC': None,
    'LDA': None,
    'FV_GENERATION_METHOD': None}


def cluster(story_id, method):
    """
        
    """
    articles = souce_relegence.get_articles_by_story(story_id)
    if method == 'fv':
        cluster_dict, sentence_objects = run_feature_generation_method(articles, story_id)

