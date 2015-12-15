import numpy as np
import sys;

import math; from math import *;

import functions_module
from functions_module import *;
import copy;

# module contains some useful geometrical classes and functions (methods)

#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

def Generate3DRotationMatrix ( Angle ): # angle counter-clockwise

    """ returns a rotation matrix that rotates a 3D point    """
    """ in 3D counter-clockwise by input Angle along Z axis  """

    RotationMatrix3D = [ [ cos ( Angle ), - sin ( Angle ), 0.0 ], \
                         [ sin ( Angle ),   cos ( Angle ), 0.0 ], \
                         [ 0.0,             0.0,           1.0 ] ]

    return RotationMatrix3D

#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

class SetOfVectors ( list ):

      """
      stores N K-dimensional vectors
      """

      def __init__ ( self, Vectors ):

          self. Content = [ ]

          for InputVector in Vectors:

              self.Content. append ( InputVector ) 
          
          return

#####################################################################################################################################################

          """
          returns the dihedral angle between two anchored vectors
          """

      def Dihedral ( self ):


          Axis =  SetOfPoints ( [self. Content [ 0 ]. AnchorPoint, self. Content [ 1 ]. AnchorPoint ] ). Vector ( )

          Vector1 = SetOfVectors ( [ self. Content [ 0 ], Axis ] ). VectorProduct ( )

          Vector2 = SetOfVectors ( [ Axis, self. Content [ 1 ] ] ). VectorProduct ( )

          return SetOfVectors ( [ Vector1, Vector2 ] ). AngleDEG ( )

#####################################################################################################################################################

      def VectorProduct ( self ): # ok since you can only compute cross product in 3D space, then the vectors would be 3D with Z = 0

          """
          returns VectorProduct of Two Vectors
          """

          A_3D = self.Content [ 0 ]
          B_3D = self.Content [ 1 ]

          if len ( A_3D) == 2: 

             A_3D. append ( 0.0 ) # makes it possible to do vector product for 2D vectors

          if len ( B_3D ) == 2:

             B_3D. append ( 0.0 ) # extension to 2D, add 3rd dimension

          Cx = ( A_3D [ 1 ] * B_3D [ 2 ] ) - ( A_3D [ 2 ] * B_3D [ 1 ] )
          Cy = ( A_3D [ 0 ] * B_3D [ 2 ] ) - ( A_3D [ 2 ] * B_3D [ 0 ] )
          Cz = ( A_3D [ 0 ] * B_3D [ 1 ] ) - ( A_3D [ 1 ] * B_3D [ 0 ] )

          C  = [ Cx, Cy, Cz ] 

          return Vector (C)

#####################################################################################################################################################

      def DotProduct ( self ):

          """ returns Dot Product of Two Vectors """

          DotProductI = 0.0

          for N in range( len(self.Content[0]) ):

              DotProductI += ( self.Content[0][N] * self.Content[1][N] )            

          return DotProductI

#####################################################################################################################################################

      def Angle ( self, AccountForAngleDirection = 'No' ):

          """
          returns Angle between two vectors [Rad]
          """

          self.Cos = self.DotProduct () / ( self. Content [ 0 ]. Length () * self. Content [ 1 ]. Length () ) 

          if 0.999 <= self.Cos <= 1.001: # handles exception that was occuring

             return 0.0   
           
          else: self.Angle = acos ( self.Cos )

          self. Sin = self.VectorProduct () [2] / ( self. Content [ 0 ]. Length () * self. Content [ 1 ]. Length () )

          if AccountForAngleDirection == 'Yes' and self. Sin <= 0.0:

             return ( -1.0 * self. Angle )

          return self.Angle

#####################################################################################################################################################

      def AngleDEG ( self, AccountForAngleDirection = 'No' ):

          """
          returns Angle between two vectors [DEG]
          """

          return ( (self.Angle(AccountForAngleDirection)/(2*math.pi))*360 )

#####################################################################################################################################################

      def Sum ( self ):

          """
          returns a sum of N vectors
          """

          SumI = [ 0.0 for N in range( len ( self. Content [0] ) ) ]

          for VectorI in self. Content:

              for I in range( len ( self. Content [0] ) ):

                  SumI[I] += VectorI [ I ]
          
          return Vector ( SumI )

