#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

import sys, os, sqlite3

import TMHelixModule;
import AtomRecordsModule;
from AtomRecordsModule import Setof2AtomRecords;

import SetOfAtomsModule
from SetOfAtomsModule import SetOfResidues


import GeometricalClassesModule as GeometricalClassesModule;
from GeometricalClassesModule import *;

import models; from models import TMHelixModel, TMProtein;

#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

class N_TMs_Set ( list ): # musze zrobic od razu na N secie

      """ stores a set of N Transmembrane Helices """

#####################################################################################################################################################
        
      def __init__ ( self, InputTMHelixInstances ):

          """ constructs class instance from a input list of Transmembrane Helix (class TMHelix) instances """

          self. Content = InputTMHelixInstances
          self. Order = len ( self. Content )
          self. HelixIDs = [TM.ID for TM in self. Content]
          self. HelixNterDescriptors = [TM. NterDescriptor for TM in self. Content ]

#####################################################################################################################################################

      def CenterOfMass ( self ):

          """ returns Center Of Mass for Instance """

          TM_COM_Set = [i. CenterOfMass ( ) for i in self.Content]

          return SetOfPoints ( TM_COM_Set ). CenterOfMass ( )

#####################################################################################################################################################

      def OutputToPdbFile ( self, Path ):

          """ outputs instance to PDB file """

          self.HelixIDsI = self.HelixIDs

          FileName = Path;

          for HelixID in self.HelixIDsI:

              FileName = FileName +'_'+ str ( HelixID )

          FileName = FileName + '.pdb'

          OpenedFileInstance = open ( FileName, 'w' )

          for TMHelixInstance in self.Content:

              for ResidueInstance in TMHelixInstance.Content:

                  for AtomRecordInstance in ResidueInstance.Content:

                      OpenedFileInstance.write ( AtomRecordInstance.s )

          OpenedFileInstance.flush ( ); OpenedFileInstance.close ( );

#####################################################################################################################################################

      def __repr__ ( self ):

          for TMHelixInstance in self.Content: TMHelixInstance.Print ( )

#####################################################################################################################################################

      def MainAxis ( self ):

          """ returns Main Axis of Instance """

          if Parametry. TripletMainAxisDefinition == 'SumOfMainAxesOfHelices': 

             return self. MainAxisSumOfMainAxesOfHelices ( )

#####################################################################################################################################################

      def MainAxisSumOfMainAxesOfHelices ( self ):

          """ returns Main Axis of Instance """

          HelixAxes = [ i. MainAxis (  ) for i in self. Content ]

          AxisI = SetOfVectors ( HelixAxes ). Sum ( )

          LengthI = AxisI. Length ()

          return Vector ( [ AxisI[0] / LengthI, AxisI[1] / LengthI, AxisI[2] / LengthI  ] )

#####################################################################################################################################################

      def HelixTiltsPCA ( self ):

          """ returns list containing Tilt Value for each of the TMHelix in the set """
          """ TMHelix axis defined as the main PCA direction                        """

          return [ TM. TiltPCA ( ) for TM in self.Content ]

#####################################################################################################################################################

      def HelixTiltsCOM_Vector ( self ):

          """ returns list containing Tilt Value for each of the TMHelix in the set """
          """ TMHelix axis defined as the main COM direction                        """

          return [ TM. TiltCOM_Vector ( ) for TM in self.Content ]

#####################################################################################################################################################

      def HelixTilts ( self ):

          """ returns list containing Tilt Value for each of the TMHelix in the set """

          return [ TM. Tilt ( ) for TM in self.Content ]

#####################################################################################################################################################

      def WriteToDB (self, db_path):

          # ta funkcja powinna tworzyc tez obiekt TMProtein i podlegle helisy
          # powinien stworzyc instance TMProtein

          TMProteinI = TMProtein.objects.create()
          

          """ returns list containing Tilt Value for each of the TMHelix in the set """

#          os. system('rm '+db_path) # removes from console previous database if there is one; quite dirty

#          conn = sqlite3.connect(db_path)
#          c = conn. cursor ()
#          c.execute('''CREATE TABLE TMs
#                 (ID text, AASEQ text, Tilt real, Tilt_EC real, Tilt_IC real, MainAxis_X real, MainAxis_Y real, MainAxis_Z real, KinkAngle real, Overhang real  )''')

          for TM in self.Content:
              
              tmhelix = TMHelixModel.objects.create(TMHelix_ID= TM. ID, TMHelix_Tilt = TM. Tilt(), \
                                      TMHelix_Tilt_EC = TM. Tilt_EC(), \
                                      TMHelix_Tilt_IC = TM. Tilt_IC(), \
                                      TMHelix_KinkAngle = TM. KinkAngle(), \
                                      TMHelix_Overhang = TM. Overhang(),\
                                      TMHelix_AASEQ = TM. AASEQ (),
                                      Atoms = "fejslik")

#              TMHelixModel.objects.create ()
#              Atoms = ""
              for ResidueI in TM.Content:
                  for Atom in ResidueI.Content:
                      AtomLineI = AtomLine.objects.create(Content=Atom.s)
                      
                      tmhelix. atomline_set.add(AtomLineI)
#                      Atoms= Atoms+ Atom.s
#                      print Atom.s
                      TMProteinI. atomline_set.add(tmhelix)
                      

	      TMProteinI. tmhelixmodel_set.add(tmhelix)
#          tmhelix.Atoms = Atoms
          
#              c.execute("INSERT INTO TMs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (TM. ID, TM. AASEQ (), float(format(TM. Tilt(), '.3f') ), float(format(TM. Tilt_EC(), '.3f') ),float(format(TM. Tilt_IC(), '.3f') ), float(format(TM. MainAxis()[0], '.3f') ), float(format(TM. MainAxis()[1], '.3f') ), float(format(TM. MainAxis()[2], '.3f') ), float(format(TM. KinkAngle(), '.3f') ), float(format(TM. Overhang(), '.3f') )  ))

#          conn. commit()
#          conn. close()  

          # a moze from models import TMHelix

#####################################################################################################################################################
