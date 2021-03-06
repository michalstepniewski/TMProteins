import sys

import  GeometricalClassesModule; from GeometricalClassesModule import SetOfPoints;

import SetOfAtomsModule; from   SetOfAtomsModule import Residue, SetOfAtoms;

import AtomRecordModule; from AtomRecordModule import *;

from math import sqrt; 

#####################################################################################################################################################
#####################################################################################################################################################

class PdbRecords( list ):

      """ stores records of PDB file; introduced for clarity """

      pass

#####################################################################################################################################################
#####################################################################################################################################################

class AtomRecords ( list ):

      """ stores ATOM records of PDB file """
      
      def __init__ ( self, InputAtomRecords ):
          
          self. Content = [ ]

          for InputAtomRecord in InputAtomRecords:

              AtomRecordInstance = AtomRecord ( InputAtomRecord.s )
              self. Content. append ( AtomRecordInstance )

#####################################################################################################################################################

      def XYZs ( self ):

          """ returns cartesian coordinates of atoms stored in instance of SetOfPoints class """ 

          return SetOfPoints ( [ PointInstance. XYZ for PointInstance in self. Content ] ) 

#####################################################################################################################################################

      def Center ( self ):

          """ returns geometrical center of cartesian coordinates of atoms """

          return self. XYZs(). Center ( )

#####################################################################################################################################################

      def Print ( self ):

          """ prints ATOM records stored in class """

          for self.AtomRecordInstance in self.Content:

              self.AtomRecordInstance. Print ( )

#####################################################################################################################################################

      def ExtractProteinResidues ( self ):

          """ divides ATOM records into lists representing their respective Amino Acid residues """
          """ and returns them as set of thses lists """

          self.Residue = [ ]; self.Residues = [ ]

          self.Residue.append ( self.Content [ 0 ] ) # extract the first one
       
          for N in range ( 1, len ( self.Content ) ):

              CurrentAtom = self.Content[N]; PreviousAtom = self.Content[(N-1)];
              PreviousResSeqNo  = PreviousAtom. ResidueSequenceNumber ( )
              CurrentResSeqNo  =  CurrentAtom.  ResidueSequenceNumber ( )

              if CurrentResSeqNo != PreviousResSeqNo :

                 self.Residues.append ( Residue ( self.Residue ) )

                 self.Residue = [ ]

                 self.Residue. append ( self.Content [ N ] )

              else: 

                 self.Residue.append ( self.Content [ N ] )
       
          self.Residues.append ( Residue ( self.Residue ) )

          return self.Residues

#####################################################################################################################################################

      def RotateByMatrix ( self, RotationMatrix ):

          """ transforms coordinates of ATOM records through input Rotation Matrix """

          [ Atom. RotateByMatrix ( RotationMatrix ) for Atom in self. Content ]

#####################################################################################################################################################

      def Translate ( self, Vector ):

          """ transforms coordinates of ATOM records through input translation Vector """

          [ Atom.Translate ( Vector ) for Atom in self. Content ]

#####################################################################################################################################################

      def SuperimposeOnTemplate ( self, Template ):

          """ superimposes coordinates of ATOM records on coordinates of input Template """

          TemplateGeometricalCenter = Template. Center ( )

          # done in 3 steps
          # step 1

          self. MoveToOrigin ()
          Template. MoveToOrigin ()

          # step 2

          self. RotateOnTemplate ( Template )

          # step 3

          self. Translate ( TemplateGeometricalCenter )
          Template. Translate ( TemplateGeometricalCenter )

          return

#####################################################################################################################################################


class Setof2AtomRecords ( list ):

      """ stores a pair of atoms """

      def __init__ ( self, InputAtomRecords ): 

          self. Content = [ ]

          for InputAtomRecord in InputAtomRecords:
              AtomRecordInstance = AtomRecord ( InputAtomRecord.s )
             
              self. Content. append ( AtomRecordInstance )

#####################################################################################################################################################

      def Vector(self):

          """ returns a 3D vector connecting Firs atom of input Pair with second atom of input Pair """

          Atom1 = self.Content [0]
          Atom2 = self.Content [1]

          Vector = [ Atom2.X - Atom1.X, Atom2.Y - Atom1.Y, Atom2.Z - Atom1.Z ]

          return Vector

#####################################################################################################################################################
 
      def Distance(self):

          """ returns distance between two atoms of input Pair """

          VectorI= self.Vector()
          DistanceI = sqrt( (VectorI[0]**2.0) + (VectorI[1]**2.0) + (VectorI[2]**2.0)  )

          return DistanceI

#####################################################################################################################################################

      def VdWContact (self):

          """ returns True if atoms in input pair form VdW pair and False otherwise """

          SumOfVdWRadiuses = self.Content[0].VdWRadius ( ) + self.Content[1].VdWRadius ( )

          if self.Distance() <= ( 1.0 * SumOfVdWRadiuses ):

             return True

          else:

             return False

#####################################################################################################################################################

      def VdWContactConstantThreshold (self, ConstantThreshold = 4.50 ):

          """ returns True if atoms in input pair form VdW pair and False otherwise """
          """ VdW pair is defined if two atoms are closer then input ConstantThreshold """

          SumOfVdWRadiuses = self.Content[0].VdWRadius ( ) + self.Content[1].VdWRadius ( )

          if self.Distance() <= ConstantThreshold:

             return True

          else:

             return False

