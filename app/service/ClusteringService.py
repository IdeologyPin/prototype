from app.data import souce_relegence
from app.model import Story, Article

METHODS = {
    'DOC2VEC': None,
    'LDA': None,
    'CUSTOM_FEATURES_SA': None}


def cluster(story_id, method):
    articles = souce_relegence.get_articles_by_story(story_id)
