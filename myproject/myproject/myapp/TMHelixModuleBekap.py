import ProteinChainModule; from ProteinChainModule import ProteinChain;

import  AtomRecordModule;
from  AtomRecordModule import *;

import SetOfAtomsModule; from SetOfAtomsModule import *;

import  GeometricalClassesModule;
from GeometricalClassesModule import *;

#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

class TMHelix ( ProteinChain ):

      """ stores transmembrane helix """ 

#####################################################################################################################################################

      def __init__ ( self, InputResidueInstances, ID = 0, ParametersInstance = [ ] ):

          """ constructs class instance from input list of class Residue instances """

          self.Content = [ ]

          for InputResidueInstance in InputResidueInstances:

              self.Content. append ( InputResidueInstance )

          self.ID = ID
          self. ChainID = 'X'
          self. CalculateNterDescriptor ()

#####################################################################################################################################################

      def CA_XYZs ( self ):

          """ returns cartesian coordinates of CA residues contained in class instance """

          self.XYZsI = [ Point ( [ self.CA.X , self.CA.Y,  self.CA.Z ]) for self.CA in self.CAs() ]

          return SetOfPoints ( self.XYZsI )

#####################################################################################################################################################

      def HalfHelixTiltConsistent (self, TiltDiscrepancyThreshold = 30.0 ):

          """ checks whether tilts of half helices measured by PCA and Mass Center methods are consistent """
          """ within a given threshold (default value at 30.0 DEG)                                        """
          
          HalfHelixTiltsPCAI = self. HalfHelixTiltsPCA  ()
          
          HalfHelixTiltsCOMI = self. HalfHelixTiltsCOM_Vector ()
          
          for N in range(2):
              
              if abs( HalfHelixTiltsPCAI[N] - HalfHelixTiltsCOMI[N] )>= 30.0:
                  
                  return False
          
          return True

#####################################################################################################################################################

      def MainAxis ( self ):

          """ returns Main Axis Vector of class instance """

          if Parametry. MainAxisDefinition == 'PCA':

             return self. AxisPCA ( )

          elif Parametry. MainAxisDefinition == 'COM':

             return self. AxisCOM_Vector ( )

#####################################################################################################################################################

      def AxisPCA ( self ):

          """ returns Main Axis Vector of class instance """
          """ calculated by PCA method                   """

          if Parametry. HelixDirectionality == 'NterCter':
             return self. CA_XYZs ( ). PCAAxis ( )

          elif Parametry. HelixDirectionality == 'IC_EC':
               Axis = self. CA_XYZs ( ). PCAAxis ( )

               if Axis[2]>= 0.0:
                  return Axis

               OppositeAxis = Vector ( [ -Coord for Coord in Axis ] )

               return OppositeAxis

#####################################################################################################################################################

      def AxisCOM_Vector ( self ):

         """ returns Main Axis Vector of class instance """
         """ calculated by Mass Center method           """

         COMs = self. ThinSlicesCOMs ( )

         if Parametry. HelixDirectionality == 'NterCter':

          if self. NterDescriptor =='EC':

             return SetOfPoints ( [ COMs [ 0 ], COMs [ -1 ] ] ). Vector ( )

          elif self. NterDescriptor =='IC':

             return SetOfPoints ( [ COMs [ -1 ], COMs [ 0 ] ] ). Vector ( ) 

          else:
            print self. NterDescriptor; quit ()

         elif Parametry. HelixDirectionality == 'IC_EC':

          return SetOfPoints ( [ COMs [ -1 ], COMs [ 0 ] ] ). Vector ( )

