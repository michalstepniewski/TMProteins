from __future__ import unicode_literals
import urllib2, os
from django.db import models
from celery import task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger

# Create your models here.

def getnodeName(node):

    return node.childNodes[[x.nodeName for x in node.childNodes].index('name')].childNodes[0].nodeValue

def get_attribute_value(node,attribute):
    
    try:

        return node.childNodes[[x.nodeName for x in node.childNodes].index(attribute)].childNodes[0].nodeValue

    except IndexError:
        return ''
#####

class structureQuerySet(models.QuerySet):

    def Download (self):

        import wget
        
        for structureI in self.all():
         if not structureI.Processed:
        


            url = 'http://files.rcsb.org/download/'+structureI.pdbCode+'.pdb'
            url2 = 'http://opm.phar.umich.edu/pdb/'+structureI.pdbCode.lower()+'.pdb'
            print url
            attempts = 0

            while attempts < 3:
                try:
                    response = urllib2.urlopen(url, timeout = 5)
                    
                    content = response.read()
                    chars_to_remove = ['.', '!', '?','(',')',' ','<','>','&','/'\
                                       ,';']
                    dd = {ord(c):None for c in chars_to_remove}
                    name = structureI.protein.name.translate(dd)
                    subgroup_name = structureI.protein.subgroup.name.translate(dd)
                    print name
                    os.system('mkdir -p media/DatabaseModels/8/'+subgroup_name+'/'+name )
                    f = open( 'media/DatabaseModels/8/'+subgroup_name+'/'+name+'/'+url.split('/')[-1], 'w' )
                    f.write( content )
                    f.close()
                    print 'success'
                    
                    break
                except urllib2.URLError as e:
                    attempts += 1
                    print type(e)

            url2 = 'http://opm.phar.umich.edu/pdb/'+structureI.pdbCode.lower()+'.pdb'
            
            attempts = 0                    
            while attempts < 3:
                try:
                    response = urllib2.urlopen(url2, timeout = 5)
                    
                    content = response.read()
                    chars_to_remove = ['.', '!', '?','(',')',' ','<','>','&','/'\
                                       ,';']
                    dd = {ord(c):None for c in chars_to_remove}
                    name = structureI.protein.name.translate(dd)
                    subgroup_name = structureI.protein.subgroup.name.translate(dd)

                    print name
                    os.system('mkdir -p media/DatabaseModels/8/'+subgroup_name+'/'+name )
                    f = open( 'media/DatabaseModels/8/'+subgroup_name+'/'+name+'/'+url2.split('/')[-1], 'w' )

                    f.write( content )
                    f.close()
                    print 'success'
                    
                    break
                except urllib2.URLError as e:
                    attempts += 1
                    print type(e)
#through queryset

class structureManager (models.Manager):
    pass    

class DatabaseModelManager (models.Manager):

    def Update(self):

        from xml.dom.minidom import parse
        import xml.dom.minidom
        import wget

        url = 'http://blanco.biomol.uci.edu/mpstruc/listAll/mpstrucAlphaHlxTblXml'
        attempts = 0

        while attempts < 3:
            try:
                response = urllib2.urlopen(url, timeout = 5)
                content = response.read()
                f = open( url.split('/')[-1], 'w' )
                f.write( content )
                f.close()
                break
            except urllib2.URLError as e:
                attempts += 1
                print type(e)


        
#        wget.download(url)
        DOMTree = xml.dom.minidom.parse(url.split('/')[-1])
        collection = DOMTree.documentElement

        groupss = collection.getElementsByTagName("groups")
