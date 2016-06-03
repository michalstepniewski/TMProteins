#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################
# passing parameters, lalala
import sys

import Parametry


#quit ( )
# system zaleznosci jest kijowy

import TMHelixModule;
import AtomRecordsModule;
from AtomRecordsModule import Setof2AtomRecords;

import SetOfAtomsModule
from SetOfAtomsModule import SetOfResidues


import GeometricalClassesModule as GeometricalClassesModule;
from GeometricalClassesModule import *;

import N_TMs_Sets; from N_TMs_Sets import SetOfK_N_TMs_Sets;

#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

class N_TMs_Set ( list ): # musze zrobic od razu na N secie

      """
      stores a set of N Transmembrane Helices
      """

#####################################################################################################################################################
        
      def __init__ ( self, InputTMHelixInstances ):

          self. Content = InputTMHelixInstances
          self. Order = len ( self. Content )
          self. HelixIDs = [TM.ID for TM in self. Content]
          self. HelixNterDescriptors = [TM. NterDescriptor for TM in self. Content ]
#          selParametryInstance = ReadParameterFile ( './DaneWejsciowe/PlikiZParametrami/PlikZParametrami.txt' )

#          print self. ParametryInstance. ReferenceFrame

#####################################################################################################################################################

      def Rotate ( self, Matrix ):

          [Helix. Rotate ( Matrix ) for Helix in self. Content]

          return

#####################################################################################################################################################

      def CenterOfMass ( self ):

          TM_COM_Set = [i. CenterOfMass ( ) for i in self.Content]

          return SetOfPoints ( TM_COM_Set ). CenterOfMass ( ) # because the classical way is to align COMs and then rotate, so the translation would be to put both vectors to 0,0,0

#####################################################################################################################################################

      def OutputToPdbFile ( self, Path ):

          self.HelixIDsI = self.HelixIDs

          FileName = Path;

          for HelixID in self.HelixIDsI:

              FileName = FileName +'_'+ str ( HelixID )

          FileName = FileName + '.pdb'

          OpenedFileInstance = open ( FileName, 'w' )

          for TMHelixInstance in self.Content:

              for ResidueInstance in TMHelixInstance.Content:

                  for AtomRecordInstance in ResidueInstance.Content:

                      OpenedFileInstance.write ( AtomRecordInstance.s ) # powinienem to bardziej hierarchicznie zdefiniowac I pass File Instance to another file  

          OpenedFileInstance.flush ( ); OpenedFileInstance.close ( );

#####################################################################################################################################################

      def Print ( self ):

          for TMHelixInstance in self.Content: TMHelixInstance.Print ( )

#####################################################################################################################################################

      def VdWContactPattern ( self ):             # ie. how many contacts in EC and IC Parts

          TM1_Parts, TM2_Parts = [ i. CutInNParts ( ) for i in self.Content ] # moze dlatego ze to juz zwraca TMHelix

          return [ N_TMs_Set ( [TM1_Parts [ N ], TM2_Parts [ N ] ]). VdWContactsNoAndResiduePairs ( ) [0] for N in range ( len ( TM1_Parts ) ) ]

#####################################################################################################################################################

      def VdWContactPatternMatrices ( self ): # jak operowac na matrycach

          CPM_EC = [ [ 0 for i in range( self. Order )] for j in range ( self. Order ) ]
          CPM_MM = [ [ 0 for i in range( self. Order )] for j in range ( self. Order ) ]
          CPM_IC = [ [ 0 for i in range( self. Order )] for j in range ( self. Order ) ]

          for i in range( self. Order ):

              for j in range ( self. Order ):
                  
                  if i==j: CPM_EC[i][j], CPM_MM[i][j], CPM_IC[i][j] = [0,0,0]
                  
                  else:
                     CPM_EC[i][j], CPM_MM[i][j], CPM_IC[i][j] = N_TMs_Set ( [ self.Content[i], self.Content[j] ] ). VdWContactPattern ( )
 
          return [ CPM_EC, CPM_MM, CPM_IC ] # musze jakos sprawdzic, czy ten skrot dziala

#####################################################################################################################################################

      def ContactPatternBinaryMatrices ( self ):

          EC_MM_IC = self. ContactPatternMatrices ( )
          Bin_EC_MM_IC = [ ]

          for MatrixInstance in EC_MM_IC:

              Bin_EC_MM_IC. append ( BinarizeMatrix ( MatrixInstance ) )

          return Bin_EC_MM_IC

#####################################################################################################################################################

      def ContactPatternMatricesResiduePairs( self ): # dlatego musze sie zastanowic jak to ma wygladac
# dla N = 2

          CPM_EC =  [[ [] for i in range ( self. Order) ] for j in range ( self. Order ) ]
          CPM_MM =  [[ [] for i in range ( self. Order) ] for j in range ( self. Order ) ]
          CPM_IC =  [[ [] for i in range( self. Order) ] for j in range ( self. Order )  ]

          for i in range ( self.Order ):
 
             for j in range ( self.Order ):

                  if i==j: CPM_EC[i][j], CPM_MM[i][j], CPM_IC[i][j] = [ [], [], [] ]

                  else:

                   CPM_EC[i][j], CPM_MM[i][j], CPM_IC[i][j] = N_TMs_Set ( [ self.Content[i], self.Content[j] ] ). VdWContactPattern3ResiduePairs ()

# ok, jest uproszczone, ale trzeba jeszcze lepiej
 
          return [ CPM_EC, CPM_MM, CPM_IC  ] # na razie nie zmieniam nazw, fajnie jakby miec szablon funkcji i tylko zmieniac te funkcje w srodku

