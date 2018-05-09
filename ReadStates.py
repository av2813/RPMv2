import numpy as np
import matplotlib.pyplot as plt
import rpmClassDev_Alex as rpm
import os
import importlib
import itertools
from matplotlib import animation



importlib.reload(rpm)

fieldApplied = [58.9, 59.52,60.14, 60.76, 61.38, 62.0, 62.62, 63.24, 63.86]

folder = r'C:\Users\av2813\Box\GitHub\RPM\RPMv2\AlexData'

subfolder = r'\MinorLoopHamp_'
lattice_list = []

for f in fieldApplied:
	sub = subfolder+str(f).replace('.', 'p')+'mT\\'
	name = 'Lattice_Loop7_FieldStrength0p0mT_Angle0p79.npz'
	directory = r'C:\Users\av2813\Box\GitHub\RPM\RPMv2\AlexData\MinorLoopSquareLattice25x25\\'
	file = directory + sub+name
	lattice = rpm.ASI_RPM(25,25)
	lattice.load(file)
	lattice_list.append(lattice)
	#plt.suptitle(str(np.around(f/0.62,0))+'% of Hc')
	#plt.show()
corr = np.zeros((len(lattice_list), len(lattice_list)))
i = 0
for l1 in lattice_list:
	j = 0
	for l2 in lattice_list:
		corr[i, j] = l1.correlation(l1, l2)
		j+=1
	i+=1
plt.figure()
plt.plot(np.around(np.array(fieldApplied)/0.62,0), corr[:,0])
plt.ylabel('Correlation')
plt.xlabel('Applied field (% of Hc)')
plt.title('Correlation between 95% applied field and other states')
print(corr)
fig = plt.figure()
ax = fig.add_subplot(111)
heatmap = ax.imshow(corr)
ax.set_xticks(np.arange(len(fieldApplied)))
ax.set_yticks(np.arange(len(fieldApplied)))
ax.set_xticklabels(np.around(np.array(fieldApplied)/0.62,0))
ax.set_yticklabels(np.around(np.array(fieldApplied)/0.62,0))
plt.colorbar(heatmap)
plt.title('Correlation between all final states')
#plt.axis('square')
plt.show()