#####################################################################################################################################################

      def RotationMatrix ( self ):

          """
          returns a rotation from 0th vector to 1st vector
          """

          return optimal_superposition( np.array( [ [ 0.0, 0.0, 0.0  ], self.Content[0] ] ), np.array( [ [ 0.0, 0.0, 0.0  ], self.Content[1] ] ) ).T

#####################################################################################################################################################
#####################################################################################################################################################

class Vector ( list ):

      """
      stores one N dimensional vector

      """
#####################################################################################################################################################

      def Translate ( self, Vector ):

          """ Translates point by Vector """

          for N in range ( len ( self ) ):
              
              self [ N ] += Vector [ N ]


#####################################################################################################################################################

      def CartesianToSpherical ( self ):

          """ transforms cartesian coordinates to spherical """

          X, Y, Z = self

          R = sqrt  ( X**2 + Y**2 + Z**2 )

          if R == 0.0: Theta = 0.0

          else: Theta = acos ( Z/R ) * ( 180 / math.pi )

          if X == 0.0: fi = 0.0

          else: fi = atan ( Y/X ) * ( 180 / math.pi )

          return Point ( [ R, Theta, fi ] )

#####################################################################################################################################################

      def AnchorInPoint ( self, Point ):

          """ anchors Vector in input Point """

          self. AnchorPoint = Point
          print self. AnchorPoint

#####################################################################################################################################################

      def ZPlaneIntersectionPoint ( self, Zz ):

          """ returns intersection Point of Vector with z = Zz plane """

          ScalingFactor = ( Zz - self.AnchorPoint [ 2] ) / self [ 2 ]

          ZPlaneIntersectionPointI = self. AnchorPoint . Translate ( self. Scale ( ScalingFactor ) )

          return ZPlaneIntersectionPointI

#####################################################################################################################################################

      def Scale ( self, ScalingFactor ):

          """
          Scales a Vector by Scaling Factor
          """          

          return [ Coord * ScalingFactor for Coord in self ]  

#####################################################################################################################################################

      def Length ( self ):

          """
          returns Length of the vector
          """

          LengthSq = 0.0;

          for N in range ( len ( self ) ): LengthSq += self [ N ]**2

          return sqrt ( LengthSq )  

#####################################################################################################################################################

      def AngleToAxis ( self, Axis, Unit = 'DEG', AccountForAngleDirection = 'No' ):

          """
          returns Angle between Vector and input Axis
          """

          VectorProduct = SetOfVectors ( [ self, Axis ] ).VectorProduct ( )

          VectorProductLength = Vector ( VectorProduct ).Length ( ) 

          SinAngle = VectorProduct [ 2 ] / ( self.Length ( ) * 1 )   # 1 being X Axis unit vector length

          if self [ 0 ] >= 0.0: # testuje dla roznych cwiartek

             Angle = asin ( SinAngle )

          elif self [ 0  ] <= 0.0:

               Angle = (math.pi/2) + ( ( math.pi/2 ) - asin ( SinAngle ) )

          if Unit == 'DEG':

             return SetOfVectors ( [ self, Axis ] ). AngleDEG ( )

          if Unit == 'RAD':

             return SetOfVectors ( [ self, Axis ] ). Angle ( AccountForAngleDirection )

#####################################################################################################################################################

      def AngleToXAxis ( self ):

          """
          returns Angle to X Axis
          """

          XAxis = Vector ( [ 1.0, 0.0, 0.0 ] )

          return self. AngleToAxis ( XAxis, Unit = 'RAD', AccountForAngleDirection = 'Yes' )

#####################################################################################################################################################

      def AngleToZAxis ( self ):

          """
          returns Angle to X Axis
          """

          ZAxis = Vector ( [ 0.0, 0.0, 1.0 ] )

          return self. AngleToAxis ( ZAxis )

#####################################################################################################################################################

      def SmallestAngleToZAxis ( self ):

          """ returns smallest Angle to Z Axis """

          ZAxis = [ 0.0, 0.0, 1.0 ]

          VectorProduct = SetOfVectors ( [ ZAxis, self ] ).VectorProduct ( )

          VectorProductLength = Vector ( VectorProduct ).Length ( ) 

          SinAngle = VectorProductLength / ( self.Length ( ) * 1.0 )   # 1 being Z Axis unit vector length

          Angle = asin ( SinAngle )

          return ( Angle/(2*np.pi) ) * 360

