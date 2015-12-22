#####################################################################################################################################################

import GeometricalClassesModule; from GeometricalClassesModule import *;

from odict import odict

import matplotlib.font_manager as fm

import pylab; from pylab import *

from matplotlib import rc; rc("font", family="serif")

import numpy as np; from numpy import *

import matplotlib.pyplot as plt; from matplotlib.pyplot import *

import matplotlib.gridspec as gridspec

import matplotlib.mlab as mlab

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

def hist3d_bubble(x_data, y_data, z_data, bins=10):
    import numpy as np
    import matplotlib.pyplot as pyplot
    from mpl_toolkits.mplot3d import Axes3D
    ax1 = np.histogram2d(x_data, y_data, bins=bins)
    ax2 = np.histogram2d(x_data, z_data, bins=bins)
    ax3 = np.histogram2d(z_data, y_data, bins=bins)
    xs, ys, zs = ax1[1], ax1[2], ax3[1]
    dx, dy, dz = xs[1]-xs[0],  ys[1]-ys[0], zs[1]-zs[0]
    def rdn():
        return (1-(-1))*np.random.random() + -1
    smart = np.zeros((bins, bins, bins),dtype=int)
    for (i1, j1), v1 in np.ndenumerate(ax1[0]):
        if v1==0: continue
        for k2, v2 in enumerate(ax2[0][i1]):
            v3 = ax3[0][k2][j1]
            if v1==0 or v2==0 or v3==0: continue
            num = min(v1, v2, v3)
            smart[i1, j1, k2] += num
            v1 -= num
            v2 -= num
            v3 -= num
    points = []
    for (i,j,k),v in np.ndenumerate(smart):
        points.append((xs[i], ys[j], zs[k], v))
    points = np.array(points)
    fig = pyplot.figure()
    sub = fig.add_subplot(111, projection='3d')
    sub.scatter(points[:, 0], points[:, 1], points[:, 2],
                color='black', marker='o', s=128*points[:, 3])
    sub.axes.set_xticks(xs)
    sub.axes.set_yticks(ys)
    sub.axes.set_zticks(zs)
    pyplot.ion()
    pyplot.grid()
    pyplot.show()

    return points, sub

#####################################################################################################################################################

def hist3d_color(x_data, y_data, z_data, bins=12):

    import numpy as np
    import matplotlib.pyplot as pyplot
    from mpl_toolkits.mplot3d import Axes3D

    linspejs = np.linspace( -180.0, 180.0, 9.0 )

    ax1 = np.histogram2d(x_data, y_data, bins = linspejs)
    ax2 = np.histogram2d(x_data, z_data, bins = linspejs)
    ax3 = np.histogram2d(z_data, y_data, bins = linspejs)
    xs, ys, zs = ax1[1], ax1[2], ax3[1]
    dx, dy, dz = xs[1]-xs[0],  ys[1]-ys[0], zs[1]-zs[0]

    def rdn():
        return (1-(-1))*np.random.random() + -1

    smart = np.zeros((8, 8, 8),dtype=int)

#    print len (ax1[0]); quit()

    for (i1, j1), v1 in np.ndenumerate(ax1[0]):
        if v1==0: continue
        for k2, v2 in enumerate(ax2[0][i1]):
            v3 = ax3[0][k2][j1]
            if v1==0 or v2==0 or v3==0: continue
            num = min(v1, v2, v3)
            smart[i1, j1, k2] += num
            v1 -= num
            v2 -= num
            v3 -= num
    points = []
    for (i,j,k),v in np.ndenumerate(smart):

        if v >= 5.0:

           points.append((xs[i], ys[j], zs[k], v))
    points = np.array(points)
    fig = pyplot.figure()
    sub = fig.add_subplot(111, projection='3d')

    Blues = plt.get_cmap('coolwarm')

    sub.scatter(points[:, 0], points[:, 1], points[:, 2],
                color=Blues(points[:, 3]/10.0), marker='o', s=25)

    sub.axes.set_xticks(xs)
    sub.axes.set_yticks(ys)
    sub.axes.set_zticks(zs)
    pyplot.ion()
    pyplot.grid()
    pyplot.show()
    return points, sub

