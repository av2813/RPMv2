import numpy as np
import matplotlib.pyplot as plt
import rpmClassDev_Alex as rpm

n = 5
lattice = rpm.ASI_RPM(n,n)



#fieldApplied = [58.9, 59.52,60.14, 60.76, 61.38, 62.0, 62.62, 63.24, 63.86]
#fieldApplied = [68.3, 71.3,74.4, 77.5]

corrEnd = []
monoEnd = []
magEnd = []

loops = np.arange(0,9,1)

#for f in fieldApplied:
data = np.load('MinorloopQuenchedDisorder'+str(n)+'x'+str(n)+'.npz')
field = data['arr_0']
correlation = data['arr_1']
mag = data['arr_2']
monopole = data['arr_3']
vertex = data['arr_4']

cor_split = np.split(correlation, 8)
c = []
c.append(correlation[0])
for t in cor_split:
	c.append(t[-1])
corrEnd.append(np.array(c))

mag_split = np.split(mag, 8)
c = []
c.append(np.linalg.norm(2*mag[0]))
for t in mag_split:
	c.append(np.linalg.norm(2*t[-1]))
magEnd.append(np.array(c))

mono_split = np.split(monopole, 8)
c = []
c.append(monopole[0])
for t in mono_split:
	c.append(t[-1])
monoEnd.append(np.array(c))

corr = plt.figure('Correlation')
ax_c = corr.add_subplot(111)
ax_c.plot(correlation,'.', label = np.around(np.array(f)/0.62,0))
plt.ylabel('Correlation')
plt.xlabel('Number of field steps')
plt.legend()
plt.savefig('CorrelationFieldsteps')

mag_plot = plt.figure('Magnetisation')
ax_m = mag_plot.add_subplot(111)
ax_m.plot(2*mag[:,0],'.', label = np.around(np.array(f)/0.62,0))
plt.ylabel('Magnetisation')
plt.xlabel('Number of field steps')
plt.legend()
plt.savefig('MagnetisationFieldsteps')

mono = plt.figure('Monopole')
ax_mono = mono.add_subplot(111)
ax_mono.plot(monopole,'.', label = str(np.around(np.array(f)/0.62,0))+'%')
plt.ylabel('Monopole density')
plt.xlabel('Number of field steps')
plt.legend()
plt.savefig('MonopoleFieldsteps')

mono = plt.figure('Vertex')
ax_mono = mono.add_subplot(111)
ax_mono.plot(vertex,'.', label = str(np.around(np.array(f)/0.62,0))+'%')
plt.ylabel('Vertex Percentage')
plt.xlabel('Number of field steps')
plt.legend()
plt.savefig('VertexFieldsteps')

plt.figure()
for y,l in zip(np.array(corrEnd), np.around(np.array(fieldApplied)/0.62,0)):
	plt.plot(loops,y,'o-', label = str(l)+'%')
plt.legend()
plt.title('Pecentage of field applied minor loops',fontsize=14)
plt.ylabel('Correlation')
plt.xlabel('Number of loops')
plt.legend()
plt.savefig('CorrelationLoops')

plt.figure()
for y,l in zip(np.array(magEnd), np.around(np.array(fieldApplied)/0.62,0)):
	plt.plot(loops,2*y,'o-', label = str(l)+'%')
plt.legend()
plt.title('Pecentage of field applied minor loops',fontsize=14)
plt.ylabel('Magnetisation')
plt.xlabel('Number of loops')
plt.savefig('MagnetisationLoops')

plt.figure()
for y,l in zip(np.array(monoEnd), np.around(np.array(fieldApplied)/0.62,0)):
	y = np.array(y)
	plt.plot(loops,y,'o-', label = str(l)+'%')
plt.legend()
plt.title('Pecentage of field applied minor loops',fontsize=14)
plt.ylabel('Monopole')
plt.xlabel('Number of loops')
plt.savefig('MonopoleLoops')



'''
data = np.load('MinorloopQuenchedDisorder59p52mT.npz')

field = data['arr_0']
correlation = data['arr_1']
mag = data['arr_2']
monopole = data['arr_3']


corr = plt.figure('Correlation')
ax_c = corr.add_subplot(111)
ax_c.plot( correlation,'.')


mag_plot = plt.figure('Magnetisation')
ax_m = mag_plot.add_subplot(111)
ax_m.plot( mag,'.')


mono = plt.figure('Monopole')
ax_mono = mono.add_subplot(111)
ax_mono.plot( monopole,'.')

plt.show()

'''