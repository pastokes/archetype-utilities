from digipal.models import *
from django.db.models import Q

relCharters = HistoricalItem.objects.filter(itempart__hand__in=relHands).filter(display_label__contains='charter').distinct()

roy = Q(categories__name__exact='Royal Charter')
nonRoy = Q(categories__name__contains='Grant')
misc = Q(categories__name__exact='Miscellaneous')
will = Q(categories__name__exact='Will or Bequest')
bounds = Q(categories__name__exact='Bounds')

outString = ''
outString += 'Royal Charters: %d\n' % (relCharters.filter(roy).distinct().count())
outString +=  'Non-Royal Charters: %d\n' % (relCharters.filter(nonRoy).distinct().count())
outString +=  'Misc. Charters: %d\n' % (relCharters.filter(misc).distinct().count())
outString +=  'Wills: %d\n' % (relCharters.filter(will).distinct().count())
outString +=  'Bounds: %d\n' % (relCharters.filter(bounds).distinct().count())
outString +=  'Other: %d\n' % (relCharters.exclude(roy | nonRoy | misc | will | bounds).distinct().count())

print outString

latin = Q(language__name__exact='Latin')
oe = Q(language__name__exact='Latin')
oeBounds = Q(language__name__exact='Latin with English Bounds')

for lang in Language.objects.all():
   count = relCharters.exclude(roy).filter(language__name__exact=lang.name).count()
   if (count > 0):
      print lang, count

