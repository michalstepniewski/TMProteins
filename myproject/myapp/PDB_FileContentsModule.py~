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

       os. system('rm -r myproject/myapp/static/myapp/static/*;') # clear static files
       os. system('rm -r media/TMs/*.pdb;') #clears previously extracted Transmembrane Segments stored in PDB files

       # nalezy to jakos skrocic

       for ProteinChainInstance in self. ExtractProteinChains ( ):

           os.system (' mkdir '+ OutputPath + '; mkdir '+ OutputPath +  '/TMs'); N=0; #created directory for extracted TMs

           TMSegmentsI = ProteinChainInstance. TMSegments ( )

           for MRegionResiduesSegment_I in TMSegmentsI: #smiesznie troche

                     N=N+1
                     ProteinChain( MRegionResiduesSegment_I. Content). OutputToPdbFile ( OutputPath + '/TMs/'+ ProteinChainInstance.ChainID+'_TM_'+str(N)+'_' )
                     
		     command = ' mkdir myproject/myapp/static/myapp/static/'+str(N)+'; cp script.pml media/;cp script.pml media/TMs/;cd media; pymol TMProtein.pdb -c script.pml; cd TMs/; pymol '+ProteinChainInstance.ChainID+'_TM_'+str(N)+'_X.pdb' + '  script.pml -- '+' '.join(map(str,  MRegionResiduesSegment_I. MainAxis()))+' '+' '.join(map(str,  MRegionResiduesSegment_I. Center()))+' '+' '.join(map(str,  MRegionResiduesSegment_I. Axis_EC()) )+' '+' '.join(map(str,  MRegionResiduesSegment_I. Axis_IC()))+'; cd ../..; mv media/plik1.png myproject/myapp/static/myapp/static/Protein1.png;  mv '+ OutputPath + '/TMs/plik1.png myproject/myapp/static/myapp/static/'+str(N)+'/helisa.png'; # this console script uses pymol and pymol script (script.pml) in order to generate figures displaying Transmembrane Proteins 
                     # together with extracted Transmembrane Helices

# musze czytelniej zrobic te komende

                     os.system(command)
                            
       return N_TMs_Set ( TMSegmentsI )

###############################################################################################################################################

def ReadPDBFile (PDBFilePath, db_path):

        """ uses above methods in order to extract transmembrane segments from input PDB File and store them in SQL database db_path """
        """ located at db_path  
                                                                                                     """
	PdbFileContent (readpath (PDBFilePath)). ExtractTMSegments ('media'). WriteToDB (db_path)


