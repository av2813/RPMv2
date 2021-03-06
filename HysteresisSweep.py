import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as cl
from matplotlib.ticker import MaxNLocator
#from matplotlib.colors import Normalize
import copy
import pickle
import importlib
import os

import rpmClass_Stable as rpm


importlib.reload(rpm)

Hc = 0.062
bar_length = 220e-9
vertex_gap = 1e-7
bar_thickness = 25e-9
bar_width = 80e-9
magnetisation = 800e3

angle = 90


squareLattice = rpm.ASI_RPM(10, 10, bar_length = bar_length,\
 vertex_gap = vertex_gap, bar_thickness = bar_thickness,\
 bar_width = bar_width, magnetisation = magnetisation)

i = 0
for Hc_std in np.array([0.025, 0.13, 0.2]):
	squareLattice.kagome(Hc_mean=Hc, Hc_std=Hc_std)
	squareLattice.randomMag()
	squareLattice.relax()
	Hamp = 2*Hc
	i = i+1
	print(Hamp)
	folder = r'C:\Users\av2813\Box\GitHub\RPM\KagomeHysteresis'
	directory = folder+str(i)
	if not os.path.exists(directory):
		os.makedirs(directory) 
	fieldloops, q, mag, monopole = squareLattice.fieldsweep(Hamp,30,angle, n = 5, loops = 2, folder = directory)
	np.savez('HysteresisQuenchedDisorderKagome'+str(Hc_std).replace('.', 'p'), fieldloops, q, mag, monopole)
