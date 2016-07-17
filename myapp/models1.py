# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
import sqlite3
from time import gmtime, strftime
import matplotlib
import PlotToolsModule; from PlotToolsModule import HistogramPlot
import numpy as np
from django.db import transaction
import scipy
import scipy.stats
from scipy.stats import relfreq
import math
from django.db.models import Sum, Avg
from GeometricalClassesModule import SetOfVectors, Vector, SetOfPoints, Point
from django.db.models import Avg, Max, Min
import match
from match import rmsd


class ClusterManager (models.Manager):
    pass

class ClusterQueryset (models.QuerySet):
    pass 

#class Cluster (models.Model):
#    pass

class ClusterManager (models.Manager):
    pass

class PointQueryset (models.QuerySet):
    pass 

class Point (models.Model):
    pass