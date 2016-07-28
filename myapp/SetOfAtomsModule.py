import sys;

import AtomRecordModule;
from AtomRecordModule import *;

import AtomRecordsModule 

import GeometricalClassesModule;
from GeometricalClassesModule import *;

class Parametry ():

    """ stores (or more accurately provides a namespace for Parameter values """

    pass

Parametry. MembraneLimits = [-15.0, 15.0]
Parametry. BordersOfThinSlices = [[-12.0, -6.0], [-3.0, 3.0], [6.0, 12.0]]
Parametry. BordersOf10ThinSlices = [ [-15.0, -12.0], [-12.0, -9.0 ], \
                                     [ -9.0,  -6.0], [ -6.0, -3.0 ], \
                                     [ -3.0,   0.0], [  0.0,  3.0 ], \
                                     [  3.0,   6.0], [  6.0,  9.0 ], \
                                     [  9.0,  12.0], [ 12.0, 15.0 ] ]



Parametry. MainAxisDefinition = 'PCA'
Parametry. HelixDirectionality = 'NterCter'

#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

class SetOfAtoms ( list ):

      """ stores Set of Atoms """

      def __init__ ( self, InputAtomRecords ):

          """ constructs class instance from input list of Atom Records """

          self. Content = [ ]

          for InputAtomRecord in InputAtomRecords:

              AtomRecordInstance = AtomRecord ( InputAtomRecord.s )
 
              self. Content. append ( AtomRecordInstance )

          return

#####################################################################################################################################################

      def Print ( self ):

          """ prints contents of class instance """

          for AtomRecordInstance in self.Content:

              AtomRecordInstance. Print ( )

#####################################################################################################################################################

      def CenterOfMass ( self ):

          """ returns Center Of Mass of class Instnace """

          if self.Content == []: # check if there are any atoms to compute COM from ...
             print self
             print 'AtomSetIsEmpty. Unable to calcuate Center Of Mass.'

          X_Sum, Y_Sum, Z_Sum, Mass_Sum  = [ 0.0, 0.0, 0.0, 0.0 ] 

          for Atom in self. Content:
          
              X_Sum += ( Atom .X * Atom .Mass () )
              Y_Sum += ( Atom .Y * Atom .Mass () )
              Z_Sum += ( Atom .Z * Atom .Mass () ) 

              Mass_Sum += Atom .Mass ()

          CenterOfMass = [ (Coord_Sum / Mass_Sum) for Coord_Sum in [X_Sum, Y_Sum, Z_Sum ] ]

          return CenterOfMass

#####################################################################################################################################################

      def Vector ( self ):

          """ returns a Vector connecting First atom in set to Second atom in set """

          Atom1 = self.Content [0]
          Atom2 = self.Content [1]

          VectorI = [ Atom2.X - Atom1.X, Atom2.Y - Atom1.Y, Atom2.Z - Atom1.Z ]

          return Vector ( VectorI )

#####################################################################################################################################################
 
      def Distance ( self ):

          """ returns Distance between First and Second atom in set """

          return self.Vector ( ). Length ( )

#####################################################################################################################################################

      def VdWContact (self):

          """ checks whether there is VdW contact between First and Second atom in set """

          SumOfVdWRadiuses = self.Content[0].VdWRadius ( ) + self.Content[1].VdWRadius ( )

          if self.Distance() <= ( 1.0 * SumOfVdWRadiuses ):

             return True

          else:

             return False

#####################################################################################################################################################

      def VdWContactConstantThreshold (self, ConstantThreshold = 4.50 ):

          """ checks whether there is VdW contact between First and Second atom in set """

          SumOfVdWRadiuses = self.Content[0].VdWRadius ( ) + self.Content[1].VdWRadius ( )

          if self.Distance() <= ConstantThreshold :

             return True

          else:

             return False

#####################################################################################################################################################
#####################################################################################################################################################

class Residue ( SetOfAtoms ):

      """ stores ATOM records contained in Amino Acid residue """

      def __init__ ( self, InputAtomRecords ):

          """ constructs class instance from input list of ATOM records """

          self. Content = [ ]

          for InputAtomRecord in InputAtomRecords:

              AtomRecordInstance = AtomRecord ( InputAtomRecord.s )
 
              self. Content. append ( AtomRecordInstance )
          
          return

#####################################################################################################################################################

      def HydrogenBondDonors ( self ) :

          """ return Hydrogen Bond donors contained in Amino Acid Residue """

          Type = 'NH '

          AminoacidAtomLexicon = { 'ARG' : 'NE ', \
                                   'ASN' : 'ND2', \
                                   'HIS' : 'NE2', \
                                   'SER' : 'OG ', \
                                   'TYR' : 'OH ', \
                                   'ARG' : 'NH1', \
                                   'CYS' : 'SG ', \
                                   'HIS' : 'ND1', \
                                   'THR' : 'OG1', \
                                   'ARG' : 'NH2', \
                                   'GLN' : 'NE2', \
                                   'LYS' : 'NZ ', \
                                   'TRP' : 'NE1'    }

          HydrogenBondDonorsI = [ ]

          HydrogenBondDonorsI. append ( self. SelectAtomByName ( Type ) )

          if self. Name in AminoacidAtomLexicon. keys ( ):

             HydrogenBondDonorsI. append ( self. SelectAtomByName ( AminoacidAtomLexicon [ self. Name ] ) )

          return HydrogenBondDonorsI