####################################################################################################################################

class H1H2H3PointsForHenrisPlot ( list ):

      def TranslateH1ToOrigin ( self ):

          H1 = self [ 0 ]
          H2 = self [ 1 ]
          H3 = self [ 2 ]

          H1_O = [ - H1 [ 0 ], - H1 [ 1 ] ]

          H1_trans = [ H1 [ 0 ] + H1_O [ 0 ] , H1 [ 1 ] + H1_O [ 1 ] ]
          H2_trans = [ H2 [ 0 ] + H1_O [ 0 ] , H2 [ 1 ] + H1_O [ 1 ] ]
          H3_trans = [ H3 [ 0 ] + H1_O [ 0 ] , H3 [ 1 ] + H1_O [ 1 ] ]
          self = H1H2H3PointsForHenrisPlot ( [ H1_trans, H2_trans, H3_trans ] )
            
          return self

#####################################################################################################################################################

      def AlignH1H2ToXAxis ( self ):

          H1 = self [ 0 ]
          H2 = self [ 1 ]
          H3 = self [ 2 ]
          
          

          H1_H2x = H2 [ 0 ] - H1 [ 0 ]
          H1_H2y = H2 [ 1 ] - H1 [ 1 ]          

          H1_H2 = Vector2D ( [ H1_H2x, H1_H2y ] )

#          H1_H2 = Vector2D ( [ 0.0, 1.0 ] )

          Angle = H1_H2.AngleToXAxis ( )

#          if H1_H2x < 0.0 # jesli jes

#          print Angle

          H1rot = Point2D ( H1 ).RotateByAngle ( Angle )
          H2rot = Point2D ( H2 ).RotateByAngle ( Angle )
          H3rot = Point2D ( H3 ).RotateByAngle ( Angle )

          H1H2H3PointsRot = [ H1rot, H2rot, H3rot ]        

          return H1H2H3PointsRot

#####################################################################################################################################################
#####################################################################################################################################################

# now in what form do we want to have this array, maybe just Six
# zle sie przepisuje;

def ScatterPlot ( H1H2H3Array, OutputFile ): # trzeba to zrobic inaczej

# jak skoncze to, to probuje ile moge ruszyc manuskryptu

# wiec zrobmy tak zeby z Array'u kolumn [ X1, Y1, X2, Y2, X3, Y3 ]

#################################################################

    fig = figure(num=None, figsize=( 11.7, 11.7  ), dpi=320)
    gs = gridspec.GridSpec(2, 1,height_ratios=[1,1])
    ax1 = fig.add_subplot(gs[0])
    ax1.axes.get_xaxis().set_ticks([-120,-100,-80,-60,-40,-20,-10,0,10,20,40,60,80,100,120])
    ax1.axes.get_yaxis().set_ticks([-120,-100,-80,-60,-40,-20,-10,0,10,20,40,60,80,100,120])


    H1Xs = array ( H1H2H3Array [:,0] ) ; 
    H1Ys = array ( H1H2H3Array [:,1] )

    color = 'black'; size = 1; alpha1 = 20; # punkt H1 na czarno
    plt.scatter ( H1Xs, H1Ys, c=color)
#    plt.scatter ( H1Xs, H1Ys , color='0.75' , s=1.0, alpha=alpha1 )

##################################################################

    H2Xs = array ( H1H2H3Array [:,2] ) ; 
    H2Ys = array ( H1H2H3Array [:,3] )

    color = 'red'; size = 1; alpha1 = 20; # punkt H2 na czerwono
    plt.scatter ( H2Xs, H2Ys, c=color)
