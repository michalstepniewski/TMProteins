# to trzebaby to jakos zrobic zeby robilo


# Illustrates the SALIGN iterative multiple structure alignment
from modeller import *
import modeller.salign
import os
import numpy as np
import time, sys

def dir_pairwise_salign_iterative(dir):
    
    files = os.listdir( dir )

    length = len(files)
    
    f_rms=open('rmsmatrix_dir.csv','w')
    f_rmsd=open('rmsdmatrix_dir.csv','w')

    
    RMSDMatrixI = np.zeros((length,length))
    RMSMatrixI = np.zeros((length,length))
    
    for N1 in range(length):
        
        for N2 in range(N1+1,length):
            
            t0 = time.time()
            
            r = pairwise_salign(files[N1],files[N2])
            
            RMSI=r.rms
            
            RMSDI = r.drms
            
            RMSDMatrixI.itemset((N1,N2),(RMSDI))
            RMSDMatrixI.itemset((N2,N1),(RMSDI))
            
            RMSMatrixI.itemset((N1,N2),(RMSI))
            RMSMatrixI.itemset((N2,N1),(RMSI))
            
            print RMSDI#;quit()
            
            f_rmsd.write(str(RMSDI)+',')
            f_rmsd.flush()
            
            f_rms.write(str(RMSI)+',')
            f_rms.flush()
            
            t1 = time.time()
            
            total = t1 - t0
            
            print total
            
        f_rms.write('\n')
        f_rmsd.write('\n')    

    f_rms.close()
    f_rmsd.close()
    
    return [RMSMatrixI, RMSDMatrixI]

def dir_pairwise_salign(dir):
    
    files = os.listdir( dir )

    length = len(files)
    
    f_rms=open('rmsmatrix_dir2.csv','w')
    f_rmsd=open('rmsdmatrix_dir2.csv','w')

    
    RMSDMatrixI = np.zeros((length,length))
    RMSMatrixI = np.zeros((length,length))
    
    for N1 in range(length):
        
        print N1
        
        for N2 in range(N1+1,length):
            
            print '   '+str(N2)
            
            r = pairwise_salign(files[N1],files[N2])
            
            RMSI=r.rms
            
            RMSDI = r.drms
            
            RMSDMatrixI.itemset((N1,N2),(RMSDI))
            RMSDMatrixI.itemset((N2,N1),(RMSDI))
            
            RMSMatrixI.itemset((N1,N2),(RMSI))
            RMSMatrixI.itemset((N2,N1),(RMSI))
            
#            print RMSDI#;quit()
            
            f_rmsd.write(str(RMSDI)+',')
            f_rmsd.flush()
            
            f_rms.write(str(RMSI)+',')
            f_rms.flush()
            
        f_rms.write('\n')
        f_rmsd.write('\n')    

    f_rms.close()
    f_rmsd.close()
    
    return [RMSMatrixI, RMSDMatrixI]

def dir_pairwise_align(dir,fout):
    
    files = os.listdir( dir )
    
    f=open('files.txt','w')
    
    for N in range(len(files)):
        f.write(str(N)+' '+files[N]+'\n')
        
    f.flush()
    f.close()
    
    length = len(files)
    
    f_rms=open('rmsmatrix_'+fout+'.csv','w')
    f_rmsd=open('rmsdmatrix_'+fout+'.csv','w')

    
    RMSDMatrixI = np.zeros((length,length))
    RMSMatrixI = np.zeros((length,length))
    
    times = np.empty([1, 1],dtype=float)
    times = []
    times = np.array(times)
    
    for N1 in range(length):
        
        print N1
        
        for N2 in range(N1+1,length):
            
            print '   '+str(N2)
            
            t0 = time.time()
            
            pairwise_align(files[N1],files[N2])
            
            t1 = time.time()
            
            total = float(t1 - t0)
            
            print total
            
            times = np.append(times,[total],axis=0)
            
            average_time = np.average(times)
            
#            print times
            
            print 'Average time:' +str(average_time)
            
#            RMSI=r.rms
            
#            RMSDI = r.drms
            
#            RMSDMatrixI.itemset((N1,N2),(RMSDI))
#            RMSDMatrixI.itemset((N2,N1),(RMSDI))
            
