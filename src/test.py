__author__ = 'sasinda'
from aol.relegence import Relegence

r=Relegence()
respJson=r.stories.by_subject('91485332')


print respJson