# Hydrogen donor protein atoms
# analyzed in this study were: NH of the main chain, ARG NE,
# ASN ND2, HIS NE2, SER OG, TYR OH, ARG NH1, CYS
# SG, HIS ND1, THR OG1, ARG NH2, GLN NE2, LYS NZ
# and TRP NE1;

#####################################################################################################################################################

      def SelectAtomByName ( self, Name ):

          """ return last Atom from residue with given Atom Name """

          for AtomInstance in self. Content:

              if AtomInstance. Name == Name:

                 return AtomInstance

#####################################################################################################################################################

      def HydrogenBondAPrimAcceptorPairs ( self ):

          """ return Hydrogen Bond Donor and Acceptor Pairs """

          AType = 'O  '

          APrimType = 'C  '

          AAminoacidAtomLexicon = { 'ASN' : 'OD1', \
                                 'GLN' : 'OE1', \
                                 'MET' : 'SD ', \
                                 'ASP' : 'OD1', \
                                 'GLU' : 'OE1', \
                                 'SER' : 'OG ', \
                                 'ASP' : 'OD2', \
                                 'GLU' : 'OE2', \
                                 'THR' : 'OG1', \
                                 'CYH' : 'SG ', \
                                 'HIS' : 'ND1', \
                                 'TYR' : 'OH '     }

          APrimAminoacidAtomLexicon = { 'ASN' : 'CG ', \
                                     'GLN' : 'CD ', \
                                     'MET' : 'CG ', \
                                     'ASP' : 'CG ', \
                                     'GLU' : 'CD ', \
                                     'SER' : 'CB ', \
                                     'ASP' : 'CG ', \
                                     'GLU' : 'CD ', \
                                     'THR' : 'CB ', \
                                     'CYH' : 'CB ', \
                                     'HIS' : 'CG ', \
                                     'TYR' : 'CZ '     }

          HydrogenBondAPrimAcceptorPairsI = [ ]

          HydrogenBondAPrimAcceptorPairsI. append ( [ self. SelectAtomByName ( APrimType ), self. SelectAtomByName ( AType ) ] )

          if self. Name in AAminoacidAtomLexicon. keys ( ):

             HydrogenBondAPrimAcceptorPairsI. append ( [ self. SelectAtomByName ( APrimAminoacidAtomLexicon [ self. Name ] ), self. SelectAtomByName ( APrimAminoacidAtomLexicon [ self. Name ] ) ] )

          return self. HydrogenBondAPrimAcceptorPairsI

#####################################################################################################################################################

      def RotateByMatrix ( self, Matrix ):

          """ rotate coordinates of Amino Acid Residue atoms by given Matrix """

          for AtomI in self. Content:

              AtomI. RotateByMatrix ( Matrix )

          return

#####################################################################################################################################################

      def Print ( self ):

          """ prints contents of Amino Acid Residue """

          for AtomRecordInstance in self.Content:

              AtomRecordInstance. Print ( )

#####################################################################################################################################################

      def CA ( self ):

          """ returns CA atom of AminoAcid Residue               """
          """ In care residue is incomplete and does not have CA """
          """ returns N or C                                     """

          for AtomRecordInstance in self.Content:

              Name = AtomRecordInstance. Name

              if Name == ' CA ':

                 CA = AtomRecordInstance

          try: 
               return CA

          except UnboundLocalError:

                 print 'Incomplete Residue does not contain CA. Will try to go with N'

                 for AtomRecordInstance in self.Content:

                     Name = AtomRecordInstance. Name

                     if Name == ' N  ' :

                        N = AtomRecordInstance

                 try: return N

                 except UnboundLocalError:

                        print 'Incomplete Residue does not contain CA nor N. Will try to go with C'

                        for AtomRecordInstance in self.Content:

                            Name = AtomRecordInstance .Name 

                            if Name == ' C  ' :

                               C = AtomRecordInstance
                        self. Print ()
                        return C

#####################################################################################################################################################

      def M ( self ):

          """ checks whether Residue is located in lipid membrane """

          Zcoord = self.Z ()

          if ( Zcoord  >= Parametry. MembraneLimits [0] ) and ( Zcoord  <=  Parametry. MembraneLimits [1] ) :  
             
             return True
          else:
                return False

#####################################################################################################################################################

      def SequenceNumber ( self ):

          """ returns Residue Amino Acid sequence ID """

          AtomRecordInstance = self.Content [ 0 ]

          return AtomRecordInstance.ResidueSequenceNumber ( )

