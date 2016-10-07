import json
import bson.json_util as bson
def to_json(dto):
    return  json.dumps(dto.__dict__)


class BaseDto(object):
     def to_json(self):
         return json.dumps(self)

class SubjectList(BaseDto):

    def __init__(self,subjects):
        self.subjects = subjects
        self.count = len(subjects)

    @classmethod
    def from_mongo(self, subjects_bson):
        subs=[]
        for s in subjects_bson:
            subs.append(bson.dumps(s))
        return  SubjectList(subs)



