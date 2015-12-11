import sys, math
from math import *

# module contains a few useful mathematical functions

###################################################

def Generate2DRotationMatrix ( Angle ):

    """ returns a 2D rotation matrix that rotates a 2D point """
    """ in 2D counter-clockwise by input Angle               """

    RotationMatrix2D = [ [ cos ( Angle ), - sin ( Angle ) ], \
                         [ sin ( Angle ),   cos ( Angle ) ] ]

    return RotationMatrix2D

###################################################

def Generate3DRotationMatrix ( Angle ): # angle counter-clockwise

    """ returns a rotation matrix that rotates a 3D point    """
    """ in 3D counter-clockwise by input Angle along Z axis  """

    RotationMatrix3D = [ [ cos ( Angle ), - sin ( Angle ), 0.0 ], \
                         [ sin ( Angle ),   cos ( Angle ), 0.0 ], \
                         [ 0.0,             0.0,           1.0 ] ]


    return RotationMatrix3D

###################################################

def BinarizeNat ( Nat ):

    """ returns 0 if input Natural number is 0  """
    """ and 0 otherwise                         """

    if Nat == 0:
       return 0
    else: 
       return 1

#####################################################
