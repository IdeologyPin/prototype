from flask_restful import Resource
from flask_restful import reqparse

from app.api.dto import TrendingStoryListDto
from app.data import relegence_service as rs
relegence_api=rs.relegence_API

# /stories/<story_id> -> details about story
class StoryAPI(Resource):

    '''
    get story details + doc urls for the story.
    '''
    def get(self, story_id):
        return relegence_api.stories.by_story_id(story_id)


class StoryListAPI(Resource):
    '''
        :route: /story/?[subject-id=string]
    '''
    def __init__(self):
        parser = self.parser = reqparse.RequestParser()
        parser.add_argument('subject-id')

    '''
    get list of stories
    '''
    def get(self):
        args = self.parser.parse_args()
        return relegence_api.stories.by_subject(args['subject-id'], {'numDocs': 100})


class StoryTrendingAPI(Resource):
    '''
        :route: /story/trending/<int:subject_id>
    '''
    def __init__(self):
        parser = self.parser = reqparse.RequestParser()
        parser.add_argument('subject-id')

    '''
    get list of stories
    '''
    def get(self, subject_id):
        args = self.parser.parse_args()
        raw_data = relegence_api.trending.by_subject(subject_id, {'numDocs': 1})
        return TrendingStoryListDto.from_relegence(raw_data)