#####################################################################################################################################################

      def HalfHelixAxes ( self ):

          """ returns Axes Vectors for EC and IC segments of Helix """

          if Parametry. HalfHelixAxesDefinition == 'COM':

            COMs = self. ThinSlicesCOMs ( )

            if Parametry. HelixDirectionality == 'NterCter':

             if self.NterDescriptor == 'EC':

                HalfHelixAxesI = SetOfVectors ( [ SetOfPoints ( [ COMs [ 0 ], COMs [ 1 ] ] ). Vector ( ), SetOfPoints( [ COMs [ 1 ], COMs [ 2 ] ]) . Vector ( ) ] )

             elif self.NterDescriptor == 'IC':
                                                                  # E            # M                                           #M       #I
                HalfHelixAxesI = SetOfVectors ( [ SetOfPoints ( [ COMs [ 2 ], COMs [ 1 ] ] ). Vector ( ), SetOfPoints( [ COMs [ 1 ], COMs [ 0 ] ]) . Vector ( ) ] )

            elif Parametry. HelixDirectionality == 'IC_EC' :

                HalfHelixAxesI = SetOfVectors ( [ SetOfPoints ( [ COMs [ 2 ], COMs [ 1 ] ] ). Vector ( ), SetOfPoints( [ COMs [ 1 ], COMs [ 0 ] ]) . Vector ( ) ] )

            return HalfHelixAxesI

          elif Parametry. HalfHelixAxesDefinition == 'PCA':

             return SetOfVectors ( [self. ExtractSlice (Range). AxisPCA () for Range in Parametry. PCASlicesRanges ] )

#####################################################################################################################################################

      def HalfHelixAxesCOM_Vector ( self ):

            """ returns Axes for EC and IC segments of Helix """
            """ calculated by Mass Center method             """

            COMs = self. ThinSlicesCOMs ( )

            if Parametry. HelixDirectionality == 'NterCter':

             if self.NterDescriptor == 'EC':

                HalfHelixAxesI = SetOfVectors ( [ SetOfPoints ( [ COMs [ 0 ], COMs [ 1 ] ] ). Vector ( ), SetOfPoints( [ COMs [ 1 ], COMs [ 2 ] ]) . Vector ( ) ] )

             elif self.NterDescriptor == 'IC':
                                                                  # E            # M                                           #M       #I
                HalfHelixAxesI = SetOfVectors ( [ SetOfPoints ( [ COMs [ 2 ], COMs [ 1 ] ] ). Vector ( ), SetOfPoints( [ COMs [ 1 ], COMs [ 0 ] ]) . Vector ( ) ] )

            elif Parametry. HelixDirectionality == 'IC_EC' :

                HalfHelixAxesI = SetOfVectors ( [ SetOfPoints ( [ COMs [ 2 ], COMs [ 1 ] ] ). Vector ( ), SetOfPoints( [ COMs [ 1 ], COMs [ 0 ] ]) . Vector ( ) ] )

            else: 
                print  self.NterDescriptor; quit ()

            return HalfHelixAxesI

#####################################################################################################################################################

      def HalfHelixAxesPCA ( self ):

          """ returns Axes for EC and IC segments of Helix """
          """ calculated by PCA method                     """

          return SetOfVectors ( [ i. AxisPCA( ) for i in self. CutInTwoParts ( ) ] ) 

#####################################################################################################################################################

      def TiltPCA ( self ):

          """ returns Tilt value for TM Helix """
          """ calculated by PCA method        """

          return self. AxisPCA ( ). AngleToZAxis ( )

#####################################################################################################################################################

      def TiltCOM_Vector ( self ):

          """ returns Tilt value for TM Helix """
          """ calculated by Mass Center method        """

          return self. AxisCOM_Vector ( ). AngleToZAxis ( )

#####################################################################################################################################################

      def Tilt ( self ):

          """ returns the Tilt value of a Helix """

          return self. MainAxis ( ). AngleToZAxis ( )

#####################################################################################################################################################

      def ZSlices ( self, BordersOfSlices ):

          """ extracts Z slices based on Z coordinate ranges """

          TMHelixInstances = [ ]; Slices = [ ]

          for N in range ( len ( BordersOfSlices ) ):
              Slices. append ( [ ] )

          for ResidueInstance in self.Content:

              Atom_Z = ResidueInstance.CA ().Z

              for N in range ( len ( BordersOfSlices ) ):

                  if Atom_Z >= BordersOfSlices [N][0] and Atom_Z <= BordersOfSlices [N][1]:
                     Slices [N].append ( ResidueInstance )

          return [ TMHelix ( Slice, self.ID ) for Slice in Slices ]

#####################################################################################################################################################

      def ExtractSlice ( self, BordersOfSlice ):

          """ extracts Z slices based on Z ranges """

          Slice = [ ]

          for ResidueInstance in self.Content:

              Atom_Z = ResidueInstance.CA ().Z

              if Atom_Z >= BordersOfSlice [0] and Atom_Z <= BordersOfSlice [1]:
                 Slice. append ( ResidueInstance )

          return  TMHelix ( Slice, self.ID )

