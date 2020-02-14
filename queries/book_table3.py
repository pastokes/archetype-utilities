from digipal.models import *
from django.db.models import Q

usShortNames = ('Huntington', 'Folger', 'Lilly', 'Grand Haven', 'Newberry', 'Getty', 'Pierpont Morgan', 'Scheide', 'New York, PL', 'Illinois', 'Kenneth Spencer', 'Ellis')

usRepos = Repository.objects.filter(short_name__in=usShortNames).distinct()
euRepos = Repository.objects.filter(british_isles=False).exclude(short_name__in=usShortNames)
otherUKRepos = Repository.objects.filter(british_isles=True).exclude(short_name__in=('BL', 'Bodleian', 'CCCC'))

relHands = Hand.objects.filter(relevant=True).distinct()

blHands = relHands.distinct().filter(item_part__current_item__repository__short_name='BL').distinct()
bodHands = relHands.filter(item_part__current_item__repository__short_name='Bodleian').distinct()
ccccHands = relHands.filter(item_part__current_item__repository__short_name='CCCC').distinct()

otherUKHands = relHands.filter(item_part__current_item__repository__in=otherUKRepos).distinct()

usHands = relHands.filter(item_part__current_item__repository__in = usRepos).distinct()
euHands = relHands.filter(item_part__current_item__repository__in = euRepos).distinct()
nonUKHands = relHands.filter(item_part__current_item__repository__british_isles=False).distinct()


blHIs = HistoricalItem.objects.filter(itempart__hand__in=blHands).filter(itempart__current_item__repository__short_name='BL').distinct()
bodHIs = HistoricalItem.objects.filter(itempart__hand__in=bodHands).filter(itempart__current_item__repository__short_name='Bodleian').distinct()
ccccHIs = HistoricalItem.objects.filter(itempart__hand__in=ccccHands).filter(itempart__current_item__repository__short_name='CCCC').distinct()
otherUKHIs = HistoricalItem.objects.filter(itempart__hand__in=otherUKHands).filter(itempart__current_item__repository__in=otherUKRepos).distinct()
usHIs = HistoricalItem.objects.filter(itempart__hand__in=usHands).filter(itempart__current_item__repository__in=usRepos).distinct()
euHIs = HistoricalItem.objects.filter(itempart__hand__in=euHands).filter(itempart__current_item__repository__in=euRepos).distinct()
nonUKHIs = HistoricalItem.objects.filter(itempart__hand__in=nonUKHands).distinct()

allMSS = HistoricalItem.objects.filter(display_label__contains='manuscript').filter(itempart__hand__in=relHands).distinct()
allCharters = HistoricalItem.objects.filter(display_label__contains='charter').filter(itempart__hand__in=relHands).distinct()

isMS = Q(display_label__contains='manuscript')
isCharter = Q(display_label__contains='charter')

outString = ''
outString += 'BL: %d Hands, %d MSS, %d Charters\n' % (blHands.count(), blHIs.filter(isMS).distinct().count(), blHIs.filter(isCharter).distinct().count()) 
outString += 'CCCC: %d Hands, %d MSS, %d Charters\n' % (ccccHands.count(), ccccHIs.filter(isMS).distinct().count(), ccccHIs.filter(isCharter).distinct().count()) 
outString += 'Bodleian: %d Hands, %d MSS, %d Charters\n' % (bodHands.count(), bodHIs.filter(isMS).distinct().count(), bodHIs.filter(isCharter).distinct().count()) 
outString += 'Other UK: %d Hands, %d MSS, %d Charters\n' % (otherUKHands.count(), otherUKHIs.filter(isMS).distinct().count(), otherUKHIs.filter(isCharter).distinct().count()) 
outString += 'US: %d Hands, %d MSS, %d Charters\n' % (usHands.count(), usHIs.filter(isMS).distinct().count(), usHIs.filter(isCharter).distinct().count()) 
outString += 'Other: %d Hands, %d MSS, %d Charters\n' % (euHands.count(), euHIs.filter(isMS).distinct().count(), euHIs.filter(isCharter).distinct().count()) 
outString += 'Total Non-UK: %d Hands, %d MSS, %d Charters\n' % (nonUKHands.count(), nonUKHIs.filter(isMS).distinct().count(), nonUKHIs.filter(isCharter).distinct().count()) 
outString += 'Total: %d Hands, %d MSS, %d Charters\n' % (relHands.count(), allMSS.count(), allCharters.count())

print outString

allMSS.exclude(id__in=blHIs.values('id')).exclude(id__in=bodHIs.values('id')).exclude(id__in=ccccHIs.values('id')).exclude(id__in=otherUKHIs.values('id')).exclude(id__in=usHIs.values('id')).exclude(id__in=euHIs.values('id'))