#    plt.scatter ( H2Xs, H2Ys , c=color, s=size, alpha=alpha1 )

##################################################################

    H3Xs = array ( H1H2H3Array [:,4] ) ; 
    H3Ys = array ( H1H2H3Array [:,5] )

    color = 'blue'; size = 1; alpha1 = 20; # punkt H3 na niebiesko
    plt.scatter ( H3Xs, H3Ys, c=color)
    
    plt.savefig(OutputFile ,dpi=100)



#    plt.scatter ( H3Xs, H3Ys , c=color, s=size, alpha=alpha1 )

#################################################################



#   heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
#   extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]



# Xposs=[ 1.0,2.0 ]

#      text( (0.09*n)+Xpos , 105.0,receptor, verticalalignment='bottom',horizontalalignment='center',  rotation='vertical')
# Have to think about it, text

# table=odict([])

# fig = figure(num=None, figsize=( 8.3, 11.7  ), dpi=320)
# gs = gridspec.GridSpec(2, 1,height_ratios=[1,1])
# ax1 = fig.add_subplot(gs[0])

##############################

# 'black'

# bedziemy mysleli potem, najpierw zrobmy zeby plotowalo cokolwiek
#####################################################################################################################################################
#####################################################################################################################################################


def ScatterPlot1 ( XYArray, OutputFile ):

    import numpy
    plt.clf()

    Xs = array ( XYArray [:,0] ) ; 
    Ys = array ( XYArray [:,1] )
#    print XYArray. transpose ()
    print numpy.corrcoef ( numpy. array (XYArray). transpose () )
    print OutputFile
#    quit ()
# cross 0,608; 
# tilt 0.474;
#    print Xs; 

    plt.scatter ( Xs, Ys)    
    plt.savefig (OutputFile ,dpi=320)
    plt.clf()

    return

#####################################################################################################################################################

def HistogramPlot ( H2Xs, OutputFile,Min = -180, Max = 180, BinNo = 37 ):

# nie jestem pewien gdzie histogram, daje biny; musialbym sprawdzic ...
#"""
#Make a histogram of normally distributed random numbers and plot the
#analytic PDF over it
#"""
#    mu, sigma = 100, 15
#    x = mu + sigma * np.random.randn(10000)

    fig = plt.figure()
    ax  = fig.add_subplot(111)

#    H2Xs = array ( H1H2H3Array [:,2] )
# the histogram of the data
#    n, bins, patches = ax.hist(H2Xs, 50, normed=1, facecolor='green', alpha=0.75)
#    min_H2Xs = min ( H2Xs ); max_H2Xs = max ( H2Xs );
#    numBins = 5
#    print H2Xs
#    bins = np.linspace( min_H2Xs, max_H2Xs, 18 ) #int ( max_H2Xs - min_H2Xs ) * 2.0 )

    bins = np.linspace( Min, Max, BinNo)# (Max-Min) + 1 );

#    lista = [ 1, 2, 50, 30 ]
    Array = np.array ( H2Xs )
    print Array
#    print bins; quit()
    ax.hist( Array, bins)#color='green',alpha=0.8)
    plt.xlim(-180, 180)

# hist uses np.histogram under the hood to create 'n' and 'bins'.
# np.histogram returns the bin edges, so there will be 50 probability
# density values in n, 51 bin edges in bins and 50 patches.  To get
# everything lined up, we'll compute the bin centers
#    bincenters = 0.5*(bins[1:]+bins[:-1])
# add a 'best fit' line for the normal PDF
#    y = mlab.normpdf( bincenters, 0, 100)
#    y = n
#    l = ax.plot(bincenters, y, 'r--', linewidth=1)

#    ax.set_xlabel('Smarts')
#    ax.set_ylabel('Probability')
#ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
#    ax.set_xlim(40, 160)
#    ax.set_ylim(0, 0.03)
#    ax.grid(True)

