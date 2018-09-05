'''
Alex Code

'''

#Import the necessary packages to run the code
import rpmClass_Stable as rpm 		#Most recent version of the RPM artificial spin ice code

from importlib import *	 		#Package to update the version of rpmClass_Stable
import numpy as np			#Mathematics package

reload(rpm)		#Reloads RPM file

import importlib			#Package to update the 
import numpy as np

#importlib.reload(rpm)		#
import matplotlib.pyplot as plt
from matplotlib2tikz import save as tikz_save
import os



Disorder = [0.0, 0.05, 0.2]

Hc = 0.062
bar_length = 400e-9
vertex_gap = 1e-7
bar_thickness = 20e-9
bar_width = 80e-9
magnetisation = 800e3


Lattice = rpm.ASI_RPM(50, 50, bar_length = bar_length,\
 vertex_gap = vertex_gap, bar_thickness = bar_thickness,\
 bar_width = bar_width, magnetisation = magnetisation)

Lattice.square(Hc_mean=Hc, Hc_std=0.05)
x, y = (51, 50)
Lattice.relax(Happlied = np.array([100.,100,0.]), n=1)
satField_list = []
n_list = []
Lattice.randomMag()
for i in np.arange(1, 51):
	saturatedLocField = Lattice.Hlocal2(x,y, n=i)
	fieldStrength = (saturatedLocField[0]**2+saturatedLocField[1]**2)**0.5
	satField_list.append(fieldStrength)
	#print(saturatedLocField)
	#Lattice.localPlot(x, y, i)
	n_list.append(i)

plt.figure()
plt.plot(n_list, 1000*np.array(satField_list), '.', color = 'darkblue')
plt.xlabel('Radius of bars included')
plt.ylabel('Magnetic field strength (mT)')
plt.ylim([0, 4])
folder = r'C:\Users\av2813\Box\Writing\ESA\Images\MacroSpinSim\RadiusIncluded'
file = 'RandSquare4'
tikz_save(os.path.join(folder, file+'.tikz'))
plt.savefig(os.path.join(folder, file+'.png'))
plt.savefig(os.path.join(folder, file+'.pdf'))
plt.savefig(os.path.join(folder, file+'.pgf'))
plt.show()