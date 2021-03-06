import PdbRecordModule; from PdbRecordModule import *;

import GeometricalClassesModule;
from   GeometricalClassesModule  import Point


#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

class AtomRecord ( object ):

   """ ATOM record from PDB file """

   def __init__(self, *args, **kwargs):

       """ initializes name, cartesian coordinates (X,Y,Z), atom name and amino acid name """

       self. s = str(*args, **kwargs)
       self. X = float( self.s[(31-1):(38)] )
       self. Y = float( self.s[(39-1):(46)] )
       self. Z = float( self.s[(47-1):(54)] )
       self. XYZ = Point([ self.X, self.Y, self.Z ])

       self. Name = self.s[(13-1):(16)]
       self. AAThreeLetter = self.s [ (18-1) : (20) ]

#####################################################################################################################################################

   def __repr__ ( self ):
       print self.s

#####################################################################################################################################################

   def Element ( self ): # 77 - 78        LString(2)      Element symbol, right-justified.  

       """ atom element """

       self.ElementI = self.s [ (77-1): 78 ]

       if self.ElementI == '  ':

          self.ElementI = ' '+self.s [ 13 ] # ' ' added for internal consistency reasons

       return self.ElementI

#####################################################################################################################################################

                                  #23 - 26        Integer         Residue sequence number. 
   def ResidueSequenceNumber ( self ):

       """ returns Residue Sequence Number """

       self.ResSeqNo = int ( self.s [23:26] ) # watch out!

       return self.ResSeqNo

#####################################################################################################################################################

   def Mass ( self ):

       """ returns atom mass """

       Element = self.s [ (77-1):(79-1) ]

       ElementMassLexicon =  { ' C' : 12.011, \
                               ' H' : 1.008 , \
                               ' O' : 15.999, \
                               ' N' : 14.007, \
                               ' P' : 30.973762, \
                               ' S' : 32.06         }

       try:

            Mass = ElementMassLexicon [ Element ]

       except KeyError:

            Element = ' '+self.s [ 13 ]
            Mass = ElementMassLexicon [ Element ]

       return Mass

#####################################################################################################################################################

   def AA ( self ):

       """ returns amino acid name as one letter """

       ThreeLetterToOneLetterLexicon      = { 'ARG' : 'R', \
                                              'HIS' : 'H', \
                                              'LYS' : 'K', \
                                              'ASP' : 'D', \
                                              'GLU' : 'E', \
                                              'SER' : 'S', \
                                              'THR' : 'T', \
                                              'ASN' : 'N', \
                                              'GLN' : 'Q', \
                                              'CYS' : 'C', \
                                              'SEC' : 'U', \
                                              'GLY' : 'G', \
                                              'PRO' : 'P', \
                                              'ALA' : 'A', \
                                              'VAL' : 'V', \
                                              'ILE' : 'I', \
                                              'LEU' : 'L', \
                                              'MET' : 'M', \
                                              'PHE' : 'F', \
                                              'TYR' : 'Y', \
                                              'TRP' : 'W', \
                                              'UNK' : 'X'    }

       self.AAOneLetter = ThreeLetterToOneLetterLexicon [ self.AAThreeLetter ] 
    
       return self.AAOneLetter

#####################################################################################################################################################

   def Chain ( self ):

       """ returns Protein Chain ID of atom """

       self.ChainID = self.s [ (22-1) ]

       return self.ChainID

#####################################################################################################################################################

   def VdWRadius ( self ):

       """ returns VdW radius of atom """

       ElementRadiusLexicon = { ' H' : 1.20, \
                                ' C' : 1.70, \
                                ' N' : 1.55, \
                                ' O' : 1.52, \
                                ' F' : 1.47, \
                                ' P' : 1.80, \
                                ' S' : 1.80, \
                                'CL' : 1.75, \
                                'CU' : 1.4, }

       VdWRadiusI = ElementRadiusLexicon [ self.Element() ]

       return VdWRadiusI

#####################################################################################################################################################

   def RotateByMatrix ( self, RotationMatrix ):

       """ rotates atom by given matrix """

       self. XYZ. Rotate ( RotationMatrix )

       [ self. X, self.Y, self.Z ]  = self. XYZ # ok :)

       self.s = self.s [ :30 ]+ ''.join( [ '%8.3f' % Coord for Coord in self. XYZ ]) +self.s[ 54: ]

#####################################################################################################################################################

   def Translate ( self, Vector ):

       """ translates atom by given vector """

       self. XYZ. Translate ( Vector )

       [ self. X, self.Y, self.Z ]  = self. XYZ

       self.s = self.s [ :30 ]+ ''.join( [ '%8.3f' % Coord for Coord in self. XYZ ]) + self.s[ 54: ]