#    plt.show()

    plt.savefig(OutputFile ,dpi=320)
    plt.cla()

#####################################################################################################################################################

def StackedHistogramPlot ( H2Xs, OutputFile,Min = -18, Max = 18 ):

    return

#####################################################################################################################################################

def DoubleHistogramPlot ( H2Xs, H3Xs, OutputFile ):

    min_H2Xs = min ( H2Xs ); max_H2Xs = max ( H2Xs );
    min_H3Xs = min ( H3Xs ); max_H3Xs = max ( H3Xs );

    Minimum = min ( min_H2Xs, min_H3Xs ); Maximum = max ( max_H2Xs, max_H3Xs );

    import random
    import numpy
    from matplotlib import pyplot
    print 'Minimum, Maximum'
    print Minimum; print Maximum

    bins = numpy.linspace( Minimum, Maximum, int ( Maximum - Minimum ) * 2.0 ) # i musze to lepiej wymyslec, tak zeby bylo np co 0.5

#    print bins

    pyplot.hist( H2Xs, bins, alpha=0.5, color = 'blue')
    pyplot.hist( H3Xs, bins, alpha=0.5, color = 'red' )
#    pyplot.show()

    pyplot.savefig(OutputFile ,dpi=320)

    pyplot.clf()

#####################################################################################################################################################

def StepHistogram ( Arrays ):
# zapomnialem ze mowimy o stacked bar plot tak naprawde, musze cos zjesc 
# chyba ze od razu wejsciem bedzie matryca
# tak jest najlepiej

    import numpy as np
    import pylab as P

    XYZ = np.vstack(( Arrays ))

    P.figure()

# bins = [100,125,150,160,170,180,190,200,210,220,230,240,250,275,300]

#    n, bins, patches = P.hist(  XYZ.T, 10, normed=1, histtype='bar',\
#     stacked=True)

# color = ['crimson', 'burlywood', 'chartreuse']

# P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)

#    P.show()

#
# we can also stack using the step histtype

    P.figure()

    n, bins, patches = P.hist(XYZ.T, 10, histtype='step', stacked=True, fill=True) 

# musimy to wykorzystac, pobawic sie stepem, jesli nie wyjdzie to pokombinowac z barem zeby bar drugi byl naprawde suma pierwszego i drugiego arrayu

    P. savefig(OutputFile ,dpi=300)

    P. clf()

    return

#####################################################################################################################################################    

def BarPlot ( InputArray, OutputFile, Title = 'DummyTitle' ):

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.mlab as mlab


    NumeryTypu = array ( InputArray [:,0] ) ; 

    fig = plt.figure()
    ax  = fig.add_subplot(111)
    width=(NumeryTypu[1]-NumeryTypu[0] )/2


    print NumeryTypu

    values = array ( InputArray [:,1] )    

    ax.bar(NumeryTypu, values, width=width)

    title(Title)

#    ax.set_xticks(np.arange(len(NumeryTypu)) + width/2)
#    ax.set_xticklabels(NumeryTypu ) # , rotation=90)

    plt.savefig(OutputFile ,dpi=300)

    return # moze pora spac a jutro zrobie bar plota

#####################################################################################################################################################

def BarPlotBackup ( InputArray, OutputFile ):

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.mlab as mlab

    fig = plt.figure()
    ax  = fig.add_subplot(111)
    width=0.8

    NumeryTypu = array ( InputArray [:,0] ) ; 
    print NumeryTypu

    values = array ( InputArray [:,1] )    

    ax.bar(range(len(NumeryTypu)), values, width=width)
    ax.set_xticks(np.arange(len(NumeryTypu)) + width/2)
    ax.set_xticklabels(NumeryTypu ) # , rotation=90)

    plt.savefig(OutputFile ,dpi=300)

    return # moze pora spac a jutro zrobie bar plota

