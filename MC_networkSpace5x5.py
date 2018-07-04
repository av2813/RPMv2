import rpmClass_Stable as rpm

import os
import importlib
import matplotlib.pyplot as plt
import numpy as np
<<<<<<< HEAD
from functools import reduce
=======
>>>>>>> master
import time
import sys

sys.setrecursionlimit(1500)
importlib.reload(rpm)
#parameters
Hc = 0.062
Hc_std = 0.05
bar_length = 400e-9
vertex_gap = 100e-9
bar_thickness = 15e-9
bar_width = 80e-9
magnetisation = 800e3

# baseLattice = rpm.ASI_RPM(5,5,bar_length = bar_length, vertex_gap = vertex_gap, bar_thickness = bar_thickness, \
#         bar_width = bar_width, magnetisation = magnetisation)
# baseLattice.square(Hc, Hc_std)

# baseLattice.searchRPM_monte(100, 0.95*Hc/np.cos(45/190*np.pi), Htheta = 45, steps =10, n=3,loops=4, folder = 'RPMnetwork5x5v2')
def runMC(size):
	baseLattice = rpm.ASI_RPM(size,size,bar_length = bar_length, vertex_gap = vertex_gap, bar_thickness = bar_thickness, \
        bar_width = bar_width, magnetisation = magnetisation)
	baseLattice.square(Hc, Hc_std)

	baseLattice.searchRPM_monte(100, 0.95*Hc/np.cos(45/180*np.pi), Htheta = 45, steps =4, n=3,loops=6, folder = 'RPMnetwork5x5v2')

def runMC_single(size):
	baseLattice = rpm.ASI_RPM(size,size,bar_length = bar_length, vertex_gap = vertex_gap, bar_thickness = bar_thickness, \
        bar_width = bar_width, magnetisation = magnetisation)
	baseLattice.square(Hc, Hc_std)
	#baseLattice.randomMag()
	#baseLattice.fieldSweep(0.95*Hc/np.cos(45/180*np.pi), 4, 45, n=3, loops=6, folder = r'RPMnetwork5x5v5\Initial')
	baseLattice.searchRPM_single(0.95*Hc/np.cos(45/180*np.pi), Htheta = 45, steps =4, n=3,loops=6, folder = 'RPMnetwork5x5v5')

def runMC_multiple(size):
	baseLattice = rpm.ASI_RPM(size,size,bar_length = bar_length, vertex_gap = vertex_gap, bar_thickness = bar_thickness, \
        bar_width = bar_width, magnetisation = magnetisation)
	baseLattice.square(Hc, Hc_std)
	baseLattice.randomMag()
	baseLattice.fieldSweep(0.95*Hc/np.cos(45/180*np.pi), 4, 45, n=3, loops=6, folder = r'RPMnetwork5x5v5\Initial')
	baseLattice.searchRPM_multiple(100, 5, 0.95*Hc/np.cos(45/180*np.pi), Htheta = 45, steps =4, n=3,loops=6, folder = 'RPMnetwork5x5v5')

def readMC(folder, end, size = 10):
	lattice_list_start = []
	lattice_list_end = []
	endstr = '_'+str(end)+'Loop1_FieldStrength'
	startstr = '_'+str(0)+'Loop'
	for root, dirs, files in os.walk(folder):
		for file in files:
			if file[-4:] == '.npz' and (startstr) in file:
				lattice = rpm.ASI_RPM(size,size)
				lattice.load(os.path.join(root,file))
				lattice_list_start.append(lattice)
			if file[-4:] == '.npz' and (endstr) in file:
				lattice = rpm.ASI_RPM(size,size)
				lattice.load(os.path.join(root,file))
				lattice_list_end.append(lattice)

	corrstart = np.zeros((len(lattice_list_start), len(lattice_list_start)))
	corrend = np.zeros((len(lattice_list_start), len(lattice_list_start)))
	relcorrstart = []
	relcorrend = []
	i = 0 
	M0 = rpm.ASI_RPM(size,size)
	M0.load(r'C:\Users\av2813\Documents\GitHub\RPMv2\RPMnetwork5x5v5\InitialState.npz')
	for l1, l3 in zip(lattice_list_start, lattice_list_end):
		j = 0
		for l2, l4 in zip(lattice_list_start, lattice_list_end):
			corrstart[i, j] = l1.correlation(l1, l2)
			corrend[i, j] = l3.correlation(l3, l4)
			j+=1
		relcorrstart.append(M0.correlation(M0,l1))
		relcorrend.append(M0.correlation(M0,l3))
		i+=1
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.plot(np.array(corrstart).flatten(), np.array(corrstart).flatten(),'.')
	fig1 = plt.figure()
	plt.plot(relcorrstart, relcorrend, '.')
	fig2 = plt.figure()
	ax2 = fig2.add_subplot(111)
	heatmap = ax2.imshow(corrend)
	#ax2.set_xticks(np.arange(len(lattice_list_start)))
	#ax2.set_yticks(np.arange(len(lattice_list_start)))
	#ax.set_xticklabels(np.around(np.array(lattice_list_end),0))
	#ax.set_yticklabels(np.around(np.array(lattice_list_end),0))
	plt.colorbar(heatmap)
	plt.title('Correlation between all final states')
	#plt.axis('square')
	plt.show()

def countStates(file, end, size = 7):
	lattice_list_start = []
	lattice_list_end = []
	endstr = '_'+str(end)+'Loop1_FieldStrength'
	startstr = '_'+str(0)+'Loop'
	for root, dirs, files in os.walk(folder):
		for file in files:
			if file[-4:] == '.npz' and (startstr) in file:
				lattice = rpm.ASI_RPM(size,size)
				lattice.load(os.path.join(root,file))
				lattice_list_start.append(lattice)
			if file[-4:] == '.npz' and (endstr) in file:
				lattice = rpm.ASI_RPM(size,size)
				lattice.load(os.path.join(root,file))
				lattice_list_end.append(lattice)
	i = 0 
	M0 = rpm.ASI_RPM(size,size)
	M0.load(r'C:\Users\av2813\Documents\GitHub\RPMv2\RPMnetwork5x5v5\InitialState.npz')
	for l1, l3 in zip(lattice_list_start, lattice_list_end):


#runMC_single(7)
#runMC_multiple(10)
readMC(r'C:\Users\av2813\Documents\GitHub\RPMv2\RPMnetwork5x5v5', 39, size = 7)