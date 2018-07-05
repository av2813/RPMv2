import rpmClass_Stable as rpm
import importlib

importlib.reload(rpm)	
#parameters
Hc = 0.062
Hc_std = 0
bar_length = 400e-9
vertex_gap = 100e-9
bar_thickness = 15e-9
bar_width = 80e-9
magnetisation = 800e3

#Graphing and save/load test
kagomeLattice1 = rpm.ASI_RPM(5,5,bar_length = bar_length, vertex_gap = vertex_gap, bar_thickness = bar_thickness, \
        bar_width = bar_width, magnetisation = magnetisation)
#kagomeLattice1.tiltedSquare(45)
#kagomeLattice1.graph()
#kagomeLattice1.randomMag()
print('test')
folder = r'C:\Users\alexv\Box\GitHub\RPM\RPM_Data'
kagomeLattice1.fieldSweepAnimation(folder, name = 'Lattice_counter')
kagomeLattice1.fieldplot()
#plt.show()