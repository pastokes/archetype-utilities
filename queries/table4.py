from digipal.models import *
from django.db.models import Q

relHands = Hand.objects.filter(relevant=True).distinct()
relIPs = ItemPart.objects.filter(hand__in=relHands).distinct()
relHIs = HistoricalItem.objects.filter(itempart__hand__in=relHands).filter(display_label__contains='manuscript').distinct()
relCollations = Collation.objects.filter(historical_item__itempart__hand__in=relHands).distinct()

frags = relCollations.filter(fragment=True).distinct()
complete = relCollations.filter(fragment=False).distinct()

q1 = Q(leaves__exact=1)
q2 = Q(leaves__exact=2)
q3_99 = Q(leaves__gte=3) & Q(leaves__lte=99)
q100_199 = Q(leaves__gte=100) & Q(leaves__lte=199)
q200_299 = Q(leaves__gte=200) & Q(leaves__lte=299)
q300 = Q(leaves__gte=300)

outString = ''

outString += '1: %d %d %d\n' % (frags.filter(q1).count(), complete.filter(q1).count(), relCollations.filter(q1).count())
outString += '2: %d %d %d\n' % (frags.filter(q2).count(), complete.filter(q2).count(), relCollations.filter(q2).count())
outString += '3-99: %d %d %d\n' % (frags.filter(q3_99).count(), complete.filter(q3_99).count(), relCollations.filter(q3_99).count())
outString += '100-199: %d %d %d\n' % (frags.filter(q100_199).count(), complete.filter(q100_199).count(), relCollations.filter(q100_199).count())
outString += '200-299: %d %d %d\n' % (frags.filter(q200_299).count(), complete.filter(q200_299).count(), relCollations.filter(q200_299).count())
outString += '300+: %d %d %d\n' % (frags.filter(q300).count(), complete.filter(q300).count(), relCollations.filter(q300).count())

print outString

# Get list of 'top 20' longest manuscripts
for hi in HistoricalItem.objects.filter(collation__leaves__gte=1).filter(itempart__hand__relevant=True).distinct().order_by('-collation__leaves')[0:20]:
    hi, Category.objects.filter(historicalitem__id=hi.id), Collation.objects.get(historical_item__id=hi.id).leaves

# Get list of shortest non-fragmentary MSS. However, this doesn't seem to work, as it looks like there's a problem with the representation of Collation objects for HIs with multiple IPs. See https://jira.dighum.kcl.ac.uk/browse/DIGIPAL-107
complete.filter(Q(leaves__lt=100)).count()

# List all MS HistoricalItems with no Collation record
relHIs.exclude(collation__leaves__gte=1)