#####################################################################################################################################################
#####################################################################################################################################################

class Point ( list ):

      """ stores an N dimensional Point """

#####################################################################################################################################################

      def CartesianToSpherical ( self ):

          """ transforms cartesian coordinates to spherical """

          X, Y, Z = self

          R = sqrt  ( X**2 + Y**2 + Z**2 )

          if R == 0.0: Theta = 0.0

          else: Theta = acos ( Z/R ) * ( 180 / math.pi )

          if X == 0.0: fi = 0.0
         
          else: fi = atan ( Y/X ) * ( 180 / math.pi )

          return Point ( [ R, Theta, fi ] )

#####################################################################################################################################################

      def Rotate ( self, RotationMatrix  ):

          """ returns Point rotated by a Rotation Matrix """

          Point1 = [ ]

          for I in range (  len ( self ) ):
              Coord = 0.0

              for J in range ( len ( self ) ):

                  Coord += RotationMatrix [I][J] * self [J]
              Point1. append ( Coord )

          return Point1

#####################################################################################################################################################

      def Translate ( self, Vector ):

          """ Translates point by Vector """

          for N in range ( len ( self ) ):
              
              self [ N ] += Vector [ N ]

#####################################################################################################################################################

      def RotateByAngle ( self, Angle ):

          """ returns Point rotated By Angle ( in 2D) or along Z Axis """

          if len ( self ) == 2:

             RotationMatrix = Generate2DRotationMatrix ( Angle )


          elif len ( self ) == 3:

             RotationMatrix = Generate3DRotationMatrix ( Angle )
          
          Point1 = self.Rotate ( RotationMatrix )

          return Point1

#####################################################################################################################################################
#####################################################################################################################################################

class SetOfPoints ( list ):

      """ stores Set of K N Kdimensional points """

#####################################################################################################################################################

      def __init__ ( self, InputPoints ):

          """ constructs SetOfPoints class instance from input list of Point instances """

          self. Content = [ InputPoint for InputPoint in InputPoints ] 

#####################################################################################################################################################

      def RotateByAngle ( self, Angle ):

          """ returns SetOfPoints rotated By Angle ( in 2D) or along Z Axis """

          [ PointI. RotateByAngle ( Angle ) for PointI in self. Content ]

#####################################################################################################################################################

      def CartesianToSpherical ( self ):

          """ transforms cartesian coordinates of SetOfPoints to spherical """

          return SetOfPoints ( [ PointI. CartesianToSpherical ( ) for PointI in self. Content ] )

#####################################################################################################################################################

      def SuperimposeOnTemplate ( self, Template ):

          """ transforms cartesian coordinates of SetOfPoints so that it is superimposed on another another SetOfPoints ( template ) """

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

      def Superimpose3On2Template ( self, Template ):

          """ transforms cartesian coordinates of SetOfPoints so that it is superimposed on another another SetOfPoints ( template ) """
          """ for superimposing TM Helix triplet on TM Helix pair  """

          # preparation

          TemplateGeometricalCenter = Template. Center ( ) # jest ok
          SelfGeometricalCenter = FirstTwoOfSelf. Center ( )

          # done in 3 steps
          # step 1

          self. Translate ( [ -Coord for Coord in SelfGeometricalCenter ]  )
          Template. MoveToOrigin ()

          # step 2

          self. Rotate3On2Template ( Template )

          # step 3

          self. Translate ( TemplateGeometricalCenter )
          Template. Translate ( TemplateGeometricalCenter )

          return

#####################################################################################################################################################

      def Rotate3On2Template ( ):

          """ transforms cartesian coordinates of SetOfPoints so that it is rotated on another another SetOfPoints ( template ) """
          """ for superimposing TM Helix triplet on TM Helix pair  """

          FirstTwoOfSelf = SetOfPoints ( self. Content [:1] )
          RotationMatrix = SetsOfPoints ( FirstTwoOfSelf, Template )

          self. Rotate ( RotationMatrix )
          
          return

