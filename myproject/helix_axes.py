# axes.py
from pymol.cgo import *
from pymol import cmd
from pymol.vfont import plain
from sys import argv
 
# create the axes object, draw axes with cylinders coloured red, green,
#blue for X, Y and Z

#powinienem ogarnac to i podpisy w jakis elegancki sposob;

#powinienem to rozbic jakos

#######################################################################################################

def helix_axes(c_x, c_y, c_z, mAx_x, mAx_y, mAx_z, cec_x, cec_y, cec_z, ecAx_x, ecAx_y, ecAx_z, cic_x, cic_y, cic_z, icAx_x, icAx_y, icAx_z, o1_x, o1_y, o1_z, o2_x, o2_y, o2_z ):

        c_x, c_y, c_z, mAx_x, mAx_y, mAx_z, cec_x, cec_y, cec_z, ecAx_x, ecAx_y, ecAx_z, cic_x, cic_y, cic_z, icAx_x, icAx_y, icAx_z, o1_x, o1_y, o1_z, o2_x, o2_y, o2_z = [float(Arg) for Arg in [c_x, c_y, c_z, mAx_x, mAx_y, mAx_z, cec_x, cec_y, cec_z, ecAx_x, ecAx_y, ecAx_z, cic_x, cic_y, cic_z, icAx_x, icAx_y, icAx_z, o1_x, o1_y, o1_z, o2_x, o2_y, o2_z]]
 
	obj = [
	   CYLINDER, c_x, c_y, c_z, c_x,  c_y, c_z+5., 0.2, 1.0, 1.0, 1.0, 0., 0.0, 1.0,
	   CYLINDER, c_x, c_y, c_z, mAx_x, mAx_y, mAx_z, 0.2, 1.0, 1.0, 1.0, 1., 0.0, 0,
	   CYLINDER, cec_x, cec_y, cec_z, ecAx_x, ecAx_y, ecAx_z, 0.2, 1.0, 1.0, 1.0, 0., 1.0, 0.0,
	   CYLINDER, cic_x, cic_y, cic_z, icAx_x, icAx_y, icAx_z, 0.2, 1.0, 1.0, 1.0, 0., 0.0, 1.0,
	   CYLINDER, o1_x, o1_y, o1_z, o2_x, o2_y, o2_z, 0.2, 1.0, 1.0, 1.0, 0., 0.0, 0.0,

	   ]
 
# add labels to axes object (requires pymol version 0.8 or greater, I
# believe
 

	cyl_text(obj,plain,[c_x,  c_y, c_z+5.],'Z',0.20,color=[0.0,0.0,0.0],axes=[[1,0,0],[0,1,0],[0,0,1]])
	cyl_text(obj,plain,[mAx_x,mAx_y,mAx_z],'M',0.10,color=[0.0,0.0,0.0],axes=[[1,0,0],[0,1,0],[0,0,1]])
	cyl_text(obj,plain,[ecAx_x,ecAx_y,ecAx_z],'Ec',0.10,color=[0.0,0.0,0.0],axes=[[1,0,0],[0,1,0],[0,0,1]])
	cyl_text(obj,plain,[icAx_x,icAx_y,icAx_z],'Ic',0.10,color=[0.0,0.0,0.0],axes=[[1,0,0],[0,1,0],[0,0,1]])
	cyl_text(obj,plain,[o1_x,o1_y,o1_z],'Oec',0.10,color=[0.0,0.0,0.0],axes=[[1,0,0],[0,1,0],[0,0,1]])
	cyl_text(obj,plain,[o2_x,o2_y,o2_z],'Oic',0.10,color=[0.0,0.0,0.0],axes=[[1,0,0],[0,1,0],[0,0,1]])


	cmd.load_cgo(obj,'axes')

#######################################################################################################

cmd.extend( "helix_axes", helix_axes );
