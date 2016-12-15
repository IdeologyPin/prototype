from aol import relegence
from app.model import Subject, Meta, Story, Article
import datetime
import app.jobQ as jq
relegence_API=relegence.Relegence()

class RelegenceService(object):
    def __init__(self):
        self.rq=jq.get_RQ()


    def get_articles_by_story(self, story_id):
        story=Story.find_by_id(story_id)
        if story==None:
            s=relegence_API.stories.by_story_id(story_id, {'numDocs': 100})
            story=smodel=Story(story_id=s['id'], title=s['title'], mag_score=s['magScore'],
                               num_total_docs=s['numTotalDocs'], num_original_docs=s['numOriginalDocs']
                               # ,topic_creation_time= s['topicCreationTime'], last_topic_activity_time = s['lastTopicActivityTime']
                               )
            smodel.save()
            articles=s['articles']
            for a in articles:
                fname=a['id'].replace('/','|')
                amodel=Article(article_id=fname, story=smodel, source=a['source']['title'], \
                               link=a['link'], title=a['title'], snippet=a['snippet'], \
                               author=a['author']['name'], text=a['content'], file_name=fname, \
                               source_id=a['source']['id'])
                amodel.save()
        return Article.find_by_story(story)

    def get_treinding_by_subject(self, subject_id):
        # raw_data = relegence_API.trending.by_subject(subject_id, {'numDocs': 1})
        # fetch all docs for the subject as well.
        # self.rq.enqueue(job_save_alpha_docs_by_trending, subject_id)
        raw_data = relegence_API.trending.by_subject(subject_id, {'numDocs': 1, 'withDocs': True})
        return raw_data

    def sync_relegence_hierarchy(self):
        subjects=relegence_API.taxenomy.get_subjects_hierarchy()['data']
        queue=[]
        stack=[]

        # bfs search and add subject hierarchy(multiple roots) to db.
        # level order traverse bottom up, since child objects need to be saved first in db for references.

        for s in subjects:
            queue.append(s)

        while len(queue) > 0:
            sub=queue.pop(0)

            child_ids=[]
            for child in sub['children']:
                queue.append(child)
                child_ids.append(int(child['id']))

            model=Subject(subject_id=int(sub['id']), name=sub['name'], children=child_ids)
            stack.append(model)

        #Faster than popping last, just reverse order get by index.
        for i in range(len(stack)-1,-1,-1):
            model=stack[i]
            model.save()