#####################################################################################################################################################

      def MainAxis ( self ): # w jaki sposob definiujemy glowna os trypletu, a moze to os z?

          if Parametry. TripletMainAxisDefinition == 'SumOfMainAxesOfHelices': 

             return self. MainAxisSumOfMainAxesOfHelices ( )

#####################################################################################################################################################

      def MainAxisSumOfMainAxesOfHelices ( self ):

          HelixAxes = [ i. MainAxis (  ) for i in self. Content ]

           # wektory powinny byc zdefiniowane w n wymiarowej przestrzeni

          AxisI = SetOfVectors ( HelixAxes ). Sum ( )

          LengthI = AxisI. Length ()

          return Vector ( [ AxisI[0] / LengthI, AxisI[1] / LengthI, AxisI[2] / LengthI  ] )

#####################################################################################################################################################
# passing class instance as function argument python
# musze poeksperymentowac :)

      def SuperimposeMainAxisonZAxis ( self ):

          RotationMatrix = SetOfVectors ( [ self.MainAxis(), [0.0, 0.0, 1.0] ] ). RotationMatrix ( )

          self. RotateByMatrix ( RotationMatrix )

          return

#####################################################################################################################################################

      def VdWContactPattern3ResiduePairs ( self ):             # ie. how many contacts in EC and IC, defined for N = 2


          TM1_Parts, TM2_Parts = [ i.CutInNParts ( ) for i in self.Content ]      

          return [ N_TMs_Set ( [ TM1_Parts [N], TM2_Parts [N] ] ). VdWContactsNoAndResiduePairs ( ) [1] for N in range ( len ( TM1_Parts ) ) ]

#####################################################################################################################################################

#      def HelixNterDescriptors ( self ):
# this is also tricky! 

#          return [ TMHelixInstance. NterDescriptor for TMHelixInstance in self.Content ]

#####################################################################################################################################################

      def RelativeOrientationMatrix ( self ):

          ROM = [ [ 'AP' for i in range ( self. Order )] for j in range ( self. Order ) ]

          NterDescriptors = self.HelixNterDescriptors 

          for i in range ( self. Order ):

              for j in range ( self. Order ):

                  if NterDescriptors[i] == NterDescriptors[j]:

                     ROM [i][j] ='P' 

          return ROM

#####################################################################################################################################################

      def HelixTiltsPCA ( self ):

          return [ TM. TiltPCA ( ) for TM in self.Content ]

#####################################################################################################################################################

      def HelixTiltsCOM_Vector ( self ):

          return [ TM. TiltCOM_Vector ( ) for TM in self.Content ]


#####################################################################################################################################################

      def HelixTilts ( self ):

          return [ TM. Tilt ( ) for TM in self.Content ]

#####################################################################################################################################################

      def HalfHelixTilts ( self ): # to jest matryca, wiec

          EC_Tilts = [ 0.0 for i in range( self. Order ) ]
          IC_Tilts = [ 0.0 for i in range( self. Order ) ]

          for i in range ( self. Order ):

              EC_Tilts[i], IC_Tilts[i]  = self. Content[i]. HalfHelixTilts ()  # musze sprawdzic, czy sie da assignowac podwojnie
# nie da sie inaczej na razie bo inaczej bedzie wpisywac rzedy do arrayow
          return [ EC_Tilts, IC_Tilts ]

#####################################################################################################################################################

      def HalfHelixTiltsPCA ( self ): # to jest matryca, wiec

          EC_Tilts = [ 0.0 for i in range( self. Order ) ]
          IC_Tilts = [ 0.0 for i in range( self. Order ) ]

          for i in range ( self. Order ):

              EC_Tilts[i], IC_Tilts[i]  = self. Content[i]. HalfHelixTiltsPCA ()  # musze sprawdzic, czy sie da assignowac podwojnie
# nie da sie inaczej na razie bo inaczej bedzie wpisywac rzedy do arrayow
          return [ EC_Tilts, IC_Tilts ]

#####################################################################################################################################################

      def HalfHelixTiltsCOM_Vector ( self ): # to jest matryca, wiec

          EC_Tilts = [ 0.0 for i in range( self. Order ) ]
          IC_Tilts = [ 0.0 for i in range( self. Order ) ]

          for i in range ( self. Order ):

              EC_Tilts[i], IC_Tilts[i]  = self. Content[i]. HalfHelixTiltsCOM_Vector ()  # musze sprawdzic, czy sie da assignowac podwojnie
# nie da sie inaczej na razie bo inaczej bedzie wpisywac rzedy do arrayow
          return [ EC_Tilts, IC_Tilts ]

#####################################################################################################################################################

      def MinimumDistanceMatrices ( self ):

          EC = [ [ 0.0 for i in range( self. Order ) ] for j in range ( self. Order ) ]
          MM = [ [ 0.0 for i in range( self. Order ) ] for j in range ( self. Order ) ]
          IC = [ [ 0.0 for i in range( self. Order ) ] for j in range ( self. Order ) ]

          for i in range ( self. Order ):

              for j in  range ( self. Order ): 
# glupio sie czuje to kopiujac, ta funkcja powinna od razu zwracac tez pary residuow

                  EC[i][j], MM[i][j], IC[i][j] = N_TMs_Set ( [ self.Content[i], self.Content[j] ] ).MinimumDistancePattern ( )
 
          return [ EC, MM, IC ]

