import rpmClass_Stable as rpm
import os
import importlib
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce
import time

importlib.reload(rpm)		#make sure that the class is updated with any changes


Hc = 0.062
Hc_std = 0
bar_length = 400e-9
vertex_gap = 100e-9
bar_thickness = 15e-9
bar_width = 80e-9
magnetisation = 800e3

baseLattice = rpm.ASI_RPM(100,100,bar_length = bar_length, vertex_gap = vertex_gap, bar_thickness = bar_thickness, \
        bar_width = bar_width, magnetisation = magnetisation)

baseLattice.square(Hc, Hc_std)
baseLattice.randomMag()
baseLattice.latticeFieldHistogram(5, save = True)
baseLattice.effectiveCoerciveHistogram(5,save = True)
