from digipal.models import *
from django.db.models import Q

# Total number of annotations
tot_annotations = 0
for a in User.objects.all():
   c = Annotation.objects.filter(author__username=a.username).count()
   if c > 0:
      print a.username, c
      tot_annotations += c

print "Total: ", tot_annotations

# Number of images which have annotations (very crude, but fine for this purpose!)
num_annotated_pages = 0
for p in Image.objects.all():
   c = Annotation.objects.filter(image__id = p.id).count()
   if c > 5:
     num_annotated_pages += 1

print "Num. Annotated Pages: ", num_annotated_pages, " out of ", Image.objects.all().count()   

# Number of scribal hands which have descriptions
HandDescription.objects.filter(source__name="digipal").count()

# List of images without annotations
for p in Image.objects.all():
   c = Annotation.objects.filter(image__id = p.id).count()
   if c < 5:
      print p.item_part.display_label + "\t" + p.locus + "\thttps://digipal-stg.cch.kcl.ac.uk/digipal/page/" + str(p.id)

