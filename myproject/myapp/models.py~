# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
import sqlite3
from time import gmtime, strftime

#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

class TMHelixManager (models.Manager):

    """ manager for objects: instances of TMHelix class """

    def read_helices_from_given_db (self, db_path):

        """ reads Transmembrane Helices and their feature(s) (Tilt from SQL database """

	conn = sqlite3.connect(db_path)
	conn.row_factory = sqlite3.Row

	c = conn.cursor()
	c.execute('select * from TMs')
	r = c.fetchall()
# musze to przerobic na tworzenie z pdb, i musze sie pozbyc raw sql, moze z ReadPDB to dobry pomysl
	for i in r:

		tmhelix = self.create(TMHelix_ID= i['ID'], TMHelix_Tilt = i['Tilt'], \
                                      TMHelix_Tilt_EC = i['Tilt_EC'], \
                                      TMHelix_Tilt_IC = i['Tilt_IC'], \
                                      TMHelix_KinkAngle = i['KinkAngle'], \
                                      TMHelix_Overhang = i['Overhang'],\
                                      TMHelix_AASEQ = i['AASEQ'],\
                                       )

        return

#####################################################################################################################################################

    def ReadPDB (self, pdb_bath, db_path):

        """ reads PDB file to SQL database """

        ReadPDBFile (pdb_bath, db_path)	#

#####################################################################################################################################################
#####################################################################################################################################################

class TMProteinManager(models.Manager): #zmienic to na TMProtein

    """ object storing PDB File to be uploaded """

#####################################################################################################################################################

    def ReadPDB (self, pdb_bath, db_path):
        from PDB_FileContentsModule import ReadPDBFile

        """ reads PDB file to SQL database """

        ReadPDBFile (pdb_bath, db_path)	

#####################################################################################################################################################

def user_directory_path( filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format( filename)

#####################################################################################################################################################

def get_upload_path(instance, filename):
    name, ext = filename.split('.')
    file_path = '{name}/{name}.{ext}'.format( name=name, ext=ext) 
    return file_path

#####################################################################################################################################################

class TMProtein (models.Model): #zmienic to na TMProtein

    """ object storing PDB File to be uploaded """

    TMProtein_ID = models.CharField(max_length=200)
    tmproteinfile = models.FileField(upload_to=get_upload_path)#'uploads/%Y/%m/%d/%H/%M')
    path = models.CharField(get_upload_path, max_length=200)
    objects  = TMProteinManager ()

#####################################################################################################################################################

    def getPath (self):

        return get_upload_path
   
#####################################################################################################################################################


    def save_to_own_folder (self, ):

        self. tmproteinfile = models.FileField(upload_to=self.TMProtein_ID)

        return

#####################################################################################################################################################

    def read_helices_from_given_db (self, db_path):

        """ reads Transmembrane Helices and their feature(s) (Tilt from SQL database """

	conn = sqlite3.connect(db_path)
	conn.row_factory = sqlite3.Row

	c = conn.cursor()
	c.execute('select * from TMs')
	r = c.fetchall()
# musze to przerobic na tworzenie z pdb, i musze sie pozbyc raw sql, moze z ReadPDB to dobry pomysl
	for i in r:

		tmhelix = TMHelixModel.objects.create(TMHelix_ID= i['ID'], TMHelix_Tilt = i['Tilt'], \
                                      TMHelix_Tilt_EC = i['Tilt_EC'], \
                                      TMHelix_Tilt_IC = i['Tilt_IC'], \
                                      TMHelix_KinkAngle = i['KinkAngle'], \
                                      TMHelix_Overhang = i['Overhang'],\
                                      TMHelix_AASEQ = i['AASEQ'],\
                                      )
		self. TMHelixModel_set.add(tmhelix)

        return

#####################################################################################################################################################

    def ReadPDB (self, pdb_bath, db_path):

        """ reads PDB file to SQL database """

        from PDB_FileContentsModule import getHelicesfromPDBFile, ReadPDBFile

        for TM in getHelicesfromPDBFile (pdb_bath, db_path):

#              TMHelixModel.objects.create ()

              tmhelix = TMHelixModel.objects.create(TMHelix_ID= TM. ID, TMHelix_Tilt = TM. Tilt(), \
                                      TMHelix_Tilt_EC = TM. Tilt_EC(), \
                                      TMHelix_Tilt_IC = TM. Tilt_IC(), \
                                      TMHelix_KinkAngle = TM. KinkAngle(), \
                                      TMHelix_Overhang = TM. Overhang(),\
                                      TMHelix_AASEQ = TM. AASEQ (),\
                                      TMHelix_pdb_path = '/'.join(pdb_bath.split('/')[:-1])+'/TMs/',\
                                      )
	      self. tmhelixmodel_set.add(tmhelix)

#        ReadPDBFile (pdb_bath, db_path)	#



#####################################################################################################################################################
#####################################################################################################################################################

class TMHelixModel (models.Model):

    """ object representing transmembrane helix """

    TMHelix_ID = models.CharField(max_length=200)
    TMHelix_AASEQ = models.CharField(max_length=200)
    TMHelix_Tilt = models.FloatField (null=True)
    TMHelix_Tilt_EC = models.FloatField (null=True)
    TMHelix_Tilt_IC = models.FloatField (null=True)
    TMHelix_KinkAngle = models.FloatField (null=True)
    TMHelix_Overhang = models.FloatField (null=True)
    TMHelix_pdb_path = models.CharField(max_length=200)

    TMProtein = models.ForeignKey(TMProtein, on_delete=models.CASCADE, null=True)

    objects = TMHelixManager()

#####################################################################################################################################################

    def __str__(self):

        return self.TMHelix_ID

#####################################################################################################################################################

    @classmethod
    def create(cls, ID):

        """ creates new object: instance of TMHelix class """

        tmhelix = cls(TMHelix_ID=ID, attributes={})
        return tmhelix

####################################################################################################################################################
####################################################################################################################################################

#class UserFolder(models.Model):
#    name = models.CharField(null=True)
#    parent = models.ForeignKey("Folder", null=True,)  # self-referential

####################################################################################################################################################
####################################################################################################################################################

#class UserImage(models.Model):
#    name = models.CharField(null=True)
#    image = models.ImageField(null=True)
#    # Optional, null folder could just mean it resides in the base user folder
#    folder = models.ForeignKey(UserFolder, null=True,)
