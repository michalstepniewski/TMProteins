import ProteinChainModule; from ProteinChainModule import ProteinChain;

import  AtomRecordModule;
from  AtomRecordModule import *;

import SetOfAtomsModule; from SetOfAtomsModule import *;

import  GeometricalClassesModule;
from GeometricalClassesModule import *;
import numpy;

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
             Axis = self. CA_XYZs ( ). PCAAxis ( )
             print [self. CA_XYZs ( ).Content[n] for n in [0,-1]]
             print SetOfPoints ([self. CA_XYZs ( ). Content[n] for n in [0,-1]]). Vector()[-1]

             if numpy.sign( SetOfPoints([self. CA_XYZs ( ).Content[n] for n in [0,-1]]).Vector()[-1]) == numpy.sign(Axis[2]):
                return Axis
             else:
                OppositeAxis = Vector ( [ -Coord for Coord in Axis ] )
                return OppositeAxis

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

      def Tilt_EC ( self ):

          """ returns the Tilt value of a Helix """

          return self. ExtractSlice([-2.0,12.0]). MainAxis ( ). AngleToZAxis ( )

#####################################################################################################################################################

      def Axis_EC ( self ):

          """ returns the Tilt value of a Helix """

          return self. ExtractSlice([-2.0,12.0]). MainAxis ( )

#####################################################################################################################################################

      def Tilt_IC ( self ):

          """ returns the Tilt value of a Helix """

          return self.ExtractSlice([-12.0,2.0]). MainAxis ( ). AngleToZAxis ( )

#####################################################################################################################################################

      def Axis_IC ( self ):

          """ returns the Tilt value of a Helix """

          return self.ExtractSlice([-12.0,2.0]). MainAxis ( )

#####################################################################################################################################################

      def KinkAngle ( self ):

          return SetOfVectors([self. Axis_EC (), self. Axis_IC ()]). AngleDEG ()

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

#####################################################################################################################################################

      def DrawAxesInPymol ( self, N ):
          import os
          
 
          CenterOfMassI = self. CenterOfMass ()     # we get CenterOfMass for the whole helix
          CenterOfMass_ICI =  self. ExtractSlice([-12.0,2.0]). CenterOfMass ()
          CenterOfMass_ECI =  self. ExtractSlice([2.0,12.0]). CenterOfMass ()
          OverhangPointsI  =  self. OverhangPoints ()

          MainAxisI     = Vector([ coord * 10.0 for coord in self.  MainAxis  ()])  # we get main Helix Axis
          ECAxisI       = Vector([ coord * 10.0 for coord in self.  Axis_EC  ()])  # we get Extracellular Axis
          ICAxisI       = Vector([ coord * 10.0 for coord in self.  Axis_IC  ()]) # we get Intracellular Axis
          
          MainAxisI. Translate(CenterOfMassI); ECAxisI. Translate(CenterOfMass_ECI);
          ICAxisI. Translate(CenterOfMass_ICI);

#musze puscic wszytkie osie
          
          CenterOfMassStr, CenterOfMassECStr, CenterOfMassICStr, MainAxisIStr, ECAxisIStr, ICAxisIStr, OverhangPointsIStr0, OverhangPointsIStr1 = [', '.join(map(str, Arg )) for Arg in [CenterOfMassI, CenterOfMass_ECI, CenterOfMass_ICI, MainAxisI, ECAxisI, ICAxisI, OverhangPointsI[0], OverhangPointsI[1] ] ]

          HelixAxesArgs = CenterOfMassStr +', '+ MainAxisIStr +', '+CenterOfMassECStr +', '+ ECAxisIStr +', '+CenterOfMassICStr +', '+ICAxisIStr+', '+OverhangPointsIStr0+', '+OverhangPointsIStr1

          BarDProtein = 'set depth_cue, 0; bg_color white; show cartoon; hide lines;set cartoon_transparency, 0.5; zoom center, 20; ray 500,500; png plik1.png; quit;'
          BarDHelix = 'set seq_view, 1;run helix_axes.py;helix_axes ' + HelixAxesArgs + ';' + BarDProtein
          TMHelixPDBFileName = self.ChainID+'_TM_'+str(N)+'_X.pdb'
