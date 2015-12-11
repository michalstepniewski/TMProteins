import sys

import inspect

import AtomRecordsModule;
from  AtomRecordsModule import AtomRecords;

import TMHelixModule; from TMHelixModule import *;

import AtomRecordModule;
from   AtomRecordModule import *;

import SetOfAtomsModule; from SetOfAtomsModule import Residue, SetOfResidues;

#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

class SetOfSetsOfResidues ( list ):

      def __init__ ( self, InputSetsOfResidues ):

          self. Content = [ InputSetOfResidues for InputSetOfResidues in InputSetsOfResidues ]

#####################################################################################################################################################

      def Print ( self ):

          [ SetOfResiduesInstance. Print ( ) for SetOfResiduesInstance in self. Content ]

      
#####################################################################################################################################################
#####################################################################################################################################################

class ProteinChain ( SetOfResidues ):

   """ stores Amino Acid residues contained in one Protein Chain """

   def __init__ (self, InputResidueInstances, InputChainID = 'X' ):

       """ constructs class Instance from input list of Amino Acid residues """

       self.Content = []    
       self.ChainID = InputChainID 

       for InputResidueInstance in InputResidueInstances: 
           
           self.Content. append ( InputResidueInstance ) # chwilowo, ciezko wymyslec dobry konstruktor

#####################################################################################################################################################

   def OutputToPdbFile ( self, Path ):

       """ outputs atoms of Protein Chain into PDB File """

       FileName = Path  + self.ChainID + '.pdb';

       OpenedFileInstance = open ( FileName, 'w' )

       for ResidueInstance in self.Content:

           for AtomRecordInstance in ResidueInstance.Content:

               OpenedFileInstance.write ( AtomRecordInstance.s )

       OpenedFileInstance.flush ( ); OpenedFileInstance.close ( );

#####################################################################################################################################################

   def AASEQ ( self ):

       """ returns Amino Acid Sequence (in one letter code) of class Instance """

       self.AASEQ = ''

       return ''.join ( [ self.Residue. AA ( ) for self. Residue in self. Content ] )

#####################################################################################################################################################

   def AASEQ_Z ( self ):

       """ returns  Amino Acid Sequence (in one letter code) of class Instance """
       """ together with Z coordinates of Amino Acid Residues                  """

       return '\n'.join([ ' '.join(['#AASEQ_Z TM', str(self. ID), self.Residue. AA ( ), str( self.Residue. Z ( ) ) ]) for self.Residue in self.Content ]) + '\n'

#####################################################################################################################################################

   def Segment (FirstResNo, LastResNo ):

       """ returns a Segment of Amino Acid Residues starting from FirstResNo ID to LastResNo ID """

       self. Segment = [ ]

       for self.Residue in self.Content:

           if ( FirstResNo <= self.Residue.SequenceNumber ( ) <= LastResNo ):

              self. Segment. append ( self. Residue ) 

       return self. Segment

#####################################################################################################################################################

   def MRegionResidues (self):

       """ returns residues located in the lipid membrane region """

       self.MResidues = [ ]

       for self.Residue in self.Content: 

           if self.Residue .M ( ): # if it is in the membrane

              self.MResidues.append ( self.Residue )

       return self.MResidues

#####################################################################################################################################################

   def MRegionResiduesSegments ( self ):

       """ returns continuous segments of Protein Chain located in the lipid membrane region """

       self. MRegionResidues_I = self. MRegionResidues ( )

       self. MRegionResiduesSegments_I = [ ];

       if self.MRegionResidues_I != [ ]:

          self.MRegionResiduesSegment = [ ];

          self.MRegionResiduesSegment.append ( self.MRegionResidues_I [ 0 ] ) # take care of the First Residue

          for N in range ( 1, len ( self.MRegionResidues_I ) ):

              if self.MRegionResidues_I [ N ]. SequenceNumber ( ) - self.MRegionResidues_I [ N - 1 ]. SequenceNumber ( ) == 1 :

                 self.MRegionResiduesSegment.append ( self.MRegionResidues_I [ N ] )
       
              else:
                 self.MRegionResiduesSegments_I. append ( SetOfResidues( self.MRegionResiduesSegment ) )

                 self.MRegionResiduesSegment = [ ]

                 self.MRegionResiduesSegment.append ( self.MRegionResidues_I [ N ] )
                 

          self.MRegionResiduesSegments_I. append ( SetOfResidues( self.MRegionResiduesSegment ) ) # take care of the last one

       self.MRegionResiduesSegment = [ ]

       return SetOfSetsOfResidues ( self. MRegionResiduesSegments_I )

#####################################################################################################################################################

   def TMSegments ( self ):

       """ returns Transmembrane Segments of Protein Chain """

       import TMHelixModule; from TMHelixModule import TMHelix; # imported here in order to avoid circular reference

       MSegments = self. MRegionResiduesSegments ( )

       TMSegments_I = [ ]

       ID = 1

       for MSegmentI in MSegments. Content:

           MSegmentInstance = MSegment ( MSegmentI.Content )

           if MSegmentInstance. CrossingMembrane () and  MSegmentInstance. TransMembrane ( )  :

                  TMSegments_I. append ( TMHelix ( MSegmentInstance.Content, ID ) ); ID=ID+1;

       return   TMSegments_I

