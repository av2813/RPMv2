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
relax_field = np.array([100.,100.,0.])

angle = 45

squareLattice = rpm.ASI_RPM(10, 10, bar_length = bar_length,\
vertex_gap = vertex_gap, bar_thickness = bar_thickness,\
bar_width = bar_width, magnetisation = magnetisation)

Hc_std = 0.05
#squareLattice.load('SaturatedLattice1.npz')


#squareLattice.relax(Happlied = relax_field)
#squareLattice.graph()


#squareLattice.save('SaturatedLattice1.npz')


squareLattice.square(Hc_mean=Hc, Hc_std=Hc_std)
squareLattice.save('SaturatedLattice_5x5_3')
squareLattice.graph()
squareLattice.randomMag()
squareLattice.save('RandomLattice_5x5_3')
squareLattice.graph()
plt.show()
#squareLattice.save('RandomLattice1')
"""
Hamp = 0.95*Hc
folder = r'D:\From old laptop\Postdoc\Data\RPM-results\MinorLoopHamp_'
directory = folder+str(np.around(Hamp*1000,4)).replace('.', 'p')+'mT'
fieldloops, q, mag, monopole = squareLattice.fieldsweep(Hamp/np.cos(np.pi*angle/180),20,angle, n = 5, loops = 8, folder = directory)
np.savez('MinorloopQuenchedDisorder'+str(np.around(Hamp*1000,4)).replace('.', 'p')+'mT', fieldloops, q, mag, monopole)
"""