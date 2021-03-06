# archetype-utilities

Collection of tools to help working with the [Archetype framework](https://github.com/kcl-ddh/digipal/).

Most of these are very rough and ready, but they could conceivably be developed and integrated as Django commands in future:

* **IIIFHarvester**: Attempts to download all images associated with a given manifest, with given parameters for scale, quality etc.
  Can be used with the image bulk-edit functions in Archetype to import images more quickly.
* **import_charset**: Attempts to load in a new set of Ontographs, Characters, Allographs, and Components from a JSON file and add these into the Archetype database. Must be run from within the Archetype Django environment by using `manage.py shell`
* **alphabet_grc.json**: A basic sample file of the Greek alphabet, as a demonstration for use with import_charset_django
* **queries**: These are scripts that query the [DigiPal instance](http://digipal.eu) of Archetype. They're included as demonstrations of the [Django QuerySet API](https://docs.djangoproject.com/en/3.0/ref/models/querysets/) for advanced querying. Most of these queries were written to generate the tables in Stokes, _English Vernacular Minuscule from Æthelred to Cnut_ (Cambridge, 2014).

**Use all these tools with caution: they have not been carefully tested and most if not all have known issues. Be sure to back up your Archetype instance before using any of them, as they could easily corrupt or overwrite your data.**

Peter A. Stokes, École Pratique des Hautes Études, Université PSL