#####################################################################################################################################################
# a wiec od poczatku
def StackedBarPlot ( InputArray, OutputFile, width = 0.9 ): #powinienem ustawic na zmienna
# width to powinno byc cos winput arrayu

    

    fig = plt.figure()
    ax  = fig.add_subplot(111)

    Z = array ( InputArray [:,0] ) ; ax. set_xticks(Z);

#    width =  ( (Z[1]-Z[0]) ) - 1.0

    width = 0.9
    
    colors = [ 'Dummy','DarkBlue', 'Cyan', 'LightGreen', 'Orange', 'Brown', 'Black' ]

    bottomI = [0.0 for J in range(len(InputArray[:,0]) ) ]

    Values = InputArray [ :,1 ];
    ax.bar(Z, Values, width=width, color = colors [ 1 ] ) # bo pierwszy bez bottomu

#    plt.savefig(OutputFile ,dpi=320)
    for J in range( len(Values) ): bottomI[J] += Values [ J ]

    for I in range (2, len(InputArray[0])):
        
        Values = InputArray [ :,I ];     
        print Values;  
        ax.bar( Z, Values, width=width, color = colors [ I ], bottom = bottomI )
        for J in range(len(Values) ): bottomI[J]+= Values [ J ]
        print bottomI;

    plt.savefig(OutputFile ,dpi=320);

    return

#####################################################################################################################################################

def PanelOfStackedBarZProfiles ( Uklad, OutputFile ):

# wiec to powinno zwracac figure zlozona z szesciu paneli
# przerobimy to w matplotlibie

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(nrows=len(Uklad), ncols=len(Uklad[0]))

    fig.set_size_inches(10.5,18.5) # zmienic size na ten przepisany
    subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=None)

    left  = 0.125  # the left side of the subplots of the figure
    right = 0.9    # the right side of the subplots of the figure
    bottom = 0.1   # the bottom of the subplots of the figure
    top = 0.9      # the top of the subplots of the figure
    wspace = 1.5   # the amount of width reserved for blank space between subplots
    hspace = 0.5   # the amount of height reserved for white space between subplots


#    colors = [ 'Dummy','DarkBlue', 'Cyan', 'LightGreen', 'Orange', 'Brown' ]

    colors = [ 'Dummy','DarkBlue', 'Cyan', 'LightGreen', 'Orange', 'Brown', 'Black' ]

# glowny problem jest taki ze facing lipid membrane naleza w tej chwili do buried a powinny byc gdzie indziej,
# w tabeli powinny byc tez dane dotyczace tej powierzchni przed facing i to jest problem
# takie dane mozna wziac tylko z modeli :P 

 # Or equivalently,  "plt.tight_layout()"

#    plt.show() # musze poszukac jeszcze raz jak to szlo

#    fig = plt.figure()
#    axes[0][0]  = fig.add_subplot(111)

#    Titles = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ];

#    Titles = [ 'B', 'D', 'F', 'H', 'A', 'C', 'E', 'G' ]

#    Titles = [ 'A', 'B', 'C', 'D', 'E' ]

    Titles = [ '', '', '', '', '','','','','','','','','','','' ]

#    if len(Uklad)[0] == 5: 

    for M in range ( len(Uklad) ):

        axes[M][0].set_ylabel('N')
        

        for N in range ( len (Uklad[0]) ):

            InputArray = array ( Uklad [M][N] ) # bo musimy to naprawde skopiowac

            print 'InputArray '+ str(M)+' '+str(N)

#            print InputArray

            Z = array ( InputArray [:,0] ) ;
#            axes[M][N].set_title(Titles[(M*4)+N])#, x=6.0 )
            axes[M][N].set_title(Titles[N])#, x=6.0 ) 
#            axes[M][N]. set_xticks( [ -90.0, -60.0, -30.0,   0.0,  30.0,  60.0,  90.0 ] ) # ticki moga byc gdzie sa
            axes[M][N]. set_xticks( [ -90.0, -60.0, -30.0,   0.0, 10.0, 20.0, 30.0,  60.0,  90.0 ] ) # ticki moga
            axes[M][N]. set_yticks( [   0.0,  50.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0 ] )