#####################################################################################################################################################

      def Print ( self ):

          """ prints the Set Of points """

          [ PointInstance. Print ( ) for PointInstance in self. Content ]

#####################################################################################################################################################

      def Vector ( self ):

          """ returns Vector pointing from 0th point to 1st Point """

          self.Vector = [ ]

          for N in range ( len ( self. Content [0] ) ):

              self.Vector. append ( self. Content [1][N] - self. Content [0][N] )  

          return Vector ( self.Vector )

#####################################################################################################################################################

      def Distance ( self ):

          """ returns Distance between first Two Points of a set """
          """ designed for set of 2 points                       """

          return self.Vector ( ). Length ()

#####################################################################################################################################################

      def PCAAxis ( self ):

          """ returns Axis through SetOfPoints determined by PCA """

          data = np.array( self. Content )
          datamean=data.mean(axis=0)
          uu, dd, vv = np.linalg.svd(data - datamean)
          PCAAxisI = vv[0]

          return Vector ( PCAAxisI )

#####################################################################################################################################################

      def DistanceToPCAAxis ( self, Axis =[] ):

          """ returns distance to Axis through SetOfPoints determined by PCA """

          if Axis != []:

             PCAAxisI = Axis

          else:

             data = np.array( self. Content )
             datamean=data.mean(axis=0)
             uu, dd, vv = np.linalg.svd(data - datamean)
             PCAAxisI = vv[0]

          MC = self. Center ()

          a = PCAAxisI [2]/ PCAAxisI[0]
          b = PCAAxisI [2]/ PCAAxisI[1] 

          c = MC[2] - (a * MC[0]) - (b * MC[1])

          SumDsq = 0.0

          for P in self. Content:

              Dsq = ( (a*P[0]) + (b*P[1]) + c - P[2] )**2 / (a**2 + b**2) #nie jestem pewien czy to jest poprawne

              SumDsq += Dsq

          return sqrt ( SumDsq ) 

#####################################################################################################################################################

      def Center ( self ):

          """ returns Geometrical center for SetOf(3D)Points """

          self. SumX, self. SumY, self. SumZ  = [ 0.0, 0.0, 0.0 ]

          for PointInstance in self.Content:

              self.SumX += PointInstance [0]
              self.SumY += PointInstance [1]
              self.SumZ += PointInstance [2]

          No = float ( len ( self.Content ) )

          return [ self.SumX/No, self.SumY/No, self.SumZ/No ] 

#####################################################################################################################################################

      def Translate ( self, Vector ):

          """ Translates each Point in a set """

          [ Point. Translate ( Vector ) for Point in self. Content ]            

#####################################################################################################################################################

      def TranslateToOrigin ( self ):

          """ Translates SetOfPoints so that Geometrical Center is now in [ 0.0, 0.0, 0.0 ] """

          VectorI = self.Center ( )
          
          return self. Translate ( [-VectorI[0],-VectorI[1],-VectorI[2] ] )

#####################################################################################################################################################

      def RotateByMatrix ( self, RotationMatrix ):

          """ rotates each Point by input Rotation Matrix """

          [ PointInstance. Rotate ( RotationMatrix ) for PointInstance in self. Content ]

#####################################################################################################################################################

      def Array (self):

          """ returns SetOfPoints as an Array """

          ciag1 = [ ]

          for i in range ( len (self.Content ) ):

              for j in range ( len(self.Content[0]) ):

                  el1 = [ float (c) for c in self.Content[i] ]

                  ciag1. append ( el1 ); # moze bede mogl to zmienic

          return np.array(ciag1)

#####################################################################################################################################################
#####################################################################################################################################################

class HierarchicalSetOfPoints ( list ):

      """ stores k instances of SetOfPoints    """
      """ this is meant for triplet of helices """
      """ where each helix is a set of points  """

#####################################################################################################################################################

      def __init__ ( self, InputSetsOfPoints ):

          """ constructs class Instance from input list of SetOfPoints instances """

          self. Content = [ InputSetOfPoints for InputSetOfPoints in InputSetsOfPoints ]

