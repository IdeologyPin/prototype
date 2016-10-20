import time
from app.data import RelegenceService
from app.model import Meta
import app.model as model

def init():
    model.init_connection()
    meta=Meta.get_data();
    if meta==None:

        meta=Meta(r_subject_synced=0)
        rs=RelegenceService()
        if meta.r_subject_synced==0:
             rs.sync_relegence_hierarchy()
             meta.r_subject_synced=long(time.time())

        meta.save()