#####################################################################################################################################################

      def MinimumDistancePattern ( self ):             # ie. how many contacts in EC and IC Parts, defined for N = 2
 
          TM1, TM2 = self.Content

          TM1_Parts = TM1.CutInNParts ( )
          TM2_Parts = TM2.CutInNParts ( )

          TM1_Parts, TM2_Parts = [ i.CutInNParts ( ) for i in self.Content ]                

          return [ N_TMs_Set ( [ TM1_Parts [ N ], TM2_Parts [ N ] ] ). MinimumDistance ( ) for N in range ( len ( TM1_Parts ) ) ]

#####################################################################################################################################################

      def MinimumDistance ( self ): # fajnie jakby byl szablon dla tych metod, moge stworzyc taki szablon, defined for N = 2

          self.MinimumDistanceI = 1000.0

          TM1, TM2 = self.Content

          for TM1ResidueInstance in TM1.Content:

              for TM2ResidueInstance in TM2.Content:

                  self.MinimumDistanceI = min ( self.MinimumDistanceI, Setof2AtomRecords ( [ TM1ResidueInstance. CA(), TM2ResidueInstance. CA() ] ). Distance()  )

          return self.MinimumDistanceI

#####################################################################################################################################################

      def AlignOnZAxis ( ):

          return

#####################################################################################################################################################

      def CrossingAngle ( ):

          return

#####################################################################################################################################################

      def HelixKinkAngles ( self ):

#          self. HelixKinkAngles = 

          return [ TMHelixI. KinkAngle () for TMHelixI in self. Content ]

#####################################################################################################################################################

      def HelixOverhangLengths ( self ):

          return [ TMHelixI. Overhang () for TMHelixI in self. Content ]

#####################################################################################################################################################

# nie wiem gdzies musze to inicjowac, hmmm
      def OutputRepresentation ( self, ProteinNterDescriptor = 'XX',Path='DummyPath' ): # to PDB(like) format file

          print 'OutputtingRepresentation'

# moze zadziala
          if Parametry. ReferenceFrame == 'MainAxis': # bez sensu troche ze nie mozna passowac argumentow

             self. SuperimposeMainAxisonZAxis ( )

# ech, na razie tyle

          line = '#REMARK  HELIX IDS                        '

          self.HelixIDsI = self.HelixIDs

          StrHelixIDs = [ str(i) for i in self.HelixIDs ]

          File_Name = Path + '_' + '_'.join ( [ str(i) for i in self.HelixIDs ] ) + '_Representation.txt'

          print File_Name

          file = open ( File_Name, 'w' ) 
          
          TMLine = '#REMARK  HELIX IDS  TM'+ '  TM'. join ( StrHelixIDs ) + '\n';

          file. write ( TMLine );

          line = '#REMARK\n'; file. write ( line );

# na razie wygaszamy
#          line = '#REMARK MM SLICE COMs (TM'+ID1+'-TM'+ID2+')|(TM'+ID2+'-TM'+ID3+') vectors Angle [DEG] %8.3f\n' % self. MMTM1TM2TM3VectorsAngleDEG ( ); file. write ( line );
# %8.3f
#          line = line +'%8.3f\n'  str ( self. MMTM1TM2TM3VectorsAngleDEG ( ) ) + '\n'; file. write ( line )

          line = '#REMARK\n'; file. write ( line );

          line = '#REMARK Clockwise/AntiClockwise (Nter EC)        '
#          line = line + self.ClockwiseAntiClockwise() + '\n'; file. write ( line ); 
          line = '#REMARK\n'; file. write ( line );


          line = '#REMARK PCA TILTS OF HELICES to Z AXIS [DEG] \n'; file. write ( line );
          file. write ( 'TM'+ '  TM'. join ( StrHelixIDs ) + '\n' );
          line = ''.join( [ '%8.3f' % HelixTiltPCA for HelixTiltPCA in self. HelixTiltsPCA ( ) ]) + '\n'; file. write ( line );
          line = '#REMARK\n'; file. write ( line );

          line = '#REMARK COM VECTOR TILTS OF HELICES to Z AXIS [DEG] \n'; file. write ( line );
          file. write ( 'TM'+ '  TM'. join ( StrHelixIDs ) + '\n' );
          line = ''.join( [ '%8.3f' % HelixTiltCOM_Vector for HelixTiltCOM_Vector in self. HelixTiltsCOM_Vector ( ) ]) + '\n'; file. write ( line );
          line = '#REMARK\n'; file. write ( line );

          line = '#REMARK  KINK ANGLES OF HELICES to Z AXIS [DEG] \n'; file. write ( line );
          file. write ( 'TM'+ '  TM'. join ( StrHelixIDs ) + '\n' );
          line = '#REMARK\n'; file. write ( line );
          line = ''.join( [ '%8.3f' % HelixKinkAngle for HelixKinkAngle in self. HelixKinkAngles ( ) ]) + '\n'; file. write ( line );

          line = '#REMARK OVERHANG LENGTHS OF HELICES to Z AXIS [DEG] \n'; file. write ( line );
          file. write ( 'TM'+ '  TM'. join ( StrHelixIDs ) + '\n' );
          line = '#REMARK\n'; file. write ( line );
          line = ''.join( [ '%8.3f' % HelixOverhangLength for HelixOverhangLength in self. HelixOverhangLengths ( ) ]) + '\n'; file. write ( line );

          line = '#REMARK\n'; file. write ( line );

          line = '#REMARK  PCA TILTS OF HALF HELICES to Z AXIS [ DEG ]\n '; file. write ( line );
          file. write ( 'TM'+ '  TM'. join ( StrHelixIDs ) + '\n' );
          line = '#REMARK                                       EC '; file. write ( line );
          line = ''.join(['%8.3f' % ECHalfHelixTiltPCA for ECHalfHelixTiltPCA in self.HalfHelixTiltsPCA ()[ 0 ] ]) + '\n'; file. write ( line );
          line = '#REMARK                                       IC '; file. write ( line );   
          line =''.join(['%8.3f' % ICHalfHelixTiltPCA for ICHalfHelixTiltPCA in self.HalfHelixTiltsPCA ()[ 1 ] ])+'\n'; file.write ( line );               
          line = '#REMARK\n'; file. write ( line );

          line = '#REMARK  COM VECTOR TILTS OF HALF HELICES to Z AXIS [ DEG ]\n '; file. write ( line );
          file. write ( 'TM'+ '  TM'. join ( StrHelixIDs ) + '\n' );
          line = '#REMARK                                       EC '; file. write ( line );
          line = ''.join(['%8.3f' % ECHalfHelixTiltCOM_Vector for ECHalfHelixTiltCOM_Vector in self.HalfHelixTiltsCOM_Vector ()[ 0 ] ]) + '\n'; file. write ( line );
          line = '#REMARK                                       IC '; file. write ( line );   
          line =''.join(['%8.3f' % ICHalfHelixTiltCOM_Vector for ICHalfHelixTiltCOM_Vector in self.HalfHelixTiltsCOM_Vector ()[ 1 ] ])+'\n'; file.write ( line );               
          line = '#REMARK\n'; file. write ( line );