#####################################################################################################################################################

      def RotateByMatrix ( self, RotationMatrix ):

          """ rotates SetsOfPoints By Matrix """

          [ SetOfPointsInstance. RotateByMatrix ( RotationMatrix ) for SetOfPointsInstance in self. Content ]

#####################################################################################################################################################

      def Translate ( self, VectorInstance ):

          """ Translates each SetOfPoint by Vector """

          [ SetOfPointsInstance. Translate ( VectorInstance ) for SetOfPointsInstance in self. Content ]

#####################################################################################################################################################

      def CartesianToISC_IC ( self ): # we assume 6 points [ 3 x 2 ] are input

          """ returns Internal Spherical Coordinates of class Instance """
          """ meant for Helix Triplets (intracellular half)            """

          Kopia = copy.deepcopy ( self )

          Wektor = SetOfPoints ([ Kopia. Content[0]. Content[0], [0.0, 0.0, 0.0 ]]). Vector ( )

          Kopia. Translate ( Wektor );

          Kat = SetOfVectors([ SetOfPoints( [ Kopia. Content[0]. Content[0], Kopia. Content[1]. Content[0] ]).Vector(), Vector([1.0,0.0,0.0])  ]). Angle ( )

          Kopia. RotateByAngle ( -Kat )# orient H1H2 to X Axis

          R1 = Kopia. Content[1]. Content[0]. CartesianToSpherical ( ) [0]
          R2, Theta, Fi = Kopia. Content[2]. Content[0]. CartesianToSpherical ( )

          R, Theta1, Fi1 = Kopia. Content[0]. Content[1]. CartesianToSpherical ( )

          Kopia2 = copy. deepcopy ( Kopia. Content[1] )

          Wektor2 = SetOfPoints( [Kopia2. Content [ 0 ], [0.0, 0.0, 0.0 ]]). Vector ( )

          Kopia2. Translate ( Wektor2 )

          R, Theta2, Fi2 = Kopia2. CartesianToSpherical ( ). Content [1]

          Kopia3 = copy.deepcopy ( Kopia. Content[2] )

          Wektor3 = SetOfPoints( [Kopia3. Content [ 0 ], [0.0, 0.0, 0.0 ]]). Vector ( )

          Kopia3. Translate ( Wektor3 )

          R, Theta3, Fi3 = Kopia3. CartesianToSpherical ( ). Content [1]

          return [ R1, R2, Fi, Theta1, Fi1, Theta2, Fi2, Theta3, Fi3 ]

#####################################################################################################################################################
#####################################################################################################################################################

      def CartesianToISC_EC ( self ): #tu musimy przyjac kilka zalozen mamy 6 punktow [ 3 x 2 ]

          """ returns Internal Spherical Coordinates of class Instance """
          """ meant for Helix Triplets (extracellular half)            """

          Kopia = copy.deepcopy ( self )

          Wektor = SetOfPoints ([ Kopia. Content[0]. Content[1], [0.0, 0.0, 0.0 ]]). Vector ( )

          Kopia. Translate ( Wektor ); #Move to [0,0,0]

          Kat = SetOfVectors([ SetOfPoints( [ Kopia. Content[0]. Content[1], Kopia. Content[1]. Content[1] ]).Vector(), Vector([1.0,0.0,0.0])  ]). Angle ( )

          Kopia. RotateByAngle ( -Kat )

          R1 = Kopia. Content[1]. Content[1]. CartesianToSpherical ( ) [0]
          R2, Theta, Fi = Kopia. Content[2]. Content[1]. CartesianToSpherical ( )

          R, Theta1, Fi1 = Kopia. Content[0]. Content[2]. CartesianToSpherical ( )

          Kopia2 = copy. deepcopy ( Kopia. Content[1] )

          Wektor2 = SetOfPoints( [Kopia2. Content [ 1 ], [0.0, 0.0, 0.0 ]]). Vector ( )

          Kopia2. Translate ( Wektor2 )

          R, Theta2, Fi2 = Kopia2. CartesianToSpherical ( ). Content [2]

          Kopia3 = copy.deepcopy ( Kopia. Content[2] )

          Wektor3 = SetOfPoints( [Kopia3. Content [ 1 ], [0.0, 0.0, 0.0 ]]). Vector ( )

          Kopia3. Translate ( Wektor3 )

          R, Theta3, Fi3 = Kopia3. CartesianToSpherical ( ). Content [2]
          
          return [ R1, R2, Fi, Theta1, Fi1, Theta2, Fi2, Theta3, Fi3 ]

