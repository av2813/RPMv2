import rpmClassDev_Alex as rpm
import os
import importlib
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce

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
kagomeLattice = rpm.ASI_RPM(5, 5)
kagomeLattice1 = rpm.ASI_RPM(10, 10)
kagomeLattice1.kagome()
#kagomeLattice1.graph()
#kagomeLattice.kagome2()
#filename = 'KagomeTest.npy'
#kagomeLattice.save(os.path.join(os.getcwd(),filename))
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.randomMag()
kagomeLattice1.domainSize()
kagomeLattice1.relax()
#kagomeLattice.load(os.path.join(os.getcwd(),filename))
#kagomeLattice.graph()
#kagomeLattice.fieldplot()


kagomeLattice1.vertexCharge2()
kagomeLattice1.graphCharge()
print(kagomeLattice1.monopoleDensity())
plt.show()
'''
s = rpm.ASI_RPM(5,5)
s.short_shakti()
s.graph()

s = rpm.ASI_RPM(5,5)
s.long_shakti()
s.graph()


t = rpm.ASI_RPM(2,2)
t.tetris()
t.graph()
'''