# axes.py
from pymol.cgo import *
from pymol import cmd
from pymol.vfont import plain

from sys import argv

argumenty = [float(arg) for arg in sys.argv[1:]] # arguments start from second argv[1:]

center  = argumenty [:3] # helix center of mass
my_argv = argumenty [3: ] # helix: Main, EC, IC axes

my_argv = [coord *10.0 for coord in my_argv] # we scale axes times 10

for n in range(len(my_argv)):

    my_argv[n] += center [n % 3]  # we translate the end of axes by the coords of center

# add labels to axes object (requires pymol version 0.8 or greater, I
# believe
 

# Cylinder #1 on left.
x1,y1,z1 = center[0], center[1], center[2] # start point

r1,g1,b1 = 0,0,0 # color (black)
x2,y2,z2 = my_argv[0], my_argv[1], my_argv[2] # end point; to bedzie vector Main Axis
x3,y3,z3 = my_argv[3], my_argv[4], my_argv[5] # end point; to bedzie vector EC   Axis
x4,y4,z4 = my_argv[6], my_argv[7], my_argv[8] # end point; to bedzie vector IC   Axis


r2,g2,b2 = 1,0,0 # color (red)
r3,g3,b3 = 1,1,0 # color (yellow)
r4,g4,b4 = 0,1,0 # color (green)
r5,g5,b5 = 0,0,1 # color (blue)

radius = 0.7

cmd.load_cgo( [ 9.0, x1, y1, z1, x2, y2, z2, radius, r1, g1, b1, r2, g2, b2 ], "cylinder1" )
cmd.load_cgo( [ 9.0, x1, y1, z1, x3, y3, z3, radius, r1, g1, b1, r4, g4, b4 ], "cylinder3" )
cmd.load_cgo( [ 9.0, x1, y1, z1, x4, y4, z4, radius, r1, g1, b1, r5, g5, b5 ], "cylinder4" )

cmd.load_cgo( [ 9.0, x1, y1, z1, x1, y1, z2 , radius, r1, g1, b1, r3, g3, b3 ], "cylinder2" ) # z axis
cyl_text(plain,[x2, y2, z2],'Main Axis',0.20,axes=[[3,0,0],[0,3,0],[0,0,3]])

cgo = []
 
axes = [[20.0,0.0,0.0],[0.0,20.0,0.0],[0.0,0.0,20.0]]
 
pos = [0.0,0.0,0.0]
wire_text(cgo,plain,pos,'Hello World',axes)

set depth_cue, 0
#bg_color white
show cartoon
hide lines
zoom center, 20
ray 500,500
png plik1.png
quit
