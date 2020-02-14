from digipal.models import *
from django.db.models import Q

# I'm not sure if this really counts what I want, but still...
# Surely there's a more efficient way using Django queries, but I'm not sure what it is.

graphlist = set()
for gc in GraphComponent.objects.all():
   if gc.graph not in graphlist:
      graphlist.add(gc.graph)

len(graphlist)
