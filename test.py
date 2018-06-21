import rpmClass_Stable as rpm
import os
import importlib
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce
import time

importlib.reload(rpm)		#make sure that the class is updated with any chanes

#parameters
Hc = 0.062
Hc_std = 0
bar_length = 400e-9
vertex_gap = 100e-9
bar_thickness = 15e-9
bar_width = 80e-9
magnetisation = 800e3

#Graphing and save/load test
kagomeLattice1 = rpm.ASI_RPM(30,30,bar_length = bar_length, vertex_gap = vertex_gap, bar_thickness = bar_thickness, \
        bar_width = bar_width, magnetisation = magnetisation)
kagomeLattice1.tiltedSquare(45)
#kagomeLattice1.graph()
kagomeLattice1.randomMag()
<<<<<<< HEAD
kagomeLattice1.localFieldHistogram(31,30,6, 30000)
kagomeLattice1.graph()

#kagomeLattice1.square()
#kagomeLattice1.randomMag()
#kagomeLattice1.localPlot(31,30,1)

'''
for bar_length in np.array([400,600,1000])*1e-9:
=======
kagomeLattice1.localPlot(31,30,1)
for bar_length in np.array([600,1000])*1e-9:
>>>>>>> 51ab61ff4af36566f3168b77f336f55167bfb574
	for width in np.array([80, 140])*1e-9:
		for gaps in np.array([100, 200])*1e-9:
			kagomeLattice1 = rpm.ASI_RPM(30,30,bar_length = bar_length, vertex_gap = gaps, bar_thickness = bar_thickness, \
        bar_width = width, magnetisation = magnetisation)
			kagomeLattice1.square()
			for n in np.arange(1, 6):
				kagomeLattice1.localFieldHistogram(31,30, n, 10000, save = True)
				
'''

#kagomeLattice1.square(Hc = Hc, Hc_std=Hc_std)
#folder = r'C:\Users\av2813\Box\Simulations\Mumax3\mumax3.9final_windows\HPCResults\GroundSemiCircle\pkl'
'''
mag =[]
monopole=[]
q = []
field_steps = np.linspace(0,Hmax,steps+1)
field_steps = np.append(field_steps, np.linspace(Hmax,-Hmax,2*steps+1))
field_steps = np.append(field_steps, np.linspace(-Hmax,0,steps+1))
fieldloops = field_steps*np.array([np.cos(Htheta),np.sin(Htheta), 0.])
for root, dirs, files in os.walk(folder):
	for file in files:
		if '.npz' in file and 'AppliedFieldState' in file:
			squareLattice.load(os.path.join(root,file))
			mag.append(rpm.netMagnetisation())
			monopole.append(rpm.monopoleDensity())
			q.append(rpm.correlation(self.previous,self))
			#vertex.append(rpm.vertexTypePercentage())
np.savez('MinorloopQuenchedDisorder'+str(np.around(Hamp*1000,4)).replace('.', 'p')+'mT', fieldloops, q, mag, monopole)
'''

#kagomeLattice1.updateFolder(r'C:\Users\av2813\Box\GitHub\RPM\AlexData\MinorLoopSquareLattice25x25_QuenchedDisorder0p05\MinorLoopsData\MinorLoopHamp_58p9mT', 'square', 0.062, 0.05)
#kagomeLattice1.graph()
#kagomeLattice.kagome2()
#filename = 'KagomeTest.npy'
#kagomeLattice.save(os.path.join(os.getcwd(),filename))
#file = 'Lattice_Loop3_FieldStrength-83p3mT_Angle0p79.npz'
#kagomeLattice.load(file)
#kagomeLattice1.randomMag()

#kagomeLattice1.fieldSweep(0.95*Hc/np.cos(45*np.pi/180), 1, 45, n=4, loops = 4)
#kagomeLattice1.fieldPlot()
#kagomeLattice1.vertexEnergy()
#kagomeLattice1.correlationHistogram()
#kagomeLattice1.vertexHistogram()

# start1 = time.time()
# kagomeLattice1.vertexTypePercentage()
# end1 = time.time()
# kagomeLattice1.vertexTypeMap()
# kagomeLattice1.vertexHistogram()
# kagomeLattice1.correlationHistogram()
# #kagomeLattice1.localCorrelation()

# #kagomeLattice.load(os.path.join(os.getcwd(),filename))
# #kagomeLattice.graph()
# #kagomeLattice.fieldplot()

# start2 = time.time()
# kagomeLattice1.vertexCharge2()
# end2 = time.time()

# print(end1-start1, end2-start2)
# #kagomeLattice1.graphCharge()
# print(kagomeLattice1.monopoleDensity())
# #plt.show()
# '''
# s = rpm.ASI_RPM(5,5)
# s.short_shakti()
# s.graph()

# s = rpm.ASI_RPM(5,5)
# s.long_shakti()
# s.graph()


# t = rpm.ASI_RPM(2,2)
# t.tetris()
# t.graph()
# '''