#####################################################################################################################################################
#####################################################################################################################################################

      def CartesianToISC ( self ): #tu musimy przyjac kilka zalozen mamy 6 punktow [ 3 x 2 ]

          """ returns Internal Spherical Coordinates of class Instance """

          Kopia = copy.deepcopy ( self )

          H1 = Kopia. Content[0]
          H2 = Kopia. Content[1]

          Wektor = SetOfPoints ([H1. Content[0], [0.0, 0.0, 0.0 ]]). Vector ( )

          Kopia. Translate ( Wektor ); #Move to [0,0,0]

          Kat = SetOfVectors([ SetOfPoints( [ H1. Content[0], H2. Content[0] ]).Vector(), Vector([1.0,0.0,0.0])  ] ). Angle ( )
          Kopia. RotateByAngle ( -Kat ) # orient H1H2 to X Axis

          H3 = Kopia. Content[2]

          R1            = H2. Content[0]. CartesianToSpherical ( ) [0]
          R2, Theta, Fi = H3. Content[0]. CartesianToSpherical ( )

          print Kopia. Content[0]; Kopia. Content[0]. Content[-1]; # quit ()

          R, Theta1, Fi1 = H1. Content[-1]. CartesianToSpherical ( )

          Kopia2 = copy. deepcopy ( H2 )

          Wektor2 = SetOfPoints( [Kopia2. Content [ 0 ], [0.0, 0.0, 0.0 ]]). Vector ( )

          Kopia2. Translate ( Wektor2 )

          R, Theta2, Fi2 = Kopia2. CartesianToSpherical ( ). Content [-1]

          Kopia3 = copy.deepcopy ( H3 )

          Wektor3 = SetOfPoints( [Kopia3. Content [0], [0.0, 0.0, 0.0 ]]). Vector ( )

          Kopia3. Translate ( Wektor3 )

          R, Theta3, Fi3 = Kopia3. CartesianToSpherical ( ). Content [-1]
          
          return [ R1, R2, Fi, Theta1, Fi1, Theta2, Fi2, Theta3, Fi3 ]

#####################################################################################################################################################

      def RotateByAngle ( self, Angle ):

          """ returns SetsOfPoints rotated By Angle ( in 2D) or along Z Axis """

          [ SetOfPointsI. RotateByAngle ( Angle ) for SetOfPointsI in self. Content ]

#####################################################################################################################################################

      def NonHierarchicalSetOfPoints ( self ):

          """ joins SetsOfPoints into one SetOfPoints """

          self.NonHierarchicalSetOfPointsInstance = []

          for SetOfPointsInstance in self.Content:

              for PointInstance in SetOfPointsInstance. Content:

                  self.NonHierarchicalSetOfPointsInstance. append ( PointInstance )

          return SetOfPoints ( self. NonHierarchicalSetOfPointsInstance )

#####################################################################################################################################################

      def Print ( self ):

          """ prints set Of Points """

          [ SetOfPointsInstance. Print ( ) for SetOfPointsInstance in self. Content ] 

#####################################################################################################################################################

      def Center ( self ):

          """ returns GeometricalCenter for SetsOfPoints """

          return self. NonHierarchicalSetOfPoints ( ). Center ( )    

#####################################################################################################################################################
#####################################################################################################################################################

class SetOfHierarchicalSetsOfPoints ( list ):

      """ stores N HierarchicalSetsOfPoints """
      """ meant for Sets Of Triplets        """

#####################################################################################################################################################

      def __init__ ( self, InputHierarchicalSetsOfPoints ):

          """ constructs class instance from input list of HierarchicalSetOfPoints instances """

          self. Content = [ InputHierarchicalSetOfPoints for InputHierarchicalSetOfPoints in InputHierarchicalSetsOfPoints ]

