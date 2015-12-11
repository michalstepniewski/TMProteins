# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
import sqlite3

from PDB_FileContentsModule import ReadPDBFile

#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

class TMProtein(models.Model):

    """ represents Transmembrane Protein """

    pass

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

	for i in r:

		tmhelix = self.create(TMHelix_ID= i['ID'], TMHelix_Tilt = i['Tilt'], \
                                      TMHelix_Tilt_EC = i['Tilt_EC'], \
                                      TMHelix_Tilt_IC = i['Tilt_IC'])#, \






#		tmhelix. TMHelix_Tilt = i['Tilt']
#		tmhelix. TMHelix_Tilt_EC = i['Tilt']
#		tmhelix. TMHelix_Tilt_IC = i['Tilt']
#                tmhelix.attributes = {}


        return

    def ReadPDB (self, pdb_bath, db_path):

        """ reads PDB file to SQL database """

        ReadPDBFile (pdb_bath, db_path)	

#####################################################################################################################################################
#####################################################################################################################################################

class TMHelix(models.Model):

    """ object representing transmembrane helix """

    TMHelix_ID = models.CharField(max_length=200)
    TMHelix_Tilt = models.FloatField (null=True)
    TMHelix_Tilt_EC = models.FloatField (null=True)
    TMHelix_Tilt_IC = models.FloatField (null=True)

    objects = TMHelixManager()

    def __str__(self):

        return self.TMHelix_ID

    @classmethod
    def create(cls, ID):

        """ creates new object: instance of TMHelix class """

        tmhelix = cls(TMHelix_ID=ID, attributes={})
        return tmhelix

#####################################################################################################################################################
#####################################################################################################################################################

class Document(models.Model):

    """ object storing PDB File to be uploaded """

    docfile = models.FileField(upload_to='')
    pub_date = timezone.now ()