#####################################################################################################################################################

   def ProteinNterOrientation ( self ):

       """ returns Orientation of N terminus of Protein Chain """

       NterOrientation_I = self. TMSegments ( ) [ 0 ]. NterDescriptor ( )

       return NterOrientation_I

#####################################################################################################################################################
#####################################################################################################################################################

class MSegment ( ProteinChain ):

      """ stores Membrane Segment of Protein Chain """
      """ inherits from Protein Chain              """

#####################################################################################################################################################

      def CrossingMembrane ( self, MembraneBorders = [-10.0, 10.0 ] ):

          """ checks whether MSegment instance is crossing the lipid Membrane """
          """ ie. not a reentrant loop                                        """

          FirstZ = self.Content [ 0 ]. Z ()

          if FirstZ <= 0.0:

             for ResidueI in self.Content:

                 if ResidueI. Z () >= 0.0: return True

          elif FirstZ >= 0.0:

             for ResidueI in self.Content:

                 if ResidueI. Z () <= 0.0: return True

          return False

#####################################################################################################################################################

      def TiltConsistent (self):

          """ checks whether Tilt Values are calculated by PCA and MassCenter method are consistent """
          """ within given threshold defined in Parameters """

          if self. PCAMCTiltDifference <= Parametry. PCAMCTiltDifferenceThreshold:

             return True

#####################################################################################################################################################

      def Helical (self):

          """ checks whether Segment is Helical above percentage threshold """
          """ defined in Parameters """

          if self. PercentHelicity >= Parametry. PercentHelicityThreshold:

             return True

          else:

             return False

#####################################################################################################################################################


      def TransMembrane ( self, MembraneBorders = [-10.0, 10.0 ] ):

          """ checks whether MSegment instance is TransMembrane """

          FirstZ, LastZ = [ ResidueI. Z ( ) for ResidueI in [ self.Content [ 0 ], self.Content [ -1 ] ]  ]

          if ( ( FirstZ <= MembraneBorders [0] ) and ( LastZ >= MembraneBorders [1] ) ) or \
             ( ( FirstZ >=  MembraneBorders [1] ) and ( LastZ <= MembraneBorders [0] ) ):

             return True

          else:

             return False

#####################################################################################################################################################

      def Monotoniczny ( self, Threshold = 5.0 ):

          """ checks whether MSegment instance is monotonic """

          FirstZ = self.Content [ 0 ]. Z ( );

          if FirstZ <= 0.0:

             HighestZ = FirstZ

             for ResidueI in self.Content:

                 HighestZ = max ( HighestZ, ResidueI. Z ( ) )

                 MonotonicityDeviation = HighestZ - ResidueI. Z ( )

                 if MonotonicityDeviation >= Threshold:

                    return False

          elif FirstZ >= 0.0:

             LowestZ = FirstZ

             for ResidueI in self.Content:

                 LowestZ = min ( LowestZ, ResidueI. Z ( ) )

                 MonotonicityDeviation = ResidueI. Z ( ) - LowestZ

                 if MonotonicityDeviation >= Threshold:

                    return False

          return True

#####################################################################################################################################################

      def ExtractMonotonics ( self, Threshold = 5.0 ):

          """ extracts monotonic segments from segment instance """

          Monotonics = [ ]

          FirstZ = self.Content [ 0 ]. Z ( );

          Monotonic = [ ]

          N = 0

          while N <= ( len ( self. Content ) -1 ):
                Monotonic = [ ]

                FirstZ = self.Content [ N ]. Z ( )

                if FirstZ <= 0.0:

                   HighestZ = FirstZ

                   MonotonicityDeviation = HighestZ - self.Content [ N ]. Z ( )
                   Monotonic = [ ]

                   while N <= ( len ( self. Content ) - 1 ) and MonotonicityDeviation <= Threshold :

                         HighestZ = max ( HighestZ, self.Content [ N ]. Z ( ) )

                         MonotonicityDeviation = HighestZ - self.Content [ N ]. Z ( )

                         Monotonic. append ( self.Content [ N ] )

                         N += 1

                   Monotonics. append ( MSegment ( Monotonic ) )
                   Monotonic = [ ]

                elif FirstZ >= 0.0:

                   LowestZ = FirstZ

                   MonotonicityDeviation = self.Content [ N ]. Z ( ) - LowestZ
                   Monotonic = [ ]

                   while N <= ( len ( self. Content ) -1 ) and MonotonicityDeviation <= Threshold :

                         LowestZ = min ( LowestZ, self.Content [ N ]. Z ( ) ) 

                         MonotonicityDeviation = self.Content [ N ]. Z ( ) - LowestZ

                         Monotonic. append ( self.Content [ N ] )

                         N += 1

                   Monotonics. append ( MSegment ( Monotonic ) )
                   Monotonic = [ ]
          
          return Monotonics
