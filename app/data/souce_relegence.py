from aol import relegence
from app.model import Subject, Meta
import datetime

relegence=relegence.Relegence()

def sync_relegence_hierarchy():
    m= Meta.get_meta_data()

    if m.rel_subj_sync ==None:
        subjects=relegence.taxenomy.get_subjects_hierarchy().data
        queue=[]
        stack=[]

        # bfs search and add subject hierarchy(multiple roots) to db.
        # level order traverse bottom up, since child objects need to be saved first in db for references.

        for s in subjects:
            queue.append(s)

        while len(queue) > 0:
            sub=queue.pop(0)

            child_ids=[]
            for child in sub.children:
                queue.append(child)
                child_ids.append(int(child.id))

            model=Subject(subject_id=int(sub.id), name=sub.name, children=child_ids)
            stack.append(model)

        #Faster than popping last, just reverse order get by index.
        for i in range(len(stack),-1,-1):
            model=stack[i]
            model.save()

        m.rel_subj_sync=datetime.datetime.now()
        m.save()