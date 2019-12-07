# -*- coding: utf-8 -*-
"""
A rough script to create new Ontograph, Character, Allograph and Component
records from a JSON file as input.

TODO: The script is hacked together pretty quickly and needs a lot of tidying up
TODO: It's very insensitive to problems in the JSON; at a minimum it should 
      allow for optional arguments to be ommitted.
TODO: At the moment, if it finds a pre-existing record with the same name then
      it doesn't change that record but does use it to link all further objects
      down the hierarchy. This is not necessarily desirable and needs further
      consideration (perhaps even with a user flag to select behaviour).
TODO: Add proper help
TODO: Add proper command line flags
TODO: Integrate into Archetype as a Django command 

Created on Sat Dec  7 15:31:55 2019

@author: peterstokes
"""

import json
import requests
from digipal.models import *

fname = "alphabet_grc.json"
path = "digipal_project/customisations/commands/"
json_url = "https://raw.githubusercontent.com/pastokes/archetype-utilities/master/alphabet_grc.json"
ENCODING = "utf-8"
LOCAL_FILE = True

if LOCAL_FILE:
    with open(path+fname, "r") as infile:
        alpha = json.loads(infile.read().decode(ENCODING))
else:
    conn = requests.get(json_url).encoding(ENCODING)
    alpha = conn.json()
    



# TODO: Need to check for missing attributes in JSON file
sort_order = 0
for o in alpha["Ontographs"]:
    try:
        # TODO: The logic here is backwards, though: the except block is in fact
        # the normal, expected behaviour.
        new_ont = Ontograph.objects.get(name=o["name"])
        print("Warning: Ontograph " + o["name"].encode(ENCODING) + " already exists")
        pass
    except Ontograph.DoesNotExist:
        new_ont = Ontograph(name=o["name"])
        new_ont.ontograph_type, _ = OntographType.objects.get_or_create(name=o["type"])
        new_ont.sort_order = sort_order
        sort_order += 10
        new_ont.save()
    
    for c in o["Characters"]:
        try:
            new_c = Character.objects.get(name=c["name"])
            print("Warning: Character " + c["name"].encode(ENCODING) + " already exists")
        except Character.DoesNotExist:
            new_c = Character(name=c["name"])
            new_c.form, _ = CharacterForm.objects.get_or_create(name=c["form"])
            new_c.unicode_point = c["unicode_point"]
            new_c.ontograph = new_ont
            new_c.save()
        
        for a in c["Allographs"]:
            # Want to create multiple allogrpahs even of the same name
            #new_a = get_or_create(Allograph, a["name"])
            try:
                new_a = Allograph.objects.get(name=a["name"], character=new_c)
                print("Warning: Allograph " + a["name"].encode(ENCODING) + " " + new_c.encode(ENCODING) + " already exists")
            except Allograph.DoesNotExist:
                new_a = Allograph(name=a["name"])
                new_a.character = new_c
                new_a.save()
                
            # Create new components
            try:
                for comp in a["Components"]:
                    new_comp, _ = Component.objects.get_or_create(name=comp["name"])
                    AllographComponent.objects.get_or_create(allograph=new_a, component=new_comp)
            except KeyError:
                print("Warning: No Components found for Allograph " + a["name"].encode(ENCODING) + new_c.name.encode(ENCODING))
                pass
            
