from flask_restful import Resource
from flask_restful import reqparse
from app.model import Subject
from app.api.dto import *

class SubjectListAPI(Resource):
    '''
    /taxonomy/subjects/
    '''
    def get(self):
        subs=Subject.objects
        dto=SubjectListDto.from_mongo(subs)
        return dto.to_dict()

class EntityAPI(Resource):
    '''
    /taxonomy/entities/
    '''
    def get(self):
        pass