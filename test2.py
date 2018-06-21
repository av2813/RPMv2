import rpmClass_Stable as rpm
import os
import importlib
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce
import time

importlib.reload(rpm)		#make sure that the class is updated with any chanes

#parameters
Hc = 0.062
Hc_std = 0
bar_length = 400e-9
vertex_gap = 100e-9
bar_thickness = 15e-9
bar_width = 80e-9
magnetisation = 800e3

#Graphing and save/load test
kagomeLattice1 = rpm.ASI_RPM(5,5,bar_length = bar_length, vertex_gap = vertex_gap, bar_thickness = bar_thickness, \
        bar_width = bar_width, magnetisation = magnetisation)
kagomeLattice1.square()
kagomeLattice1.randomMag()
state_info = kagomeLattice1.searchRPM_monte(5, 0.062*0.95)
'''
for bar_length in np.array([600,1000])*1e-9:
	for width in np.array([80, 140])*1e-9:
		for gaps in np.array([100, 200])*1e-9:
			kagomeLattice1 = rpm.ASI_RPM(30,30,bar_length = bar_length, vertex_gap = gaps, bar_thickness = bar_thickness, \
        bar_width = width, magnetisation = magnetisation)
			kagomeLattice1.square()
			for n in np.arange(1, 6):
				kagomeLattice1.localFieldHistogram(31,30, n, 10000, save = True)
'''