# trzeba zrobic zeby sie nie robila proteina bo to za wolno
          ShellCommand = 'mkdir myproject/myapp/static/myapp/static/'+str(N)+'; cp helix_axes.py media/TMs/; cd media; pymol TMProtein.pdb -d \''+BarDProtein+'\';'+' cd TMs; pymol '+TMHelixPDBFileName +' -d \''+BarDHelix+'\';'' cd ../..; mv media/plik1.png myproject/myapp/static/myapp/static/Protein1.png;  mv  media/TMs/plik1.png myproject/myapp/static/myapp/static/'+str(N)+'/helisa.png;'

	  os. system (ShellCommand)

#####################################################################################################################################################

      def Overhang ( self, OverhangRanges = [ [1.0, 10.0], [-10.0, -1.0] ] ):

          COM_EC, COM_MM, COM_IC = self. ThinSlicesCOMs ( ) #[ 0 ]

          """
          returns the overhang
          ( it is actually a bit tricky )
          """

          ZSliceI = self. ZSlice (   OverhangRanges[0][0], OverhangRanges[0][1] )
          
          COM_EC = ZSliceI. CenterOfMass ( )
          
          Axis1 = ZSliceI. AxisPCA ( )
          
          ScalingFactor = -COM_EC[2]/Axis1 [2]
          Axis1 = Axis1. Scale ( ScalingFactor )

          ZSliceI = self. ZSlice ( OverhangRanges[1][0], OverhangRanges[1][1] )
          COM_IC = ZSliceI. CenterOfMass ( )
          Axis2 = ZSliceI. AxisPCA ( )
          ScalingFactor = -COM_IC[2]/Axis2 [2]
          Axis2 = Axis2. Scale ( ScalingFactor )

#          print Axis2

          P1 = Point(COM_EC); P2 = Point(COM_IC);

          P1. Translate ( Axis1 ); P2. Translate ( Axis2 );

#          print P1; print P2; quit ()


          return SetOfPoints ( [ P1, P2 ] ). Distance ( )

# overhang can be calculated in simplified way or in the exact way
# simplified way assumes that overhang occurs in the middle of membrane
# thus overhang is the XY distance between COM of Epsilon1 width
# at ( Z + Epsilon2 ) to (Z - Epsilon2)

#####################################################################################################################################################

      def OverhangPoints ( self, OverhangRanges = [ [1.0, 10.0], [-10.0, -1.0] ] ):

          COM_EC, COM_MM, COM_IC = self. ThinSlicesCOMs ( ) #[ 0 ]

          """
          returns the overhang
          ( it is actually a bit tricky )
          """

          ZSliceI = self. ZSlice (   OverhangRanges[0][0], OverhangRanges[0][1] )
          
          COM_EC = ZSliceI. CenterOfMass ( )
          
          Axis1 = ZSliceI. AxisPCA ( )
          
          ScalingFactor = -COM_EC[2]/Axis1 [2]
          Axis1 = Axis1. Scale ( ScalingFactor )

          ZSliceI = self. ZSlice ( OverhangRanges[1][0], OverhangRanges[1][1] )
          COM_IC = ZSliceI. CenterOfMass ( )
          Axis2 = ZSliceI. AxisPCA ( )
          ScalingFactor = -COM_IC[2]/Axis2 [2]
          Axis2 = Axis2. Scale ( ScalingFactor )

#          print Axis2

          P1 = Point(COM_EC); P2 = Point(COM_IC);

          P1. Translate ( Axis1 ); P2. Translate ( Axis2 );

#          print P1; print P2; quit ()


          return [ P1, P2 ]

# overhang can be calculated in simplified way or in the exact way
# simplified way assumes that overhang occurs in the middle of membrane
# thus overhang is the XY distance between COM of Epsilon1 width
# at ( Z + Epsilon2 ) to (Z - Epsilon2)

#####################################################################################################################################################

