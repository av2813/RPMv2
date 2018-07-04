import rpmClass_Stable as rpm 		#Most recent version of the RPM artificial spin ice code
import importlib			#Package to update the version of rpmClass_Stable
import numpy as np			#Mathematics package


importlib.reload(rpm)		#Reloads RPM file



#Parameters 

#Material Parameters
Hc = 0.062					#Coercive Field
Hc_std = 5					#Stanard deviation in the coercive field (as a percentage)
bar_length = 600e-9			#Bar length in m
vertex_gap = 100e-9			#Vertex gap in m
bar_thickness = 15e-9		#Bar thickness in m
bar_width = 80e-9			#Bar width in m
magnetisation = 830e3		#Saturation magnetisation of material in A/m (permalloy is 830e3)

#Lattice Parameters
size = 5					#Define the size of the lattice

#Minor loop Parameters
field_max = 0.95*Hc/np.cos(np.pi/4)			#Maximum field to by applied at field angle measured in Telsa 
field_angle = 45.			#Angle at which the field will be applied in degrees
steps = 5					#Number of steps between the minimum value of the coercive field
							#and the maxium field specified above. Total number of steps in a 
							#minor loop is = 4*(steps+1)
neighbours = 4				#The radius of neighbouring spins that are included in the local
							#field calculation
loops = 4					#The number of minor field loops to be done

#File information
folder = r'C:\Users\alexv\OneDrive\Documents\GitHub\RPMv2\FlipStateTest'	#The folder for the files to be saved in.
													#must in the format as shown

#Define the system
#The parameters defined above go into the function below that defines the 
#characteristics of the lattice.
lattice = rpm.ASI_RPM(size,size,bar_length = bar_length, \
					vertex_gap = vertex_gap, bar_thickness = bar_thickness, \
        			bar_width = bar_width, magnetisation = magnetisation)
lattice.square(Hc, Hc_std/100)	#Specify whether it is a square or kagome lattice
#lattice.kagome(Hc, Hc_std/100)	#example of kagome

'''
lattice.randomMag()
lattice.fieldSweep(Hmax = field_max, steps = steps, \
					Htheta = field_angle, n=neighbours, \
					loops=loops, folder = folder)
lattice.searchRPM_single(field_max, Htheta = 45, steps =5, n=neighbours,loops=loops, folder = folder)
'''

lattice.analysisSingleFlip(folder)
folder = r'C:\Users\alexv\OneDrive\Documents\GitHub\RPMv2\MCStateTest'
lattice.analysisMC(folder)