# how to resolve aminoacid preference? 
#          line = '#REMARK  ContactPatternMatrix      TM'+ID1+'/TM'+ID2+'  TM'+ID2+'/TM'+ID3+'  TM'+ID1+'/TM'+ID3+'\n'; file. write ( line );

          file. write ( 'TM'+ '  TM'. join ( StrHelixIDs ) + '\n' );
# musze sie polozyc i odpoczac ale jestem na pewno na dobrej drodze ... :) 
          
          BinaryContactPatternMatrices = self. VdWContactPatternMatrices ()  # wiec powinno chodzic

          for N in range ( len (BinaryContactPatternMatrices) ):
              line = '#REMARK\n'; file. write ( line );

              BinaryContactPatternMatrix = BinaryContactPatternMatrices [ N ]
              
              Halfs = ['EC','IC','Main']; Threes = ['EC','MM','IC']; Halfs2 = ['EC','IC','Main'];

              for I in range ( len ( BinaryContactPatternMatrix  ) ): # mysle ze cos zle zrobilem

                  line ='#REMARK  ContactPatternMatrix  '+Threes[N]+'        '+'        '.join ( [ str(i) for i in BinaryContactPatternMatrix [ I ] ] ) +'\n'; file. write ( line ); 

              line = '#REMARK\n'; file. write ( line );
# musze zmienic format tego

          CONTACT_RESIDUES_MATRICES =  self.ContactPatternMatricesResiduePairs()
# zmieniam format
          for N in range ( len ( CONTACT_RESIDUES_MATRICES ) ):

              CONTACT_RESIDUES_MATRIX = CONTACT_RESIDUES_MATRICES [ N ]

              for I in range ( len ( CONTACT_RESIDUES_MATRIX ) ):

                  line = '# CONTACT RESIDUES '+Threes [ N ]+'\t'+'\t'.join([str(i) for i in CONTACT_RESIDUES_MATRIX [ I ]])+ '\n'; file. write ( line );


          MinimumDistanceMatricesI = self.MinimumDistanceMatrices ()

          for N in range ( len ( MinimumDistanceMatricesI ) ):

              line = '#REMARK\n'; file. write ( line );

              MinimumDistanceMatrix = MinimumDistanceMatricesI [ N ]

              for I in range ( len ( MinimumDistanceMatrix ) ):

                  line = '#REMARK  MinimumDistanceMatrix  ' + Threes [ N ]+''.join(['%9.3f' %Distance for Distance in MinimumDistanceMatrix [ I ] ])+ '\n'; file. write ( line );

          line = '#REMARK\n'; file. write ( line );

          line = '#REMARK NterDescriptors Protein '+'TM'+ '  TM'. join ( StrHelixIDs ) + '\n'; file. write ( line );

# i should leave it for later

          line = '#REMARK                      '+ProteinNterDescriptor + ' '.join ( self.HelixNterDescriptors  ) + '\n'; file. write ( line );

          line = '#REMARK\n'; file. write ( line );
# zmienic na matryce
          line = '#REMARK RelativeOrientationMatrix '+'TM'+ '  TM'. join ( StrHelixIDs ) + '\n'; file. write ( line );
          
          line = '#REMARK                      '; 
          RelativeOrientationMatrixI =  self. RelativeOrientationMatrix ( )

          for I in range ( len ( RelativeOrientationMatrixI  ) ):
              line='#REMARK RelativeOrientationMatrix '+' '.join( RelativeOrientationMatrixI[I]  )+'\n'; file. write ( line );

#              line = line + ' '+HelixRelativeOrientation;
# zrobie sobie matryce 

