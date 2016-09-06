import os, sys

import N_TMs_Set; from  N_TMs_Set import N_TMs_Set;

import TMHelixModule; from TMHelixModule import TMHelix
import ProteinChainModule; from ProteinChainModule import ProteinChain, MSegment

from IO import readpath;

#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

class PdbFileContent ( list ):

   """ stores Contents of PDB file """

   def __init__ ( self, InputPdbRecords ):

      """ constructs Class instance from set of Input PDB records """

      import PdbRecordModule; from  PdbRecordModule import * # imported here in order to avoid circular reference 

      # if objects are imported inside objects instead of at the beginning of the module file this is usually 
      # done to avoid circular reference

      self.Content = [ ]

      for InputPdbRecord in InputPdbRecords:

          PdbRecordInstance = PdbRecord ( InputPdbRecord )

          self.Content. append ( PdbRecordInstance )

      return

#####################################################################################################################################################

   def AtomRecords ( self ):                                        # 

      """ extracts ATOM records from PDB file content """

      import PdbRecordModule; from PdbRecordModule import *;
      import AtomRecordsModule; from AtomRecordsModule import *;      
      import AtomRecordModule; from AtomRecordModule import *; 

      self.AtomRecordsI= []

      for PdbRecordInstance in self.Content:

         if PdbRecordInstance.Type()=='ATOM  ':

            self.AtomRecordsI.append( AtomRecord ( PdbRecordInstance.s ) ) # so it is an instance

      return AtomRecords ( self.AtomRecordsI )

#####################################################################################################################################################

   def ExtractProteinResidues ( self ):

       """ extracts Amino Acid Residues from PDB file content """

       self.AtomRecordsInstances = self.AtomRecords ( )

       self.ProteinResidueInstances = self.AtomRecordsInstances.ExtractProteinResidues ( )
   
       return self.ProteinResidueInstances

#####################################################################################################################################################

   def ExtractProteinChains ( self, OutputPath = 'ExtractedProteinChains' ):

       """ extracts Protein Chains from PDB File Contents """

       import ProteinChainModule; from ProteinChainModule import ProteinChain; # imported here to avoid cricular reference

       self. ProteinChainInstances = [];
       self.ProteinResidueInstances = self.ExtractProteinResidues ( );
       self. ProteinChainI  = [ self.ProteinResidueInstances [ 0 ] ]; # we initialize Protein Chain starting it at 1st residue        

       for N in range ( 1, len ( self.ProteinResidueInstances ) ):

           if self.ProteinResidueInstances [ N ]. Chain ( ) != self.ProteinResidueInstances [ N-1 ]. Chain ( ):

              ProteinChainInstance = ProteinChain ( self.ProteinChainI, self.ProteinResidueInstances [ N-1 ]. Chain ( )  )
              self.ProteinChainInstances. append ( ProteinChainInstance )

              self.ProteinChainI = [ self.ProteinResidueInstances [ N ] ];
              ProteinChainInstance.OutputToPdbFile ( OutputPath )

           else:

              self.ProteinChainI. append ( self.ProteinResidueInstances [ N ] ) #powinno byc inaczej zrobione, dorobic metode append na protein chain
# tymczasem zrobic zeby apka robila wiecej rzeczy, tzn drukowala wiecej wartosci, ciekawe kiedy to zdebaguje

       ProteinChainInstance = ProteinChain ( self.ProteinChainI, self.ProteinResidueInstances [ N ]. Chain ( ) )

       self.ProteinChainInstances. append ( ProteinChainInstance )  

       return self.ProteinChainInstances

#####################################################################################################################################################

   def ExtractTMSegments ( self, OutputPath ):

       """ extracts Transmembrane Segments from PDB file content """

       # nalezy to jakos skrocic

       for ProteinChainInstance in self. ExtractProteinChains ( ):

           os.system (' mkdir '+ OutputPath + '; mkdir '+ OutputPath +  '/TMs'); N=0; #created directory for extracted TMs

           TMSegmentsI = ProteinChainInstance. TMSegments ( )

           for MRegionResiduesSegment_I in TMSegmentsI:
                    

 #smiesznie troche
# ta funkcjonalnosc sie rozbudowala i to jest troche problem; nalezy dodac to jako metode do TMHelix chyba
# 
                     N=N+1
#                     TMPath = 
                     ProteinChain( MRegionResiduesSegment_I. Content). OutputToPdbFile ( OutputPath + '/TMs/'+ ProteinChainInstance.ChainID+'_TM_'+str(N)+'_' )
                     MRegionResiduesSegment_I. ChainID = ProteinChainInstance. ChainID

                     MRegionResiduesSegment_I. DrawAxesInPymol (N, OutputPath + '/TMs/')
                            
       return N_TMs_Set ( TMSegmentsI )


###############################################################################################################################################

def ReadPDBFile (PDBFilePath, db_path):

        """ uses above methods in order to extract transmembrane segments from input PDB File and store them in SQL database db_path """
        """ located at db_path """  
        # 

        PDBFilePathFolder = '/'.join(PDBFilePath.split('/')[:-1])
       
        print PDBFilePathFolder
                                                                                                     
	PdbFileContent (readpath (PDBFilePath)). ExtractTMSegments (PDBFilePathFolder). WriteToDB (db_path)

def getHelicesfromPDBFile (PDBFilePath):

        """ uses above methods in order to extract transmembrane segments from input PDB File and store them in SQL database db_path """
        """ located at db_path  """

        PDBFilePathFolder = '/'.join(PDBFilePath.split('/')[:-1])
    
                                                                                                    
	return PdbFileContent (readpath (PDBFilePath)). ExtractTMSegments (PDBFilePathFolder). Content

def GetAtomsFromPDBFile (PDBFilePath):
    print ''.join([Atom.s for Atom in PdbFileContent (readpath (PDBFilePath)). AtomRecords ().Content ])
    return ''.join([Atom.s for Atom in PdbFileContent (readpath (PDBFilePath)). AtomRecords ().Content ])

# powinienem uzyc create
