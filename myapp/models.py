# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
import sqlite3
from time import gmtime, strftime
import matplotlib
import PlotToolsModule; from PlotToolsModule import HistogramPlot
import numpy as np
from django.db import transaction
import scipy
import scipy.stats
from scipy.cluster.vq import *
from scipy.stats import relfreq
import math
from django.db.models import Sum, Avg
from GeometricalClassesModule import SetOfVectors, Vector, SetOfPoints, Point
from django.db.models import Avg, Max, Min
import match
from match import rmsd
from models1 import *
import openpyxl

#print 'importing Picture'
#from fileupload.models import Picture
#print Picture
#print 'imported Picture'

def kMedoids(D, k, tmax=100):
    # determine dimensions of distance matrix D
    m, n = D.shape
    print D

    # randomly initialize an array of k medoid indices
    M = np.sort(np.random.choice(n, k))

    # create a copy of the array of medoid indices
    Mnew = np.copy(M)

    # initialize a dictionary to represent clusters
    C = {}

    for t in xrange(tmax):
        # determine clusters, i.e. arrays of data indices
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]
            

        # update cluster medoids
        for kappa in range(k):
            J = np.mean(D[np.ix_(C[kappa],C[kappa])],axis=1)
            print J
            j = np.argmin(J)
            Mnew[kappa] = C[kappa][j]
        np.sort(Mnew)

        # check for convergence
        if np.array_equal(M, Mnew):
            break

        M = np.copy(Mnew)
    else:
        # final update of cluster memberships
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]

    # return results
    return M, C

def to_csv(array,path):
    
    f = open(path,'w')
    
    for row in array:
        
        f.write(','.join([str(item) for item in row])+'\n')
    
    f.flush()
    f.close()
    
    return

def from_csv(path):
    
    array = []
    
    f=open(path,'r')
    
    for row in f.readlines():
        
        array.append([float(item) for item in row.split(',')])
                       
    return np.array(array)

def getRMSDMatrix(crdssI):
#ta matryca pewnie bedzie za dluga na JSONA a i tak musi wejsc do pamieci

    length = len(crdssI)
    
    print length
        
    RMSDMatrixI = np.zeros((length,length))
        
    for N1 in range(length):
        
        print N1
        for N2 in range(N1+1,length):
            RMSDI = RMSD(crdssI[N1],crdssI[N2])
            
            RMSDMatrixI.itemset((N1,N2),(RMSDI))
            RMSDMatrixI.itemset((N2,N1),(RMSDI))       
        
         
    to_csv(RMSDMatrixI,'media/RMSDMatrix.csv')

    return RMSDMatrixI

def RMSD (objs1,objs2):
    
    
    
    return rmsd (np.array(objs1), np.array(objs2))

#import match.py

def probability (Value, Distribution):
    
    
    return

def contact(obj1,obj2):
    
    X = obj1.X - obj2.X
    
    if -5.0 < X < 5.0:
        Y = obj1.Y -obj2.Y
        if -5.0 < Y < 5.0:
            if (X**2 + Y**2 + (obj1.Z-obj2.Z)**2) < (obj1.VdWRadius+obj2.VdWRadius+0.5)**2:
                return True

    return False
            
def contact_m(objs1,objs2):
    
    q1 = objs1.aggregate(Min('X'),Max('X'),Min('Y'),Max('Y'))
    q2 = objs2.aggregate(Min('X'),Max('X'),Min('Y'),Max('Y'))

    if ((max(q1['X__min'],q2['X__min']) - min(q1['X__max'],q2['X__max']) <= 5.0) and \
       (max(q1['Y__min'],q2['Y__min']) - min(q1['Y__max'],q2['Y__max']) <= 5.0)):

       for obj1 in objs1:
           for obj2 in objs2:
               if contact(obj1,obj2):
                   return True

#trzeba to pozmieniac zeby zwracalo contact amino acids
# pousuwac w shellu rzeczy z bazy danych
# 

    return False


def distance(obj1, obj2):

    return  ((obj1.X-obj2.X)**2\
           + (obj1.Y-obj2.Y)**2\
           + (obj1.Z-obj2.Z)**2)**0.5