# zmienic na matryce
          CrossingAnglesMatricesI = self. CrossingAnglesMatrices ( )

          for N in range( len (CrossingAnglesMatricesI) ):

              line = '#REMARK\n'; file. write ( line );

              for I in range( len (CrossingAnglesMatricesI[N]) ):

                  JoinLista = "".join(format(x, "8.3f") for x in CrossingAnglesMatricesI[N][I])

                  line='#REMARK CrossingAnglesMatrix '+Halfs2[N]+' '+JoinLista+'\n'; file. write ( line );  

          CrossingAnglesMatricesI = self. DihedralAnglesMatrices ( )

          for N in range( len (CrossingAnglesMatricesI) ):

              line = '#REMARK\n'; file. write ( line );

              for I in range( len (CrossingAnglesMatricesI[N]) ):

                  JoinLista = "".join(format(x, "8.3f") for x in CrossingAnglesMatricesI[N][I])

                  line='#REMARK DihedralAnglesMatrix '+Halfs[N]+' '+JoinLista+'\n'; file. write ( line );         

          line = '#REMARK\n'; file. write ( line );
          line = '#STARTMDL\n'; file. write ( line );

# moglbym sprobowac to uruchomic, ale lepiej jest miec tez hmmm projekt plakatu, hmmm zobacze czy zadziala :)          
#           
          for Helix in self.Content: # musze to lepiej ogarnac, ale na razie tyle

              IDi = Helix.ID

              Helix.EcAASEQ, Helix.MmAASEQ, Helix.IcAASEQ = Helix. WideSlicesAASEQ ( )
              EC_COM, MM_COM, IC_COM = Helix. ThinSlicesCOMs ( )
              EC_1_3_VEC, IC_1_3_VEC = Helix.EC_IC_1_3_VECs ( ) # agdzie MM, aa nie potrzeba 
              

#              EM_Axis, IM_Axis = Helix.HalfHelixAxes ( ) # moze to cos w inicie wiec

              EM_Axis, IM_Axis = Helix. HalfHelixAxes ( ). Content # zmniejszyc ilosc wywolan funkcji
              EM_AxisDev, IM_AxisDev = Helix. HalfHelixAxesDevs ( ) # zmniejszyc ilosc wywolan funkcji

              line = '#AASEQ '+Helix.EcAASEQ +'\n'; file. write ( line );

              line = '#CENTRE    TM%2d EC %8.3f %8.3f %8.3f\n' %( IDi, EC_COM[0], EC_COM[1], EC_COM[2] ); file. write ( line );
              line = '#1-3VEC    TM%2d EC %8.3f %8.3f %8.3f\n' %( IDi, EC_1_3_VEC[0], EC_1_3_VEC[1], EC_1_3_VEC[2] ); file. write ( line );
              line = '#AXIS      TM%2d EM %8.3f %8.3f %8.3f\n' %( IDi, EM_Axis[0], EM_Axis[1], EM_Axis[2] ); file. write ( line );
              line = '#AxisDev   TM%2d EM %8.3f\n' %( IDi, EM_AxisDev); file. write ( line );
  
              line = '#AASEQ '+Helix.MmAASEQ+'\n'; file. write ( line );
              line = '#CENTRE    TM%2d MM %8.3f %8.3f %8.3f\n' %( IDi, MM_COM[0], MM_COM[1], MM_COM[2] ); file. write ( line );  
              line = '#1-3VEC    TM%2d IC %8.3f %8.3f %8.3f\n' %( IDi, IC_1_3_VEC[0], IC_1_3_VEC[1], IC_1_3_VEC[2] );file. write ( line);            
              line = '#AXIS      TM%2d IM %8.3f %8.3f %8.3f\n' %( IDi, IM_Axis[0], IM_Axis[1], IM_Axis[2] ); file. write ( line );
              line = '#AxisDev   TM%2d IM %8.3f\n' %( IDi, IM_AxisDev); file. write ( line );

              line = '#AASEQ '+Helix.IcAASEQ+'\n'; file. write ( line );
              line = '#CENTRE    TM%2d IC %8.3f %8.3f %8.3f\n' %( IDi, IC_COM[0], IC_COM[1], IC_COM[2] ); file. write ( line );
              line = '#TER\n'; file. write ( line );
              line = Helix. AASEQ_Z ( ); file. write ( line );

          line = '#ENDMDL\n'; file. write ( line );

######################## drukuje IC_ISC ###############################################################

          line = 'printing ISC\n'; file. write ( line );

#          print [SetOfPoints( [ Point( PointI ) for PointI in Helix. ThinSlicesCOMs ( ) ] ) for Helix in self.Content];
#          quit ();

          self. ISC = HierarchicalSetOfPoints ( [ SetOfPoints( [ Point( PointI ) for PointI in Helix. ThinSlicesCOMs ( ) ] ) for Helix in self.Content ] ). CartesianToISC ( ); # niech bedzie dolnych upakowanie
# musze sobie podzielic

          line = str ( self.ISC ) + '\n'; file. write ( line ); # make more efficient
# to nie moze byc to samo, musze miec EC_ISC i IC_ISC, nie wiem czemu boli mnie glowa

          line = 'printing IC ISC\n'; file. write ( line );

          self. IC_ISC = HierarchicalSetOfPoints ( [ SetOfPoints( [ Point( PointI ) for PointI in Helix. ThinSlicesCOMs ( )[1:]] ) for Helix in self.Content ] ). CartesianToISC ( ); # niech bedzie dolnych upakowanie
# musze sobie podzielic

          line = str ( self.IC_ISC ) + '\n'; file. write ( line ); # make more efficient
