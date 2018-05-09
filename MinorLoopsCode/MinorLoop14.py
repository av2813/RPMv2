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

import rpmClassDev_Alex as rpm


importlib.reload(rpm)

Hc = 0.062
bar_length = 220e-9
vertex_gap = 1e-7
bar_thickness = 25e-9
bar_width = 80e-9
magnetisation = 800e3

angle = 45


squareLattice = rpm.ASI_RPM(25, 25, bar_length = bar_length,\
 vertex_gap = vertex_gap, bar_thickness = bar_thickness,\
 bar_width = bar_width, magnetisation = magnetisation)



Hc_std = 0.05
squareLattice.load('RandomLattice1.npz')
Hamp = 1.2*Hc
folder = r'C:\Users\av2813\Box\GitHub\RPM\RPMv2\AlexData\MinorLoopHamp_'
directory = folder+str(np.around(Hamp*1000,4)).replace('.', 'p')+'mT'
fieldloops, q, mag, monopole = squareLattice.fieldsweep(Hamp/np.cos(np.pi*angle/180),20,angle, n = 5, loops = 8, folder = directory)
np.savez('MinorloopQuenchedDisorder'+str(np.around(Hamp*1000,4)).replace('.', 'p')+'mT', fieldloops, q, mag, monopole)