#            axes[M][N]. set_yticks( [   0.0,  10.0,  20.0,  30.0,  40.0 ] )
#, 250.0, 300.0, 350.0, 400.0 ] )

            labels = axes[M][N].get_xticklabels()

#            title = axes[M][N].get_title ()
#            title. set_rotation(90)

            for label in labels:
                label.set_rotation(90)

            labels = axes[M][N].get_yticklabels()

            for label in labels:
                label.set_rotation(90)

#show() 

#            axes[M][N].set_xlabel('Z coordinate (A)')#, x=6.0) # czemu nie dzialasz? 
#            axes[M][N].set_xlabel('Z (A)')#, x=6.0) # czemu nie dzialasz?            
            axes[M][N].set_xlabel('RMSD (A)')#, x=6.0) # czemu nie dzialasz?             

# tylko te labele
#            axes[M][N].set_xlim(-70.0, 70.0)

#            axes[M][N].set_xlim(-40.0,  40.0)
            axes[M][N].set_xlim(- 0.0,  30.0)
#            axes[M][N].set_ylim(- 0.0, 400.0)
#            axes[M][N].set_ylim(- 0.0, 160.0)
            axes[M][N].set_ylim(- 0.0, 160.0)
#            width = 9 # for now
# trzeba by to skontrolowac po prostu, wziac grafy only buried itd

            width = 2

            TestN = len ( InputArray [ 0 ] )

            for I in range (2, TestN ): # I to nr kolumny, czyli od drugiej kolumny, 0 = z, 1 - ss bond, 2 - bto

                for J in range ( len ( Z ) ): # teraz bedziemy dodawac tak zeby nastepny byl widoczny zza poprzedniego

                    InputArray  [ J ][ I ]+=  InputArray  [ J ][ I-1 ]

#            print 'InputArray '+ str(M)+' '+str(N)
# czy nie bylo pomyslu na lepszego stacked bara ...

            for I in range ( (TestN -1), 0, -1 ):
        
                Values = InputArray [ :,I ]; 

                axes[M][N].bar(Z, Values, width=width, color = colors [ I ] )

            plt.savefig(OutputFile ,dpi=320, format='png')

    fig.tight_layout()

#####################################################################################################################################################

def PanelOfDCHs ( Uklad, OutputFile ):

# wiec to powinno zwracac figure zlozona z szesciu paneli
# przerobimy to w matplotlibie

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(nrows=len(Uklad), ncols=len(Uklad[0]))

    fig.set_size_inches(10.5,18.5) # zmienic size na ten przepisany
    subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=None)

    left  = 0.125  # the left side of the subplots of the figure
    right = 0.9    # the right side of the subplots of the figure
    bottom = 0.1   # the bottom of the subplots of the figure
    top = 0.9      # the top of the subplots of the figure
    wspace = 1.5   # the amount of width reserved for blank space between subplots
    hspace = 0.5   # the amount of height reserved for white space between subplots

    colors = [ 'Dummy','DarkBlue', 'Cyan', 'LightGreen', 'Orange', 'Brown', 'Black' ]

# glowny problem jest taki ze facing lipid membrane naleza w tej chwili do buried a powinny byc gdzie indziej,
# w tabeli powinny byc tez dane dotyczace tej powierzchni przed facing i to jest problem
# takie dane mozna wziac tylko z modeli :P 

 # Or equivalently,  "plt.tight_layout()"

#    plt.show() # musze poszukac jeszcze raz jak to szlo

#    fig = plt.figure()
#    axes[0][0]  = fig.add_subplot(111)

#    Titles = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ];

#    Titles = [ 'B', 'D', 'F', 'H', 'A', 'C', 'E', 'G' ]

