from aol import relegence
from app.model import Subject, Meta, Story, Article
import datetime

relegence=relegence.Relegence()

def get_articles_by_story(story_id):
    story=Story.find_by_id(story_id)
    if story==None:
        s=relegence.story.by_story_id(story_id, {'numDocs': 100})
        story=smodel=Story(story_id=s.id, title=s.title, mag_score=s.magScore, num_total_docs=s.numTotalDocs, num_original_docs=s.numOriginalDocs)
        smodel.save()
        articles=s.articles
        for a in articles:
            fname=a.id.replace('/','#')
            amodel=Article(article_id=a.id, story=smodel, source=a.source, link=a.link, title=a.title, snippet=a.snippet, file_name=fname)
            amodel.save()

    return Article.find_by_story(story)

def sync_relegence_hierarchy():
    subjects=relegence.taxenomy.get_subjects_hierarchy()['data']
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

