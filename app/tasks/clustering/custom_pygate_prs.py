from pygate import *
from pygate.ext.google_nlp import SentimentAnalyserPR
from pygate.ext.spacy_io import SpacyDoc
from pygate.ext.textacy import KeyTermAnnotatorPR
from pygate.prs import SPMRulePR
from pygate.ext.relegence_nlp import RelEntityTagger

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

    def __init__(self, kt=False, ent=False, all_sent =True):
        self.kt = kt
        self.ent = ent
        self.all_sent = all_sent

    def process(self,doc):
        '''
        :type doc SpacyDoc
        :param doc:
        :return:
        '''
        for kt in doc['KeyTerm']:
            sents=doc.query_overlappedby_y(kt, 'Sentence')
            s=sents[0] #type: Annotation
            s.add_relation('key_term', kt)
#             s.set_feature('key_terms', s.get_relation('key_term'))
        for entity in doc['Entity']:
            if len(entity.text)<200:
                s.add_relation('entity', entity)
        s.add_feature('domain_id', domain_id)

        for sent in doc['Sentence']:
            #watever the filtering
            sent #type: Annotation
            has_kt=bool(sent.get_relation('key_term'))
            has_ent=bool(sent.get_relation('entity'))

            if (self.kt and has_kt) or (self.ent and has_ent) or self.all_sent:
                sent.set_attribute('FSentence', True)



class SentimentHighlighter(PR):

    def process(self,doc):
        '''
        :type doc SpacyDoc
        :param doc:
        :return:
        '''
        THRESHOLD=0.6

        pos=[]
        neg=[]
        for sent in doc.sents:
            if 'gs_score' in sent.features:
                score=sent.get_feature('gs_score')
                if score>THRESHOLD:
                    ann=Annotation(sent.text, sent.tStart, sent.tEnd, sent.cStart, sent.cEnd, 'PosSentiment',doc)
                    pos.append(ann)
                elif score< -1*THRESHOLD:
                    ann = Annotation(sent.text, sent.tStart, sent.tEnd, sent.cStart, sent.cEnd, 'NegSentiment', doc)
                    neg.append(ann)

        doc.set_annotation_set('PosSentiment', pos)
        doc.set_annotation_set('NegSentiment', neg)

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