def get_upload_path(instance, filename):
    name, ext = filename.split('.')
    file_path = '{name}/{name}.{ext}'.format( name=name, ext=ext) 
    return file_path

class Clustering (models.Model):
    
        idx = models.FloatField(null=True)
        no_cluster = models.CharField(max_length=10000,null=True)
        distance = models.CharField(max_length=10000,null=True)

class Cluster (models.Model):
    
        pass
#        idx = models.FloatField(null=True)
#        no_cluster = models.CharField(max_length=10000,null=True)
#        distance = models.CharField(max_length=10000,null=True)    


class XLSFile(models.Model):
    
    xlsfile = models.FileField(upload_to=get_upload_path)#'uploads/%Y/%m/%d/%H/%M')
    path = models.CharField(get_upload_path, max_length=200)
    TMProtein_ID = models.CharField(max_length=200)


    def Read(self, xls_path, database_id):
        
        wb = openpyxl.load_workbook(xls_path)
           
#        first_sheet = book.get_sheet_by_index(0)
              
        from xml_parser.models import DatabaseModel,structure
           
        sheet = wb.get_sheet_by_name('Sheet1')
        
#        Species = 
        Resolutions = sheet.columns[4]
        PDBCodes = sheet.columns[5] #F
        Chains = sheet.columns[6] #G
        
        DatabaseModelI = DatabaseModel.objects.get(pk=database_id)
        
        with transaction.atomic():
         
         for row in range(2, sheet.max_row):
            print Resolutions[row].value
            print PDBCodes[row].value

            structureI = structure.objects.create(
            pdbCode = PDBCodes[row].value, \
            resolution = Resolutions[row].value, \
            Chain = Chains[row].value)
            DatabaseModelI.structure_set.add(structureI)
#        quit()    
        return

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
    
    
    def ReadXLS(self, XLSFile):
        
        print XLSFile
        
        quit()
        
                

#####################################################################################################################################################

    def ExtractConsecutiveHelixPairs (self):
    
        [tmprotein. ExtractConsecutiveHelixPairs() for tmprotein in self.all()]
        
        return


#####################################################################################################################################################

    def ReadPDB (self, pdb_path, db_path):
        from PDB_FileContentsModule import ReadPDBFile

        """ reads PDB file to SQL database """

        ReadPDBFile (pdb_path, db_path)	


class TMProteinQuerySet(models.QuerySet):

#####################################################################################################################################################

    def ExtractConsecutiveHelixTriplets (self):
    
        [tmprotein. ExtractConsecutiveHelixTriplets() for tmprotein in self.all()]
        
        return

    def ExtractInteractingHelixTriplets (self):
    
        [tmprotein. ExtractInteractingHelixTriplets() for tmprotein in self.all()]
        
        return

#####################################################################################################################################################

    def ExtractInteractingHelixPairs (self):
    
        [tmprotein. ExtractInteractingHelixPairs() for tmprotein in self.all()]
        
        return


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
    tmproteinfile = models.FileField(upload_to=get_upload_path,null=True)#'uploads/%Y/%m/%d/%H/%M')
    path = models.CharField(get_upload_path, max_length=200)
    Atoms = models.TextField(null=True,default="fejslik")
    objects  = TMProteinManager ().from_queryset(TMProteinQuerySet)()
    Score=models.FloatField(null=True)
    Set = models.CharField(max_length=10,null=True) #'Reference' or 'Test'
    from xml_parser.models import structure
    structure = models.ForeignKey(structure, on_delete=models.CASCADE, null=True)
    
    def getPath (self):

        return get_upload_path
    
    def getScore(self):
        for tmhelixtripleti in self.tmhelixtriplet_set.all():
            tmhelixtripleti.getScore()
        self.Score=self.tmhelixtriplet_set.aggregate(Avg('Score'))['Score__avg']
#        print self.Score; #quit()
        self.save()
#        quit()
        return self.Score
            

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


    def ReadPDB (self, pdb_path):#, db_path):

        """ reads PDB file to extract TM Helices """

        from PDB_FileContentsModule import getHelicesfromPDBFile, ReadPDBFile, GetAtomsFromPDBFile

        self. Atoms = GetAtomsFromPDBFile (pdb_path)