# to nie moze byc to samo, musze miec EC_ISC i IC_ISC, nie wiem czemu boli mnie glowa
##################### wydrukowal IC_ISC ###############################################################
################################## drukuje EC_ISC (dopiero co dodalem) ################################

          line = 'printing EC ISC\n'; file. write ( line );

          self. EC_ISC = HierarchicalSetOfPoints ( [ SetOfPoints( [ Point( PointI ) for PointI in Helix. ThinSlicesCOMs ( )[:2]] ) for Helix in self.Content ] ). CartesianToISC ( ); # niech bedzie dolnych upakowanie
          
          line = str ( self.EC_ISC ) + '\n'; file. write ( line ); # make more efficient

##############################  wydrukowal EC_ISC (dopiero co dodalem) ################################


          [r, theta,fi, theta1, fi1, theta2, fi2, theta3, fi3 ] = HierarchicalSetOfPoints ( [ SetOfPoints( [ Point( PointI ) for PointI in Helix. ThinSlicesCOMs ( )[1:]] ) for Helix in self.Content ] ). CartesianToISC ( ); # niech bedzie dolnych upakowanie

          Fis = [ str(fi1), str(fi2) ] # kolumny Fi1 i Theta1 sa sobie rowne, czy we wszystkich czy tylko w jednym?
          # poszukac w reprezentacjach

          MMFis = [ ]

          for N in range( len(self.Content)-2 ):

              r, theta,fi, theta1, fi1, theta2, fi2, theta3, fi3  = HierarchicalSetOfPoints ( [ SetOfPoints( [ Point ( PointI ) for PointI in Helix. ThinSlicesCOMs ( )[1:]] ) for Helix in [ self.Content[0], self.Content[1], self.Content[N+3-1] ] ] ). CartesianToISC ( );

              MMFis. append ( str(fi) )

              Fis. append ( str(fi3) )

########################################### drukuje IC Fis ############################################

          line = 'IC Fis\n'; file. write ( line );

          line = ' '.join( Fis ) + '\n'; file. write ( line );

################################### wydrukowal IC Fis #################################################

          line = 'printing EC ISC\n'; file. write ( line );

          line = str ( self.ISC ) + '\n'; file. write ( line );

########################################################################################################
# kalkuluje i drukuje EC Fis #

          [r, theta,fi, theta1, fi1, theta2, fi2, theta3, fi3 ] = HierarchicalSetOfPoints ( [ SetOfPoints( [ Point( PointI ) for PointI in Helix. ThinSlicesCOMs ( )[:2][::-1]] ) for Helix in self.Content ] ). CartesianToISC ( ); # niech bedzie dolnych upakowanie

          Fis = [ str(fi1), str(fi2) ]

# wiec teraz to co brakuje to ery i 

          for N in range( len(self.Content)-2 ):

              r, theta,fi, theta1, fi1, theta2, fi2, theta3, fi3  = HierarchicalSetOfPoints ( [ SetOfPoints( [ Point ( PointI ) for PointI in Helix. ThinSlicesCOMs ( )[:2][::-1]] ) for Helix in [ self.Content[0], self.Content[1], self.Content[N+3-1] ] ] ). CartesianToISC ( );

              Fis. append ( str(fi3) )


          line = 'EC Fis\n'; file. write ( line );

          line = ' '.join( Fis ) + '\n'; file. write ( line );

#######################################################################################################

          line = 'MM 1-2-3 Fis\n'; file. write ( line );

          line = ' '.join( MMFis ) + '\n'; file. write ( line );       

#######################################################################################################

          print 'Representation File written'

# i have to check the Contact Pattern Matrix so it is in agreement / derived from Minimum Distance Matrix

#####################################################################################################################################################

      def MinimizeInModeller ( self ):

          self.OutputToPdbFile ( PreminimizedPDBFilePath )

          ModellerOptimize ( PreminimizedPDBFilePath )

          MinimizedNSet = ReadNSetFromOwnPDB ( ModellerPreminimizedPDBPath+'.B'  )

          return MinimizedNSet

#####################################################################################################################################################

      def TransformToFitCOMCoordsTemplate ( self, COMCoordsTemplate ):

          [ Helix.FitToRepresentation ( COMCoordsTemplate [N] ) for Helix in self. Content ]

          return FittedNSet 

######## teraz beda funkcje dla par ###

#####################################################################################################################################################

      def NoVdWContacts ( self, ZRange = Parametry. AtomicContactZRange ):

          self. NoVdWContactsI = 0;

          TM1, TM2 = self.Content;

          for TM1ResidueInstance in TM1.Content:

              if ( (TM1ResidueInstance.Z >= ZRange[0]) and ( TM1ResidueInstance.Z <= ZRange[1]) ):

               for TM2ResidueInstance in TM2.Content:

                  if ( (TM2ResidueInstance.Z >= ZRange[0]) and ( TM2ResidueInstance.Z <= ZRange[1]) ):

                   #Setof2ResiduesInstance = SetOfResidues ( [ TM1ResidueInstance, TM2ResidueInstance ] )

                   if SetOfResidues ( [ TM1ResidueInstance, TM2ResidueInstance ] ). VdWContact ( ): # a wiec nie liczy tego kontentu, trzeba sprawdzic wyzej
                     self. NoVdWContactsI += 1
                  
          return self. NoVdWContactsI #ok teraz zmienic matryce kontaktow

