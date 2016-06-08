from __future__ import unicode_literals
import urllib2
from django.db import models

# Create your models here.

def getnodeName(node):

    return node.childNodes[[x.nodeName for x in node.childNodes].index('name')].childNodes[0].nodeValue

def get_attribute_value(node,attribute):

    return node.childNodes[[x.nodeName for x in node.childNodes].index(attribute)].childNodes[0].nodeValue
#####


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


        subgroups = groups.getElementsByTagName("subgroups")

        subgroups = subgroups[0].getElementsByTagName("subgroup")

        for subgroup in subgroups:

            subgroup_name = subgroup.childNodes[[x.nodeName for x in groups.childNodes].index('name')].childNodes[0].nodeValue

            proteins = subgroup.getElementsByTagName("protein")

            for protein in proteins:
                print protein.childNodes
                print [x.nodeName for x in protein.childNodes]
                attributes = ['pdbCode','name','species','taxonomicDomain','expressedInSpecies',\
                          'resolution', 'description' ]
                pdbCode = protein.childNodes[[x.nodeName for x in protein.childNodes].index('pdbCode')].childNodes[0].nodeValue
                name = protein.childNodes[[x.nodeName for x in protein.childNodes].index('name')].childNodes[0].nodeValue
                species = protein.childNodes[[x.nodeName for x in protein.childNodes].index('species')].childNodes[0].nodeValue
                taxonomicDomain= protein.childNodes[[x.nodeName for x in protein.childNodes].index('taxonomicDomain')].childNodes[0].nodeValue
                print protein.childNodes[[x.nodeName for x in protein.childNodes].index('expressedInSpecies')].childNodes
#                expressedInSpecies= protein.childNodes[[x.nodeName for x in protein.childNodes].index('expressedInSpecies')].childNodes[0].nodeValue
                resolution= protein.childNodes[[x.nodeName for x in protein.childNodes].index('resolution')].childNodes[0].nodeValue
#                description= protein.childNodes[[x.nodeName for x in protein.childNodes].index('description')].childNodes[0].nodeValue
#                expressedInSpecies= protein.childNodes[[x.nodeName for x in protein.childNodes].index('expressedInSpecies')].childNodes[0].nodeValue

#                pdbCode,name,species,taxonomicDomain,expressedInSpecies, resolution, description = [ protein.childNodes[[x.nodeName for x in protein.childNodes].index(attribute)].childNodes[0].nodeValue for attribute in attributes]

#                pdbCode,name,species,taxonomicDomain,expressedInSpecies, resolution, description = [ get_attribute_value(protein,attribute) for attribute in attributes]

                structure.objects.create( pdbCode = pdbCode,
                                      name = name,
                                      species = species,
                                      taxonomicDomain = taxonomicDomain,
#                                      expressedInSpecies = expressedInSpecies,
                                      resolution = resolution,
#                                      description = description,
                                      Type = 'master')
                                      
                bibliography = protein.getElementsByTagName("bibliography")[0]
        
                attributes = [ 'pubMedId', 'authors', 'year', 'title', 'journal',\
                           'volume', 'issue', 'pages', 'doi', 'notes']

            
                pubMedId, authors, year, title, journal,\
                volume, issue, pages, doi, notes = [ get_attribute_value(bibliography,attribute) for attribute in attributes]


class DatabaseModel (models.Model):
    objects  = DatabaseModelManager ()
    
    pass


class group(models.Model):

    name = models.CharField(max_length=200,null=True)

class subgroup(models.Model):

    name = models.CharField(max_length=200,null=True)

    group = models.ForeignKey(group)

class protein(models.Model):

    name = models.CharField(max_length=200,null=True)

    group = models.ForeignKey(group)

#pdbCode,name,species,taxonomicDomain,expressedInSpecies,resolution,description,bibliography,
#                     secondaryBibliographies,relatedPdbEntries,memberProteins)

class structure(models.Model):

      pdbCode = models.CharField(max_length=4,null=True)
      name = models.CharField(max_length=200,null=True)
      species = models.CharField(max_length=200,null=True)
      taxonomicDomain = models.CharField(max_length=200,null=True)
      expressedInSpecies = models.CharField(max_length=200,null=True)
      resolution = models.CharField(max_length=200,null=True)
      description = models.CharField(max_length=200,null=True)
#      bibliography
#      secondaryBibliographies
      Type = models.CharField(max_length=20,null=True) #master, relatedPdbEntries, memberProteins


class bibliography(models.Model):

    pubMedId = models.CharField(max_length=200,null=True)
    authors = models.CharField(max_length=200,null=True)
    year = models.IntegerField(null=True)
    title = models.CharField(max_length=200,null=True)
    journal = models.CharField(max_length=200,null=True)
    volume = models.CharField(max_length=200,null=True)
    issue = models.CharField(max_length=200,null=True)
    pages = models.CharField(max_length=200,null=True)
    doi = models.CharField(max_length=200,null=True)
    notes = models.CharField(max_length=200,null=True)