#        movies[0]

        groups = groupss[0].childNodes[1]
        groupname = groups.childNodes[1].childNodes[0].nodeValue

        groups.childNodes[5].childNodes[5].childNodes[1].childNodes[0].nodeValue
        groupname = groups.childNodes[[x.nodeName for x in groups.childNodes].index('name')].childNodes[0].nodeValue

        groupI = group.objects.create(name = groupname)

        subgroups = groups.getElementsByTagName("subgroups")

        subgroups = subgroups[0].getElementsByTagName("subgroup")

        for subgroupI in subgroups:

            subgroup_name = subgroupI.childNodes[[x.nodeName for x in groups.childNodes].index('name')].childNodes[0].nodeValue

            subgroupII = subgroup.objects.create(name = subgroup_name)
            groupI.subgroup_set.add(subgroupII)

            proteins = subgroupI.getElementsByTagName("protein")

            for proteinI in proteins:
#                print protein.childNodes
#                print [x.nodeName for x in protein.childNodes]
                attributes = ['pdbCode','name','species','taxonomicDomain','expressedInSpecies',\
                          'resolution', 'description' ]
#                pdbCode = protein.childNodes[[x.nodeName for x in protein.childNodes].index('pdbCode')].childNodes[0].nodeValue
#                name = protein.childNodes[[x.nodeName for x in protein.childNodes].index('name')].childNodes[0].nodeValue
#                species = protein.childNodes[[x.nodeName for x in protein.childNodes].index('species')].childNodes[0].nodeValue
#                taxonomicDomain= protein.childNodes[[x.nodeName for x in protein.childNodes].index('taxonomicDomain')].childNodes[0].nodeValue
#                print protein.childNodes[[x.nodeName for x in protein.childNodes].index('expressedInSpecies')].childNodes
#                expressedInSpecies= protein.childNodes[[x.nodeName for x in protein.childNodes].index('expressedInSpecies')].childNodes[0].nodeValue
#                resolution= protein.childNodes[[x.nodeName for x in protein.childNodes].index('resolution')].childNodes[0].nodeValue
#                description= protein.childNodes[[x.nodeName for x in protein.childNodes].index('description')].childNodes[0].nodeValue
#                expressedInSpecies= protein.childNodes[[x.nodeName for x in protein.childNodes].index('expressedInSpecies')].childNodes[0].nodeValue

#                pdbCode,name,species,taxonomicDomain,expressedInSpecies, resolution, description = [ protein.childNodes[[x.nodeName for x in protein.childNodes].index(attribute)].childNodes[0].nodeValue for attribute in attributes]

                pdbCode,name,species,taxonomicDomain,expressedInSpecies, resolution, description = [ get_attribute_value(proteinI,attribute) for attribute in attributes]
                proteinII = protein.objects.create( name = name,                                      
                                      species = species,
                                      taxonomicDomain = taxonomicDomain,
                                      description = description,
                                      )
                
                structureII = structure.objects.create( pdbCode = pdbCode,
                                      name = name,
                                      species = species,
                                      taxonomicDomain = taxonomicDomain,
                                      expressedInSpecies = expressedInSpecies,
                                      resolution = resolution,
                                      description = description,
                                      Type = 'master')
                
                proteinII.structure_set.add(structureII) 
                subgroupII.protein_set.add(proteinII)               
# to teraz tutaj te nie mastery wziac                
#                            subgroupI = subgroup.objects.create(name = subgroup_name)
#            group.subgroup_set.add(subgroupI)
                                      
                bibliographyI = proteinI.getElementsByTagName("bibliography")[0]
        
                attributes = [ 'pubMedId', 'authors', 'year', 'title', 'journal',\
                           'volume', 'issue', 'pages', 'doi', 'notes']

            
                pubMedId, authors, year, title, journal,\
                volume, issue, pages, doi, notes = [ get_attribute_value(bibliographyI,attribute) for attribute in attributes]

                bibliographyII = bibliography.objects.create(pubMedId=pubMedId,
                                                            authors=authors,
                                                            year=year,
                                                            title=title,
                                                            journal=journal,
                                                            volume=volume,
                                                            issue=issue,
                                                            pages=pages,
                                                            doi=doi,
                                                            notes=notes)
