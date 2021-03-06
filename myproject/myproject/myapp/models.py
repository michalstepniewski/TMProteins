# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.utils import timezone
import sqlite3
from time import gmtime, strftime
import matplotlib
import PlotToolsModule; from PlotToolsModule import HistogramPlot
import numpy as np

from GeometricalClassesModule import SetOfVectors, Vector, SetOfPoints, Point

class TMHelixManager (models.Manager):

    """ manager for objects: instances of TMHelix class """

#####################################################################################################################################################

    def single_helix_stats (self):

        """ calculates TM Helix Stats and plots histograms to .png """

        for Value in ['TMHelix_Tilt', 'TMHelix_Tilt_EC', 'TMHelix_Tilt_IC', 'TMHelix_KinkAngle', 'TMHelix_Overhang']:
#            print self. values_list('TMHelix_Tilt', flat=True)

            HistogramPlot(np.array(self. values_list(Value, flat=True)), 'myproject/myapp/static/myapp/static/Stats/SingleHelix/'+Value )
        #zrobic jakies dict coby robilo ranges, uzaleznialo np od zakresu albo od czegos

        return

#####################################################################################################################################################

    def extracthelixpairs (self):

        """ extracts helix pairs """

        # to mozna zrobic na zbiorze helis; sprawdzic w django jak wyselekcjonowac zestaw helis z 1go bialka
        # i zrobic z nich N_TMs_Set

        return

#####################################################################################################################################################

    def extracthelixtriplets (self):

        """ extracts helix triplets """

        # to mozna zrobic na zbiorze helis; sprawdzic w django jak wyselekcjonowac zestaw helis z 1go bialka
        # i zrobic z nich N_TMs_Set

        return

#####################################################################################################################################################

    def read_helices_from_given_db (self, db_path):

        """ reads Transmembrane Helices and their feature(s) (Tilt from SQL database """

	conn = sqlite3.connect(db_path)
	conn.row_factory = sqlite3.Row

	c = conn.cursor()
	c.execute('select * from TMs')
	r = c.fetchall()
# musze to przerobic na tworzenie z pdb, i musze sie pozbyc raw sql, moze z  to dobry pomysl
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

    def ReadPDB (self, pdb_path, db_path):

        """ reads PDB file to SQL database """

        ReadPDBFile (pdb_path, db_path)	#

class TMProteinManager(models.Manager): #zmienic to na TMProtein

    """ object storing PDB File to be uploaded """

#####################################################################################################################################################

    def ExtractConsecutiveHelixPairs (self):
    
        [tmprotein. ExtractConsecutiveHelixPairs() for tmprotein in self.all()]
        
        return

#####################################################################################################################################################

    def ExtractConsecutiveHelixTriplets (self):
    
        [tmprotein. ExtractConsecutiveHelixTriplets() for tmprotein in self.all()]
        
        return

#####################################################################################################################################################

    def ReadPDB (self, pdb_path, db_path):
        from PDB_FileContentsModule import ReadPDBFile

        """ reads PDB file to SQL database """

        ReadPDBFile (pdb_path, db_path)	


