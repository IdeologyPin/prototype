import spacy
# import pygate
import os
REDIS_URL='redis://localhost:6379'

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/usr/local/google_nlp.json'

PARSERS={}

def init_spacy():
    global spacy_parser
    parser = spacy.load('en')
    PARSERS['spacy_parser'] = parser
    print "Spacy Initialized"