# encoding: utf-8
from django.db import models
from myapp.models import   TMProtein
print TMProtein
#import myproject.myapp.models  as sthg
import myapp as sthg
vars(sthg)
#import myapp.models as sthg

#from myapp.models import TMProtein
#import myproject.myapp.models as sthg
#print vars(sthg)
#quit()
class Picture(models.Model):
    """This is a small demo using just two fields. The slug field is really not
    necessary, but makes the code simpler. ImageField depends on PIL or
    pillow (where Pillow is easily installable in a virtualenv. If you have
    problems installing pillow, use a more generic FileField instead.

    """
    file = models.FileField(upload_to="PDBs")
    slug = models.SlugField(max_length=50, blank=True)

    def __unicode__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Picture, self).save(*args, **kwargs)
        
#        from PDB_FileContentsModule import getHelicesfromPDBFile, ReadPDBFile, GetAtomsFromPDBFile
#        ReadPDB (self, pdb_path, db_path)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)


