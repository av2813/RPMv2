import rpmClass_Alexv1 as rpm
import os
import importlib
import matplotlib.pyplot as plt
import numpy as np

importlib.reload(rpm)		#make sure that the class is updated with any chanes

#parameters
Hc = 0.062
Hc_std = 0.05
bar_length = 220e-9
vertex_gap = 1e-8
bar_thickness = 25e-9
bar_width = 80e-9
magnetisation = 800e3

#Graphing and save/load test
kagomeLattice = rpm.ASI_RPM(15, 15)
kagomeLattice.kagome()
filename = 'KagomeTest.npy'
kagomeLattice.save(os.path.join(os.getcwd(),filename))
kagomeLattice.randomMag()
kagomeLattice.graph()
kagomeLattice.load(os.path.join(os.getcwd(),filename))
kagomeLattice.graph()


#field sweep test, count different test
angle = 45
Hamp = 0.95*Hc
squareLattice = rpm.ASI_RPM(15, 15, bar_length = bar_length,\
 vertex_gap = vertex_gap, bar_thickness = bar_thickness,\
 bar_width = bar_width, magnetisation = magnetisation)
squareLattice.square(Hc_mean=Hc, Hc_std=Hc_std)
squareLattice.randomMag(100)
squareLattice.graph()
q = squareLattice.fieldsweep(Hamp/np.cos(np.pi*angle/180),5,angle, n = 5, loops = 10)
squareLattice.graph()


def makePlot(x,y):
	fig, ax =plt.subplots()
	ax.plot(x, y)

makePlot(np.arange(1, len(q)+1), q)


plt.show()		#makes sure this is at the end of the code
'''

#testing code
				

test = ASI_RPM(15,15)
test.square()
test2 = ASI_RPM(10,10)
test2.kagome()
#grid= test.returnLattice()
#print grid
"""
test.graph()
"""
"""
#print(test.dipole(np.array([0.0,1.0]), np.array([1.0,1.0]),np.array([0.0,0.0])))
localfield = []
for num in np.arange(1, 20, 1):
	localfield.append(np.linalg.norm(test.Hlocal2(9,9, n = num)))
print(localfield)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.arange(1, 20, 1), localfield)
plt.title('Local field Calculation')
plt.ylabel(r'Local Field Strength (T)')
plt.xlabel(r'Number of Unit Cells')
print()
"""

#test.randomMag()
#test.graph()
#localfield = []
#for num in np.arange(1, 20, 1):
#    localfield.append(np.linalg.norm(test.Hlocal2(9,9, n = num)))
#print(localfield)
#fig2 = plt.figure(2)
#ax2 = fig2.add_subplot(111)
#ax2.plot(np.arange(1, 20, 1), localfield)
#plt.title('Local field Calculation')
#plt.ylabel(r'Local Field Strength (T)')
#plt.xlabel(r'Number of Unit Cells')
#beforerelax = copy.deepcopy(test)
#beforerelax.graph()
#test.relax(Happlied = [-0.03,-0.03])
#print('test',test)
#after = copy.deepcopy(test)
#after.graph()
#print("before relax", beforerelax.returnLattice())
#print("after relax", after.returnLattice())
#beforerelax.graph()
#after.graph()
test.randomMag()

plt.show()
#print(test.correlation(after.returnLattice(), beforerelax.returnLattice()))
#print(test.correlation(after, beforerelax))

#test2 =Lattice(20,20)
#test2.kagome()
#test2.graph()
#print(test.dipole(np.array([0,1]), np.array([1,1]),np.array([0,0])))

#print(test.Hlocal(3,2))
#test.changeMagnetisation(800e7)
q,q_test = test.fieldsweep(0.0297/np.cos(np.pi/4),5,45, n = 5, loops = 3)
fig_q = plt.figure()
ax2 = fig_q.add_subplot(111)
ax2.plot(np.arange(0, len(q_test), 1), q_test,'o')
plt.title('Correlation Function')
plt.ylabel(r'Correlation')
plt.xlabel(r'Number of loops')
plt.show()

#test.relax(Happlied = [0.03,0.03])
#test.graph()

'''


# '''
# 	def graphCount(self):
# 	'''
# 	'''
# 		Plots the positions and directions of the bar magnetisations as a quiver graph
# 		'''
# 		'''
# 		grid = self.lattice
# 		X = grid[:,:,0].flatten()
# 		Y = grid[:,:,1].flatten()
# 		Mx = grid[:,:,2].flatten()
# 		My = grid[:,:,3].flatten()
# 		Hc = grid[:,:,4].flatten()
# 		C = grid[:,:,5].flatten()
# 		cl.Normalize(C)
# 		figCount =plt.figure()
# 		axCount = plt.gca()
# 		plt.set_cmap(cm.jet)
# 		graphCount = axCount.quiver(X, Y, Mx, My, (C), angles='xy', scale_units='xy', scale=1, pivot = 'mid')
# 		axCount.set_xlim([-1, self.side_len_x])
# 		axCount.set_ylim([-1, self.side_len_y])
# 		plt.colorbar(graphCount)
# 		plt.draw()
# 	'''