#####################################################################################################################################################

      def SuperpositionMatrix ( self, AllowPerturbations = False, AllowFlip = False ):

          """ returns rotation matrix from 0th HierSetOfPoints to 1stHierSetOfPoints """

          HierarchicalSetOfPointsInstance1, HierarchicalSetOfPointsInstance2  = self. Content

          NonHierarchicalSetOfPointsInstance1 = [ ]

          for SetOfPointsInstance in self. Content [0]:

              NonHierarchicalSetOfPointsInstance1. append ( SetOfPointsInstance )


          if AllowPerturbations:

             RMSDs = [ ]; Matrices = [ ];

             minRMSD = 1000.0

             for Perturbation in Perturbations( len ( self. Content[1] ) ):

                 PerturbationInstance = [ self. Content [ 1 ] [i] for i in Perturbation ]

                 NonHierarchicalSetOfPointsInstance2 = [ ]

                 for SetOfPointsInstance in PerturbationInstance:

                     NonHierarchicalSetOfPointsInstance2. append ( SetOfPointsInstance )
             
                 Matrices. append ( optimal_superposition ( np.array(ciag1), np.array(ciag2) ).T )
                 RMSDs. append ( rmsd (np.array(ciag1), np.array(ciag2))  )

                 if AllowFlip:

                    ciag2 = []

                    for i in range ( len (self[0] ) ):

                        for j in range ( len(self[0][0])-1,-1,-1 ):

                            el2 = [ float (c) for c in Centres1Perturbation [i][j] ]

                            ciag2. append ( el2 );
             
                    Matrices. append ( optimal_superposition ( np.array(ciag1), np.array(ciag2) ).T )
                    RMSDs. append ( rmsd (np.array(ciag1), np.array(ciag2))  )

             minRMSD = min ( RMSDs ); 

             return Matrices [ RMSDs. index ( minRMSD) ]


          else:

             ciag2 = [ ]

             for i in range ( len (self[0] ) ):

                 for j in range ( len(self[0][0]) ):

                     el2 = [ float (c) for c in self[1][i][j] ]

                     ciag2. append ( el2 );

          return optimal_superposition( np.array(ciag1), np.array(ciag2) ).T # ok a wiec gdzie jest translacja do zera?
          
#####################################################################################################################################################
#####################################################################################################################################################

class SetsOfPoints ( list ):

      """ contains N sets of points """

#####################################################################################################################################################

      def RMSD ( self ):

          """ returns RMSD between two sets of points """

          ciag1 = []; ciag2 = []

          for i in range ( len (self[0] ) ):

              for j in range ( len(self[0][0]) ):

                  el1 = [ float (c) for c in self[0][i][j] ]
                  el2 = [ float (c) for c in self[1][i][j] ]

                  ciag1. append ( el1 ); ciag2. append ( el2 );

          ciag1C = SetOfPoints ( ciag1 ). TranslateToOrigin (). Array ( ); # tu jest blad
          ciag2C = SetOfPoints ( ciag2 ). TranslateToOrigin ( ). Array ( ); # to jest template!
          
          return  rmsd (np.array(ciag1C), np.array(ciag2C)) # to bedzie z match.py

#####################################################################################################################################################

      def SuperpositionMatrix ( self, AllowPerturbations = False, AllowFlip = False ):

          """ returns rotation from 0th SetOfPoints on 1st SetOfPoints """

          ciag1 = []

          for i in range ( len ( self [0] ) ):

              for j in range ( len ( self [0][0] ) ):

                  Punkt1 = [ float ( Coord ) for Coord in self[0][i][j] ]

                  ciag1. append ( Punkt1 )

          if AllowPerturbations:

             RMSDs = [ ]; Matrices = [ ];

             minRMSD = 1000.0;

             Centres1 = self.Content[1]

             for Perturbation in Perturbations( len ( self.Content[1] ) ):

                 Centres1Perturbation = [ Centres1 [i] for i in Perturbation ]

                 ciag2 = [] 

                 for i in range ( len (self[0] ) ):

                     for j in range ( len(self[0][0]) ):

                         el2 = [ float (c) for c in Centres1Perturbation [i][j] ]

                         ciag2. append ( el2 );
             
                 Matrices. append ( optimal_superposition ( np.array(ciag1), np.array(ciag2) ).T )
                 RMSDs. append ( rmsd (np.array(ciag1), np.array(ciag2))  )

                 if AllowFlip:

                    ciag2 = []

                    for i in range ( len (self[0] ) ):

                        for j in range ( len(self[0][0])-1,-1,-1 ):

                            el2 = [ float (c) for c in Centres1Perturbation [i][j] ]

                            ciag2. append ( el2 );
             
                    Matrices. append ( optimal_superposition ( np.array(ciag1), np.array(ciag2) ).T )
                    RMSDs. append ( rmsd (np.array(ciag1), np.array(ciag2))  )

             minRMSD = min ( RMSDs ); 

             return Matrices [ RMSDs. index ( minRMSD) ]


          else:

             ciag2 = [ ]

             for i in range ( len (self[0] ) ):

                 for j in range ( len(self[0][0]) ):

                     el2 = [ float (c) for c in self[1][i][j] ]

                     ciag2. append ( el2 );

          return optimal_superposition( np.array(ciag1), np.array(ciag2) ).T # ok a wiec gdzie jest translacja do zera?