#                                                                        )
                structureII.bibliography_set.add(bibliographyII) 

class DatabaseModel (models.Model):    
    objects  = DatabaseModelManager ()
    name = models.CharField(max_length=200,null=True)
    def Update(self):

        from xml.dom.minidom import parse
        import xml.dom.minidom
        import wget
        import datetime
        import os

        url = 'http://blanco.biomol.uci.edu/mpstruc/listAll/mpstrucAlphaHlxTblXml'
        attempts = 0
        today = datetime.datetime.today()
        date = str(today.year)+'-'+str(today.month)+'-'+str(today.day)
        os.system('mkdir -p '+date)
        
        while attempts < 3:
            try:
                response = urllib2.urlopen(url, timeout = 5)
                content = response.read()
                f = open( date +'/'+ url.split('/')[-1], 'w' )
                f.write( content )
                f.close()
                break
            except urllib2.URLError as e:
                attempts += 1
                print type(e)


        
#        wget.download(url)
        DOMTree = xml.dom.minidom.parse( date+'/' + url.split('/')[-1])
        collection = DOMTree.documentElement

        groupss = collection.getElementsByTagName("groups")
#        movies[0]

        groups = groupss[0].childNodes[1]
        groupname = groups.childNodes[1].childNodes[0].nodeValue

        groups.childNodes[5].childNodes[5].childNodes[1].childNodes[0].nodeValue
        groupname = groups.childNodes[[x.nodeName for x in groups.childNodes].index('name')].childNodes[0].nodeValue

        groupI = group.objects.create(name = groupname)

        subgroups = groups.getElementsByTagName("subgroups")

        subgroups = subgroups[0].getElementsByTagName("subgroup")
        if self.structure_set.exists():
            pdbCodes = self.structure_set.all().values_list('pdbCode', flat=True).all()
        else: pdbCodes=[]
#        if not pdbCodes:
        print pdbCodes
#           [pdbCodes]
        for subgroupI in subgroups:

            subgroup_name = subgroupI.childNodes[[x.nodeName for x in groups.childNodes].index('name')].childNodes[0].nodeValue

            subgroupII = subgroup.objects.create(name = subgroup_name)
            groupI.subgroup_set.add(subgroupII)

            proteins = subgroupI.getElementsByTagName("protein")

            for proteinI in proteins:
#                print protein.childNodes
#                print [x.nodeName for x in protein.childNodes]
                attributes = ['pdbCode','name','species','taxonomicDomain','expressedInSpecies',\
                          'resolution', 'description' ]
#                pdbCode = protein.childNodes[[x.nodeName for x in protein.childNodes].index('pdbCode')].childNodes[0].nodeValue
#                name = protein.childNodes[[x.nodeName for x in protein.childNodes].index('name')].childNodes[0].nodeValue
#                species = protein.childNodes[[x.nodeName for x in protein.childNodes].index('species')].childNodes[0].nodeValue
#                taxonomicDomain= protein.childNodes[[x.nodeName for x in protein.childNodes].index('taxonomicDomain')].childNodes[0].nodeValue
#                print protein.childNodes[[x.nodeName for x in protein.childNodes].index('expressedInSpecies')].childNodes
#                expressedInSpecies= protein.childNodes[[x.nodeName for x in protein.childNodes].index('expressedInSpecies')].childNodes[0].nodeValue
#                resolution= protein.childNodes[[x.nodeName for x in protein.childNodes].index('resolution')].childNodes[0].nodeValue
#                description= protein.childNodes[[x.nodeName for x in protein.childNodes].index('description')].childNodes[0].nodeValue
#                expressedInSpecies= protein.childNodes[[x.nodeName for x in protein.childNodes].index('expressedInSpecies')].childNodes[0].nodeValue

