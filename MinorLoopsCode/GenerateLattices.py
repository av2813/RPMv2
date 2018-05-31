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


squareLattice = rpm.ASI_RPM(5, 5, bar_length = bar_length,\
 vertex_gap = vertex_gap, bar_thickness = bar_thickness,\
 bar_width = bar_width, magnetisation = magnetisation)



Hc_std = 0.05
#squareLattice.load('RandomLattice1.npz')
squareLattice.square(Hc_mean=Hc, Hc_std=Hc_std)
squareLattice.save('Lattice1_Saturated5x5')
squareLattice.randomMag()
squareLattice.save('Lattice1_Random5x5')
squareLattice.square(Hc_mean=Hc, Hc_std=Hc_std)
squareLattice.save('Lattice2_Saturated5x5')
squareLattice.randomMag()
squareLattice.save('Lattice2_Random5x5')
squareLattice.square(Hc_mean=Hc, Hc_std=Hc_std)
squareLattice.save('Lattice3_Saturated5x5')
squareLattice.randomMag()
squareLattice.save('Lattice3_Random5x5')

