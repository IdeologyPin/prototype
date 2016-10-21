from mongoengine import *

def init_connection():
    connect('perspect_db')


class Meta(Document):
    r_subject_synced = LongField()

    @classmethod
    def get_data(cls):
        return cls.objects.first()


class Subject(Document):
    subject_id = IntField(primary_key=True)
    name = StringField()
    children = ListField(ReferenceField('self'))
    meta = {
        'indexes': [
            '$name'  # text index
        ]
    }

    @classmethod
    def search(cls, words):
        cls.objects().search_text(words).order_by('$text_score')


class Entity(Document):
    pass


class Story(Document):
    story_id = LongField(primary_key=True)
    title = StringField();
    mag_score = IntField();
    num_total_docs = IntField();
    num_original_docs = IntField();

    @classmethod
    def find_by_id(cls, story_id):
        return Story.objects(story_id=story_id).first()


class Article(Document):
    article_id = StringField(primary_key=True);
    story = ReferenceField(Story);
    source = StringField();
    link = StringField();
    title = StringField();
    snippet = StringField();
    file_name = StringField();
    published = DateTimeField();
    author = StringField();
    content = StringField();

    @classmethod
    def find_by_story(cls, story):
        return cls.objects(story=story)


class Centroid(EmbeddedDocument):
    id = StringField()
    name = StringField()
    tags = ListField(StringField())
    vector = ListField(FloatField())


class Node(EmbeddedDocument):
    article = ReferenceField('Article')
    span_ids=ListField(IntField())
    span_type=StringField()
    label = StringField()
    vector = ListField(FloatField())
    scores = MapField(FloatField())  # centroid_id -> float
    link = StringField()


class SpanNode(EmbeddedDocument):
    pass


class Clustering(Document):
    name = StringField()
    method = StringField()
    collection_id=StringField()
    clusters = ListField(EmbeddedDocumentField(Centroid))
    nodes = ListField(EmbeddedDocumentField(Node))
    status = StringField()

    @classmethod
    def by_collection_id(cls, collection_id):
        '''
        :param collection_id: can be story_id or subject_id, or any article collection you specified.
        :return:
        '''
        return Clustering.objects(collection_id=collection_id)

