import rpmClassDev_Alex as rpm
import importlib
import numpy as np

importlib.reload(rpm)

Hc = 0.062
Hc_std = 0.05
bar_length = 220e-9
vertex_gap = 1e-8
bar_thickness = 25e-9
bar_width = 80e-9
magnetisation = 800e3

Hc = 0.062
Hc_std = 0.05

squareLattice = rpm.ASI_RPM(10, 10, bar_length = bar_length,\
 vertex_gap = vertex_gap, bar_thickness = bar_thickness,\
 bar_width = bar_width, magnetisation = magnetisation)

squareLattice.square(Hc, 0.05)
monopole = []
mag =[]
fieldsteps = np.linspace(1, 60, 10)*1e-4
for Hs in fieldsteps:
	squareLattice.fieldTemperature(Hs, Hc, n=3, nangle=36)
	monopole.append(squareLattice.monopoleDensity())
	mag.append(squareLattice.netMagnatisation())




