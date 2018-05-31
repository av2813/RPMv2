import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as cl
from matplotlib.ticker import MaxNLocator
import copy
import rpmClass_Stable as rpm

Hc = 0.062
bar_length = 220e-9
vertex_gap = 1e-7
bar_thickness = 25e-9
bar_width = 80e-9
magnetisation = 800e3

angle = 45

n = 15
squareLattice = rpm.ASI_RPM(n, n, bar_length = bar_length,\
 vertex_gap = vertex_gap, bar_thickness = bar_thickness,\
 bar_width = bar_width, magnetisation = magnetisation)



Hc_std = 0.05
#squareLattice.load('RandomLattice1.npz')
squareLattice.square(Hc_mean=Hc, Hc_std=Hc_std)
squareLattice.save('Lattice1_Saturated'+str(n)+'x'+str(n))
squareLattice.randomMag()
squareLattice.save('Lattice1_Random'+str(n)+'x'+str(n))
squareLattice.square(Hc_mean=Hc, Hc_std=Hc_std)
squareLattice.save('Lattice2_Saturated'+str(n)+'x'+str(n))
squareLattice.randomMag()
squareLattice.save('Lattice2_Random'+str(n)+'x'+str(n))
squareLattice.square(Hc_mean=Hc, Hc_std=Hc_std)
squareLattice.save('Lattice3_Saturated'+str(n)+'x'+str(n))
squareLattice.randomMag()
squareLattice.save('Lattice3_Random'+str(n)+'x'+str(n))

