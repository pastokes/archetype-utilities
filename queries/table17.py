from digipal.models import *
from django.db.models import Q

glHands = Hand.objects.filter(relevant=True).filter(gloss_only=True).distinct()

glHIs = HistoricalItem.objects.filter(itempart__hand__in=glHands).distinct()

hiCounter = 0
handCounter = 0
for c in Category.objects.all():
    catHands = glHands.filter(glossed_text=c).distinct()
    if catHands.count() > 0:
        hiCount = HistoricalItem.objects.filter(itempart__hand__in=catHands).distinct().count()
        print c, hiCount, catHands.count()
        handCounter += catHands.count()
        hiCounter += hiCount

print 'Total: ', counter, handCounter

# Check for glossing hands with no text specified: need to fix any that are present 
glHands.filter(glossed_text__isnull=True)

for h in glHands.filter(glossed_text__isnull=True):
    hi = HistoricalItem.objects.get(itempart__hand=h)
    print h, '[H', h.id, ']: ', hi, CurrentItem.objects.get(itempart__historical_item=hi), ' - ', Description.objects.filter(historical_item=hi).filter(source__label__exact='G.')[0].description
    print '-----------------------------------------'

# Check for glossing hands with no number of glosses specified: need to fix any that are present 
glHands.filter(glossed_text__isnull=True)

for h in glHands.filter(num_glosses__isnull=True):
    hi = HistoricalItem.objects.get(itempart__hand=h)
    print h, '[H', h.id, ']: ', hi, CurrentItem.objects.get(itempart__historical_item=hi)
    print '-----------------------------------------'



# But doesn't really work: this doesn't tell you which text is glossed; it only tells you what the categories of HI are which contain glosses which is not the same thing.
# E.g. G.555 has glosses to the HE, but its Category is both 'Bede, HE' and 'Caedmon's Hymn', so CH also appears as 'glossed'.
#counter = 0
#for c in Category.objects.filter(historicalitem__hand__in=glHands).distinct():
#    print c, glHands.filter(item_part__hand__glossed_text=c).distinct().count()
#    counter += glHands.filter(item_part__hand__glossed_text=c).distinct().count()
#
#print 'Total: ', counter


