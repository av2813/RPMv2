import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as cl
from matplotlib.ticker import MaxNLocator
import copy
import rpmClassDev_Alex as rpm

Hc = 0.062
bar_length = 220e-9
vertex_gap = 1e-7
bar_thickness = 25e-9
bar_width = 80e-9
magnetisation = 800e3

angle = 45

n = 5
Hper = 0.94
squareLattice = rpm.ASI_RPM(n, n, bar_length = bar_length,\
 vertex_gap = vertex_gap, bar_thickness = bar_thickness,\
 bar_width = bar_width, magnetisation = magnetisation)



squareLattice.load('Lattice1_Random5x5.npz')
Hamp = Hper*Hc
fieldloops, q, mag, monopole, vertex = squareLattice.fieldsweep(Hamp/np.cos(np.pi*angle/180),20,angle, n = 5, loops = 8)
np.savez('MinorloopQuenchedDisorder1_Random'+str(n)+'x'+str(n), fieldloops, q, mag, monopole, vertex)


squareLattice.load('Lattice2_Random5x5.npz')
Hamp = Hper*Hc
fieldloops, q, mag, monopole, vertex = squareLattice.fieldsweep(Hamp/np.cos(np.pi*angle/180),20,angle, n = 5, loops = 8)
np.savez('MinorloopQuenchedDisorder2_Random'+str(n)+'x'+str(n), fieldloops, q, mag, monopole, vertex)


squareLattice.load('Lattice3_Random5x5.npz')
Hamp = Hper*Hc
fieldloops, q, mag, monopole, vertex = squareLattice.fieldsweep(Hamp/np.cos(np.pi*angle/180),20,angle, n = 5, loops = 8)
np.savez('MinorloopQuenchedDisorder3_Random'+str(n)+'x'+str(n), fieldloops, q, mag, monopole, vertex)


squareLattice.load('Lattice1_Saturated5x5.npz')
Hamp = Hper*Hc
fieldloops, q, mag, monopole, vertex = squareLattice.fieldsweep(Hamp/np.cos(np.pi*angle/180),20,angle, n = 5, loops = 8)
np.savez('MinorloopQuenchedDisorder1_Saturated'+str(n)+'x'+str(n), fieldloops, q, mag, monopole, vertex)


squareLattice.load('Lattice2_Saturated5x5.npz')
Hamp = Hper*Hc
fieldloops, q, mag, monopole, vertex = squareLattice.fieldsweep(Hamp/np.cos(np.pi*angle/180),20,angle, n = 5, loops = 8)
np.savez('MinorloopQuenchedDisorder2_Saturated'+str(n)+'x'+str(n), fieldloops, q, mag, monopole, vertex)


squareLattice.load('Lattice3_Saturated5x5.npz')
Hamp = Hper*Hc
fieldloops, q, mag, monopole, vertex = squareLattice.fieldsweep(Hamp/np.cos(np.pi*angle/180),20,angle, n = 5, loops = 8)
np.savez('MinorloopQuenchedDisorder3_Saturated'+str(n)+'x'+str(n), fieldloops, q, mag, monopole, vertex)