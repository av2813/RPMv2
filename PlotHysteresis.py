
import numpy as np
import matplotlib.pyplot as plt
import rpmClassDev_Alex as rpm


Disorder = [0.0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25]

for d in Disorder:
	data = np.load('HysteresisQuenchedDisorder'+str(d).replace('.','p')+ '.npz')
	field = data['arr_0']
	correlation = data['arr_1']
	mag = data['arr_2']
	monopole = data['arr_3']

	corr = plt.figure('Correlation')
	ax_c = corr.add_subplot(111)
	ax_c.plot(field[:,1],correlation,'o-', label = d)

	mag_plot = plt.figure('Magnetisation (y-direction)')
	ax_m = mag_plot.add_subplot(111)
	ax_m.plot(field[:,1]*1000,2*mag[:,1],'o-', label = str(d*100)+'%')
	plt.xlabel('Magnetic field (mT)')
	plt.ylabel('Magnetisation (y-direction)')
	plt.legend()
	plt.title('Hysteresis Quenched Disorder (My)')
	#mono = plt.figure('Monopole')
	#ax_mono = mono.add_subplot(111)
	#ax_mono.plot(monopole/4.*(25.**2/24.**2),'.')


plt.show()