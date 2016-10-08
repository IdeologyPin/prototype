ARTICLE_FOLDER='/srv/perspect/'
spacy_parser = None


def init_mongo():
   import init_mongo


def init_spacy():
    import spacy
    spacy_parser = spacy.load('en')