#####################################################################################################################################################

      def NoVdWContactsAndHydrogenBonds ( self ):

          self.NoVdWContactsI = 0

          TM1 = self.Content [ 0 ]; TM2 = self.Content [ 1 ];

          for TM1ResidueInstance in TM1.Content:

              for TM2ResidueInstance in TM2.Content:

                  Setof2ResiduesInstance = SetOfResidues ( [ TM1ResidueInstance, TM2ResidueInstance ] )

                  if Setof2ResiduesInstance.VdWContactOrHydrogenBond ( ): # a wiec nie liczy tego kontentu, trzeba sprawdzic wyzej
                     self.NoVdWContactsI+= 1
                  
          return self.NoVdWContactsI #ok teraz zmienic matryce kontaktow

#####################################################################################################################################################

      def MinimumDistanceBetweenAxes ( OsieJakoOdcinki ):


          return MinimalnaOdlegloscPomiedzyOdcinkami ( OsieJakoOdcinki )
          
######### najlepiej jakby te dwie funkcje zwracaly od razu obie te rzeczy ###### byloby szybciej ###
#####################################################################################################################################################

      def VdWContactsNoAndResiduePairs ( self ): # defined for N = 2

          VdWContactResiduePairsI = [ ]; VdWContactsNo = 0;

          TM1, TM2 = self.Content;

          for TM1ResidueInstance in TM1.Content:

              for TM2ResidueInstance in TM2.Content:

                  Setof2ResiduesInstance = SetOfResidues ( [ TM1ResidueInstance, TM2ResidueInstance ] )

                  if Setof2ResiduesInstance. VdWContact ( ):

                     VdWContactResiduePairI = [ TM1ResidueInstance.Name ( ), TM2ResidueInstance.Name ( ) ] # w formacie 109S na przyklad
                     VdWContactResiduePairsI. append ( VdWContactResiduePairI )
                     VdWContactsNo += 1

          return [VdWContactsNo, VdWContactResiduePairsI] #ok teraz zmienic matryce kontaktow
#########

#####################################################################################################################################################

#####################################################################################################################################################

      def VdWContactResiduePairs ( self ): # defined for N = 2

          VdWContactResiduePairsI = [ ]

          TM1, TM2 = self.Content;

          for TM1ResidueInstance in TM1.Content:

              for TM2ResidueInstance in TM2.Content:


                  Setof2ResiduesInstance = SetOfResidues ( [ TM1ResidueInstance, TM2ResidueInstance ] )

                  if Setof2ResiduesInstance. VdWContact ( ):

                     VdWContactResiduePairI = [ TM1ResidueInstance.Name ( ), TM2ResidueInstance.Name ( ) ] # w formacie 109S na przyklad
                     VdWContactResiduePairsI. append ( VdWContactResiduePairI )
                  
          return VdWContactResiduePairsI #ok teraz zmienic matryce kontaktow      
#########

#####################################################################################################################################################

      def MinimumCADistance ( self ): # fajnie jakby byl szablon dla tych metod

          self.MinimumDistanceI = 1000.0

          TM1, TM2 = self.Content;

          for TM1ResidueInstance in TM1.Content:

              for TM2ResidueInstance in TM2.Content:

                  Setof2CAAtomRecordsInstance = Setof2AtomRecords ( [ TM1ResidueInstance.CA(), TM2ResidueInstance.CA() ] )

                  if Setof2CAAtomRecordsInstance.Distance() <= self.MinimumDistanceI:
                  
                     self.MinimumDistanceI = Setof2CAAtomRecordsInstance.Distance ()

          return self.MinimumDistanceI

##########

#####################################################################################################################################################
#ok, wiec ogarnalem Range ...
# teraz musze ogarnac w CommandLine kategorie 

      def IsVdWPair( self, NoVdWContactsThreshold = 3, ZRange = [-8.0, 8.0 ] ):

          if self. NoVdWContacts ( ZRange ) >= NoVdWContactsThreshold :

             return True
# wiec moze tu jest zlo, potrzebuje kawy albo czegos

          return False

#####################################################################################################################################################

      def ExtractTouchingNSets ( self, OutputPath = 'ExtractedTouchingNsetsDataset', Order = 2 ):

          if Order == 2:

             SetOfTouchingNsetsInstance = self. ExtractTouching2Sets ( )             

          return SetOfTouchingNsetsInstance

#####################################################################################################################################################

      def DihedralAnglesMatrices ( self ):

          EMs = [ ]; IMs = [ ]; EMCrossingAnglesMatrix = [ ]; IMCrossingAnglesMatrix = [ ];

          # chodzi o to zeby half helix crossing angles matrices jeszcze bylo

          for Helix in self.Content:

              EM, IM = Helix.HalfHelixAxes ( ). Content

#              EM, IM = Helix. COM_Axes_EC_MM_IC ( )   

              EM. AnchorInPoint ( Helix. ThinSlicesCOMs() [ 1 ] )
              IM. AnchorInPoint ( Helix. ThinSlicesCOMs() [ 1 ] )
              print EM. AnchorPoint        


              EMs. append (EM)
              IMs. append (IM)

          print EMs [ 0 ]. AnchorPoint               