def user_directory_path( filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format( filename)

def get_upload_path(instance, filename):
    name, ext = filename.split('.')
    file_path = '{name}/{name}.{ext}'.format( name=name, ext=ext) 
    return file_path

class TMProtein (models.Model): #zmienic to na TMProtein

    """ object storing PDB File to be uploaded """

    TMProtein_ID = models.CharField(max_length=200)
    tmproteinfile = models.FileField(upload_to=get_upload_path)#'uploads/%Y/%m/%d/%H/%M')
    path = models.CharField(get_upload_path, max_length=200)
    atoms = models.TextField(null=True,default="fejslik")
    objects  = TMProteinManager ()

    def getPath (self):

        return get_upload_path

    def save_to_own_folder (self, ):

        self. tmproteinfile = models.FileField(upload_to=self.TMProtein_ID)

        return


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


    def ReadPDB (self, pdb_path, db_path):

        """ reads PDB file to extract TM Helices """

        from PDB_FileContentsModule import getHelicesfromPDBFile, ReadPDBFile, GetAtomsFromPDBFile

        self. atoms = GetAtomsFromPDBFile (pdb_path)
        print self.atoms
#        for AtomI in self.Atoms:
#            self.atom_set.add(AtomI)

#        print self.Atoms; quit ()
#        print self.pk; 
#        self.atom_set.add(atom)

        for TM in getHelicesfromPDBFile (pdb_path):

#              TMHelixModel.objects.create ()

            AtomsI = ''
            

            tmhelix = TMHelixModel.objects.create(TMHelix_ID= TM. ID, TMHelix_Tilt = TM. Tilt(), \
                                      TMHelix_Tilt_EC = TM. Tilt_EC(), \
                                      TMHelix_Tilt_IC = TM. Tilt_IC(), \
                                      TMHelix_KinkAngle = TM. KinkAngle(), \
                                      TMHelix_Overhang = TM. Overhang(),\
                                      TMHelix_AASEQ = TM. AASEQ (),\
                                      TMHelix_pdb_path = '/'.join(pdb_path.split('/')[:-1])+'/TMs/',
                                      Atoms = AtomsI 
                                      )

            for ResidueI in TM.Content:
                for AtomI in ResidueI.Content:
                    #  7 - 11        Integer         Atom serial number
                    
                    atom = Atom.objects.create(Atom_ID = AtomI.s[6:11],  Text = AtomI.s)
                    
#                    self.atom_set.add(atom)
                    tmhelix.atom_set.add(atom)
                    print 'added atom to tmhelix atom set'
                    print datetime.datetime.now()
            
#            print tmhelix.atom_set.show()
            
#                    AtomsI = AtomsI + AtomI.s + '\n'

            tmhelix.MainAxis_X, tmhelix.MainAxis_Y, tmhelix.MainAxis_Z = TM. MainAxis () 

            tmhelix.ECAxis_X, tmhelix.ECAxis_Y, tmhelix.ECAxis_Z = TM. ExtractSlice([-2.0,12.0]). MainAxis ( )

            tmhelix.ICAxis_X, tmhelix.ICAxis_Y, tmhelix.ICAxis_Z = TM. ExtractSlice([-12.0,2.0]). MainAxis ( )
    
            [tmhelix.MC_EC_X, tmhelix.MC_EC_Y, tmhelix.MC_EC_Z],\
            [tmhelix.MC_MM_X, tmhelix.MC_MM_Y, tmhelix.MC_MM_Z],\
            [tmhelix.MC_IC_X, tmhelix.MC_IC_Y, tmhelix.MC_IC_Z]  =  TM. ThinSlicesCOMs ( )  
                            
            self. tmhelixmodel_set.add(tmhelix)

#        ReadPDBFile (pdb_path, db_path)	#


    def ExtractConsecutiveHelixPairs (self):
        
        NoHelices = self. tmhelixmodel_set.count()
        
        if NoHelices >= 2:
        
            for N in range(NoHelices - 1):
               
                tmhelixpair = TMHelixPair.objects.create()
#                print N; print N+1;
#                print self. tmhelixmodel_set.all().values_list('id', flat=True)
                
                tmhelixpair.tmhelixmodel_set.add(self. tmhelixmodel_set.get(TMHelix_ID=str(N+1)))   
                tmhelixpair.tmhelixmodel_set.add(self. tmhelixmodel_set.get(TMHelix_ID=str(N+2)))
                tmhelixpair.getCrossingAngle ()              

                self.tmhelixpair_set.add(tmhelixpair)  
                
                print  'Count '+str(tmhelixpair.tmhelixmodel_set.count())        
                #sprawdzic czy dobrze bedzie
        return

    def ExtractConsecutiveHelixTriplets (self):
        
        NoHelices = self. tmhelixmodel_set.count()
        
        if NoHelices >= 3:
        
            for N in range(NoHelices - 2):
               
                tmhelixtriplet = TMHelixTriplet.objects.create()

                
                tmhelixtriplet.tmhelixmodel_set.add(self. tmhelixmodel_set.get(TMHelix_ID=str(N+1)))   
                tmhelixtriplet.tmhelixmodel_set.add(self. tmhelixmodel_set.get(TMHelix_ID=str(N+2)))              
                tmhelixtriplet.tmhelixmodel_set.add(self. tmhelixmodel_set.get(TMHelix_ID=str(N+3)))              

                tmhelixtriplet. getPhi ()
                
                self.tmhelixtriplet_set.add(tmhelixtriplet)  


        return

#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

class TMHelixPairManager (models.Manager):

    """ manager for objects: TM Helix Pair """



    def helix_pair_stats (self):

        """ calculates TM Helix Pair Stats and plots histograms to .png """

        for Value in ['CrossingAngle','CrossingAngleEC','CrossingAngleIC']:

            HistogramPlot(np.array(self. values_list(Value, flat=True)), 'myproject/myapp/static/myapp/static/Stats/HelixPair/'+Value )
        #zrobic jakies dict coby robilo ranges, uzaleznialo np od zakresu albo od czegos

        return



#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

class TMHelixTripletManager (models.Manager):

    """ manager for objects: TM Helix Triplet """


    def helix_triplet_stats (self):

        """ calculates TM Helix Triplet Stats and plots histograms to .png """

        for Value in ['Phi']:

            HistogramPlot(np.array(self. values_list(Value, flat=True)), 'myproject/myapp/static/myapp/static/Stats/HelixTriplet/'+Value )
        #zrobic jakies dict coby robilo ranges, uzaleznialo np od zakresu albo od czegos

        return





class TMHelixPair (models.Model):
    
    """ object storing TM Helix Pair """
    
    objects = TMHelixPairManager ()
    CrossingAngle = models.FloatField (null=True)
    CrossingAngleEC = models.FloatField (null=True)
    CrossingAngleIC = models.FloatField (null=True)
    TMProtein = models.ForeignKey(TMProtein, on_delete=models.CASCADE, null=True)

#####################################################################################################################################################

    def Interacting (self,VdWContactZRange =[-8.0, 8.0]):
        
        """ returns True if Two Helices Are Interacting """
        
        pass
        
        return

#####################################################################################################################################################

    def getCrossingAngle (self):
        
        """ calculates Crossing Angle """
                            
        Axes = [[tmhelix.MainAxis_X,tmhelix.MainAxis_Y,tmhelix.MainAxis_Z] for tmhelix in self.tmhelixmodel_set.all ()]
        
        self.CrossingAngle = SetOfVectors([Vector(Axes[0]), Vector(Axes[1]) ]) .AngleDEG ()
        Axes = [[tmhelix.ECAxis_X,tmhelix.ECAxis_Y,tmhelix.ECAxis_Z] for tmhelix in self.tmhelixmodel_set.all ()]
        self.CrossingAngleEC = SetOfVectors([Vector(Axes[0]), Vector(Axes[1]) ]) .AngleDEG ()
        Axes = [[tmhelix.ICAxis_X,tmhelix.ICAxis_Y,tmhelix.ICAxis_Z] for tmhelix in self.tmhelixmodel_set.all ()]
        self.CrossingAngleIC = SetOfVectors([Vector(Axes[0]), Vector(Axes[1]) ]) .AngleDEG ()
        
        return

#####################################################################################################################################################

    def getCrossingAngleEC (self):

        """ calculates Crossing Angle in the Extracellular Leaflet """
        
        Axes = []
                            
        Axes = [[tmhelix.ECAxis_X,tmhelix.ECAxis_Y,tmhelix.ECAxis_Z] for tmhelix in self.tmhelixmodel_set]
        
        CrossingAngleEC = SetOfVectors([Axes[0], Axes[1] ]) .AngleDEG ()
        
        return

#####################################################################################################################################################

    def getCrossingAngleIC (self):

        """ calculates Crossing Angle in the Intracellular Leaflet """
        
        Axes = []
                            
        Axes = [[tmhelix.ICAxis_X,tmhelix.ICAxis_Y,tmhelix.ICAxis_Z] for tmhelix in self.tmhelixmodel_set]
        
        CrossingAngleIC = SetOfVectors([Axes[0], Axes[1] ]) .AngleDEG ()
        
        return



class TMHelixTriplet (models.Model):
    
    """ object storing TM Helix Pair """
    objects = TMHelixTripletManager ()
    Phi = models.FloatField (null=True)
    TMProtein = models.ForeignKey(TMProtein, on_delete=models.CASCADE, null=True)

#####################################################################################################################################################
    
    def getPhi (self):
        
        helices = self.tmhelixmodel_set.all ()
            
        P1 = [helices[0].MC_MM_X,helices[0].MC_MM_Y,helices[0].MC_MM_Z]
        P2 = [helices[1].MC_MM_X,helices[1].MC_MM_Y,helices[1].MC_MM_Z]
        P3 = [helices[2].MC_MM_X,helices[2].MC_MM_Y,helices[2].MC_MM_Z]
        Vec1 = SetOfPoints([P1,P2]).Vector()
        Vec2 = SetOfPoints([P1,P3]).Vector()
        self.Phi = SetOfVectors([Vec1, Vec2 ]) .AngleDEG ()

#####################################################################################################################################################

    def Interacting (self,VdWContactZRange =[-8.0, 8.0]):
        
        """ returns True if Two Helices Are Interacting """
        
        pass
        
        return

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
    Atoms = models.TextField(null=True,default="fejslik")

    TMProtein = models.ForeignKey(TMProtein, on_delete=models.CASCADE, null=True)
    TMHelixPair = models.ManyToManyField(TMHelixPair)
    TMHelixTriplet = models.ManyToManyField(TMHelixTriplet)

    MainAxis_X = models.FloatField (null=True)
    MainAxis_Y = models.FloatField (null=True)
    MainAxis_Z = models.FloatField (null=True)

    ECAxis_X = models.FloatField (null=True)
    ECAxis_Y = models.FloatField (null=True)
    ECAxis_Z = models.FloatField (null=True)

    ICAxis_X = models.FloatField (null=True)
    ICAxis_Y = models.FloatField (null=True)
    ICAxis_Z = models.FloatField (null=True)
    
    MC_EC_X = models.FloatField (null=True)
    MC_EC_Y = models.FloatField (null=True)
    MC_EC_Z = models.FloatField (null=True)
    
    MC_MM_X = models.FloatField (null=True)
    MC_MM_Y = models.FloatField (null=True)
    MC_MM_Z = models.FloatField (null=True)
    
    MC_IC_X = models.FloatField (null=True)
    MC_IC_Y = models.FloatField (null=True)
    MC_IC_Z = models.FloatField (null=True)
            
    objects = TMHelixManager()


    def __str__(self):

        return self.TMHelix_ID


    @classmethod
    def create(cls, ID):

        """ creates new object: instance of TMHelix class """

        tmhelix = cls(TMHelix_ID=ID, attributes={})
        return tmhelix


#class UserFolder(models.Model):
#    name = models.CharField(null=True)
#    parent = models.ForeignKey("Folder", null=True,)  # self-referential


#class UserImage(models.Model):
#    name = models.CharField(null=True)
#    image = models.ImageField(null=True)
#    # Optional, null folder could just mean it resides in the base user folder
#    folder = models.ForeignKey(UserFolder, null=True,)

class AtomManager (models.Manager):

    """ manager for Atom class objects """
    
    def show(self):        
        
        Text = ''
        
        for AtomI in self.all():
            
             print AtomI.Text
             Text = Text+AtomI.Text+'\n'
        
        return Text

class   Atom (models.Model):

    """ object representing AtomLine """
    
    TMProtein = models.ForeignKey(TMProtein, on_delete=models.CASCADE, null=True) #znalezc szybsza alternatywe
    TMHelixModel = models.ForeignKey(TMHelixModel, on_delete=models.CASCADE, null=True)
    Text = models.CharField(max_length=200)
    objects = AtomManager()
    Atom_ID = models.CharField(max_length=200)

    @classmethod
    def create(cls, ID):

        """ creates new object: instance of TMHelix class """

        atom = cls(Atom_ID=ID, attributes={})
        return atom

class ResidueManager (models.Manager):
    
    """ object managing Amino Acid Residues """
    
    pass

class Residue (models.Model):
    
    """ object representing Amino Acid Residue """
    
    objects = ResidueManager()
    
    pass