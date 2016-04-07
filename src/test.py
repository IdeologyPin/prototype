__author__ = 'sasinda'
from aol.relegence import Relegence

r=Relegence()
respJson=r.taxenomy.hierarchy.get_subjects()
print respJson