#        self.atom_set.add(atom)
        with transaction.atomic():
         for TM in getHelicesfromPDBFile (pdb_path):
           if len(TM.Content)>0: 
            from SetOfAtomsModule import Parametry   
            print Parametry. BordersOfThinSlices 

#              TMHelixModel.objects.create ()

            AtomsI = ''
            try: 
             print TM. ThinSlicesCOMs ( );
             [MC_EC_X, MC_EC_Y, MC_EC_Z],\
             [MC_MM_X, MC_MM_Y, MC_MM_Z],\
             [MC_IC_X, MC_IC_Y, MC_IC_Z]  =  TM. ThinSlicesCOMs ( )
#            print tmhelix.MC_EC_X
            except ZeroDivisionError:
             break
            tmhelix = TMHelixModel.objects.create(TMHelix_ID= TM. ID, TMHelix_Tilt = TM. Tilt(), \
                                      TMHelix_Tilt_EC = TM. Tilt_EC(), \
                                      TMHelix_Tilt_IC = TM. Tilt_IC(), \
                                      TMHelix_KinkAngle = TM. KinkAngle(), \
                                      TMHelix_Overhang = TM. Overhang(),\
                                      TMHelix_AASEQ = TM. AASEQ (),\
                                      TMHelix_pdb_path = '/'.join(pdb_path.split('/')[:-1])+'/TMs/',
                                      Atoms = AtomsI,
                                      MC_EC_X = MC_EC_X,
                                      MC_EC_Y = MC_EC_Y,
                                      MC_EC_Z = MC_EC_Z,
                                      MC_MM_X = MC_MM_X,
                                      MC_MM_Y = MC_MM_Y,
                                      MC_MM_Z = MC_MM_Z,
                                      MC_IC_X = MC_IC_X,
                                      MC_IC_Y = MC_IC_Y,
                                      MC_IC_Z = MC_IC_Z
                                      )
            
            for ResidueI in TM.Content:
                ResidueModelI = Residue.objects.create(Residue_ID=ResidueI.Content[0].s[6:11], AAThreeLetter = ResidueI.Content[0].AAThreeLetter )
                
                for AtomI in ResidueI.Content:
                    #  7 - 11        Integer         Atom serial number
                    
                        atom = Atom.objects.create(Atom_ID = AtomI.s[6:11],  Text = AtomI.s)
#moze by to dac do create
                        atom.X = AtomI.X
                        atom.Y = AtomI.Y
                        atom.Z = AtomI.Z
                        atom.Mass = AtomI.Mass()
                        atom.VdWRadius = AtomI.VdWRadius()
                        atom.AAThreeLetter = AtomI.AAThreeLetter
                        atom.save()
                        self.atom_set.add(atom)
                        tmhelix.atom_set.add(atom)
                        ResidueModelI.atom_set.add(atom)
                        
                ResidueModelI.AAThreeLetter = ResidueI.Content[0].AAThreeLetter
#                
                ResidueModelI.CenterOfMass()

                ResidueModelI.save()
                tmhelix.residue_set.add(ResidueModelI)
#                print ResidueModelI.Z
#                print ResidueModelI.AAThreeLetter
#                print Residue.objects.all().values_list('AAThreeLetter')

#                quit()
            
           # print tmhelix.atom_set.show()
                

#            quit()    
            
#                    AtomsI = AtomsI + AtomI.s + '\n'

            tmhelix.MainAxis_X, tmhelix.MainAxis_Y, tmhelix.MainAxis_Z = TM. MainAxis () 

            tmhelix.ECAxis_X, tmhelix.ECAxis_Y, tmhelix.ECAxis_Z = TM. ExtractSlice([-2.0,12.0]). MainAxis ( )

            tmhelix.ICAxis_X, tmhelix.ICAxis_Y, tmhelix.ICAxis_Z = TM. ExtractSlice([-12.0,2.0]). MainAxis ( )
    
            [tmhelix.MC_EC_X, tmhelix.MC_EC_Y, tmhelix.MC_EC_Z],\
            [tmhelix.MC_MM_X, tmhelix.MC_MM_Y, tmhelix.MC_MM_Z],\
            [tmhelix.MC_IC_X, tmhelix.MC_IC_Y, tmhelix.MC_IC_Z]  =  TM. ThinSlicesCOMs ( )  
            tmhelix.save()                
            self. tmhelixmodel_set.add(tmhelix)
            self.save()
