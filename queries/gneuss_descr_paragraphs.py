from digipal.models import *

descg_set = Description.objects.filter(description__contains='</p><p>').filter(source=Source.objects.get(label='G.'))
for d in descg_set:
   print '<li><a href="https://digipal-stg.cch.kcl.ac.uk/admin/digipal/historicalitem/',d.historical_item.id,'">', d.historical_item.id, '</a>', d.description, '</li>'

