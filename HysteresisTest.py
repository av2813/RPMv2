'''
Alex Code

'''

#Import the necessary packages to run the code
import rpmClass_Stable as rpm 		#Most recent version of the RPM artificial spin ice code

import importlib			#Package to update the version of rpmClass_Stable
import numpy as np			#Mathematics package

importlib.reload(rpm)		#Reloads RPM file

import importlib			#Package to update the 
import numpy as np

importlib.reload(rpm)		#
import os



Disorder = [0.0, 0.05, 0.2]

Hc = 0.062
bar_length = 400e-9
vertex_gap = 1e-7
bar_thickness = 20e-9
bar_width = 80e-9
magnetisation = 800e3

angle = 30


Lattice = rpm.ASI_RPM(25, 25, bar_length = bar_length,\
 vertex_gap = vertex_gap, bar_thickness = bar_thickness,\
 bar_width = bar_width, magnetisation = magnetisation)
i = 0
for Hc_std in np.array([0.0, 0.05, 0.2]):
	Lattice.kagome(Hc_mean=Hc, Hc_std=Hc_std)
	#squareLattice.randomMag()
	#Lattice.relax()
	Hamp = 2*Hc
	i = i+1
	print(Hamp)
	folder = r'C:\Users\av2813\Box\Writing\ESA\Images\MacroSpinSim\Hysteresis\Kagome'
	directory = folder+str(Hc_std).replace('.', 'p')
	if not os.path.exists(directory):
		os.makedirs(directory) 
	Lattice.fieldSweep(Hamp,50,angle, n = 10, loops = 2, folder = directory)



for d in Disorder:
	data = np.load('HysteresisQuenchedDisorderKagome'+str(d).replace('.','p')+ '.npz')
	field = data['arr_0']
	correlation = data['arr_1']
	mag = data['arr_2']
	monopole = data['arr_3']

	corr = plt.figure('Correlation'+str(d))
	ax_c = corr.add_subplot(111)
	ax_c.plot(field[:,1],correlation,'o-', label = d)

	mag_plot = plt.figure('Magnetisation (y-direction)'+str(d))
	ax_m = mag_plot.add_subplot(111)
	ax_m.plot(field[:,1]*1000,2*mag[:,1],'o-', label = str(d*100)+'%')
	plt.xlabel('Magnetic field (mT)')
	plt.ylabel('Magnetisation (y-direction)')
	plt.legend()
	plt.title('Hysteresis Quenched Disorder (My)')
	mono = plt.figure('Monopole Density'+str(d))
	ax_mono = mono.add_subplot(111)
	ax_mono.plot(field[20:,1]*1000,monopole[20:],'o-', label = str(d*100)+'%')
	plt.xlabel('Magnetic field (mT)')
	plt.ylabel('Monopole Density')
	plt.legend()
	plt.title('Hysteresis Quenched Disorder (Monopole)')

plt.show()