#                pdbCode,name,species,taxonomicDomain,expressedInSpecies, resolution, description = [ protein.childNodes[[x.nodeName for x in protein.childNodes].index(attribute)].childNodes[0].nodeValue for attribute in attributes]

                pdbCode,name,species,taxonomicDomain,expressedInSpecies, resolution, description = [ get_attribute_value(proteinI,attribute) for attribute in attributes]
                
                if pdbCode not in pdbCodes:
                 pdbCodes.append(pdbCode)
                
                 proteinII = protein.objects.create( name = name,                                      
                                      species = species,
                                      taxonomicDomain = taxonomicDomain,
                                      description = description,
                                      )
                
                 structureII = structure.objects.create( pdbCode = pdbCode,
                                      name = name,
                                      species = species,
                                      taxonomicDomain = taxonomicDomain,
                                      expressedInSpecies = expressedInSpecies,
                                      resolution = resolution,
                                      description = description,
                                      Type = 'master')
                 self. structure_set.add(structureII)
                 self.protein_set.add(proteinII)
                 proteinII.structure_set.add(structureII) 
                 subgroupII.protein_set.add(proteinII)               
# to teraz tutaj te nie mastery wziac                
#                            subgroupI = subgroup.objects.create(name = subgroup_name)
#            group.subgroup_set.add(subgroupI)
                                      
                 bibliographyI = proteinI.getElementsByTagName("bibliography")[0]
        
                 attributes = [ 'pubMedId', 'authors', 'year', 'title', 'journal',\
                            'volume', 'issue', 'pages', 'doi', 'notes']

            
                 pubMedId, authors, year, title, journal,\
                 volume, issue, pages, doi, notes = [ get_attribute_value(bibliographyI,attribute) for attribute in attributes]

                 bibliographyII = bibliography.objects.create(pubMedId=pubMedId,
                                                            authors=authors,
                                                            year=year,
                                                            title=title,
                                                            journal=journal,
                                                            volume=volume,
                                                            issue=issue,
                                                            pages=pages,
                                                            doi=doi,
                                                            notes=notes)
#                                                                        )
                 structureII.bibliography_set.add(bibliographyII) 
            self.save()
    
    def Process(self):
        from myapp.models1 import Parameters
        ParametersI = Parameters. objects. create (BordersOfThinSlices = '-12.0,-6.0;-3.0,3.0;6.0,12.0')
        self.parameters = ParametersI
        self.save()
        for structureI in self.structure_set.all():
            print structureI.Processed
            if not structureI.Processed: 
            
               structureI.Process(self.parameters)
    
class Operation(models.Model):
    name = models.CharField(max_length=200,null=True)
    DatabaseModel = models.ForeignKey(DatabaseModel, on_delete=models.CASCADE, null=True)
    parameters = models.CharField(max_length=2000,null=True) #in json format perhaps

class RMSDMatrix(models.Model):
    name = models.CharField(max_length=200,null=True)
    DatabaseModel = models.ForeignKey(DatabaseModel, on_delete=models.CASCADE, null=True)
    Operation =  models.ForeignKey(Operation, on_delete=models.CASCADE, null=True)
    path = models.CharField(max_length=2000,null=True) #in json format perhaps
    #thinking of a way to store contents efficiently

class group(models.Model):

    name = models.CharField(max_length=200,null=True)
    DatabaseModel = models.ForeignKey(DatabaseModel, on_delete=models.CASCADE, null=True)

class subgroup(models.Model):

    name = models.CharField(max_length=200,null=True)
    group = models.ForeignKey(group, on_delete=models.CASCADE, null=True)

class protein(models.Model):

    name = models.CharField(max_length=200,null=True)
    species = models.CharField(max_length=200,null=True)
    taxonomicDomain = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=2000,null=True)
    chain = models.CharField(max_length=2000,null=True)
#    group = models.ForeignKey(group)
    subgroup = models.ForeignKey(subgroup, on_delete=models.CASCADE, null=True)
    DatabaseModel = models.ForeignKey(DatabaseModel, on_delete=models.CASCADE, null=True)