#            RMSMatrixI.itemset((N1,N2),(RMSI))
#            RMSMatrixI.itemset((N2,N1),(RMSI))
            
#            print RMSDI#;quit()
            
#            f_rmsd.write(str(RMSDI)+',')
#            f_rmsd.flush()
            
#            f_rms.write(str(RMSI)+',')
#            f_rms.flush()
            
#        f_rms.write('\n')
#        f_rmsd.write('\n')    

#    f_rms.close()
#    f_rmsd.close()
    
#    return [RMSMatrixI, RMSDMatrixI]


def pairwise_salign_iterative(file1,file2):

    log.none()
    env = environ()
    env.io.atom_files_directory = ['.', '../atom_files','media/PDBs/Triplets/']

    aln = alignment(env)
    for (code, chain) in ((file1.split('.')[0], 'A'),  (file2.split('.')[0], 'A')):
        mdl = model(env, file=code)
        aln.append_model(mdl, atom_files=code, align_codes=code+chain)

    modeller.salign.iterative_structural_align(aln)

    aln.write(file='1is3A-it.pap', alignment_format='PAP')
    aln.write(file='1is3A-it.ali', alignment_format='PIR')

    mdl = model(env, file=file1.split('.')[0])

##    code = '1u19'; chain = 'A'

#    mdl = model(env, file=code, model_segment=('FIRST:'+chain, 'LAST:'+chain))

    atmsel = selection(mdl)#.only_atom_types('CA')

#    code = '1u19'; chain = 'A'

    mdl2 = model(env, file=file2.split('.')[0])

    #mdl2 = model(env, file='1uld')
    print 'superposing'
    r = atmsel.superpose(mdl2, aln)

    print r.rms
    print r.drms

    return r

def pairwise_salign(file1,file2):

    log.none()
    env = environ()
    env.io.atom_files_directory = ['.', '../atom_files','media/PDBs/Triplets/']

    aln = alignment(env)
    for (code, chain) in ((file1.split('.')[0], 'A'),  (file2.split('.')[0], 'A')):
        mdl = model(env, file=code)
        aln.append_model(mdl, atom_files=code, align_codes=code+chain)

    aln.salign()##.iterative_structural_align(aln)

    aln.write(file='media/PDBs/Triplets/PAPs/'+file1+file2+'.pap', alignment_format='PAP')
    aln.write(file='media/PDBs/Triplets/ALIs/'+file1+file2+'.ali', alignment_format='PIR')
    aln.write(file='media/PDBs/Triplets/FASTAs/'+file1+file2+'.fasta', alignment_format='FASTA')

    mdl = model(env, file=file1.split('.')[0])

##    code = '1u19'; chain = 'A'

#    mdl = model(env, file=code, model_segment=('FIRST:'+chain, 'LAST:'+chain))

    atmsel = selection(mdl)#.only_atom_types('CA')

#    code = '1u19'; chain = 'A'

    mdl2 = model(env, file=file2.split('.')[0])

    #mdl2 = model(env, file='1uld')
#    print 'superposing'
    r = atmsel.superpose(mdl2, aln)

#    print r.rms
#    print r.drms

    return r

def pairwise_align(file1,file2):

    log.none()
    env = environ()
    env.io.atom_files_directory = ['.', '../atom_files','media/PDBs/Triplets/']

    aln = alignment(env)
    for (code, chain) in ((file1.split('.')[0], 'A'),  (file2.split('.')[0], 'A')):
        mdl = model(env, file=code)
        aln.append_model(mdl, atom_files=code, align_codes=code+chain)

#    aln.salign()##.iterative_structural_align(aln)

#    aln.write(file='media/PDBs/Triplets/PAPs/'+file1+file2+'.pap', alignment_format='PAP')
#    aln.write(file='media/PDBs/Triplets/ALIs/'+file1+file2+'.ali', alignment_format='PIR')
    aln.write(file='media/PDBs/FASTAs/'+file1+file2+'.fasta', alignment_format='FASTA')

dir_pairwise_align(sys.argv[1], sys.argv[2])

# teraz moze moglbym to jakos programistycznie rozbic na dwa procesy