#####################################################################################################################################################

      def AA ( self ):

          """ returns Amino Acid name of Residue """

          AtomRecordInstance = self.Content  [ 0 ]

          return AtomRecordInstance.AA ( )

#####################################################################################################################################################

      def Chain ( self ):

          """ returns chain of Amino Acid Residue """

          AtomRecordInstance = self.Content  [ 0 ]

          return AtomRecordInstance.Chain ( )

#####################################################################################################################################################

      def Name ( self ):

          """ returns Name and sequence ID of Amino Acid Residue """

          NameI = str(self. SequenceNumber ( ))+self.AA();

          return NameI

#####################################################################################################################################################

      def Z ( self ):

          """ returns Z coordinate of CA atom """
          
          return self.CA (). Z

#####################################################################################################################################################

      def Mass ( self ):

          """ returns Mass of Amino Acid Residue """

          self.MassSum = 0.0

          for AtomRecordInstance in self.Content:  self.MassSum += AtomRecordInstance. Mass ( )

          return self.MassSum

#####################################################################################################################################################
#####################################################################################################################################################

class SetOfResidues ( list ):

      """ stores Set of class Residue instances """

#####################################################################################################################################################

      def __init__ (self, InputResidueInstances ):

          """ constructs class Instance from input list of Residue Instances """
         
          self.Content = []      

          for InputResidueInstance in InputResidueInstances: 

              self.Content. append ( InputResidueInstance )

#####################################################################################################################################################

      def Print ( self ):

          """ prints contents of class instance """

          for ResidueInstance in self.Content:

              ResidueInstance. Print ( )

#####################################################################################################################################################

      def CenterOfMass ( self ):

          """ returns Center Of Mass for SetOfResidues instance """

          if self.Content == []: # check if there are any atoms to compute COM from ...
             print self
             print 'Set Of Residues is Empty. AtomSetIsEmpty'

          X_Sum, Y_Sum, Z_Sum, Mass_Sum = [ 0.0, 0.0, 0.0, 0.0 ]

          for ResidueInstance in self.Content:
          
              X_Sum += ( ResidueInstance.CenterOfMass()[0] * ResidueInstance .Mass () )
              Y_Sum += ( ResidueInstance.CenterOfMass()[1] * ResidueInstance .Mass () )
              Z_Sum += ( ResidueInstance.CenterOfMass()[2] * ResidueInstance .Mass () ) 

              Mass_Sum += ResidueInstance .Mass () 

          CenterOfMassI = [ (CoordSum / Mass_Sum) for CoordSum in [ X_Sum, Y_Sum, Z_Sum] ]

          return CenterOfMassI

#####################################################################################################################################################

      def VdWContact ( self ):

          """ checks whether there is VdW contact between first and second Residue of the set """

          Res1, Res2 = self.Content[:2]

          for AtomRecordInstance1 in Res1.Content:

              for AtomRecordInstance2 in Res2.Content:

                  if SetOfAtoms ( [ AtomRecordInstance1, AtomRecordInstance2 ] ). VdWContact ():

                     return True

          return False

#####################################################################################################################################################

      def HydrogenBond ( self, DADistanceThreshold = 3.9  ):

          """ checks whether there is VdW contact between first and second Residue of the set """

          AA1 = self. Content [ 0 ]

          AA2 = self. Content [ 1 ]

          AcceptorAprimPairs = AA1. HydrogenBondAPrimAcceptorPairs ( )

          Donors = AA2. HydrogenBondDonors ( )

          for AcceptorAprimPair in AcceptorAprimPairs:

              Acceptor = AcceptorAprimPair [ 0 ]

              for Donor in Donors:

                  if [ Acceptor, Donor ]. Distance ( ) <= DADistanceThreshold:

                     if [ [ Acceptor, APrim ], [ Acceptor, Donor ] ]. Angle ( ):

                        return True      

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

          AcceptorAprimPairs = AA2. HydrogenBondAPrimAcceptorPairs ( )

          Donors = AA1. HydrogenBondDonors ( )

          for AcceptorAprimPair in AcceptorAprimPairs:

              Acceptor = AcceptorAprimPair [ 0 ]

              for Donor in Donors:

                  if [ Acceptor, Donor ]. Distance ( ) <= DADistanceThreshold:

                     if [ [ Acceptor, APrim ], [ Acceptor, Donor ] ]. Angle ( ):

                        return True                   

# musze znac AJ-A-D 90.0, wiec tak naprawde potrzebuje czterech atomow

# A' - A -- D - D'                

# D-A < 3.9 A

          return False

#####################################################################################################################################################

      def VdWContactOrHydrogenBond ( self ):

          """ checks whether there is VdW contact or hydrogen bond between first and second Residue of the set """

          Res1, Res2 = self.Content

          if ( self. VdWContact ( ) or  self. HydrogenBond () ):

             return True   

          return False

#####################################################################################################################################################

      def CAs ( self ):

          """returns set of CA atoms of Residue instances contained in the set """
 
          return [ ResidueInstance. CA ( ) for ResidueInstance in self. Content ]
