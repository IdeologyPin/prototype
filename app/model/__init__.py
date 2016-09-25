from models import *
import time
import app.data.souce_relegence as sr


meta=Meta.get_data();
if meta==None:

    meta=Meta(r_subject_synced=0)

    if meta.r_subject_synced==0:
         sr.sync_relegence_hierarchy()
         meta.r_subject_synced=long(time.time())

    meta.save()