#            print Residue.objects.all().values_list('AAThreeLetter')#;quit()
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
                tmhelixpair.save()
                self.tmhelixpair_set.add(tmhelixpair)  
# mozna to lepiej rozpisac, ale to na potem                
#                print  'Count '+str(tmhelixpair.tmhelixmodel_set.count())        
                #sprawdzic czy dobrze bedzie
        return

    def ExtractInteractingHelixTriplets (self):
        
     triplet_pkss = []
        
     print self.TMProtein_ID
        
        
     with transaction.atomic():        
        if not self.tmhelixpair_set.all():

            self. ExtractInteractingHelixPairs ()
        #bedzie to trzeba zoptymalizowac jakos
        
        NoPairs = self.tmhelixpair_set.count()
        
        helices = self.tmhelixpair_set.all()
        pair_pks= self.tmhelixpair_set.values_list('pk')
        
        print pair_pks
        
        length = len(pair_pks)
        
#        print type(pair_pks)
        
#        print pair_pks[0]
#        print pair_pks[1]
#        print pair_pks[2]        
#        print pair_pks[3]        

#        quit()
        
        for N1 in range(length):
            
                print pair_pks[N1][0]
            
                pks = TMHelixPair.objects.get(pk=pair_pks[N1][0]).tmhelixmodel_set.values_list('pk')
            
#                print pks
            
                for N2 in range(N1+1,length):
                
                    pks2 = TMHelixPair.objects.get(pk=pair_pks[N2][0]).tmhelixmodel_set.values_list('pk')
                
#                    print (pks|pks2).distinct()

                
 #                   from itertools import chain
                    
#                    print pks, pks2, pks|pks2
                    
#                    print pks|pks2

                    if (pks|pks2).distinct().count() ==3:
                        
                        triplet_pks = (pks|pks2).distinct().order_by('pk')
                        
                        lista = [triplet_pk[0] for triplet_pk in triplet_pks]
                        
                        if lista not in triplet_pkss:
                            
                            print triplet_pkss
                            print triplet_pks

                            triplet_pkss.append(lista)
                        
                        
#                        print 'found Triplet'
                    
                            tmhelixtriplet = TMHelixTriplet.objects.create(Set=self.Set)
                    
                            tmhelixtriplet.tmhelixmodel_set = self.tmhelixmodel_set.filter(id__in=triplet_pks).order_by('pk')
                    
                            tmhelixtriplet. getPhi ()
                            tmhelixtriplet.save()
                            self.tmhelixtriplet_set.add(tmhelixtriplet)  
                    self.save()
                    
    
    def ExtractInteractingHelixPairs (self):
        
        print self.TMProtein_ID
        
        NoHelices = self. tmhelixmodel_set.count()
        
        if NoHelices >= 2:
 # moze trzeba to na wyzszym poziomie zrobic       
            for N in range(NoHelices - 1):
# to teraz w petli sprawdzic czy jest kontakt i do przodu               
             for N2 in range(N+1,NoHelices):
                tmhelixpair = TMHelixPair.objects.create()
#                print N; print N+1;
#                print self. tmhelixmodel_set.all().values_list('id', flat=True)
# dziala, tylko troche wolno, poza tym mozna by to zrefaktoryzowac 
# jako querysetu, wiec moze najpierw uzyc atom_set
                tmhelixpair.tmhelixmodel_set.add(self. tmhelixmodel_set.get(TMHelix_ID=str(N+1)))   
                tmhelixpair.tmhelixmodel_set.add(self. tmhelixmodel_set.get(TMHelix_ID=str(N2+1)))
                
# mozna sprawdzic na tm helixpair czy jest contact
                Contact = tmhelixpair.Contact()
                if not Contact:
                    tmhelixpair.delete()
                
                else:
                    
                    tmhelixpair.getCrossingAngle ()              
                    tmhelixpair.save()
                    self.tmhelixpair_set.add(tmhelixpair)  
                    self.save()
                    print self.tmhelixpair_set.all()
