# axes.py
from pymol.cgo import *
from pymol import cmd
from pymol.vfont import plain

from sys import argv
my_argv = [float(arg) for arg in argv[1:]]
print my_argv[0], my_argv[1]

 
#rotate x, 90.0

# add labels to axes object (requires pymol version 0.8 or greater, I
# believe
 
cyl_text(obj,plain,[-5.,-5.,-1],'Origin',0.20,axes=[[3,0,0],[0,3,0],[0,0,3]])
cyl_text(obj,plain,[10.,0.,0.],'X',0.20,axes=[[3,0,0],[0,3,0],[0,0,3]])
cyl_text(obj,plain,[0.,10.,0.],'Y',0.20,axes=[[3,0,0],[0,3,0],[0,0,3]])
cyl_text(obj,plain,[0.,0.,10.],'Main',0.20,axes=[[3,0,0],[0,3,0],[0,0,3]])


# Cylinder #1 on left.
x1,y1,z1 = 0, 0, 0 # start point
r1,g1,b1 = 0,0,0 # color (black)
x2,y2,z2 = my_argv[0]*10.0, my_argv[1]*10.0, my_argv[2]*10.0 # end point; to bedzie vector main axis
x3,y3,z3 = my_argv[3]*10.0, my_argv[4]*10.0, my_argv[5]*10.0 # end point; to bedzie vector main axis
x4,y4,z4 = my_argv[6]*10.0, my_argv[7]*10.0, my_argv[8]*10.0 # end point; to bedzie vector main axis


r2,g2,b2 = 1,0,0 # color (red)
r3,g3,b3 = 1,1,0 # color (yellow)
r4,g4,b4 = 0,1,0 # color (green)
r5,g5,b5 = 0,0,1 # color (blue)
radius = 0.5
cmd.load_cgo( [ 9.0, x1, y1, z1, x2, y2, z2, radius, r1, g1, b1, r2, g2, b2 ], "cylinder1" )
cmd.load_cgo( [ 9.0, x1, y1, z1, x3, y3, z3, radius, r1, g1, b1, r4, g4, b4 ], "cylinder3" )
cmd.load_cgo( [ 9.0, x1, y1, z1, x4, y4, z4, radius, r1, g1, b1, r5, g5, b5 ], "cylinder4" )

cmd.load_cgo( [ 9.0, x1, y1, z1, 0., 0.,40. , radius, r1, g1, b1, r3, g3, b3 ], "cylinder2" )
cyl_text(plain,[x2, y2, z2],'Main Axis',0.20,axes=[[3,0,0],[0,3,0],[0,0,3]])

cgo = []
 
axes = [[20.0,0.0,0.0],[0.0,20.0,0.0],[0.0,0.0,20.0]]
 
pos = [0.0,0.0,0.0]
wire_text(cgo,plain,pos,'Hello World',axes)

#rotate x, 90.0
#rotate x, 90.0, cylinder1
#rotate x, 90.0, cylinder2
set depth_cue, 0
#bg_color white
show cartoon
hide lines
zoom center, 20
ray 500,500
png plik1.png
quit
