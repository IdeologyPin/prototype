from mongoengine import *

connect('perspect_db')

class Meta(Document):
    rel_subj_sync=DateTimeField()

    @classmethod
    def get_data(cls):
        return cls.objects.first()


class Subject(Document):
    subject_id=IntField(primary_key=True)
    name=StringField()
    children=ListField(ReferenceField('self'))
    meta ={
        'indexes':[
            '$name' #text index
         ]
    }

    @classmethod
    def search(cls, words):
        cls.objects().search_text(words).order_by('$text_score')


class Entity(Document):
    pass

class Story(Document):
    pass

class Aritcle(Document):
    pass



class Centroid(EmbeddedDocument):
    pass

class Clustering(Document):
    name=StringField()
    clusters=ListField(EmbeddedDocumentField(Centroid))
    articles=MapField() #cluster_id -> ArticleNode list



class ArticleNode(EmbeddedDocument):
    article=ReferenceField('Article')