#                    print  'Count '+str(tmhelixpair.tmhelixmodel_set.count())        
                #sprawdzic czy dobrze bedzie
        return

    def ExtractConsecutiveHelixTriplets (self):
        
        
        
        NoHelices = self. tmhelixmodel_set.count()
        
        if NoHelices >= 3:
        
            for N in range(NoHelices - 2):
               
                tmhelixtriplet = TMHelixTriplet.objects.create(Set=self.Set)

                
                tmhelixtriplet.tmhelixmodel_set.add(self. tmhelixmodel_set.get(TMHelix_ID=str(N+1)))   
                tmhelixtriplet.tmhelixmodel_set.add(self. tmhelixmodel_set.get(TMHelix_ID=str(N+2)))              
                tmhelixtriplet.tmhelixmodel_set.add(self. tmhelixmodel_set.get(TMHelix_ID=str(N+3)))              
                
                print str(N+1)
                print str(N+2)
                print str(N+3) 
                
                print tmhelixtriplet.tmhelixmodel_set.values_list('TMHelix_ID')
                print 'MC_MM_X'
                print tmhelixtriplet.tmhelixmodel_set.values_list('MC_MM_X')
                print self.structure.pdbCode
                
                
                
                tmhelixtriplet. getPhi ()
                tmhelixtriplet.save()
                self.tmhelixtriplet_set.add(tmhelixtriplet)  
                self.save()

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
#            print self. values_list('Phi')
            new_list = np.array([x for x in np.array(self. values_list('Phi',flat=True)) if x is not None])
#            print 'new_list'
#            print new_list
#            print self. values_list('id')
#            print np.array(self. values_list(Value, flat=True))
            relfrequency = relfreq(new_list,18,defaultreallimits=(0,180))
            print relfrequency
            print relfrequency[0]
            print relfrequency[0][int(math.floor((165.0+relfrequency[1])/relfrequency[2]))]
            HistogramPlot(new_list, 'myproject/myapp/static/myapp/static/Stats/HelixTriplet/'+Value )
        #zrobic jakies dict coby robilo ranges, uzaleznialo np od zakresu albo od czegos
        # wydrukowac statsy, najlepiej znormalizowane
        return





class TMHelixPair (models.Model):
    
    """ object storing TM Helix Pair """
    
    objects = TMHelixPairManager ()
    CrossingAngle = models.FloatField (null=True)
    CrossingAngleEC = models.FloatField (null=True)
    CrossingAngleIC = models.FloatField (null=True)
    TMProtein = models.ForeignKey(TMProtein, on_delete=models.CASCADE, null=True)

#####################################################################################################################################################

    def Contact(self):
        with transaction.atomic():        
            TMHelices = self.tmhelixmodel_set.all ()
        
            TMHelix1 = TMHelices[0]
            TMHelix2 = TMHelices[1]
            
            if contact_m(TMHelix1.atom_set.all(),TMHelix2.atom_set.all()):
                return True
        
#            for Residue1 in TMHelix1.residue_set.all():
            
#                for Residue2 in TMHelix2.residue_set.all():
                
                # wykorzystac object set: 
#                    if Residue.objects.filter(id__in=(Residue1.pk,Residue2.pk)).Contact():
#to musi byc jakos zmienione
# tylko nie wiem jeszcze jak                    
#                        return True
        
        return False
# zastanawiam sie czy nie wziac tego z modellera albo biopythona
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

class TMHelixTripletQuerySet(models.QuerySet):

    def RMSD(self):
        
        
        return RMSD(self[0].Crds(), self[1].Crds())
    
    def Crds(self):
        
        return [ tripletI.Crds() for tripletI in self ]
# trzeba bedzie pK z tego zachowac
    def Cluster(self):

#        if not self.RMSDMatrix:
        
        if not hasattr(self, 'RMSDMatrix'):
            
           import os.path 
           if os.path.isfile('media/RMSDMatrix.csv'):
               
               self.RMSDMatrix= from_csv('media/RMSDMatrix.csv')
               
           else:   
               
               self.getRMSDMatrix()
        
        centroids, idx = kMedoids ( self.RMSDMatrix, 6 )
        
        ClusteringI = Clustering.objects.create()
        
        print 'idx'
        
        print idx
        
#        no_cluster,distance = vq(self.RMSDMatrix,centroids)

