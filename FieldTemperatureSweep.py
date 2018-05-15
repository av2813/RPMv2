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

squareLattice.kagome(Hc, 0.05)
monopole = []
mag =[]
fieldsteps = np.arange(0.1, 60, 1.)*1e-3
for Hs in fieldsteps:
	print(Hs)
	squareLattice.randomMag()
	squareLattice.fieldTemperature(Hs, n=3, nangle=1)
	squareLattice.graph()
	monopole.append(squareLattice.monopoleDensity())
	mag.append(squareLattice.netMagnetisation())
	print(mag, monopole)
	squareLattice.graph()
	squareLattice.save('TemperatureSweep'+str(Hs).replace('.', 'p'))




