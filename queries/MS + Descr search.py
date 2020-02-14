from digital.models import *

searchstring = 'scribble'

his = HistoricalItem.objects.all().filter(description__description__icontains=searchstring)

print "<html>" + \
         "<head>" + \
           "<title>Search results for '" + searchstring + "'</title>" + \
         "</head>" + \
         "<body>" + \
            "<p>Search for '"+ searchstring + "' gave ", his.count(), "results.</p>"

for h in his:
  for ip in h.item_parts.all():
    print "<h2>", ip.current_item, "</h2>"
  print Description.objects.all().filter(historical_item=h).filter(description__icontains=searchstring)[0].description.replace(searchstring, "<strong>" + searchstring + "</strong>")

print "  </body>" + \
         "</html>"