#        searchval = 3
#ii = np.where(values == searchval)[0]

 #       ClusteringI.idx = idx
 #       ClusteringI.no_cluster = ','.join(no_cluster)
 #       ClusteringI.distance=str(distance)
 #       ClusteringI.save()
        
        print 'centroids'
        print centroids
 #       print 'no_cluster'
 #       print no_cluster
 #       print 'distance'
 #       print distance

        return

    def getRMSDMatrix(self):
#ta matryca pewnie bedzie za dluga na JSONA a i tak musi wejsc do pamieci
        self.RMSDMatrix = getRMSDMatrix (self.Crds())
        return self.RMSDMatrix

#        length = len(self)        
#        RMSDMatrixI = np.zeros((length,length))        
        
#        for N1 in range(length):
#            for N2 in range(N1+1,length):
#                print self[N1].TMProtein.TMProtein_ID, self[N2].TMProtein.TMProtein_ID
#                RMSDI = self.filter(id__in=(self[N1].pk,self[N2].pk)).RMSD()
#                print RMSDI
#                RMSDMatrixI.itemset((N1,N2),(RMSDI))
#                RMSDMatrixI.itemset((N2,N1),(RMSDI))       
#        print RMSDMatrixI
#        quit()        

        return RMSDMatrixI

class TMHelixTriplet (models.Model):
    
    """ object storing TM Helix Pair """
    objects = TMHelixTripletManager ().from_queryset(TMHelixTripletQuerySet)()
    Phi = models.FloatField (null=True)
    TMProtein = models.ForeignKey(TMProtein, on_delete=models.CASCADE, null=True)
    Score = models.FloatField (null=True)
    Set = models.CharField(max_length=10,null=True)
    Type = models.CharField(max_length=20,null=True)
    Cluster = models.IntegerField(null=True)

#####################################################################################################################################################

    def Crds(self):

# brzydko to jest zrobione
        
        CrdsI = []
        
        for tmhelix in self.tmhelixmodel_set.all():
            
            CrdsI.append([tmhelix.MC_EC_X, tmhelix.MC_EC_Y, tmhelix.MC_EC_Z ])
            CrdsI.append([tmhelix.MC_MM_X, tmhelix.MC_MM_Y, tmhelix.MC_MM_Z ])
            CrdsI.append([tmhelix.MC_IC_X, tmhelix.MC_IC_Y, tmhelix.MC_IC_Z ])
        
        return CrdsI


    def getScore(self):
#        self.Score = probability(self.Phi,TmTripletSet)

#        for Value in ['Phi']:
#            print self. values_list('Phi')
        new_list = np.array([x for x in np.array(TMHelixTriplet.objects.filter(Set='Reference'). values_list('Phi',flat=True)) if x is not None])
#            print 'new_list'
#            print new_list
#            print self. values_list('id')
#            print np.array(self. values_list(Value, flat=True))
        relfrequency = relfreq(new_list,18,defaultreallimits=(0,180))
#        print relfrequency; 
 #           print relfrequency
 #           print relfrequency[0]
 #           print relfrequency[0][int(math.floor((165.0+relfrequency[1])/relfrequency[2]))]
 #           HistogramPlot(new_list, 'myproject/myapp/static/myapp/static/Stats/HelixTriplet/'+Value )
        self.Score = relfrequency[0][int(math.floor((self.Phi)/relfrequency[2]))]
#        print self.Phi
#        print 
#        print int(math.floor((180.0+self.Phi+relfrequency[1])/relfrequency[2]))
#        print 
        self.save()
#        print self.Score
        #quit()
        return self.Score

#####################################################################################################################################################
    
    def getPhi (self):

        ids = self.tmhelixmodel_set.all ().values_list('id')
        helices = self.tmhelixmodel_set.all ()
        [helix1, helix2, helix3] = self.tmhelixmodel_set.all ()
#        print helices.values_list('MC_MM_X')    
#        print helix1.MC_MM_X
#        print helix3.MC_MM_X
        
        
        
        P1 = [helix1.MC_MM_X,helix1.MC_MM_Y,helix1.MC_MM_Z]
        P2 = [helix2.MC_MM_X,helix2.MC_MM_Y,helix2.MC_MM_Z]        
        P3 = [helix3.MC_MM_X,helix3.MC_MM_Y,helix3.MC_MM_Z]

