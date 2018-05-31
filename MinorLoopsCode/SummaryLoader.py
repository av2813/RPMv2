
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as cl
from matplotlib.ticker import MaxNLocator
#from matplotlib.colors import Normalize
import copy
import pickle
import importlib

import rpmClassDev_Alex as rpm



kagomeLattice1 = rpm.ASI_RPM(10, 10)
#kagomeLattice1.square(Hc = Hc, Hc_std=Hc_std)
folder = r'C:\Users\av2813\Box\Simulations\Mumax3\mumax3.9final_windows\HPCResults\GroundSemiCircle\pkl'
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