#          quit ()

          for I in range ( len (EMs) ):
              EMCrossingAnglesMatrixRow = [ ]

              
              for J in range ( len ( EMs ) ):
                  if J == I: EMCrossingAnglesMatrixRow. append ( 0.0 )
                  else: EMCrossingAnglesMatrixRow. append ( SetOfVectors( [ EMs [I], EMs [J] ] ).Dihedral ( ) )
              EMCrossingAnglesMatrix. append ( EMCrossingAnglesMatrixRow )


          for I in range ( len (IMs) ):
              IMCrossingAnglesMatrixRow = [ ]
              
              for J in range ( len ( IMs ) ):
                  if J == I: IMCrossingAnglesMatrixRow. append ( 0.0 )
                  else: IMCrossingAnglesMatrixRow. append ( SetOfVectors( [ IMs [I], IMs [J] ] ).Dihedral ( ) )
              IMCrossingAnglesMatrix. append ( IMCrossingAnglesMatrixRow )


          return [ EMCrossingAnglesMatrix, IMCrossingAnglesMatrix ]

#####################################################################################################################################################
# Crossing Angle Matrices
      def CrossingAnglesMatrices ( self ):

          EMs = [ ]; IMs = [ ]; Mains = [ ];
          EMCrossingAnglesMatrix = [ ]; IMCrossingAnglesMatrix = [ ];
          MainCrossingAnglesMatrix = [ ];

          # chodzi o to zeby half helix crossing angles matrices jeszcze bylo

          for Helix in self.Content:

              EM, IM = Helix.HalfHelixAxes ( ). Content

#              EM, IM = Helix. COM_Axes_EC_MM_IC ( )          

              EMs. append (EM)
              IMs. append (IM)
              Mains. append (Helix. MainAxis (  ))

          for I in range ( len (EMs) ):
              EMCrossingAnglesMatrixRow = [ ]
              
              for J in range ( len ( EMs ) ):

                  EMCrossingAnglesMatrixRow. append ( SetOfVectors( [ EMs [I], EMs [J] ] ).AngleDEG ( ) )
              EMCrossingAnglesMatrix. append ( EMCrossingAnglesMatrixRow )


          for I in range ( len (IMs) ):
              IMCrossingAnglesMatrixRow = [ ]
              
              for J in range ( len ( IMs ) ):

                  IMCrossingAnglesMatrixRow. append ( SetOfVectors( [ IMs [I], IMs [J] ] ).AngleDEG ( ) )
              IMCrossingAnglesMatrix. append ( IMCrossingAnglesMatrixRow )

          for I in range ( len (Mains) ):
              MainCrossingAnglesMatrixRow = [ ]
              
              for J in range ( len ( Mains ) ):

                  MainCrossingAnglesMatrixRow. append ( SetOfVectors( [ Mains [I], Mains [J] ] ).AngleDEG ( ) )
              MainCrossingAnglesMatrix. append ( MainCrossingAnglesMatrixRow )


          return [ EMCrossingAnglesMatrix, IMCrossingAnglesMatrix, MainCrossingAnglesMatrix ]

#####################################################################################################################################################

      def ExtractTouching2Sets ( self, OutputPath = 'ExtractedTouchingNsetsDataset'):

          self.TouchingPairs = []
          self.TMHelicesInstancesI = self.Content

          NoTM = len ( self.Content )

          for I in range ( NoTM ): # robie to o dwa razy za duzo to jest problem...

              TMHelix1 = self.Content [ I ]

              for J in range ( I+1, NoTM ):

                  TMHelix2 = self.Content [ J ]

                  Two_TMs_Set_Instance = N_TMs_Set ( [TMHelix1, TMHelix2 ] )

                  if Two_TMs_Set_Instance.IsVdWPair ( ):

                     self.TouchingPairs. append ( Two_TMs_Set_Instance ) 

          return SetOfK_N_TMs_Sets ( self.TouchingPairs ) 

# teraz powinienem przemyslec Apriori, z reprezentacji oczywiscie          

#####################################################################################################################################################

      def InternalSphericalCoordinatesRepresentation ( self, DistanceSetting, Origin ):

          Tm1Tm2Distance = 0.0 # ok, jak to zdefiniowac?

          Tm1Tm3Distance = 0.0
          
          Tm2Tm1Tm3Angle = 0.0

          Tm2Tm1ForwardTilt = 0.0
          Tm2Tm1SideTilt    = 0.0

          Tm3Tm1ForwardTilt = 0.0
          Tm3Tm1SideTilt    = 0.0

#

          Tm1Tm2Distance = N_TMs_Set([ self. Content[0], self. Content[1] ]). Distance ( DistanceSetting )

          Tm1Tm3Distance = N_TMs_Set([ self. Content[0], self. Content[2] ]). Distance ( DistanceSetting )

          Tm1Tm2Vector = Vector ( SetOfPoints ( Tm1.CenterOfMass(), Tm2.CenterOfMass() ) );

          Tm1Tm3Vector = Vector ( SetOfPoints ( Tm1.CenterOfMass(), Tm3.CenterOfMass() ) );

          Tm2Tm1Tm3Angle = SetOfVectors ( Tm1Tm2Vector, Tm1Tm3Vector ) 

#

          Tm2Tm1ForwardTilt = 0.0

#         equals angle of projection of Tm2 on Tm1 plane to Z = (0,0,1)
#         

#

          if Origin == 'Tm1Middle':

             Origin = self. Content [ 0 ]. CenterOfMass ( )

          self. Translate ( -Origin )
          
          # Superimpose Tm1Tm2 Vector on ( 0.0, 0.0 ) -> (0.0, Tm1Tm2Distance )

          #            
        
          return [ Tm1Tm2Distance, Tm1Tm3Distance, Tm2Tm1Tm3Angle, Tm2Tm1ForwardTilt, Tm2Tm1SideTilt, Tm3Tm1ForwardTilt, Tm3Tm1SideTilt ]

#####################################################################################################################################################