#pdbCode,name,species,taxonomicDomain,expressedInSpecies,resolution,description,bibliography,
#                     secondaryBibliographies,relatedPdbEntries,memberProteins)

class structure(models.Model):
    from myapp.models import *

    pdbCode = models.CharField(max_length=4,null=True)
    name = models.CharField(max_length=200,null=True)
    species = models.CharField(max_length=200,null=True)
    taxonomicDomain = models.CharField(max_length=200,null=True)
    expressedInSpecies = models.CharField(max_length=200,null=True)
    resolution = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=2000,null=True)
    protein = models.ForeignKey(protein, on_delete=models.CASCADE, null=True)
    objects  = structureManager () .from_queryset(structureQuerySet)()
    Path = models.CharField(max_length=2000,null=True)
    DatabaseModel = models.ManyToManyField(DatabaseModel)
#    models.ForeignKey(DatabaseModel, on_delete=models.CASCADE, null=True)
    Chain = models.CharField(max_length=4,null=True)
    Processed = models.NullBooleanField(default=False)
#      bibliography
#      secondaryBibliographies
    Type = models.CharField(max_length=20,null=True) #master, relatedPdbEntries, memberProteins

    def Process(self,ParametersI):
        from myapp.models import  TMProtein
        import os,glob
        # if self.Chain==None:
            #self.splitChains
            # w tym celu musimy otworzyc PDB
        ParametersI.SplitChains=False
        ParametersI.OPM=True
        print glob.glob(os.getcwd()+'/media/DatabaseModels/8/*/*/')         
        if ParametersI.SplitChains:
            TMProteinI = TMProtein(Set='Reference',TMProtein_ID=self.pdbCode+'_'+self.Chain ) #cos wymyslec z tym self.Chain, no i DAGa bysmy polozyli
        else:
            TMProteinI = TMProtein(Set='Reference',TMProtein_ID=self.pdbCode )
            if ParametersI.OPM:
                self.Path=glob.glob(os.getcwd()+'/media/DatabaseModels/8/*/*/'+self.pdbCode.lower()+'.pdb')
            if len(self.Path)==1:
                self.Path = self.Path[0]
                
                TMProteinI.save()
                self.tmprotein_set.add(TMProteinI)
        
        #pdbCode
#        'media/IntegralneAlfaHelikalneBialkaBlonowe/ByChain'


#        print os.getcwd()+'/media/PDBs/IntegralneAlfaHelikalneBialkaBlonowe/ByChain/*/*/'+self.pdbCode+'_'+self.Chain+'.pdb'       
# 
#        print glob.glob(os.getcwd()+'/media/PDBs/IntegralneAlfaHelikalneBialkaBlonowe/ByChain/*/*/'+self.pdbCode+'_'+self.Chain+'.pdb')        
#        self.Path = glob.glob(os.getcwd()+'/media/PDBs/IntegralneAlfaHelikalneBialkaBlonowe/ByChain/*/*/*/'+self.pdbCode+'_'+self.Chain+'.pdb')[0]
# self.pdbCode+'_'+self.Chain+'.pdb'
                print self.Path

                TMProteinI.ReadPDB(self.Path,ParametersI)
        
                self.Processed = True
                self.save()
        print self.Processed
        
class bibliography(models.Model):

    pubMedId = models.CharField(max_length=200,null=True)
    authors = models.TextField(max_length=2000,null=True)
    year = models.IntegerField(null=True)
    title = models.TextField(max_length=2000,null=True)
    journal = models.TextField(max_length=2000,null=True)
    volume = models.CharField(max_length=200,null=True)
    issue = models.CharField(max_length=200,null=True)
    pages = models.TextField(max_length=2000,null=True)
    doi = models.TextField(max_length=2000,null=True)
    notes = models. TextField(max_length=2100,null=True)
    structure = models.ForeignKey(structure, on_delete=models.CASCADE, null=True)