#####################################################################################################################################################
#####################################################################################################################################################

class HierarchicalSetsOfPoints ( list ):

      """ contains N HierSetsOfPoints """

      def __init__ ( self, InputHierarchicalSetsOfPoints ):

          self. Content = [ InputHierarchicalSetOfPoints for InputHierarchicalSetOfPoints in InputHierarchicalSetsOfPoints ]

#####################################################################################################################################################

      def RMSD ( self, AllowPerturbations = False, AllowFlip = False ):
         
          """ compute RMSD between 0th and 1st SetOfPoints """

          Array1 = self.Content[0]. NonHierarchicalSetOfPoints ( ). Array ( )

          if AllowPerturbations:

             RMSDs = [ ];

             minRMSD = 1000.0

             Centres1 = self. Content[1]

             for Perturbation in Perturbations( len ( self.Content [1] ) ):

                 Centres1Perturbation = [ Centres1 [i] for i in Perturbation ]

                 Array2 = Centres1Perturbation. NonHierarchicalSetOfPoints ( ). Array ( )

                 RMSDs. append ( rmsd (Array1, Array2)  )

                 if AllowFlip:

                    FlippedSet = [ Helix[::-1] for Helix in Centres1Perturbation ]
                    Array2 = FlippedSet. NonHierarchicalSetOfPoints ( ). Array ( )
             
                    RMSDs. append ( rmsd (Array1, Array2)  )

             minRMSD = min ( RMSDs ); 

          else:

             Array2 = self.Content[1]. NonHierarchicalSetOfPoints ( ). Array ( )

             return rmsd (Array1, Array2).T

#####################################################################################################################################################

      def SuperpositionMatrix ( self, AllowPerturbations = False, AllowFlip = False ):

          """ returns rotation between 0th and 1st HierSetOfPoints"""

          Array1 = self.Content[0]. NonHierarchicalSetOfPoints ( ). Array ( )

          if AllowPerturbations:

             RMSDs = [ ]; Matrices = [ ];


             minRMSD = 1000.0

             Centres1 = self. Content[1]

             for Perturbation in Perturbations( len ( self.Content [1] ) ):

                 Centres1Perturbation = [ Centres1 [i] for i in Perturbation ]

                 Array2 = Centres1Perturbation. NonHierarchicalSetOfPoints ( ). Array ( )
             
                 Matrices. append ( optimal_superposition ( Array1, Array2 ).T )
                 RMSDs. append ( rmsd (Array1, Array2)  )

                 if AllowFlip:

                    FlippedSet = [ Helix[::-1] for Helix in Centres1Perturbation ]
                    Array2 = FlippedSet. NonHierarchicalSetOfPoints ( ). Array ( )
             
                    Matrices. append ( optimal_superposition ( Array1, Array2 ).T )
                    RMSDs. append ( rmsd (Array1, Array2)  )

             minRMSD = min ( RMSDs ); 

             return Matrices [ RMSDs. index ( minRMSD) ]


          else:

             Array2 = self.Content[1]. NonHierarchicalSetOfPoints ( ). Array ( )

             return optimal_superposition( Array1, Array2 ).T

#####################################################################################################################################################
#####################################################################################################################################################