#    Titles = [ 'A', 'B', 'C', 'D', 'E' ]

    Titles = [ 'Kingdom', 'Localization', '', '', '','','','','','','','','','','' ]

#    if len(Uklad)[0] == 5: 

    for M in range ( len(Uklad) ):

        axes[M][0].set_ylabel('N')
        

        for N in range ( len (Uklad[0]) ):

            InputArray = array ( Uklad [M][N] ) # bo musimy to naprawde skopiowac

            print 'InputArray '+ str(M)+' '+str(N)

#            print InputArray

            print InputArray

            Z = array ( InputArray [:,0] ) ;
#            axes[M][N].set_title(Titles[(M*4)+N])#, x=6.0 )
            axes[M][N].set_title(Titles[N])#, x=6.0 ) 
#            axes[M][N]. set_xticks( [ -90.0, -60.0, -30.0,   0.0,  30.0,  60.0,  90.0 ] ) # ticki moga byc gdzie sa
            axes[M][N]. set_xticks( [ -90.0, -60.0, -30.0,   0.0, 10.0, 20.0, 30.0,  60.0,  90.0 ] ) # ticki moga
            axes[M][N]. set_yticks( [   0.0,  5.0, 10.0, 15.0, 20.0, 25.0, 300.0, 350.0, 400.0 ] )
#            axes[M][N]. set_yticks( [   0.0,  10.0,  20.0,  30.0,  40.0 ] )
#, 250.0, 300.0, 350.0, 400.0 ] )

            labels = axes[M][N].get_xticklabels()

#            title = axes[M][N].get_title ()
#            title. set_rotation(90)

            for label in labels:
                label.set_rotation(90)

            labels = axes[M][N].get_yticklabels()

            for label in labels:
                label.set_rotation(90)

#show() 

#            axes[M][N].set_xlabel('Z coordinate (A)')#, x=6.0) # czemu nie dzialasz? 
#            axes[M][N].set_xlabel('Z (A)')#, x=6.0) # czemu nie dzialasz?            
            axes[M][N].set_xlabel('Number of TMs')#, x=6.0) # czemu nie dzialasz?             

# tylko te labele
#            axes[M][N].set_xlim(-70.0, 70.0)

#            axes[M][N].set_xlim(-40.0,  40.0)
            axes[M][N].set_xlim(- 0.0,  20.0)
#            axes[M][N].set_ylim(- 0.0, 400.0)
#            axes[M][N].set_ylim(- 0.0, 160.0)
            axes[M][N].set_ylim(- 0.0, 30.0)
#            width = 9 # for now
# trzeba by to skontrolowac po prostu, wziac grafy only buried itd

            width = 0.8

            TestN = len ( InputArray [ 0 ] )

            for I in range (2, TestN ): # I to nr kolumny, czyli od drugiej kolumny, 0 = z, 1 - ss bond, 2 - bto

                for J in range ( len ( Z ) ): # teraz bedziemy dodawac tak zeby nastepny byl widoczny zza poprzedniego

                    InputArray  [ J ][ I ]+=  InputArray  [ J ][ I-1 ]

#            print 'InputArray '+ str(M)+' '+str(N)
# czy nie bylo pomyslu na lepszego stacked bara ...

            for I in range ( (TestN -1), 0, -1 ):
        
                Values = InputArray [ :,I ]; 

                axes[M][N].bar(Z, Values, width=width, color = colors [ I ] )

            plt.savefig(OutputFile ,dpi=320, format='png')

    fig.tight_layout()

#####################################################################################################################################################


#####################################################################################################################################################

def Heatmap ( ):

    import numpy
    column_labels = list('ABCD')
    row_labels = list('WXYZ')
    data = numpy.random.rand(4,4)
    from matplotlib import pyplot as plt
    heatmap = plt.pcolor(data)
    plt.show ()

    return

####################################################################################################################################################