#        print P1
#        print P2
#        print P3

        Vec1 = SetOfPoints([P1,P2]).Vector()
        Vec2 = SetOfPoints([P1,P3]).Vector()
        self.Phi = SetOfVectors([Vec1, Vec2 ]) .AngleDEG ()
#        print self.Phi
#        quit()

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
    TMHelix_pdb_path = models.CharField(max_length=2000)
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
class ResidueManager (models.Manager):
    
    """ object managing Amino Acid Residues """
    
    pass

class ResidueQuerySet(models.QuerySet):

    def manager_and_queryset_method(self):

        return

    def Contact(self):
        
        with transaction.atomic():
            print 'Res '+str(self[0].pk)        
            for Atom1 in self[0].atom_set.all():
                for Atom2 in self[1].atom_set.all():
#                print 
                    if distance(Atom1,Atom2) < 5.0:
                        return True

        return False

class Residue (models.Model): #research multiple inheritance
    
    """ object representing Amino Acid Residue """
    
    objects = ResidueManager().from_queryset(ResidueQuerySet)()
    Z = models.FloatField(null=True)
    AAThreeLetter = models.CharField(max_length=3,null=True)
    Residue_ID = models.CharField(max_length=200)
    TMHelixModel = models.ForeignKey(TMHelixModel, on_delete=models.CASCADE, null=True)
    
    def CenterOfMass ( self ):

          """ returns Center Of Mass of class Instnace """

#          if self.Content == []: # check if there are any atoms to compute COM from ...
#             print self
#             print 'AtomSetIsEmpty. Unable to calcuate Center Of Mass.'

          X_Sum, Y_Sum, Z_Sum, Mass_Sum  = [ 0.0, 0.0, 0.0, 0.0 ] 

          for Atom in self.atom_set.all():
          
              X_Sum += ( Atom .X * Atom .Mass )
              Y_Sum += ( Atom .Y * Atom .Mass )
              Z_Sum += ( Atom .Z * Atom .Mass ) 

              Mass_Sum += Atom .Mass 

          CenterOfMass = [ (Coord_Sum / Mass_Sum) for Coord_Sum in [X_Sum, Y_Sum, Z_Sum ] ]
          self.Z = CenterOfMass[2]
          self.save()
          return CenterOfMass

    @classmethod
    def create(cls, ID):

        """ creates new object: instance of TMHelix class """

        residue = cls(Residue_ID=ID, attributes={})
        return residue

class AtomManager (models.Manager):

    """ manager for Atom class objects """
    
    def show(self):        
        
        Text = ''
        
        for AtomI in self.all():
            
#             print AtomI.Text
             Text = Text+AtomI.Text#+'\n'
        
        return Text

class AtomQuerySet(models.QuerySet):

    def manager_and_queryset_method(self):

        return

    def Contact(self):
        
        if self.Distance()<2.5:
            return True

        return False

    def Distance(self):
        
#        print self[0]
#        print self[1]
        
        return    ((self[0].X-self[1].X)**2\
                 + (self[0].Y-self[1].Y)**2\
                 + (self[0].Z-self[1].Z)**2)**0.5

class   Atom (models.Model):

    """ object representing AtomLine """
    
    TMProtein = models.ForeignKey(TMProtein, on_delete=models.CASCADE, null=True) #znalezc szybsza alternatywe
    TMHelixModel = models.ForeignKey(TMHelixModel, on_delete=models.CASCADE, null=True)
    Residue = models.ForeignKey(Residue, on_delete=models.CASCADE, null=True)
#ciekawe oile to spowolni
    Text = models.CharField(max_length=200)
    objects = AtomManager().from_queryset(AtomQuerySet)()
    Atom_ID = models.CharField(max_length=200)
    X = models.FloatField(null=True)
    Y = models.FloatField(null=True)
    Z = models.FloatField(null=True)
    Mass = models.FloatField(null=True)
    AAThreeLetter = models.CharField(max_length=3,null=True)
    VdWRadius = models.FloatField(null=True)

#there should be vdW somewhere

    @classmethod
    def create(cls, ID):

        """ creates new object: instance of TMHelix class """

        atom = cls(Atom_ID=ID, attributes={})
        return atom

