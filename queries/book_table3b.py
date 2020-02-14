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

blIPs = ItemPart.objects.filter(hand__in=blHands).filter(current_item__repository__short_name='BL').distinct()
bodIPs = ItemPart.objects.filter(hand__in=bodHands).filter(current_item__repository__short_name='Bodleian').distinct()
ccccIPs = ItemPart.objects.filter(hand__in=ccccHands).filter(current_item__repository__short_name='CCCC').distinct()
otherUKIPs = ItemPart.objects.filter(hand__in=otherUKHands).filter(current_item__repository__in=otherUKRepos).distinct()
usIPs = ItemPart.objects.filter(hand__in=usHands).filter(current_item__repository__in=usRepos).distinct()
euIPs = ItemPart.objects.filter(hand__in=euHands).filter(current_item__repository__in=euRepos).distinct()
nonUKIPs = ItemPart.objects.filter(hand__in=nonUKHands).distinct()

allMSS = HistoricalItem.objects.filter(display_label__contains='manuscript').filter(itempart__hand__in=relHands).distinct()
allCharters = HistoricalItem.objects.filter(display_label__contains='charter').filter(itempart__hand__in=relHands).distinct()
allMSIPs = ItemPart.objects.filter(historical_item__display_label__contains='manuscript').filter(hand__in=relHands).distinct()
allCharterIPs = ItemPart.objects.filter(historical_item__display_label__contains='charter').filter(hand__in=relHands).distinct()

isMS = Q(historical_item__display_label__contains='manuscript')
isCharter = Q(historical_item__display_label__contains='charter')

outString = ''
outString += 'BL: %d Hands, %d MSS, %d Charters\n' % (blHands.count(), blIPs.filter(isMS).distinct().count(), blIPs.filter(isCharter).distinct().count()) 
outString += 'CCCC: %d Hands, %d MSS, %d Charters\n' % (ccccHands.count(), ccccIPs.filter(isMS).distinct().count(), ccccIPs.filter(isCharter).distinct().count()) 
outString += 'Bodleian: %d Hands, %d MSS, %d Charters\n' % (bodHands.count(), bodIPs.filter(isMS).distinct().count(), bodIPs.filter(isCharter).distinct().count()) 
outString += 'Other UK: %d Hands, %d MSS, %d Charters\n' % (otherUKHands.count(), otherUKIPs.filter(isMS).distinct().count(), otherUKIPs.filter(isCharter).distinct().count()) 
outString += 'US: %d Hands, %d MSS, %d Charters\n' % (usHands.count(), usIPs.filter(isMS).distinct().count(), usIPs.filter(isCharter).distinct().count()) 
outString += 'Other: %d Hands, %d MSS, %d Charters\n' % (euHands.count(), euIPs.filter(isMS).distinct().count(), euIPs.filter(isCharter).distinct().count()) 
outString += 'Total: %d Hands, %d MSS, %d Charters\n' % (relHands.count(), allMSIPs.count(), allCharterIPs.count())

print outString

allMSS.exclude(id__in=blHIs.values('id')).exclude(id__in=bodHIs.values('id')).exclude(id__in=ccccHIs.values('id')).exclude(id__in=otherUKHIs.values('id')).exclude(id__in=usHIs.values('id')).exclude(id__in=euHIs.values('id'))