#####################################################################################################################################################

      def CutInNParts ( self, \
                            BordersOfSlices = [ [ 10.0, 15.0 ], \
                                              [-10.0, 10.0 ],
                                              [-15.0,-10.0 ] ] \
                                                                 ): # basically by degault splits Helix Atoms into Three parts EC, MM, IC

          """ cuts the Helix into N Segments based on Z coordinate ranges input """

          return self. ZSlices ( BordersOfSlices )

#####################################################################################################################################################

      def ExtractThinSlices ( self ):

          """ returns segments extracted based on z coordinate ranges ( thin slices defined in parameter file ) """

          return self. ZSlices ( Parametry. BordersOfThinSlices )

#####################################################################################################################################################

      def ExtractWideSlices ( self ):

          """ returns segments extracted based on z coordinate ranges ( wide slices defined in parameter file ) """

          return self. ZSlices ( Parametry. BordersOfWideSlices )

#####################################################################################################################################################

      def ThinSlicesCOMs ( self ):

          """ returns Mass Centers of Thin Slices """

          return [ ThinSlice. CenterOfMass ( ) for ThinSlice in self. ExtractThinSlices ( ) ]

#####################################################################################################################################################

      def CutInTwoParts ( self ):

          """ returns two segments based on z coordinate ranges """

          BordersOfSlices = [ [ 2.0, 12.0 ], [ -12.0, -2.0 ] ]
                                  
          return self. ZSlices ( BordersOfSlices )

#####################################################################################################################################################

      def ZSlice ( self, Zmin, Zmax ):

          self.ZSliceI = [ ]

          for ResidueInstance in self.Content:

              Res_Z = ResidueInstance.Z ( )

              if Res_Z >= Zmin and Res_Z <= Zmax:

                 self.ZSliceI.append ( ResidueInstance )

          return TMHelix ( self.ZSliceI, self.ID )  

#####################################################################################################################################################

      def ZPoint ( self, Zmin, Zmax ):

          """ returns a CenterOfMass for a ZSlice """

          self.ZSlice = self.ZSlice ( Zmin, Zmax )

          self.ZPoint = SetOfAtoms ( self.ZSlice ).CenterOfMass ( )
                    
          return self.ZPoint

#####################################################################################################################################################

      def CAsCenterOfMass ( self ):

          """ returns Center Of Mass for CA atoms contained in class instance """

          return self. CAs ( ). CenterOfMass ( )

#####################################################################################################################################################

      def CalculateNterDescriptor ( self ):

          """ returns Nter location (EC or IC) """

          self.FirstRes_Z = self. Content [ 0 ] .Z ( )

          if self.FirstRes_Z >= 0.0:

             self. NterDescriptor = 'EC'

          else:

             self. NterDescriptor = 'IC'

#####################################################################################################################################################

      def ThinSlicesAASEQ ( self ):

          """ return AminoAcid sequences of Slices """

          return [ i. AASEQ ( ) for i in self. ExtractThinSlices ( ) ]

#####################################################################################################################################################

      def WideSlicesAASEQ ( self ):

          """ return AminoAcid sequences of Slices """

          return [ i. AASEQ ( ) for i in self. ExtractWideSlices ( ) ]

#####################################################################################################################################################

      def COM_Axes_EC_MM_IC ( self ):

          """ returns Axes of Half Helices        """
          """ calculated using Mass Center method """

          import GeometricalClassesModule; from GeometricalClassesModule import SetOfPoints;

          COM_EC_MM_IC_I = [ ]

          for Part in self. ExtractThinSlices ( ):

              Part_CAs = SetOfAtoms ( Part.CAs () )

              COM_EC_MM_IC_I. append ( Part_CAs.CenterOfMass ( ) )

          COM_ME_Axis = SetOfPoints ( [ COM_EC_MM_IC_I [ 1 ], COM_EC_MM_IC_I [ 0 ] ] ). Vector ( )

          COM_IM_Axis = SetOfPoints ( [ COM_EC_MM_IC_I [ 2 ], COM_EC_MM_IC_I [ 1 ] ] ). Vector ( )

          return [ COM_ME_Axis, COM_IM_Axis ]

