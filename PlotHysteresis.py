squareLattice.square(Hc_mean=Hc, Hc_std=Hc_std)
squareLattice.save('Lattice1_Saturated')
squareLattice.randomMag()
squareLattice.save('Lattice1_Random')
import numpy as np
import matplotlib.pyplot as plt
import rpmClassDev_Alex as rpm


Disorder = [0.025, 0.13]

for d in Disorder:
	data = np.load('HysteresisQuenchedDisorderKagome'+str(d).replace('.','p')+ '.npz')
	field = data['arr_0']
	correlation = data['arr_1']
	mag = data['arr_2']
	monopole = data['arr_3']

	corr = plt.figure('Correlation'+str(d))
	ax_c = corr.add_subplot(111)
	ax_c.plot(field[:,1],correlation,'o-', label = d)

	mag_plot = plt.figure('Magnetisation (y-direction)'+str(d))
	ax_m = mag_plot.add_subplot(111)
	ax_m.plot(field[:,1]*1000,2*mag[:,1],'o-', label = str(d*100)+'%')
	plt.xlabel('Magnetic field (mT)')
	plt.ylabel('Magnetisation (y-direction)')
	plt.legend()
	plt.title('Hysteresis Quenched Disorder (My)')
	mono = plt.figure('Monopole Density'+str(d))
	ax_mono = mono.add_subplot(111)
	ax_mono.plot(field[20:,1]*1000,monopole[20:],'o-', label = str(d*100)+'%')
	plt.xlabel('Magnetic field (mT)')
	plt.ylabel('Monopole Density')
	plt.legend()
	plt.title('Hysteresis Quenched Disorder (Monopole)')

plt.show()